#!/usr/bin/env python3
"""Status tables -> horizontal bar charts, one panel per city.

Two steps, both here so the table format lives in one place:

  1. tables/  — update_status.py writes the numbers as plain TSV:
       tables/countries.tsv   country, status, pride_hits_queried (one row per country)
       tables/<country>.tsv   city, pride_hits, pxd_count, in_corpus, screened,
                              annotated, blocked (one row per city; empty cell = "—",
                              i.e. the city has no curated manifest yet)
  2. plots    — this script reads only those TSVs and writes one SVG per country
                to status/plots/<country>.svg. All panels in a country share one
                x scale so cities can be compared. Stdlib only — no matplotlib.

    python scripts/plot_status.py                    # redraw every country from tables/
    python scripts/plot_status.py --country sweden   # just one (repeatable)
    python scripts/plot_status.py --from-config      # rebuild tables/ from config.yml first

update_status.py writes the tables and redraws the plots automatically. Run this
by hand after editing a TSV, or after changing STAGES / colours / layout below.
"""
from __future__ import annotations

import argparse
import csv
import math
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config.yml"
TABLE_DIR = ROOT / "tables"
PLOT_DIR = ROOT / "status" / "plots"

# (table column, bar label) — top to bottom in every panel. Add, drop or
# reorder stages here; an empty cell is drawn as "—" (e.g. no manifest yet).
STAGES = [
    ("pride_hits", "PRIDE hits"),
    ("pxd_count", "PXDs listed"),
    ("in_corpus", "In corpus"),
    ("screened", "Screened"),
    ("annotated", "Annotated"),
    ("blocked", "Blocked"),
]

# Stages that only mean something once a city has a curated manifest (pxd_list).
UNSCOPED_EMPTY = {"pxd_count", "in_corpus"}

# Layout, in px.
COLUMNS = 2           # city panels per row
PANEL_W = 420
LABEL_W = 92          # stage-name gutter left of the bars
VALUE_W = 40          # room right of the longest bar for its number
BAR_H = 14
BAR_GAP = 6
PANEL_TITLE_H = 26
PANEL_PAD = 18        # vertical space between panel rows
HEADER_H = 44         # country title + subtitle

# Light / dark colours; the SVG switches with the viewer's colour scheme.
STYLE = """
  .bg { fill: #fcfcfb; }
  .bar { fill: #2a78d6; }
  .track { fill: #f0efec; }
  .title { fill: #0b0b0b; font-size: 17px; font-weight: 600; }
  .city { fill: #0b0b0b; font-size: 13px; font-weight: 600; }
  .label, .sub { fill: #52514e; font-size: 11.5px; }
  .value { fill: #0b0b0b; font-size: 11.5px; font-variant-numeric: tabular-nums; }
  .empty { fill: #8a8983; font-size: 11.5px; }
  text { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }
  @media (prefers-color-scheme: dark) {
    .bg { fill: #1a1a19; }
    .bar { fill: #3987e5; }
    .track { fill: #2a2a28; }
    .title, .city, .value { fill: #ffffff; }
    .label, .sub { fill: #c3c2b7; }
    .empty { fill: #8f8e86; }
  }
"""


def human_status(status: str | None) -> str:
    return (status or "not_started").replace("_", " ")


