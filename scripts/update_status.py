#!/usr/bin/env python3
"""Refresh the campaign numbers from PRIDE and the working tree.

Reads config.yml, then for every city:
  * pride_hits  - union of accessions returned by the PRIDE Archive v2 full-text
                  search for each of the city's `search_terms` (written to
                  results/pride_hits/<country>/<city>.txt as a raw candidate list)
  * pxd_count   - lines in the curated manifest (`pxd_list`, or `lists/<country>/<city>.txt`
                  if that file exists), if the city is scoped
  * in_corpus   - manifest PXDs that already have an SDRF under datasets/ in
                  bigbio/sdrf-annotated-datasets (local sibling checkout by default,
                  or the live GitHub tree with --corpus github); the PXDs are written
                  to results/<country>/<city>_in_corpus.txt so tier 1 can drop them
  * sandbox     - manifest PXDs with an SDRF under sandbox/ in the same community repo
                  (written to results/<country>/<city>_in_sandbox.txt)
  * screened    - data rows in results/<country>/<city>_screen.tsv, if present
  * annotated   - non-blocked manifest PXDs with annotations/<PXD>.sdrf.tsv
                  or split annotations/<PXD>-*.sdrf.tsv artifacts
  * blocked     - manifest PXDs with a local blocker that are not already in
                  sandbox/ or datasets/ (never published upstream as a draft)

and writes the numbers back to config.yml (values only; comments and layout are
preserved), to the README block between <!-- status:begin --> / <!-- status:end -->,
to status/markdowns/<country>.md, to the plain tables in tables/<country>.tsv, and redraws
the per-city bar charts in status/plots/<country>.svg from those tables
(scripts/plot_status.py).

    python scripts/update_status.py              # everything
    python scripts/update_status.py --no-pride   # offline: manifests + annotations only
    python scripts/update_status.py --country denmark --dry-run
    python scripts/update_status.py --no-pride --corpus github   # authoritative corpus check
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plot_status import CATEGORIES, write_plots, write_tables  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config.yml"
README = ROOT / "README.md"
PRIDE_SEARCH = "https://www.ebi.ac.uk/pride/ws/archive/v2/search/projects"
PAGE_SIZE = 100
ACCESSION_RE = re.compile(r"^(PXD|PRD|MSV|RPXD|PAD)\d+$")
MACHINE_KEYS = ("pxd_count", "pride_hits", "in_corpus", "sandbox", "screened", "annotated", "blocked")
CORPUS_REPO = "bigbio/sdrf-annotated-datasets"
GITHUB_TREE = f"https://api.github.com/repos/{CORPUS_REPO}/git/trees/HEAD?recursive=1"
BEGIN, END = "<!-- status:begin -->", "<!-- status:end -->"


# --------------------------------------------------------------------------- PRIDE
def pride_search(term: str, *, retries: int = 3) -> set[str]:
    """All accessions PRIDE's full-text search returns for one keyword."""
    found: set[str] = set()
    page = 0
    while True:
        url = f"{PRIDE_SEARCH}?keyword={urllib.parse.quote(term)}&pageSize={PAGE_SIZE}&page={page}"
        for attempt in range(retries):
            try:
                with urllib.request.urlopen(url, timeout=60) as resp:
                    total = int(resp.headers.get("total_records", "0") or 0)
                    batch = json.loads(resp.read().decode())
                break
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                if attempt == retries - 1:
                    print(f"    ! PRIDE query failed for {term!r}: {exc}", file=sys.stderr)
                    return found
                time.sleep(2 * (attempt + 1))
        found.update(p["accession"] for p in batch if p.get("accession"))
        if len(batch) < PAGE_SIZE or len(found) >= total:
            return found
        page += 1


def collect_pride_hits(country: str, slug: str, city: dict, out_dir: Path) -> int:
    union: set[str] = set()
    for term in city.get("search_terms") or [city.get("name", slug)]:
        hits = pride_search(term)
        print(f"    {term!r}: {len(hits)}")
        union |= hits
    out = out_dir / country / f"{slug}.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(sorted(union)) + ("\n" if union else ""))
    return len(union)


