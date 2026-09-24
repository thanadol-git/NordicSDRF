#!/usr/bin/env python3
"""Status tables -> one stacked horizontal bar per city.

Two steps, both defined here so the table format lives in one place:

  1. tables/  — update_status.py writes plain TSV:
       tables/countries.tsv   country, name, status, pride_hits_queried (one row per country)
       tables/<country>.tsv   city, pride_hits, listed, then one column per CATEGORY
                              (one row per city; category cells are empty when the
                              city has no curated manifest yet)
     Every PXD in a city's manifest is counted in exactly one category, so the
     categories add up to `listed`.
  2. plots    — this script reads only those TSVs and writes one SVG per country
                to status/plots/<country>.svg: one row per city, one bar per row,
                split into coloured blocks per category with the count in white.
                All rows in a country share one x scale. Stdlib only.

    python scripts/plot_status.py                    # redraw every country from tables/
    python scripts/plot_status.py --country sweden   # just one (repeatable)

update_status.py rewrites the tables and redraws the plots every run, so a hand
edit to a TSV only lasts until the next run. Run this by hand after editing a
TSV, or after changing CATEGORIES / colours / layout below.
"""
from __future__ import annotations

import argparse
import csv
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = ROOT / "tables"
PLOT_DIR = ROOT / "status" / "plots"

# (table column, legend label, light colour, dark colour) — left to right in the
# bar. The order is also the priority update_status.py uses when a PXD fits more
# than one category (e.g. annotated here *and* already in the community corpus).
CATEGORIES = [
    ("annotated", "Annotated", "#2a78d6", "#3987e5"),
    ("blocked", "Blocked", "#d95926", "#d95926"),
    ("in_corpus", "In corpus", "#199e70", "#199e70"),
    ("screened", "Screened", "#c98500", "#c98500"),
    ("todo", "To do", "#8a8983", "#6b6a65"),
]
UNCURATED_LABEL = "PRIDE hits, not curated yet"

# Layout, in px.
WIDTH = 860
NAME_W = 110          # minimum row-name gutter left of the bars; widens for long names
TOTAL_W = 90          # room right of the longest bar for its total
BAR_H = 20
ROW_GAP = 10
HEADER_H = 48         # country title + subtitle
LEGEND_H = 26
MIN_BLOCK_PX = 8      # per digit + 10: small blocks are widened so their number fits

STYLE = """
  .bg { fill: #fcfcfb; }
  .title { fill: #0b0b0b; font-size: 17px; font-weight: 600; }
  .city { fill: #0b0b0b; font-size: 13px; font-weight: 600; }
  .sub, .legend, .total { fill: #52514e; font-size: 11.5px; }
  .seg { font-size: 11.5px; font-weight: 600; fill: #ffffff; font-variant-numeric: tabular-nums; }
  .uncurated { fill: none; stroke: #8a8983; stroke-width: 1.5; stroke-dasharray: 4 3; }
  text { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }
""" + "".join(f"  .c-{k} {{ fill: {light}; }}\n" for k, _, light, _ in CATEGORIES) + """
  @media (prefers-color-scheme: dark) {
    .bg { fill: #1a1a19; }
    .title, .city { fill: #ffffff; }
    .sub, .legend, .total { fill: #c3c2b7; }
    .uncurated { stroke: #8f8e86; }
""" + "".join(f"    .c-{k} {{ fill: {dark}; }}\n" for k, _, _, dark in CATEGORIES) + "  }\n"


def human_status(status: str | None) -> str:
    return (status or "not_started").replace("_", " ")


