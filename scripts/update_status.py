#!/usr/bin/env python3
"""Refresh the campaign numbers from PRIDE and the working tree.

Reads config.yml, then for every city:
  * pride_hits  - union of accessions returned by the PRIDE Archive v2 full-text
                  search for each of the city's `search_terms` (written to
                  results/pride_hits/<country>/<city>.txt as a raw candidate list)
  * pxd_count   - lines in the curated manifest (`pxd_list`, or `lists/<country>/<city>.txt`
                  if that file exists), if the city is scoped
  * in_corpus   - manifest PXDs that already have an SDRF in the community repo
                  bigbio/sdrf-annotated-datasets (local sibling checkout by default,
                  or the live GitHub tree with --corpus github); the PXDs are written
                  to results/<country>/<city>_in_corpus.txt so tier 1 can drop them
  * screened    - data rows in results/<country>/<city>_screen.tsv, if present
  * annotated   - manifest PXDs with annotations/<PXD>.sdrf.tsv
  * blocked     - manifest PXDs with annotations/<PXD>.BLOCKED.md or listed in
                  annotations/BLOCKED.md

and writes the numbers back to config.yml (values only; comments and layout are
preserved), to the README block between <!-- status:begin --> / <!-- status:end -->,
to status/<country>.md, to the plain tables in tables/<country>.tsv, and redraws
the per-city bar charts in status/plots/<country>.svg from those tables
(scripts/plot_status.py).

    python scripts/update_status.py              # everything
    python scripts/update_status.py --no-pride   # offline: manifests + annotations only
    python scripts/update_status.py --country denmark --dry-run
    python scripts/update_status.py --no-pride --corpus github   # authoritative corpus check
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
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
MACHINE_KEYS = ("pxd_count", "pride_hits", "in_corpus", "screened", "annotated", "blocked")
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
def corpus_from_github() -> set[str] | None:
    """PXDs with at least one .sdrf.tsv under datasets/ in the upstream repo (one request)."""
    req = urllib.request.Request(GITHUB_TREE, headers={"Accept": "application/vnd.github+json",
                                                        "User-Agent": "NordicSDRF-update-status"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            tree = json.loads(resp.read().decode())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"  ! GitHub tree fetch failed ({exc}); falling back to the local checkout", file=sys.stderr)
        return None
    if tree.get("truncated"):
        print("  ! GitHub tree was truncated; corpus check may under-count", file=sys.stderr)
    hits = set()
    for entry in tree.get("tree", []):
        parts = entry.get("path", "").split("/")
        if len(parts) >= 3 and parts[0] == "datasets" and parts[-1].endswith(".sdrf.tsv"):
            hits.add(parts[1])
    return hits


def corpus_from_local(cfg: dict) -> set[str]:
    base = ROOT / cfg.get("tools", {}).get("sdrf_annotated_datasets", "../sdrf-annotated-datasets") / "datasets"
    if not base.exists():
        print(f"  ! local corpus not found at {base}", file=sys.stderr)
        return set()
    return {d.name for d in base.iterdir() if d.is_dir() and any(d.glob("*.sdrf.tsv"))}


def load_corpus(cfg: dict, source: str) -> tuple[set[str], str]:
    if source == "github":
        hits = corpus_from_github()
        if hits is not None:
            return hits, f"GitHub {CORPUS_REPO}"
    return corpus_from_local(cfg), "local checkout"


# --------------------------------------------------------------------------- local counts
def conventional_list_relpath(country: str, slug: str) -> str:
    """Geographic city lists live under lists/; Olink PAD lists stay at olink_pad/."""
    if country == "olink_pad":
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
    return ids


def local_counts(country: str, slug: str, city: dict, blocked: set[str], corpus: set[str]) -> dict[str, int]:
    ids = manifest_ids(country, slug, city)
    ann = ROOT / "annotations"
    in_corpus = sorted(pxd for pxd in ids if pxd in corpus)
    if ids:
        out = ROOT / "results" / country / f"{slug}_in_corpus.txt"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(in_corpus) + ("\n" if in_corpus else ""))
    return {
        "pxd_count": len(ids),
        "in_corpus": len(in_corpus),
        "screened": screened_count(country, slug),
        "annotated": sum((ann / f"{pxd}.sdrf.tsv").exists() for pxd in ids),
        "blocked": sum(pxd in blocked for pxd in ids),
    }


def screened_ids(country: str, slug: str) -> set[str]:
    tsv = ROOT / "results" / country / f"{slug}_screen.tsv"
    if not tsv.exists():
        return set()
    return set(re.findall(r"\b(?:PXD|PRD|MSV|RPXD|PAD)\d+\b", tsv.read_text()))


def city_categories(country: str, slug: str, city: dict, blocked: set[str], corpus: set[str]) -> dict[str, int] | None:
    """Manifest PXDs split into CATEGORIES (plot_status.py), each PXD counted once.

    A PXD that fits several categories goes to the first one in CATEGORIES order
    (annotated > blocked > in corpus > screened > to do), so the counts add up to
    the manifest length. None for a city without a curated manifest.
    """
    if not manifest_relpath(country, slug, city):
        return None
    ann = ROOT / "annotations"
    screened = screened_ids(country, slug)
    tests = {
        "annotated": lambda p: (ann / f"{p}.sdrf.tsv").exists(),
        "blocked": lambda p: p in blocked,
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
    """`name:` from config.yml (e.g. "Olink PAD"), else the key title-cased."""
    return cdata.get("name") or country.title()


def country_plot(country: str, cdata: dict, plots_dir: str) -> str:
    """Heading + the horizontal bar chart drawn by scripts/plot_status.py."""
    title = f"{display_name(country, cdata)} — {human_status(cdata.get('status'))}"
    return f"### {title}\n\n![{title}: SDRF progress per city]({plots_dir}/{country}.svg)"


def render_status_block(cfg: dict) -> str:
    queried = cfg.get("pride_hits_queried", "unknown date")
    intro = (f"One chart per country, one bar per city (shared x scale within a country). A\n"
             f"curated city's bar is its manifest (`lists/<country>/<city>.txt`), split so every PXD\n"
             f"sits in exactly one block, first match wins: *Annotated* (SDRF in `annotations/`),\n"
             f"*Blocked*, *In corpus* (already has an SDRF in [`bigbio/sdrf-annotated-datasets`](https://github.com/{CORPUS_REPO}),\n"
             f"checked against {cfg.get('corpus_source', 'the local checkout')}), *Screened*, *To do*.\n"
             f"A city without a manifest shows a dashed outline sized by its raw PRIDE full-text\n"
             f"hit count (unioned over `search_terms` in `config.yml`, queried {queried}). *Olink PAD*\n"
             f"is every public Olink dataset in PRIDE's affinity archive, one row per platform\n"
             f"(`olink_pad/<platform>.txt`, rebuilt by `python scripts/build_pad_manifest.py`).\n"
             f"The numbers behind each chart are in `tables/<country>.tsv`. Regenerate with\n"
             f"`python scripts/update_status.py`; redraw the charts alone from `tables/` with\n"
             f"`python scripts/plot_status.py`.")
    charts = [country_plot(c, d, "status/plots") for c, d in cfg["countries"].items()]
    return "\n\n".join([intro, *charts])


def update_readme(block: str, dry_run: bool) -> None:
    text = README.read_text()
    if BEGIN not in text or END not in text:
        sys.exit(f"README.md needs {BEGIN} and {END} markers around the status tables")
    head, rest = text.split(BEGIN, 1)
    _, tail = rest.split(END, 1)
    new = f"{head}{BEGIN}\n{block}\n{END}{tail}"
    if not dry_run:
        README.write_text(new)


def write_status_pages(cfg: dict, dry_run: bool) -> None:
    for country, cdata in cfg["countries"].items():
        page = (f"# {display_name(country, cdata)} — {human_status(cdata.get('status'))}\n\n"
                f"Generated by `scripts/update_status.py`; PRIDE hits queried "
                f"{cfg.get('pride_hits_queried', 'unknown date')}.\n\n{country_plot(country, cdata, 'plots')}\n")
        if not dry_run:
            (ROOT / "status").mkdir(exist_ok=True)
            (ROOT / "status" / f"{country}.md").write_text(page)


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
    cfg["corpus_source"] = corpus_source
    print(f"community corpus: {len(corpus)} annotated PXDs ({corpus_source})")
    numbers: dict[tuple[str, str], dict[str, int]] = {}
    discovered_lists: dict[tuple[str, str], str] = {}
    country_status: dict[str, str] = {}
    for country, cdata in cfg["countries"].items():
        if country not in wanted:
            continue
        print(f"{country}:")
        listed = annotated = blocked_n = 0
        for slug, city in (cdata.get("cities") or {}).items():
            n = local_counts(country, slug, city, blocked, corpus)
            path = manifest_relpath(country, slug, city)
            if not path:
                n.pop("pxd_count")
                n.pop("in_corpus")
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
    breakdowns = {(country, slug): city_categories(country, slug, city, blocked, corpus)
                  for country, cdata in cfg["countries"].items()
                  for slug, city in (cdata.get("cities") or {}).items()}
    write_tables(cfg, breakdowns)
    write_plots()
    print(f"\nupdated {CONFIG.name}, README.md status block, status/<country>.md, tables/<country>.tsv, status/plots/<country>.svg"
          + ("" if args.no_pride else f", raw candidate lists in {args.hits_dir}/"))


if __name__ == "__main__":
    main()