# --------------------------------------------------------------------------- community corpus
def github_api_headers() -> dict[str, str]:
    """Headers for api.github.com; use GITHUB_TOKEN/GH_TOKEN when set (CI rate limits)."""
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "NordicSDRF-update-status",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _accessions_under(tree_entries: list[dict], top: str) -> set[str]:
    """PXD folder names that contain at least one .sdrf.tsv under top/ (datasets|sandbox)."""
    hits = set()
    for entry in tree_entries:
        parts = entry.get("path", "").split("/")
        if len(parts) >= 3 and parts[0] == top and parts[-1].endswith(".sdrf.tsv"):
            hits.add(parts[1])
    return hits


def github_tree() -> dict | None:
    req = urllib.request.Request(GITHUB_TREE, headers=github_api_headers())
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            tree = json.loads(resp.read().decode())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"  ! GitHub tree fetch failed ({exc})", file=sys.stderr)
        return None
    if tree.get("truncated"):
        print("  ! GitHub tree was truncated; corpus check may under-count", file=sys.stderr)
    return tree


def corpus_from_github() -> set[str] | None:
    """PXDs with at least one .sdrf.tsv under datasets/ in the upstream repo."""
    tree = github_tree()
    if tree is None:
        return None
    return _accessions_under(tree.get("tree", []), "datasets")


def sandbox_from_github() -> set[str] | None:
    """PXDs with at least one .sdrf.tsv under sandbox/ in the upstream repo."""
    tree = github_tree()
    if tree is None:
        return None
    return _accessions_under(tree.get("tree", []), "sandbox")


def _local_repo_base(cfg: dict) -> Path:
    return ROOT / cfg.get("tools", {}).get("sdrf_annotated_datasets", "../sdrf-annotated-datasets")


def corpus_from_local(cfg: dict) -> set[str]:
    base = _local_repo_base(cfg) / "datasets"
    if not base.exists():
        print(f"  ! local corpus not found at {base}", file=sys.stderr)
        return set()
    return {d.name for d in base.iterdir() if d.is_dir() and any(d.glob("*.sdrf.tsv"))}


def sandbox_from_local(cfg: dict) -> set[str]:
    base = _local_repo_base(cfg) / "sandbox"
    if not base.exists():
        print(f"  ! local sandbox not found at {base}", file=sys.stderr)
        return set()
    return {d.name for d in base.iterdir() if d.is_dir() and any(d.glob("*.sdrf.tsv"))}


def load_corpus(cfg: dict, source: str) -> tuple[set[str], str]:
    if source == "github":
        hits = corpus_from_github()
        if hits is not None:
            return hits, f"GitHub {CORPUS_REPO}"
        local = corpus_from_local(cfg)
        if local:
            print("  ! falling back to local checkout", file=sys.stderr)
            return local, "local checkout"
        sys.exit(
            "GitHub corpus fetch failed and no local corpus is available "
            "(set GITHUB_TOKEN / GH_TOKEN, or use --corpus local with a sibling checkout)"
        )
    return corpus_from_local(cfg), "local checkout"


def load_sandbox(cfg: dict, source: str) -> tuple[set[str], str]:
    if source == "github":
        hits = sandbox_from_github()
        if hits is not None:
            return hits, f"GitHub {CORPUS_REPO} sandbox/"
        local = sandbox_from_local(cfg)
        if local:
            print("  ! sandbox falling back to local checkout", file=sys.stderr)
            return local, "local checkout sandbox/"
        return set(), "unavailable"
    return sandbox_from_local(cfg), "local checkout sandbox/"


# --------------------------------------------------------------------------- local counts
def conventional_list_relpath(country: str, slug: str) -> str:
    """Geographic city lists live under lists/; affinity PAD lists stay at affinity_pad/."""
    if country == "affinity_pad":
        return f"{country}/{slug}.txt"
    return f"lists/{country}/{slug}.txt"


def manifest_relpath(country: str, slug: str, city: dict | None = None) -> str | None:
    """Config `pxd_list` if set, else `lists/<country>/<city>.txt` when that file exists."""
    seen: list[str] = []
    for path in (city.get("pxd_list") if city else None,
                 conventional_list_relpath(country, slug),
                 f"{country}/{slug}.txt"):
        if path and path not in seen:
            seen.append(path)
            if (ROOT / path).exists():
                return path
    return None


