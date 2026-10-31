#!/usr/bin/env python3
"""PRIDE authorship network across every curated manifest -> status/plots/authorship.svg.

Three steps, stdlib only:

  1. fetch  — every accession in lists/<country>/<city>.txt and olink_pad/<platform>.txt
              -> PRIDE project record, cached as results/authorship/cache/<acc>.json
              (gitignored: records carry e-mail addresses). Cached records are reused;
              --refresh re-downloads them.
  2. tables — people = PRIDE submitters + lab PIs + publication authors parsed from the
              record's Vancouver-style referenceLine ("Nielsen NS, Poulsen ET, ..."),
              keyed on folded surname + initials. Two people are linked once per
              dataset they share.
                tables/authorship_people.tsv  one row per person on >= 2 datasets
                tables/authorship_edges.tsv   pairs of those people sharing >= 2 datasets
  3. plot   — people on >= --min-datasets datasets, force-directed layout, node area ~
              datasets, colour = country whose manifests hold most of their datasets,
              ringed = lab PI on at least one; dark links cross a country border.

Name matching is heuristic: "Hansen J" on two papers may be two people, and one
person who publishes under two sets of initials stays split unless one set is a
prefix of exactly one other ("Enghild J" -> "Enghild JJ").

    python scripts/plot_authorship.py                     # fetch missing records, rebuild tables + SVG
    python scripts/plot_authorship.py --plot-only         # redraw the SVG from tables/
    python scripts/plot_authorship.py --min-datasets 10   # sparser plot
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from html import escape
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIDE = "https://www.ebi.ac.uk/pride/ws/archive/v2/projects/{}"
CACHE = ROOT / "results" / "authorship" / "cache"
PEOPLE_TSV = ROOT / "tables" / "authorship_people.tsv"
EDGES_TSV = ROOT / "tables" / "authorship_edges.tsv"
PLOT = ROOT / "status" / "plots" / "authorship.svg"

# (manifest group, legend label, colour) — also the legend order.
GROUPS = [
    ("sweden", "Sweden", "#2a78d6"),
    ("denmark", "Denmark", "#d6453a"),
    ("norway", "Norway", "#199e70"),
    ("finland", "Finland", "#7b55d6"),
    ("iceland", "Iceland", "#c98500"),
    ("olink_pad", "Olink PAD", "#8a8983"),
]
COLOUR = {g: c for g, _, c in GROUPS}

# PRIDE submitter accounts that are facilities, not people.
NOT_A_PERSON = re.compile(r"\b(facility|core|unit|platform|laboratory|lab|centre|center|consortium|group|"
                          r"proteomics|team|service|department|university|institute)\b", re.I)

WIDTH, HEIGHT = 960, 860
HEADER_H = 64
PAD = 28
LABEL_TOP = 40        # most-published people that get a name label (if it fits)

STYLE = """
  .bg { fill: #fcfcfb; }
  .title { fill: #0b0b0b; font-size: 17px; font-weight: 600; }
  .sub, .legend { fill: #52514e; font-size: 11.5px; }
  .edge { stroke: #b9b8b1; stroke-opacity: 0.45; fill: none; }
  .edge.cross { stroke: #3d3c38; stroke-opacity: 0.55; }
  .node { stroke: #fcfcfb; stroke-width: 1; }
  .node.pi { stroke: #0b0b0b; stroke-width: 1.6; }
  .label { fill: #0b0b0b; font-size: 10.5px; font-weight: 600; paint-order: stroke;
           stroke: #fcfcfb; stroke-width: 3px; stroke-linejoin: round; }
  .ring { fill: none; stroke: #0b0b0b; stroke-width: 1.6; }
  text { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }
  @media (prefers-color-scheme: dark) {
    .bg { fill: #1a1a19; }
    .title { fill: #ffffff; }
    .sub, .legend { fill: #c3c2b7; }
    .edge { stroke: #5a5953; }
    .edge.cross { stroke: #d8d7cf; }
    .node { stroke: #1a1a19; }
    .node.pi, .ring { stroke: #ffffff; }
    .label { fill: #ffffff; stroke: #1a1a19; }
  }
"""


# --------------------------------------------------------------------------- fetch
def manifests() -> dict[str, list[tuple[str, str]]]:
    """{accession: [(country, city), ...]} over every curated manifest."""
    out: dict[str, list[tuple[str, str]]] = {}
    for path in [*sorted((ROOT / "lists").glob("*/*.txt")), *sorted((ROOT / "olink_pad").glob("*.txt"))]:
        country = path.parent.name
        for line in path.read_text().splitlines():
            acc = line.strip()
            if acc and not acc.startswith("#"):
                out.setdefault(acc, []).append((country, path.stem))
    return out


def fetch(acc: str, refresh: bool = False) -> dict | None:
    path = CACHE / f"{acc}.json"
    if path.exists() and not refresh:
        return json.loads(path.read_text())
    for attempt in range(3):
        try:
            with urllib.request.urlopen(PRIDE.format(acc), timeout=60) as resp:
                rec = json.loads(resp.read().decode())
            path.write_text(json.dumps(rec))
            return rec
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            pass
        time.sleep(2 * (attempt + 1))
    print(f"  ! {acc}: fetch failed", file=sys.stderr)
    return None


def fetch_all(accs: list[str], refresh: bool = False) -> dict[str, dict]:
    CACHE.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        recs = dict(zip(accs, pool.map(lambda a: fetch(a, refresh), accs)))
    return {a: r for a, r in recs.items() if r}


# --------------------------------------------------------------------------- people
# Vancouver author token: "Nielsen NS", "Yau W-L", "Braga-Tanaka I 3rd".
AUTHOR = re.compile(r"^(?P<last>[^\d,;]+?)\s+(?P<ini>[A-Z\u00c0-\u00de\u0100-\u017f](?:-?[A-Z\u00c0-\u00de\u0100-\u017f]){0,4})"
                    r"(?:\s+(?:Jr|Sr|2nd|3rd|II|III))?$")
FOLD = str.maketrans({"ø": "o", "Ø": "O", "æ": "ae", "Æ": "AE", "ß": "ss", "đ": "d", "ł": "l", "Ł": "L", "ı": "i"})


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.translate(FOLD))
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def person_key(last: str, initials: str) -> str:
    return f"{fold(last).replace(' ', '').replace('-', '')}|{fold(initials).replace('-', '')}"


def ref_authors(line: str) -> list[tuple[str, str]]:
    """[(surname, initials), ...] from a PRIDE referenceLine; groups/consortia are dropped."""
    if not line or line.lstrip().startswith("<"):
        return []
    head = re.split(r"\.\s|;\s", line, maxsplit=1)[0]
    out = []
    for tok in (t.strip() for t in head.split(",")):
        m = AUTHOR.match(tok)
        if m and not NOT_A_PERSON.search(m["last"]):
            out.append((m["last"].strip(), m["ini"].replace("-", "")))
    return out


def pride_person(p: dict) -> tuple[str, str] | None:
    last = (p.get("lastName") or "").strip()
    first = (p.get("firstName") or "").strip()
    if not last or not first or NOT_A_PERSON.search(f"{first} {last}"):
        return None
    initials = "".join(part[0] for part in re.split(r"[\s.\-]+", first) if part and part[0].isalpha())
    return last, initials.upper()


def dataset_people(rec: dict) -> dict[str, dict]:
    """{person key: {"name", "roles", "affiliation", "country"}} for one PRIDE record."""
    people: dict[str, dict] = {}

    def add(last: str, initials: str, role: str, p: dict | None = None) -> None:
        entry = people.setdefault(person_key(last, initials),
                                  {"name": f"{last} {initials}", "roles": set(), "affiliation": "", "country": ""})
        entry["roles"].add(role)
        if p:
            entry["affiliation"] = entry["affiliation"] or " ".join((p.get("affiliation") or "").split())
            entry["country"] = entry["country"] or (p.get("country") or "").strip()

    for role, field in (("lab_pi", "labPIs"), ("submitter", "submitters")):
        for p in rec.get(field) or []:
            name = pride_person(p)
            if name:
                add(*name, role, p)
    for ref in rec.get("references") or []:
        for last, initials in ref_authors(ref.get("referenceLine") or ""):
            add(last, initials, "author")
    return people


def merge_initials(keys: set[str]) -> dict[str, str]:
    """Alias short-initial keys onto the one longer variant they abbreviate ("enghild|j" -> "enghild|jj").

    Only merges when exactly one longer variant shares the surname and starts with the
    short initials; two candidates (e.g. "hansen|ja" and "hansen|jb") leave "hansen|j" alone.
    """
    by_last: dict[str, list[str]] = {}
    for key in keys:
        by_last.setdefault(key.split("|")[0], []).append(key)
    alias = {}
    for group in by_last.values():
        for k in group:
            ini = k.split("|")[1]
            longer = [o for o in group if o != k and o.split("|")[1].startswith(ini)]
            if len(longer) == 1:
                alias[k] = longer[0]
    return alias


def build_network(manifest: dict[str, list[tuple[str, str]]], recs: dict[str, dict]):
    """-> (people {key: row}, edges Counter {(a, b): shared datasets})."""
    per_dataset = {acc: dataset_people(rec) for acc, rec in recs.items()}
    alias = merge_initials({k for found in per_dataset.values() for k in found})

    people: dict[str, dict] = {}
    edges: Counter = Counter()
    for acc, found in sorted(per_dataset.items()):
        members: dict[str, dict] = {}
        for k, p in found.items():
            m = members.setdefault(alias.get(k, k), {**p, "roles": set()})
            m["roles"] |= p["roles"]
            m["affiliation"] = m["affiliation"] or p["affiliation"]
            m["country"] = m["country"] or p["country"]
        for k, p in members.items():
            row = people.setdefault(k, {"name": p["name"], "datasets": [], "lab_pi": 0, "submitter": 0,
                                        "affiliation": "", "country": "", "places": Counter()})
            if len(p["name"]) > len(row["name"]):
                row["name"] = p["name"]
            row["datasets"].append(acc)
            row["lab_pi"] += "lab_pi" in p["roles"]
            row["submitter"] += "submitter" in p["roles"]
            if p["affiliation"] and ("lab_pi" in p["roles"] or not row["affiliation"]):
                row["affiliation"] = p["affiliation"]
            row["country"] = row["country"] or p["country"]
            for country, city in manifest.get(acc, []):
                row["places"][(country, city)] += 1
        for a, b in combinations(sorted(members), 2):
            edges[(a, b)] += 1
    return people, edges


# --------------------------------------------------------------------------- tables
def write_tables(people: dict[str, dict], edges: Counter) -> None:
    keep = {k for k, p in people.items() if len(p["datasets"]) >= 2}
    order = sorted(keep, key=lambda k: (-len(people[k]["datasets"]), people[k]["name"]))
    PEOPLE_TSV.parent.mkdir(exist_ok=True)
    with PEOPLE_TSV.open("w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["key", "name", "datasets", "lab_pi", "submitter", "group", "city", "pride_country",
                    "affiliation", "accessions"])
        for k in order:
            p = people[k]
            country, city = p["places"].most_common(1)[0][0] if p["places"] else ("", "")
            w.writerow([k, p["name"], len(p["datasets"]), p["lab_pi"], p["submitter"], country, city,
                        p["country"], p["affiliation"][:160], " ".join(p["datasets"])])
    with EDGES_TSV.open("w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["a", "b", "shared"])
        for (a, b), n in sorted(edges.items(), key=lambda kv: (-kv[1], kv[0])):
            if n >= 2 and a in keep and b in keep:
                w.writerow([a, b, n])


def read_tables() -> tuple[list[dict], list[dict]]:
    if not PEOPLE_TSV.exists():
        raise SystemExit(f"{PEOPLE_TSV.relative_to(ROOT)} not found — run without --plot-only first")
    with PEOPLE_TSV.open(newline="") as fh:
        people = list(csv.DictReader(fh, delimiter="\t"))
    with EDGES_TSV.open(newline="") as fh:
        edges = list(csv.DictReader(fh, delimiter="\t"))
    return people, edges


# --------------------------------------------------------------------------- layout
def force_layout(n: int, links: list[tuple[int, int, float]], iterations: int = 400, seed: int = 7):
    """Fruchterman-Reingold on the unit square with gravity, so stray components stay on screen."""
    rnd = random.Random(seed)
    pos = [[rnd.random() - 0.5, rnd.random() - 0.5] for _ in range(n)]
    k = 1.6 / math.sqrt(max(n, 1))
    temp = 0.1
    for _ in range(iterations):
        disp = [[0.0, 0.0] for _ in range(n)]
        for i in range(n):
            xi, yi = pos[i]
            for j in range(i + 1, n):
                dx, dy = xi - pos[j][0], yi - pos[j][1]
                d2 = dx * dx + dy * dy or 1e-9
                f = k * k / d2
                disp[i][0] += dx * f; disp[i][1] += dy * f
                disp[j][0] -= dx * f; disp[j][1] -= dy * f
        for i, j, w in links:
            dx, dy = pos[i][0] - pos[j][0], pos[i][1] - pos[j][1]
            d = math.hypot(dx, dy) or 1e-9
            f = d * w / k
            disp[i][0] -= dx * f; disp[i][1] -= dy * f
            disp[j][0] += dx * f; disp[j][1] += dy * f
        for i in range(n):
            disp[i][0] -= pos[i][0] * 6 * k; disp[i][1] -= pos[i][1] * 6 * k
            d = math.hypot(*disp[i]) or 1e-9
            step = min(d, temp)
            pos[i][0] += disp[i][0] / d * step
            pos[i][1] += disp[i][1] / d * step
        temp = max(temp * 0.985, 0.002)
    return pos


def components(n: int, links: list[tuple[int, int, float]]) -> list[list[int]]:
    parent = list(range(n))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for a, b, _ in links:
        parent[find(a)] = find(b)
    groups: dict[int, list[int]] = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def separate(xy: list[list[float]], radius: list[float], box: tuple[float, float, float, float], gap: float = 2.5):
    """Push overlapping discs apart in pixel space, keeping every disc inside `box`."""
    x0, y0, x1, y1 = box
    for _ in range(120):
        moved = False
        for i in range(len(xy)):
            for j in range(i + 1, len(xy)):
                dx, dy = xy[j][0] - xy[i][0], xy[j][1] - xy[i][1]
                d = math.hypot(dx, dy) or 1e-6
                overlap = radius[i] + radius[j] + gap - d
                if overlap > 0:
                    moved = True
                    ux, uy = dx / d, dy / d
                    xy[i][0] -= ux * overlap / 2; xy[i][1] -= uy * overlap / 2
                    xy[j][0] += ux * overlap / 2; xy[j][1] += uy * overlap / 2
        for (p, r) in zip(xy, radius):
            p[0] = min(max(p[0], x0 + r), x1 - r)
            p[1] = min(max(p[1], y0 + r), y1 - r)
        if not moved:
            break
    return xy


# --------------------------------------------------------------------------- plot
def authorship_svg(people: list[dict], edges: list[dict], min_datasets: int) -> str:
    shown = [p for p in people if int(p["datasets"]) >= min_datasets]
    index = {p["key"]: i for i, p in enumerate(shown)}
    links = [(index[e["a"]], index[e["b"]], int(e["shared"])) for e in edges if e["a"] in index and e["b"] in index]
    linked = {i for a, b, _ in links for i in (a, b)}
    # people with no link inside the plot are left out: they would only float at the edge
    keep = sorted(linked)
    remap = {old: new for new, old in enumerate(keep)}
    shown = [shown[i] for i in keep]
    links = [(remap[a], remap[b], w) for a, b, w in links]

    pos = force_layout(len(shown), [(a, b, 1 + math.log2(w)) for a, b, w in links])
    xs, ys = [p[0] for p in pos], [p[1] for p in pos]
    top = HEADER_H + 30
    sx = (WIDTH - 2 * PAD - 60) / ((max(xs) - min(xs)) or 1)
    sy = (HEIGHT - top - PAD) / ((max(ys) - min(ys)) or 1)
    scale = min(sx, sy)
    ox = (WIDTH - scale * (max(xs) - min(xs))) / 2 - scale * min(xs)
    oy = top + (HEIGHT - top - PAD - scale * (max(ys) - min(ys))) / 2 - scale * min(ys)
    radius = [2.2 + 1.3 * math.sqrt(int(p["datasets"])) for p in shown]
    xy = separate([[ox + scale * x, oy + scale * y] for x, y in pos], radius,
                  (PAD, top, WIDTH - PAD, HEIGHT - PAD))

    n_cross = sum(shown[a]["group"] != shown[b]["group"] for a, b, _ in links)
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="Authorship network of curated PRIDE datasets">',
        f"<style>{STYLE}</style>",
        f'<rect class="bg" width="{WIDTH}" height="{HEIGHT}" rx="6"/>',
        '<text class="title" x="12" y="22">Who publishes Nordic proteomics — PRIDE authorship network</text>',
        f'<text class="sub" x="12" y="40">{len(shown)} people on ≥ {min_datasets} curated datasets · '
        f'{len(links)} links = sharing ≥ 2 datasets ({n_cross} cross a country, drawn dark) · '
        f'node area ~ datasets · ring = lab PI</text>',
        f'<text class="sub" x="12" y="56">People = PRIDE submitters, lab PIs and publication authors, '
        f'matched on surname + initials. Colour = country holding most of their datasets.</text>',
    ]
    x = 12
    present = {p["group"] for p in shown}
    for key, label, colour in (g for g in GROUPS if g[0] in present):
        out.append(f'<circle cx="{x + 6}" cy="{HEADER_H + 10}" r="6" fill="{colour}"/>')
        out.append(f'<text class="legend" x="{x + 17}" y="{HEADER_H + 14}">{label}</text>')
        x += 17 + 7 * len(label) + 18
    out.append(f'<circle class="ring" cx="{x + 6}" cy="{HEADER_H + 10}" r="5.5" fill="none"/>')
    out.append(f'<text class="legend" x="{x + 17}" y="{HEADER_H + 14}">lab PI on ≥ 1 dataset</text>')

    for a, b, w in sorted(links, key=lambda l: (shown[l[0]]["group"] != shown[l[1]]["group"], l[2])):
        cross = " cross" if shown[a]["group"] != shown[b]["group"] else ""
        (x1, y1), (x2, y2) = xy[a], xy[b]
        out.append(f'<line class="edge{cross}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                   f'stroke-width="{0.5 + 0.6 * math.log2(w):.2f}"/>')

    for i in sorted(range(len(shown)), key=lambda i: radius[i]):
        p = shown[i]
        x, y = xy[i]
        pi = " pi" if int(p["lab_pi"]) else ""
        where = f'{p["city"].title()}, {p["group"].replace("_", " ").title()}' if p["city"] else ""
        tip = (f'{p["name"]} — {p["datasets"]} datasets ({p["lab_pi"]} as lab PI) · {where}'
               + (f' · {p["affiliation"][:90]}' if p["affiliation"] else ""))
        out.append(f'<circle class="node{pi}" cx="{x:.1f}" cy="{y:.1f}" r="{radius[i]:.1f}" '
                   f'fill="{COLOUR.get(p["group"], "#8a8983")}"><title>{escape(tip)}</title></circle>')

    placed: list[tuple[float, float, float, float]] = []
    discs = [(x, y, r) for (x, y), r in zip(xy, radius)]
    by_size = sorted(range(len(shown)), key=lambda i: -int(shown[i]["datasets"]))
    # every separate cluster gets its most-published person named, then the overall top
    comp_top = [max(c, key=lambda i: int(shown[i]["datasets"])) for c in components(len(shown), links) if len(c) >= 3]
    for i in dict.fromkeys([*sorted(comp_top, key=by_size.index), *by_size[:LABEL_TOP]]):
        name = shown[i]["name"]
        x, y = xy[i]
        w, h = 6.2 * len(name), 12
        for lx, ly, anchor in ((x + radius[i] + 3, y + 4, "start"), (x - radius[i] - 3, y + 4, "end"),
                               (x, y - radius[i] - 4, "middle"), (x, y + radius[i] + 12, "middle")):
            x0 = lx if anchor == "start" else lx - w if anchor == "end" else lx - w / 2
            box = (x0, ly - h + 2, x0 + w, ly + 2)
            clash = any(box[0] < b[2] and b[0] < box[2] and box[1] < b[3] and b[1] < box[3] for b in placed)
            covers = any(j != i and box[0] - r < cx < box[2] + r and box[1] - r < cy < box[3] + r
                         for j, (cx, cy, r) in enumerate(discs) if r > 7)
            if not clash and not covers and 2 < box[0] and box[2] < WIDTH - 2 and box[3] < HEIGHT - 2:
                placed.append(box)
                out.append(f'<text class="label" x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}">{escape(name)}</text>')
                break

    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plot-only", action="store_true", help="redraw the SVG from tables/, no records needed")
    ap.add_argument("--refresh", action="store_true", help="re-download every PRIDE record")
    ap.add_argument("--min-datasets", type=int, default=7, help="plot people on at least this many datasets")
    args = ap.parse_args()

    if not args.plot_only:
        manifest = manifests()
        recs = fetch_all(sorted(manifest), args.refresh)
        print(f"{len(recs)}/{len(manifest)} PRIDE records")
        people, edges = build_network(manifest, recs)
        write_tables(people, edges)
        print(f"{len(people)} people, {len(edges)} co-author pairs -> "
              f"{PEOPLE_TSV.relative_to(ROOT)}, {EDGES_TSV.relative_to(ROOT)}")
    PLOT.parent.mkdir(parents=True, exist_ok=True)
    PLOT.write_text(authorship_svg(*read_tables(), args.min_datasets))
    print(f"wrote {PLOT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
