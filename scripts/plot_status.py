#!/usr/bin/env python3
"""Status tables -> stacked bar charts (per city and overview).

Two steps, both defined here so the table format lives in one place:

  1. tables/  — update_status.py writes plain TSV:
       tables/countries.tsv   country, name, status, pride_hits_queried (one row per country)
       tables/<country>.tsv   city, pride_hits, listed, then one column per CATEGORY
                              (one row per city; category cells are empty when the
                              city has no curated manifest yet)
     Every PXD in a city's manifest is counted in exactly one category, so the
     categories add up to `listed`.
  2. plots    — this script reads only those TSVs and writes:
       status/plots/<country>.svg  horizontal stacked bar per city (nordic, SEA, affinity)
       status/plots/overview.svg     vertical stacked bar per Nordic country
       status/plots/sea.svg          vertical stacked bar per SEA country
       status/plots/south_asia.svg   vertical stacked bar per South Asia country
       status/plots/middle_east.svg  vertical stacked bar per Middle East country
     Stdlib only.

    python scripts/plot_status.py                    # redraw overview + sea + south_asia + middle_east + country charts
    python scripts/plot_status.py --country sweden   # one country chart (+ always region overviews)

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
# bar. update_status.py assigns each manifest PXD to the first matching category
# in this order. *Blocked* is only local blockers that are not already in
# bigbio `sandbox/` or `datasets/` — i.e. never published upstream as a draft.
CATEGORIES = [
    ("annotated", "Local SDRF", "#2a78d6", "#3987e5"),
    ("sandbox", "Sandbox", "#6b4ea3", "#7d5fb5"),
    ("blocked", "Blocked", "#d95926", "#d95926"),
    ("in_corpus", "In corpus", "#199e70", "#199e70"),
    ("screened", "Screened", "#c98500", "#c98500"),
    ("todo", "To do", "#8a8983", "#6b6a65"),
]
UNCURATED_LABEL = "PRIDE hits, not curated yet"

# Layout, in px (horizontal per-city charts).
WIDTH = 860
NAME_W = 110          # minimum row-name gutter left of the bars; widens for long names
TOTAL_W = 90          # room right of the longest bar for its total
BAR_H = 20
ROW_GAP = 10
HEADER_H = 48         # country title + subtitle
LEGEND_H = 26
MIN_BLOCK_PX = 8      # per digit + 10: small blocks are widened so their number fits

# Layout, in px (vertical per-country overview).
OVERVIEW_HEIGHT = 420
OVERVIEW_PLOT_TOP = HEADER_H + LEGEND_H + 8
OVERVIEW_PLOT_BOTTOM = 56   # room for country labels
OVERVIEW_LEFT = 52          # room for y-axis ticks
OVERVIEW_RIGHT = 20
OVERVIEW_BAR_GAP = 18
MIN_SEG_H = 14              # min px before a vertical segment shows its count

STYLE = """
  .bg { fill: #fcfcfb; }
  .title { fill: #0b0b0b; font-size: 17px; font-weight: 600; }
  .city { fill: #0b0b0b; font-size: 13px; font-weight: 600; }
  .sub, .legend, .total, .axis { fill: #52514e; font-size: 11.5px; }
  .seg { font-size: 11.5px; font-weight: 600; fill: #ffffff; font-variant-numeric: tabular-nums; }
  .uncurated { fill: none; stroke: #8a8983; stroke-width: 1.5; stroke-dasharray: 4 3; }
  .grid { stroke: #e8e7e2; stroke-width: 1; }
  text { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }
""" + "".join(f"  .c-{k} {{ fill: {light}; }}\n" for k, _, light, _ in CATEGORIES) + """
  @media (prefers-color-scheme: dark) {
    .bg { fill: #1a1a19; }
    .title, .city { fill: #ffffff; }
    .sub, .legend, .total, .axis { fill: #c3c2b7; }
    .uncurated { stroke: #8f8e86; }
    .grid { stroke: #3a3a37; }
""" + "".join(f"    .c-{k} {{ fill: {dark}; }}\n" for k, _, _, dark in CATEGORIES) + "  }\n"


def human_status(status: str | None) -> str:
    return (status or "not_started").replace("_", " ")


def country_region(cdata: dict | None = None, row: dict | None = None) -> str:
    """Campaign region: nordic | sea | south_asia | middle_east | affinity (default nordic for legacy rows)."""
    if cdata and cdata.get("region"):
        return cdata["region"]
    if row and row.get("region"):
        return row["region"]
    return "nordic"


# --------------------------------------------------------------------------- tables
def write_tables(cfg: dict, breakdowns: dict[tuple[str, str], dict[str, int] | None]) -> list[Path]:
    """config.yml + per-city category counts -> tables/countries.tsv + tables/<country>.tsv.

    `breakdowns[(country, slug)]` is {category: count} for a scoped city, None otherwise.
    """
    TABLE_DIR.mkdir(exist_ok=True)
    written = [TABLE_DIR / "countries.tsv"]
    with written[0].open("w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["country", "name", "region", "status", "pride_hits_queried"])
        for country, cdata in cfg["countries"].items():
            w.writerow([country, cdata.get("name") or country.title(),
                        country_region(cdata=cdata),
                        cdata.get("status") or "not_started",
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


def rows_for_region(rows: list[tuple[dict, list[dict]]], region: str) -> list[tuple[dict, list[dict]]]:
    return [(c, cities) for c, cities in rows if country_region(row=c) == region]


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


def legend_items() -> list[tuple[str, str, str]]:
    """(css_or_marker, label, fill_or_uncurated) for CATEGORIES + uncurated marker."""
    items = [(f"c-{k}", label, light) for k, label, light, _ in CATEGORIES]
    items.append(("uncurated", UNCURATED_LABEL, ""))
    return items


def layout_legend(start_y: float = HEADER_H + 4.0) -> tuple[list[str], float]:
    """Wrap legend chips; return (svg snippets, y just below the legend)."""
    out: list[str] = []
    x, y = 12.0, start_y
    for kind, label, fill in legend_items():
        need = 17 + 7 * len(label) + 18
        if x + need > WIDTH - 12:
            x = 12.0
            y += 16
        if kind == "uncurated":
            out.append(
                f'<rect class="uncurated" fill="none" stroke="#8a8983" x="{x}" y="{y + 0.75}" '
                f'width="12" height="10.5" rx="2"/>'
            )
        else:
            out.append(f'<rect class="{kind}" fill="{fill}" x="{x}" y="{y}" width="12" height="12" rx="2"/>')
        out.append(f'<text class="legend" x="{x + 17}" y="{y + 10}">{label}</text>')
        x += need
    return out, y + 16


def country_svg(country: dict, cities: list[dict]) -> str:
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
    legend_svg, legend_bottom = layout_legend()
    height = legend_bottom + len(cities) * (BAR_H + ROW_GAP) + 8
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" aria-label="{escape(name)} SDRF progress by city">',
        f"<style>{STYLE}</style>",
        f'<rect class="bg" width="{WIDTH}" height="{height}" rx="6"/>',
        f'<text class="title" x="12" y="22">{escape(name)} — {escape(human_status(country.get("status")))}</text>',
        f'<text class="sub" x="12" y="40">{sum(totals.values())} listed · {totals["annotated"]} local SDRFs · '
        f'{totals["sandbox"]} sandbox · {totals["todo"]} to do · {totals["blocked"]} blocked '
        f'(not in sandbox) · PRIDE queried {escape(queried)}</text>',
        *legend_svg,
    ]

    for i, city in enumerate(cities):
        y = legend_bottom + i * (BAR_H + ROW_GAP)
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


def country_category_totals(cities: list[dict]) -> dict[str, int]:
    """Sum CATEGORY columns across cities; uncurated (empty) cities contribute 0."""
    return {k: sum(cell(c, k) or 0 for c in cities) for k, *_ in CATEGORIES}


def nice_ticks(max_val: int, target: int = 4) -> list[int]:
    """A few round y-axis ticks from 0 through at least max_val."""
    if max_val <= 0:
        return [0]
    raw = max(1, max_val / target)
    magnitude = 10 ** max(0, len(str(int(raw))) - 1)
    for step in (magnitude, 2 * magnitude, 5 * magnitude, 10 * magnitude):
        if step <= 0:
            continue
        top = ((max_val + step - 1) // step) * step
        ticks = list(range(0, top + 1, step))
        if 3 <= len(ticks) <= 7:
            return ticks
    step = max(1, round(raw))
    top = ((max_val + step - 1) // step) * step
    return list(range(0, top + 1, step))


def region_overview_svg(
    rows: list[tuple[dict, list[dict]]],
    *,
    region: str,
    title: str,
    aria_label: str,
) -> str:
    """One vertical stacked bar per country in `region` (Nordic or SEA)."""
    series = []
    for country, cities in rows_for_region(rows, region):
        totals = country_category_totals(cities)
        series.append({
            "key": country["country"],
            "name": country.get("name") or country["country"].title(),
            "totals": totals,
            "listed": sum(totals.values()),
        })
    max_listed = max((s["listed"] for s in series), default=0)
    ticks = nice_ticks(max_listed)
    y_max = ticks[-1] if ticks else 1
    plot_w = WIDTH - OVERVIEW_LEFT - OVERVIEW_RIGHT
    n = max(len(series), 1)
    # SEA has more countries: keep bars readable by tightening the gap slightly.
    gap = OVERVIEW_BAR_GAP if n <= 6 else max(8.0, OVERVIEW_BAR_GAP - 6)
    bar_w = max(22.0, (plot_w - gap * (n + 1)) / n)
    grand = {k: sum(s["totals"][k] for s in series) for k, *_ in CATEGORIES}
    queried = next((c.get("pride_hits_queried") for c, _ in rows if c.get("pride_hits_queried")), "unknown date")

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{OVERVIEW_HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {OVERVIEW_HEIGHT}" role="img" '
        f'aria-label="{escape(aria_label)}">',
        f"<style>{STYLE}</style>",
        f'<rect class="bg" width="{WIDTH}" height="{OVERVIEW_HEIGHT}" rx="6"/>',
        f'<text class="title" x="12" y="22">{escape(title)}</text>',
        f'<text class="sub" x="12" y="40">{sum(grand.values())} listed · {grand["annotated"]} local SDRFs · '
        f'{grand["sandbox"]} sandbox · {grand["todo"]} to do · {grand["blocked"]} blocked '
        f'(not in sandbox) · PRIDE queried {escape(queried)}</text>',
    ]

    legend_svg, legend_bottom = layout_legend()
    out.extend(legend_svg)
    plot_top = max(OVERVIEW_PLOT_TOP, legend_bottom + 8)
    plot_h = OVERVIEW_HEIGHT - plot_top - OVERVIEW_PLOT_BOTTOM
    px_per_pxd = plot_h / max(y_max, 1)

    base_y = plot_top + plot_h
    for tick in ticks:
        gy = base_y - tick * px_per_pxd
        out.append(f'<line class="grid" x1="{OVERVIEW_LEFT}" y1="{gy:.1f}" '
                   f'x2="{WIDTH - OVERVIEW_RIGHT}" y2="{gy:.1f}"/>')
        out.append(f'<text class="axis" x="{OVERVIEW_LEFT - 8}" y="{gy + 4:.1f}" text-anchor="end">{tick}</text>')

    for i, s in enumerate(series):
        bx = OVERVIEW_LEFT + gap + i * (bar_w + gap)
        # Draw bottom → top in CATEGORIES order (annotated at bottom).
        y_cursor = base_y
        for key, label, light, _ in CATEGORIES:
            n_pxd = s["totals"][key]
            if not n_pxd:
                continue
            h = n_pxd * px_per_pxd
            y_top = y_cursor - h
            out.append(
                f'<rect class="c-{key}" fill="{light}" x="{bx:.1f}" y="{y_top:.1f}" '
                f'width="{bar_w:.1f}" height="{max(h - 1, 1):.1f}" rx="2">'
                f'<title>{escape(s["name"])} · {label}: {n_pxd}</title></rect>'
            )
            if h >= MIN_SEG_H:
                out.append(
                    f'<text class="seg" x="{bx + bar_w / 2:.1f}" y="{y_top + h / 2 + 4:.1f}" '
                    f'text-anchor="middle">{n_pxd}</text>'
                )
            y_cursor = y_top
        out.append(
            f'<text class="total" x="{bx + bar_w / 2:.1f}" y="{y_cursor - 6:.1f}" '
            f'text-anchor="middle">{s["listed"]}</text>'
        )
        # Long SEA names: allow two-line labels by inserting a soft break on space/hyphen.
        label = s["name"]
        if len(label) > 10 and n > 6:
            out.append(
                f'<text class="city" x="{bx + bar_w / 2:.1f}" y="{base_y + 14:.1f}" '
                f'text-anchor="middle" font-size="10">{escape(label)}</text>'
            )
        else:
            out.append(
                f'<text class="city" x="{bx + bar_w / 2:.1f}" y="{base_y + 18:.1f}" '
                f'text-anchor="middle">{escape(label)}</text>'
            )

    out.append("</svg>")
    return "\n".join(out) + "\n"


def overview_svg(rows: list[tuple[dict, list[dict]]]) -> str:
    """Nordic region overview (vertical bars)."""
    return region_overview_svg(
        rows,
        region="nordic",
        title="Nordic countries — listed PXDs",
        aria_label="Nordic SDRF progress by country",
    )


def sea_overview_svg(rows: list[tuple[dict, list[dict]]]) -> str:
    """SEA region overview (vertical bars), matching Nordic overview style."""
    return region_overview_svg(
        rows,
        region="sea",
        title="Southeast Asia — listed PXDs",
        aria_label="Southeast Asia SDRF progress by country",
    )


def south_asia_overview_svg(rows: list[tuple[dict, list[dict]]]) -> str:
    """South Asia region overview (vertical bars), matching Nordic/SEA style."""
    return region_overview_svg(
        rows,
        region="south_asia",
        title="South Asia — listed PXDs",
        aria_label="South Asia SDRF progress by country",
    )


def middle_east_overview_svg(rows: list[tuple[dict, list[dict]]]) -> str:
    """Middle East region overview (vertical bars), matching Nordic/SEA style."""
    return region_overview_svg(
        rows,
        region="middle_east",
        title="Middle East — listed PXDs",
        aria_label="Middle East SDRF progress by country",
    )


REGION_OVERVIEWS = (
    ("nordic", "overview.svg", overview_svg),
    ("sea", "sea.svg", sea_overview_svg),
    ("south_asia", "south_asia.svg", south_asia_overview_svg),
    ("middle_east", "middle_east.svg", middle_east_overview_svg),
)


def write_plots(countries: list[str] | None = None) -> list[Path]:
    """tables/*.tsv -> region overviews + per-country charts (all regions)."""
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    all_rows = read_tables()
    for region, filename, drawer in REGION_OVERVIEWS:
        if rows_for_region(all_rows, region):
            path = PLOT_DIR / filename
            path.write_text(drawer(all_rows))
            written.append(path)

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