def manifest_ids(country: str, slug: str, city: dict | None = None) -> list[str]:
    path = manifest_relpath(country, slug, city)
    if not path:
        return []
    return [ln.strip() for ln in (ROOT / path).read_text().splitlines() if ACCESSION_RE.match(ln.strip())]


def screened_count(country: str, slug: str) -> int:
    tsv = ROOT / "results" / country / f"{slug}_screen.tsv"
    if not tsv.exists():
        return 0
    rows = [ln for ln in tsv.read_text().splitlines() if ln.strip()]
    return max(len(rows) - 1, 0)


def blocked_ids() -> set[str]:
    ann = ROOT / "annotations"
    ids = {p.name.split(".")[0] for p in ann.glob("*.BLOCKED.md")}
    summary = ann / "BLOCKED.md"
    if summary.exists():
        ids |= set(re.findall(r"\b(?:PXD|PAD)\d{6}\b", summary.read_text()))
    for tracker in (ROOT / "results").glob("**/*_batch.tsv"):
        with tracker.open(newline="") as fh:
            rows = csv.DictReader(fh, delimiter="\t")
            if not {"accession", "annotation_status"}.issubset(rows.fieldnames or []):
                continue
            ids.update(row["accession"] for row in rows
                       if row["annotation_status"].strip().lower().startswith("blocked"))
    return ids


def has_local_annotation(pxd: str) -> bool:
    """Return true for either a single SDRF or intentional split artifacts."""
    ann = ROOT / "annotations"
    return (ann / f"{pxd}.sdrf.tsv").exists() or any(ann.glob(f"{pxd}-*.sdrf.tsv"))


def local_counts(
    country: str,
    slug: str,
    city: dict,
    blocked: set[str],
    corpus: set[str],
    sandbox: set[str],
) -> dict[str, int]:
    ids = manifest_ids(country, slug, city)
    in_corpus = sorted(pxd for pxd in ids if pxd in corpus)
    in_sandbox = sorted(pxd for pxd in ids if pxd in sandbox)
    if ids:
        out = ROOT / "results" / country / f"{slug}_in_corpus.txt"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(in_corpus) + ("\n" if in_corpus else ""))
        sout = ROOT / "results" / country / f"{slug}_in_sandbox.txt"
        sout.write_text("\n".join(in_sandbox) + ("\n" if in_sandbox else ""))
    # Config "blocked" matches the plot category: local blocker and not upstream.
    unpublished_blocked = sum(pxd in blocked and pxd not in sandbox and pxd not in corpus for pxd in ids)
    return {
        "pxd_count": len(ids),
        "in_corpus": len(in_corpus),
        "sandbox": len(in_sandbox),
        "screened": screened_count(country, slug),
        "annotated": sum(pxd not in blocked and has_local_annotation(pxd) for pxd in ids),
        "blocked": unpublished_blocked,
    }


def screened_ids(country: str, slug: str) -> set[str]:
    tsv = ROOT / "results" / country / f"{slug}_screen.tsv"
    if not tsv.exists():
        return set()
    return set(re.findall(r"\b(?:PXD|PRD|MSV|RPXD|PAD)\d+\b", tsv.read_text()))


def city_categories(
    country: str,
    slug: str,
    city: dict,
    blocked: set[str],
    corpus: set[str],
    sandbox: set[str],
) -> dict[str, int] | None:
    """Manifest PXDs split into CATEGORIES (plot_status.py), each PXD counted once.

    A PXD that fits several categories goes to the first one in CATEGORIES order
    (annotated > sandbox > blocked > in corpus > screened > to do), so the counts
    add up to the manifest length. *Blocked* is only blockers not already in
    sandbox/ or datasets/. None for a city without a curated manifest.
    """
    if not manifest_relpath(country, slug, city):
        return None
    screened = screened_ids(country, slug)
    tests = {
        "annotated": lambda p: p not in blocked and has_local_annotation(p),
        "sandbox": lambda p: p in sandbox,
        "blocked": lambda p: p in blocked and p not in sandbox and p not in corpus,
        "in_corpus": lambda p: p in corpus,
        "screened": lambda p: p in screened,
        "todo": lambda p: True,
    }
    counts = {key: 0 for key, *_ in CATEGORIES}
    for pxd in manifest_ids(country, slug, city):
        counts[next(key for key, *_ in CATEGORIES if tests[key](pxd))] += 1
    return counts