# --------------------------------------------------------------------------- tables
def write_tables(cfg: dict, breakdowns: dict[tuple[str, str], dict[str, int] | None]) -> list[Path]:
    """config.yml + per-city category counts -> tables/countries.tsv + tables/<country>.tsv.

    `breakdowns[(country, slug)]` is {category: count} for a scoped city, None otherwise.
    """
    TABLE_DIR.mkdir(exist_ok=True)
    written = [TABLE_DIR / "countries.tsv"]
    with written[0].open("w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["country", "name", "status", "pride_hits_queried"])
        for country, cdata in cfg["countries"].items():
            w.writerow([country, cdata.get("name") or country.title(), cdata.get("status") or "not_started",
                        cfg.get("pride_hits_queried", "")])
    for country, cdata in cfg["countries"].items():
        path = TABLE_DIR / f"{country}.tsv"
        with path.open("w", newline="") as fh:
            w = csv.writer(fh, delimiter="\t", lineterminator="\n")
            w.writerow(["city", "pride_hits", "listed", *(k for k, *_ in CATEGORIES)])
            for slug, city in (cdata.get("cities") or {}).items():
                cats = breakdowns.get((country, slug))
                w.writerow([city.get("name", slug), int(city.get("pride_hits") or 0),
                            sum(cats.values()) if cats else "",
                            *((cats[k] if cats else "") for k, *_ in CATEGORIES)])
        written.append(path)
    return written


def read_tables(countries: list[str] | None = None) -> list[tuple[dict, list[dict]]]:
    """[(country row from countries.tsv, [city rows from <country>.tsv]), ...] in file order."""
    index = TABLE_DIR / "countries.tsv"
    if not index.exists():
        raise SystemExit(f"{index.relative_to(ROOT)} not found — run scripts/update_status.py --no-pride first")
    with index.open(newline="") as fh:
        rows = [r for r in csv.DictReader(fh, delimiter="\t") if not countries or r["country"] in countries]
    out = []
    for row in rows:
        with (TABLE_DIR / f"{row['country']}.tsv").open(newline="") as fh:
            out.append((row, list(csv.DictReader(fh, delimiter="\t"))))
    return out


def cell(row: dict, key: str) -> int | None:
    raw = (row.get(key) or "").strip()
    return int(raw) if raw else None


# --------------------------------------------------------------------------- plots
def bar_total(city: dict) -> tuple[int, bool]:
    """(bar length in PXDs, curated?) — the manifest if there is one, else raw PRIDE hits."""
    cats = [cell(city, k) for k, *_ in CATEGORIES]
    if any(v is not None for v in cats):
        return sum(v or 0 for v in cats), True
    return cell(city, "pride_hits") or 0, False


def block_widths(counts: list[int], px_per_pxd: float) -> list[float]:
    """Proportional widths, except a non-empty block is never narrower than its number."""
    return [max(n * px_per_pxd, MIN_BLOCK_PX * len(str(n)) + 10) if n else 0 for n in counts]


def row_widths(city: dict, px_per_pxd: float) -> list[float]:
    total, curated = bar_total(city)
    if not curated:
        return [total * px_per_pxd]
    return block_widths([cell(city, k) or 0 for k, *_ in CATEGORIES], px_per_pxd)


def country_svg(country: dict, cities: list[dict]) -> str:
    height = HEADER_H + LEGEND_H + len(cities) * (BAR_H + ROW_GAP) + 8
    name_w = max(NAME_W, 12 + 8 * max((len(c["city"]) for c in cities), default=0) + 12)
    span = WIDTH - name_w - TOTAL_W - 12
    # Shared scale: shrink px-per-PXD until the widest row (after minimum widths) fits.
    px_per_pxd = span / max(1, max((bar_total(c)[0] for c in cities), default=0))
    for _ in range(20):
        widest = max((sum(row_widths(c, px_per_pxd)) for c in cities), default=0)
        if widest <= span:
            break
        px_per_pxd *= span / widest

    totals = {k: sum(cell(c, k) or 0 for c in cities) for k, *_ in CATEGORIES}
    name = country.get("name") or country["country"].title()
    queried = country.get("pride_hits_queried") or "unknown date"
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" aria-label="{escape(name)} SDRF progress by city">',
        f"<style>{STYLE}</style>",
        f'<rect class="bg" width="{WIDTH}" height="{height}" rx="6"/>',
        f'<text class="title" x="12" y="22">{escape(name)} — {escape(human_status(country.get("status")))}</text>',
        f'<text class="sub" x="12" y="40">{sum(totals.values())} datasets listed · {totals["annotated"]} annotated · '
        f"PRIDE queried {escape(queried)} · bar length = accessions in the row's manifest (dashed: raw PRIDE hits)</text>",
    ]

    # legend
    x, y = 12, HEADER_H + 4
    for key, label, light, _ in CATEGORIES:
        out.append(f'<rect class="c-{key}" fill="{light}" x="{x}" y="{y}" width="12" height="12" rx="2"/>')
        out.append(f'<text class="legend" x="{x + 17}" y="{y + 10}">{label}</text>')
        x += 17 + 7 * len(label) + 18
    out.append(f'<rect class="uncurated" fill="none" stroke="#8a8983" x="{x}" y="{y + 0.75}" width="12" height="10.5" rx="2"/>')
    out.append(f'<text class="legend" x="{x + 17}" y="{y + 10}">{UNCURATED_LABEL}</text>')

    for i, city in enumerate(cities):
        y = HEADER_H + LEGEND_H + i * (BAR_H + ROW_GAP)
        ty = y + BAR_H / 2 + 4
        cname = escape(city["city"])
        out.append(f'<text class="city" x="12" y="{ty}">{cname}</text>')
        total, curated = bar_total(city)
        widths = row_widths(city, px_per_pxd)
        x = name_w
        if not curated:
            w = widths[0]
            if total:
                out.append(f'<rect class="uncurated" fill="none" stroke="#8a8983" x="{x}" y="{y + 0.75}" width="{max(w, 2):.1f}" '
                           f'height="{BAR_H - 1.5}" rx="3"><title>{cname} · {UNCURATED_LABEL}: {total}</title></rect>')
            out.append(f'<text class="total" x="{x + w + 6:.1f}" y="{ty}">{total} PRIDE hits</text>')
            continue
        for (key, label, light, _), w in zip(CATEGORIES, widths):
            n = cell(city, key) or 0
            if not n:
                continue
            # 1px surface gap between blocks: draw each block 1px short.
            out.append(f'<rect class="c-{key}" fill="{light}" x="{x:.1f}" y="{y}" width="{max(w - 1, 1):.1f}" height="{BAR_H}" '
                       f'rx="2"><title>{cname} · {label}: {n}</title></rect>')
            out.append(f'<text class="seg" x="{x + (w - 1) / 2:.1f}" y="{ty}" text-anchor="middle">{n}</text>')
            x += w
        out.append(f'<text class="total" x="{x + 6:.1f}" y="{ty}">{total} listed</text>')

    out.append("</svg>")
    return "\n".join(out) + "\n"


def write_plots(countries: list[str] | None = None) -> list[Path]:
    """tables/*.tsv -> status/plots/<country>.svg."""
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for country, cities in read_tables(countries):
        path = PLOT_DIR / f"{country['country']}.svg"
        path.write_text(country_svg(country, cities))
        written.append(path)
    return written


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--country", action="append", help="limit to one or more countries (repeatable)")
    args = ap.parse_args()
    for path in write_plots(args.country):
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
