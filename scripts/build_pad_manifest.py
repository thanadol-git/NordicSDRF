#!/usr/bin/env python3
"""All public PRIDE affinity-archive PADs -> affinity_pad/<platform>.txt.

PRIDE has no list endpoint for PAD projects, so this walks PAD000001, PAD000002,
... through the archive API and stops after --stop-after consecutive misses past
the highest accession found (private / unreleased PADs return 404 and are simply
skipped — rerun later and they are picked up once public). Each public PAD is
filed under the first PLATFORMS entry whose pattern matches any instrument name
(Olink platforms, SomaScan, NULISA); anything else goes to `other`.

    python scripts/build_pad_manifest.py            # write manifests + candidates table
    python scripts/build_pad_manifest.py --dry-run  # print what would be written

Writes affinity_pad/<platform>.txt (one PAD per line; these are the `pxd_list`s of
the `affinity_pad` group in config.yml) and results/affinity_pad/candidates.tsv
(every public PAD with its instrument, platform, date and title). Then refresh
the numbers and plots:

    python scripts/update_status.py --no-pride --corpus github
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://www.ebi.ac.uk/pride/ws/archive/v3/projects/{}"
MANIFEST_DIR = ROOT / "affinity_pad"
CANDIDATES = ROOT / "results" / "affinity_pad" / "candidates.tsv"

# (manifest slug, substring of the lower-cased PRIDE instrument name). First match
# wins, so the specific "explore ht" sits above plain "explore". Keep the slugs in
# step with the cities under `affinity_pad` in config.yml. `other` is the fallback
# for public PADs that match none of these patterns.
PLATFORMS = [
    ("explore_ht", "explore ht"),
    ("explore", "explore"),        # Explore 3072/384, 1536, 384, bare "Olink Explore"
    ("target", "target"),          # Target 96 / Target 48
    ("reveal", "reveal"),
    ("unspecified", "olink"),      # generic "Olink instrument model"
    ("somascan", "somascan"),
    ("nulisa", "nulisa"),
]
OTHER = "other"
ALL_SLUGS = [slug for slug, _ in PLATFORMS] + [OTHER]


def fetch(accession: str, retries: int = 3) -> dict | None:
    """PRIDE project record, or None if the accession is not public."""
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(API.format(accession), timeout=60) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            err = exc
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            err = exc
        time.sleep(2 * (attempt + 1))
    sys.exit(f"PRIDE request for {accession} failed: {err}")


def platform_of(record: dict) -> tuple[str, str]:
    """(platform slug, instrument names joined) for one PRIDE record."""
    names = [i.get("name", "") for i in record.get("instruments") or []]
    joined = "; ".join(names)
    blob = " ".join(names).lower().replace("soma scan", "somascan")
    for slug, pat in PLATFORMS:
        if pat in blob:
            return slug, joined
    return OTHER, joined


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--stop-after", type=int, default=30,
                    help="consecutive missing accessions past the last hit before stopping (default 30)")
    ap.add_argument("--dry-run", action="store_true", help="print the result, write nothing")
    args = ap.parse_args()

    rows, n, misses = [], 0, 0
    while misses < args.stop_after:
        n += 1
        acc = f"PAD{n:06d}"
        record = fetch(acc)
        if record is None:
            misses += 1
            continue
        misses = 0
        slug, instruments = platform_of(record)
        rows.append({"accession": acc, "platform": slug, "instrument": instruments,
                     "publication_date": (record.get("publicationDate") or "")[:10],
                     "title": " ".join((record.get("title") or "").split())})
        print(f"  {acc}  {slug:<12} {instruments}")

    manifests = {slug: [r["accession"] for r in rows if r["platform"] == slug] for slug in ALL_SLUGS}
    print(f"\n{len(rows)} public PADs: "
          + ", ".join(f"{slug} {len(ids)}" for slug, ids in manifests.items()))
    if args.dry_run:
        return
    MANIFEST_DIR.mkdir(exist_ok=True)
    for slug, ids in manifests.items():
        (MANIFEST_DIR / f"{slug}.txt").write_text("".join(f"{a}\n" for a in ids))
    CANDIDATES.parent.mkdir(parents=True, exist_ok=True)
    with CANDIDATES.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else ["accession"], delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {MANIFEST_DIR.relative_to(ROOT)}/<platform>.txt and {CANDIDATES.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