# --------------------------------------------------------------------------- writers
def update_config_text(text: str, numbers: dict[tuple[str, str], dict[str, int]], top: dict[str, str],
                       discovered_lists: dict[tuple[str, str], str] | None = None,
                       country_status: dict[str, str] | None = None) -> str:
    """Rewrite machine-owned scalar values in place, keeping comments and order.

    `top` holds top-level bookkeeping keys (pride_hits_queried, corpus_source);
    they are updated if present and inserted just above `countries:` otherwise.
    `discovered_lists` inserts a missing `pxd_list` when `lists/<country>/<city>.txt` exists.
    `country_status` rewrites each country's `status:` from scoped-city progress.
    """
    discovered_lists = discovered_lists or {}
    country_status = country_status or {}
    out, country, city, seen = [], None, None, set()
    key_re = re.compile(r"^(\s*)([A-Za-z_][\w-]*):(.*)$")

    def flush_missing() -> None:
        # machine keys computed for this city but absent from its block: add them after the last one
        extras: list[str] = []
        if country and city and (country, city) in numbers:
            if (country, city) in discovered_lists and "pxd_list" not in seen:
                extras.append(f"{' ' * 8}pxd_list: {discovered_lists[(country, city)]}")
            for key in MACHINE_KEYS:
                if key in numbers[(country, city)] and key not in seen:
                    extras.append(f"{' ' * 8}{key}: {numbers[(country, city)][key]}")
        if extras:
            insert_at = len(out)
            while insert_at and out[insert_at - 1] == "":
                insert_at -= 1
            out[insert_at:insert_at] = extras

    for line in text.splitlines():
        m = key_re.match(line)
        if m:
            indent, key, rest = len(m.group(1)), m.group(2), m.group(3)
            if indent <= 6:
                flush_missing()
                seen = set()
            if indent == 2:
                country, city = key, None
            elif indent == 4 and country and key == "status" and country in country_status:
                line = f"    status: {country_status[country]}"
            elif indent == 6 and country:
                city = key
            elif indent == 8 and key == "pxd_list":
                seen.add("pxd_list")
            elif indent == 8 and country and city and key in MACHINE_KEYS and (country, city) in numbers:
                seen.add(key)
                if key in numbers[(country, city)]:
                    comment = rest.split("#", 1)[1] if "#" in rest else None
                    line = f"{' ' * indent}{key}: {numbers[(country, city)][key]}"
                    if comment is not None:
                        line += f"  #{comment}"
            elif indent == 0 and key in top:
                line = f"{key}: {top[key]}"
        out.append(line)
    flush_missing()
    missing_top = [f"{k}: {v}" for k, v in top.items() if not any(l.startswith(f"{k}:") for l in out)]
    if missing_top:
        insert_at = next((i for i, l in enumerate(out) if l.startswith("countries:")), len(out))
        out[insert_at:insert_at] = [*missing_top, ""]
    return "\n".join(out) + "\n"


def numbers_countries(numbers: dict[tuple[str, str], dict[str, int]]) -> set[str]:
    return {c for c, _ in numbers}


def human_status(status: str) -> str:
    return (status or "not_started").replace("_", " ")


def display_name(country: str, cdata: dict) -> str:
    """`name:` from config.yml (e.g. "Affinity PAD"), else the key title-cased."""
    return cdata.get("name") or country.title()


MARKDOWNS_DIR = "status/markdowns"
MARKDOWNS_LINK = f"[Country status pages]({MARKDOWNS_DIR}/)"


def country_plot(country: str, cdata: dict, plots_dir: str, *, collapsed: bool = False) -> str:
    """Heading + the horizontal bar chart drawn by scripts/plot_status.py.

    When `collapsed` is true (README region sections), wrap in <details> so the
    region overview stays visible and per-country charts stay one click away.
    """
    title = f"{display_name(country, cdata)} — {human_status(cdata.get('status'))}"
    image = f"![{title}: SDRF progress per city]({plots_dir}/{country}.svg)"
    if not collapsed:
        return f"### {title}\n\n{image}"
    # Blank lines inside <details> keep GitHub's markdown image renderer happy.
    return (
        f"<details>\n"
        f"<summary><strong>{title}</strong></summary>\n\n"
        f"{image}\n\n"
        f"</details>"
    )