# --------------------------------------------------------------------------- tables
def write_tables(cfg: dict) -> list[Path]:
    """config.yml numbers -> tables/countries.tsv + tables/<country>.tsv."""
    TABLE_DIR.mkdir(exist_ok=True)
    queried = cfg.get("pride_hits_queried", "")
    written = [TABLE_DIR / "countries.tsv"]
    with written[0].open("w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["country", "status", "pride_hits_queried"])
        for country, cdata in cfg["countries"].items():
            w.writerow([country, cdata.get("status") or "not_started", queried])
    for country, cdata in cfg["countries"].items():
        path = TABLE_DIR / f"{country}.tsv"
        with path.open("w", newline="") as fh:
            w = csv.writer(fh, delimiter="\t", lineterminator="\n")
            w.writerow(["city", *(k for k, _ in STAGES)])
            for slug, city in (cdata.get("cities") or {}).items():
                scoped = bool(city.get("pxd_list"))
                w.writerow([city.get("name", slug),
                            *("" if (k in UNSCOPED_EMPTY and not scoped) or city.get(k) is None
                              else int(city[k]) for k, _ in STAGES)])
        written.append(path)
    return written


def read_tables(countries: list[str] | None = None) -> list[tuple[dict, list[dict]]]:
    """[(country row from countries.tsv, [city rows from <country>.tsv]), ...] in file order."""
    index = TABLE_DIR / "countries.tsv"
    if not index.exists():
        raise SystemExit(f"{index.relative_to(ROOT)} not found — run update_status.py "
                         f"or plot_status.py --from-config first")
    with index.open(newline="") as fh:
        rows = [r for r in csv.DictReader(fh, delimiter="\t")
                if not countries or r["country"] in countries]
    out = []
    for row in rows:
        with (TABLE_DIR / f"{row['country']}.tsv").open(newline="") as fh:
            out.append((row, list(csv.DictReader(fh, delimiter="\t"))))
    return out


def cell(row: dict, key: str) -> int | None:
    raw = (row.get(key) or "").strip()
    return int(raw) if raw else None


# --------------------------------------------------------------------------- plots
def country_svg(country: dict, cities: list[dict]) -> str:
    cols = min(COLUMNS, max(len(cities), 1))
    rows = math.ceil(len(cities) / cols) if cities else 0
    panel_h = PANEL_TITLE_H + len(STAGES) * (BAR_H + BAR_GAP)
    width = cols * PANEL_W
    height = HEADER_H + rows * (panel_h + PANEL_PAD)
    scale_max = max(1, max((cell(c, k) or 0 for c in cities for k, _ in STAGES), default=0))
    bar_span = PANEL_W - LABEL_W - VALUE_W - 16

    listed = sum(cell(c, "pxd_count") or 0 for c in cities)
    annotated = sum(cell(c, "annotated") or 0 for c in cities)
    name = country["country"].title()
    queried = country.get("pride_hits_queried") or "unknown date"
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(name)} SDRF progress by city">',
        f"<style>{STYLE}</style>",
        f'<rect class="bg" width="{width}" height="{height}" rx="6"/>',
        f'<text class="title" x="12" y="22">{escape(name)} — {escape(human_status(country.get("status")))}</text>',
        f'<text class="sub" x="12" y="38">{listed} PXDs listed · {annotated} annotated · '
        f"PRIDE queried {escape(queried)}</text>",
    ]

    for i, city in enumerate(cities):
        x0 = (i % cols) * PANEL_W + 12
        y0 = HEADER_H + (i // cols) * (panel_h + PANEL_PAD)
        cname = escape(city["city"])
        out.append(f'<text class="city" x="{x0}" y="{y0 + 16}">{cname}</text>')
        for j, (key, label) in enumerate(STAGES):
            y = y0 + PANEL_TITLE_H + j * (BAR_H + BAR_GAP)
            bx = x0 + LABEL_W
            out.append(f'<text class="label" x="{bx - 8}" y="{y + BAR_H - 3}" text-anchor="end">{label}</text>')
            out.append(f'<rect class="track" x="{bx}" y="{y}" width="{bar_span}" height="{BAR_H}" rx="3"/>')
            value = cell(city, key)
            if value is None:
                out.append(f'<text class="empty" x="{bx + 6}" y="{y + BAR_H - 3}">—</text>')
                continue
            w = bar_span * value / scale_max
            if value:
                out.append(f'<rect class="bar" x="{bx}" y="{y}" width="{max(w, 2):.1f}" height="{BAR_H}" rx="3">'
                           f"<title>{cname} · {label}: {value}</title></rect>")
            out.append(f'<text class="value" x="{bx + w + 6:.1f}" y="{y + BAR_H - 3}">{value}</text>')

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
    ap.add_argument("--from-config", action="store_true", help="rebuild tables/ from config.yml before plotting")
    args = ap.parse_args()
    if args.from_config:
        import yaml
        for path in write_tables(yaml.safe_load(CONFIG.read_text())):
            print(f"wrote {path.relative_to(ROOT)}")
    for path in write_plots(args.country):
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
