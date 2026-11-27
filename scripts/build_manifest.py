#!/usr/bin/env python3
"""Build a curated lists/<country>/<city>.txt manifest from PRIDE (tier 1, no LLM).

PRIDE has no working country filter, so:
  1. run the city's `search_terms` from config.yml (plus --term extras) through the
     PRIDE full-text search and union the accessions;
  2. fetch every candidate's project record;
  3. keep an accession only if the country is confirmed by the record itself:
       - <Country> in `countries`, or a submitter's `country`, or
       - a city/institution term or the country name appears in a submitter/PI
         affiliation string (case-insensitive);
  4. write the confirmed PXDs to lists/<country>/<city>.txt (unless --dry-run) and an
     evidence table for *all* candidates to results/<country>/<city>_candidates.tsv.

Legacy `PRD` ids are reported but never written to the manifest. Accessions already
in the community corpus are kept in the manifest (the status script counts them
separately) but flagged in the evidence table.

    python scripts/build_manifest.py iceland reykjavik
    python scripts/build_manifest.py iceland reykjavik --term "University of Iceland" --term Landspitali --term deCODE
    python scripts/build_manifest.py denmark odense --dry-run
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PRIDE = "https://www.ebi.ac.uk/pride/ws/archive/v2"
PAGE_SIZE = 100

DEMONYMS = {
    "sweden": ["Swedish"], "norway": ["Norwegian"], "denmark": ["Danish"],
    "finland": ["Finnish"], "iceland": ["Icelandic"],
    "india": ["Indian"], "pakistan": ["Pakistani"], "nepal": ["Nepali", "Nepalese"],
    "sri_lanka": ["Sri Lankan"], "bangladesh": ["Bangladeshi"],
    "bhutan": ["Bhutanese"], "maldives": ["Maldivian"], "afghanistan": ["Afghan"],
    "singapore": ["Singaporean"], "thailand": ["Thai"], "malaysia": ["Malaysian"],
    "vietnam": ["Vietnamese"], "philippines": ["Filipino", "Philippine"],
    "indonesia": ["Indonesian"], "myanmar": ["Burmese", "Myanmar"],
    "laos": ["Lao", "Laotian"], "cambodia": ["Cambodian"], "brunei": ["Bruneian"],
    "timor_leste": ["Timorese"],
}


def get_json(url: str, retries: int = 3):
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                return json.loads(resp.read().decode()), int(resp.headers.get("total_records", "0") or 0)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            if attempt == retries - 1:
                print(f"  ! {url}: {exc}", file=sys.stderr)
                return None, 0
            time.sleep(2 * (attempt + 1))


def search(term: str) -> set[str]:
    found, page = set(), 0
    while True:
        url = f"{PRIDE}/search/projects?keyword={urllib.parse.quote(term)}&pageSize={PAGE_SIZE}&page={page}"
        batch, total = get_json(url)
        if not batch:
            return found
        found.update(p["accession"] for p in batch if p.get("accession"))
        if len(batch) < PAGE_SIZE or len(found) >= total:
            return found
        page += 1


def country_display_name(slug: str, cfg_country: dict | None = None) -> str:
    """Human country name for PRIDE `countries` matching (e.g. sri_lanka → Sri Lanka)."""
    if cfg_country and cfg_country.get("name"):
        return str(cfg_country["name"])
    return slug.replace("_", " ").title()


def classify(rec: dict, country_slug: str, terms: list[str], *,
             display_name: str | None = None) -> tuple[bool, str]:
    """Return (confirmed, evidence)."""
    cname = display_name or country_display_name(country_slug)
    slug_l = country_slug.lower()
    name_l = cname.lower()
    people = (rec.get("submitters") or []) + (rec.get("labPIs") or [])
    countries = rec.get("countries") or []
    if cname in countries or any((c or "").lower() == name_l for c in countries):
        return True, f"countries={countries}"
    for p in people:
        pc = (p.get("country") or "").strip().lower()
        if pc in {slug_l, name_l, slug_l.replace("_", " ")}:
            return True, f"submitter country={cname} ({p.get('name')})"
    needles = [t.lower() for t in [cname, *DEMONYMS.get(country_slug, []), *terms] if t]
    for p in people:
        aff = (p.get("affiliation") or "")
        low = aff.lower()
        hit = next((n for n in needles if n and n in low), None)
        if hit:
            return True, f"affiliation~'{hit}': {aff[:90]}"
    affs = " ; ".join((p.get("affiliation") or "")[:60] for p in people) or "(no affiliation)"
    return False, f"countries={countries} | {affs}"

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("country")
    ap.add_argument("city")
    ap.add_argument("--term", action="append", default=[], help="extra search term (repeatable)")
    ap.add_argument("--dry-run", action="store_true", help="do not write the manifest")
    args = ap.parse_args()

    cfg = yaml.safe_load((ROOT / "config.yml").read_text())
    try:
        cdata = cfg["countries"][args.country]
        city = cdata["cities"][args.city]
    except KeyError:
        sys.exit(f"{args.country}/{args.city} is not in config.yml")
    display = country_display_name(args.country, cdata)
    terms = list(dict.fromkeys([*(city.get("search_terms") or [city.get("name", args.city)]), *args.term]))
    # affiliation matching also accepts every other city term of the same country
    country_terms = list(dict.fromkeys(
        t for c in cdata["cities"].values() for t in (c.get("search_terms") or [])))

    corpus_dir = ROOT / cfg.get("tools", {}).get("sdrf_annotated_datasets", "../sdrf-annotated-datasets") / "datasets"
    corpus = {d.name for d in corpus_dir.iterdir()} if corpus_dir.exists() else set()

    print(f"{args.country}/{args.city}: searching PRIDE for {terms} (country={display})")
    candidates: set[str] = set()
    for t in terms:
        hits = search(t)
        print(f"  {t!r}: {len(hits)}")
        candidates |= hits
    print(f"  {len(candidates)} unique candidates; fetching records")

    rows, confirmed = [], []
    for acc in sorted(candidates):
        rec, _ = get_json(f"{PRIDE}/projects/{acc}")
        if not rec:
            rows.append((acc, "error", "record fetch failed", "", ""))
            continue
        ok, evidence = classify(rec, args.country, country_terms, display_name=display)
        legacy = not acc.startswith("PXD")
        verdict = "legacy_id" if legacy and ok else "confirmed" if ok else "rejected"
        rows.append((acc, verdict, evidence, "yes" if acc in corpus else "", (rec.get("title") or "")[:100]))
        if ok and not legacy:
            confirmed.append(acc)
        print(f"  {acc} {verdict:<10} {evidence[:100]}")

    out_tsv = ROOT / "results" / args.country / f"{args.city}_candidates.tsv"
    out_tsv.parent.mkdir(parents=True, exist_ok=True)
    with out_tsv.open("w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["accession", "verdict", "evidence", "in_corpus", "title"])
        w.writerows(rows)

    manifest = ROOT / "lists" / args.country / f"{args.city}.txt"
    n_rej = sum(r[1] == "rejected" for r in rows)
    n_leg = sum(r[1] == "legacy_id" for r in rows)
    print(f"\n{len(confirmed)} confirmed, {n_rej} rejected, {n_leg} legacy ids -> {out_tsv.relative_to(ROOT)}")
    if args.dry_run:
        print(f"dry run: not writing {manifest.relative_to(ROOT)}")
        return
    manifest.parent.mkdir(parents=True, exist_ok=True)
    existing = set()
    if manifest.exists():
        existing = {ln.strip() for ln in manifest.read_text().splitlines() if ln.strip()}
    if existing:
        new = sorted(set(confirmed) - existing)
        print(f"{manifest.relative_to(ROOT)} exists ({len(existing)} lines); "
              f"{len(new)} confirmed PXDs are not in it: {new}")
        print("not overwriting — merge by hand or delete the file to regenerate")
        return
    manifest.write_text("\n".join(confirmed) + ("\n" if confirmed else ""))
    print(f"wrote {manifest.relative_to(ROOT)} ({len(confirmed)} PXDs). Next:\n"
          f"    python scripts/update_status.py --no-pride --corpus github")

if __name__ == "__main__":
    main()