def overview_plot(plots_dir: str) -> str:
    """Nordic-country horizontal stacked bars, drawn by plot_status.py."""
    title = "Nordic countries — listed PXDs"
    return (
        f"### {title}\n\n"
        f"![{title}: SDRF progress by country]({plots_dir}/overview.svg)\n\n"
        f"Per-country pages: {MARKDOWNS_LINK}"
    )


def region_status(cfg: dict, region: str) -> str:
    statuses = [d.get("status") or "not_started"
                for d in cfg["countries"].values() if d.get("region") == region]
    if "in_progress" in statuses:
        return "in_progress"
    if "scoped" in statuses:
        return "scoped"
    return "not_started"


def sea_region_status(cfg: dict) -> str:
    return region_status(cfg, "sea")


def region_plot(title: str, svg_name: str, plots_dir: str) -> str:
    """Region overview markdown (horizontal bars) with a link to country pages."""
    return (
        f"### {title}\n\n"
        f"![{title}: SDRF progress by country]({plots_dir}/{svg_name})\n\n"
        f"Per-country pages: {MARKDOWNS_LINK}"
    )


def sea_plot(plots_dir: str) -> str:
    """SEA region overview (horizontal bars), matching the Nordic overview layout."""
    return region_plot("Southeast Asia — listed PXDs", "sea.svg", plots_dir)


def south_asia_plot(plots_dir: str) -> str:
    """South Asia region overview (horizontal bars), matching SEA/Nordic layout."""
    return region_plot("South Asia — listed PXDs", "south_asia.svg", plots_dir)


def middle_east_plot(plots_dir: str) -> str:
    """Middle East region overview (horizontal bars), matching SEA/Nordic layout."""
    return region_plot("Middle East — listed PXDs", "middle_east.svg", plots_dir)


def central_asia_plot(plots_dir: str) -> str:
    """Central Asia region overview (horizontal bars), matching SEA/Nordic layout."""
    return region_plot("Central Asia — listed PXDs", "central_asia.svg", plots_dir)


def countries_in_region(cfg: dict, region: str) -> list[tuple[str, dict]]:
    return [(c, d) for c, d in cfg["countries"].items() if d.get("region", "nordic") == region]


def render_status_block(cfg: dict) -> str:
    queried = cfg.get("pride_hits_queried", "unknown date")
    intro = (f"Region overviews are shown below. Per-country city charts (Nordic, SEA, South Asia,\n"
             f"Middle East, Central Asia) live in {MARKDOWNS_LINK} (and `status/plots/<country>.svg`).\n"
             f"A curated city's bar is its manifest (`lists/<country>/<city>.txt`),\n"
             f"split so every PXD sits in exactly one block: *Local SDRF* (a local file without a\n"
             f"blocker, including files awaiting review), *Sandbox* (an SDRF under `sandbox/` in\n"
             f"[`bigbio/sdrf-annotated-datasets`](https://github.com/{CORPUS_REPO})),\n"
             f"*Blocked* (local or batch-tracker blocker **and** not already in `sandbox/` or\n"
             f"`datasets/` — never published upstream as a draft), *In corpus* (already under\n"
             f"`datasets/`, checked against {cfg.get('corpus_source', 'the local checkout')}),\n"
             f"*Screened*, *To do*.\n"
             f"A city without a manifest shows a dashed outline sized by its raw PRIDE full-text\n"
             f"hit count (unioned over `search_terms` in `config.yml`, queried {queried}). *Affinity PAD*\n"
             f"is every public dataset in PRIDE's affinity archive, one row per technology\n"
             f"(Olink platforms, SomaScan, NULISA, Other; `affinity_pad/<platform>.txt`, rebuilt by\n"
             f"`python scripts/build_pad_manifest.py`). Regional search terms live in\n"
             f"`criteria/sea_cities.md`, `criteria/south_asia_cities.md`, `criteria/middleeast_cities.md`,\n"
             f"`criteria/central_asia_cities.md` / `config.yml`.\n"
             f"*To do* is ready for annotation; *Blocked* PXDs need missing metadata before a sandbox or datasets PR.\n"
             f"The numbers behind each chart are in `tables/<country>.tsv`. Regenerate with\n"
             f"`python scripts/update_status.py`; redraw the charts alone from `tables/` with\n"
             f"`python scripts/plot_status.py`.")
    affinity = countries_in_region(cfg, "affinity")
    sea = countries_in_region(cfg, "sea")
    south_asia = countries_in_region(cfg, "south_asia")
    middle_east = countries_in_region(cfg, "middle_east")
    central_asia = countries_in_region(cfg, "central_asia")
    # Per-country charts stay in status/markdowns/ + status/plots/; README only
    # shows region overviews (with a link to those pages).
    parts = [intro, overview_plot("status/plots")]
    if sea:
        parts.append(sea_plot("status/plots"))
    if south_asia:
        parts.append(south_asia_plot("status/plots"))
    if middle_east:
        parts.append(middle_east_plot("status/plots"))
    if central_asia:
        parts.append(central_asia_plot("status/plots"))
    for c, d in affinity:
        # Affinity is a single multi-row chart; keep it open with a link under the image.
        title = f"{display_name(c, d)} — {human_status(d.get('status'))}"
        parts.append(
            f"### {title}\n\n"
            f"![{title}: SDRF progress per city](status/plots/{c}.svg)\n\n"
            f"Page: [{MARKDOWNS_DIR}/{c}.md]({MARKDOWNS_DIR}/{c}.md) · all pages: {MARKDOWNS_LINK}"
        )
    return "\n\n".join(parts)


def update_readme(block: str, dry_run: bool) -> None:
    text = README.read_text()
    if BEGIN not in text or END not in text:
        sys.exit(f"README.md needs {BEGIN} and {END} markers around the status tables")
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    new = f"{head}{BEGIN}\n{block}\n{END}{tail}"
    if not dry_run:
        README.write_text(new)


def write_region_index_page(
    cfg: dict,
    pages_dir: Path,
    *,
    region: str,
    filename: str,
    heading: str,
    plot_md: str,
) -> None:
    countries = countries_in_region(cfg, region)
    if not countries:
        return
    links = "\n".join(
        f"- [{display_name(c, d)}]({c}.md) — {human_status(d.get('status'))}"
        for c, d in countries
    )
    (pages_dir / filename).write_text(
        f"# {heading} — {human_status(region_status(cfg, region))}\n\n"
        f"Generated by `scripts/update_status.py`; PRIDE hits queried "
        f"{cfg.get('pride_hits_queried', 'unknown date')}. "
        f"Region overview below; per-country city charts are linked under it.\n\n"
        f"{plot_md}\n\n"
        f"### Countries\n\n{links}\n"
    )


def write_status_pages(cfg: dict, dry_run: bool) -> None:
    pages_dir = ROOT / "status" / "markdowns"
    if not dry_run:
        pages_dir.mkdir(parents=True, exist_ok=True)
    for country, cdata in cfg["countries"].items():
        page = (f"# {display_name(country, cdata)} — {human_status(cdata.get('status'))}\n\n"
                f"Generated by `scripts/update_status.py`; PRIDE hits queried "
                f"{cfg.get('pride_hits_queried', 'unknown date')}.\n\n"
                f"{country_plot(country, cdata, '../plots')}\n")
        if not dry_run:
            (pages_dir / f"{country}.md").write_text(page)
    if dry_run:
        return
    write_region_index_page(
        cfg, pages_dir, region="sea", filename="sea.md",
        heading="Southeast Asia", plot_md=sea_plot("../plots"),
    )
    write_region_index_page(
        cfg, pages_dir, region="south_asia", filename="south_asia.md",
        heading="South Asia", plot_md=south_asia_plot("../plots"),
    )
    write_region_index_page(
        cfg, pages_dir, region="middle_east", filename="middle_east.md",
        heading="Middle East", plot_md=middle_east_plot("../plots"),
    )
    write_region_index_page(
        cfg, pages_dir, region="central_asia", filename="central_asia.md",
        heading="Central Asia", plot_md=central_asia_plot("../plots"),
    )


# --------------------------------------------------------------------------- main
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-pride", action="store_true", help="skip PRIDE queries; keep existing pride_hits")
    ap.add_argument("--country", action="append", help="limit to one or more countries (repeatable)")
    ap.add_argument("--dry-run", action="store_true", help="print the numbers, write nothing")
    ap.add_argument("--hits-dir", default="results/pride_hits", help="where raw PRIDE candidate lists go")
    ap.add_argument("--corpus", choices=["local", "github"], default="local",
                    help="where to check for existing community annotations (default: local sibling checkout)")
    args = ap.parse_args()

    text = CONFIG.read_text()
    cfg = yaml.safe_load(text)
    wanted = set(args.country or cfg["countries"])
    unknown = wanted - set(cfg["countries"])
    if unknown:
        sys.exit(f"unknown countries: {sorted(unknown)}")

    blocked = blocked_ids()
    corpus, corpus_source = load_corpus(cfg, args.corpus)
    sandbox, sandbox_source = load_sandbox(cfg, args.corpus)
    cfg["corpus_source"] = corpus_source
    print(f"community corpus: {len(corpus)} datasets/ PXDs ({corpus_source})")
    print(f"community sandbox: {len(sandbox)} sandbox/ PXDs ({sandbox_source})")
    print(f"local blockers: {len(blocked)}; "
          f"blocked∩sandbox={len(blocked & sandbox)}; "
          f"blocked∩datasets={len(blocked & corpus)}; "
          f"blocked never upstream={len(blocked - sandbox - corpus)}")
    numbers: dict[tuple[str, str], dict[str, int]] = {}
    discovered_lists: dict[tuple[str, str], str] = {}
    country_status: dict[str, str] = {}
    for country, cdata in cfg["countries"].items():
        if country not in wanted:
            continue
        print(f"{country}:")
        listed = annotated = blocked_n = 0
        for slug, city in (cdata.get("cities") or {}).items():
            n = local_counts(country, slug, city, blocked, corpus, sandbox)
            path = manifest_relpath(country, slug, city)
            if not path:
                n.pop("pxd_count", None)
                n.pop("in_corpus", None)
                n.pop("sandbox", None)
            elif not city.get("pxd_list"):
                discovered_lists[(country, slug)] = path
                city["pxd_list"] = path
            if not args.no_pride and cdata.get("pride_search", True):
                print(f"  {city.get('name', slug)} — PRIDE search")
                n["pride_hits"] = collect_pride_hits(country, slug, city, ROOT / args.hits_dir)
            numbers[(country, slug)] = n
            city.update(n)
            listed += n.get("pxd_count") or 0
            annotated += n.get("annotated") or 0
            blocked_n += n.get("blocked") or 0
            print(f"  {city.get('name', slug):<12} " + "  ".join(f"{k}={v}" for k, v in n.items()))
        status = "in_progress" if annotated or blocked_n else "scoped" if listed else "not_started"
        country_status[country] = status
        cdata["status"] = status

    top = {"corpus_source": f"{corpus_source} ({dt.date.today().isoformat()})"}
    if not args.no_pride:
        top["pride_hits_queried"] = dt.date.today().isoformat()
    cfg.update(top)
    new_text = update_config_text(text, numbers, top, discovered_lists, country_status)

    block = render_status_block(cfg)
    if args.dry_run:
        print("\n--- README status block ---\n" + block)
        return
    CONFIG.write_text(new_text)
    update_readme(block, dry_run=False)
    write_status_pages(cfg, dry_run=False)
    breakdowns = {(country, slug): city_categories(country, slug, city, blocked, corpus, sandbox)
                  for country, cdata in cfg["countries"].items()
                  for slug, city in (cdata.get("cities") or {}).items()}
    write_tables(cfg, breakdowns)
    write_plots()
    print(f"\nupdated {CONFIG.name}, README.md status block, status/markdowns/, tables/, "
          f"status/plots/overview.svg + sea.svg + south_asia.svg + middle_east.svg + central_asia.svg + per-country charts"
          + ("" if args.no_pride else f", raw candidate lists in {args.hits_dir}/"))

if __name__ == "__main__":
    main()
