#!/usr/bin/env python3
"""Build today's annotation queue (default 10 PXDs) from scoped manifests.

Skips PXDs that already have an SDRF here, a BLOCKED file, or an SDRF in the
community corpus. If a city has `results/<country>/<city>_screen.tsv`, only
`include` rows are queued (exclude/uncertain stay out). Otherwise every
remaining manifest PXD is a candidate — Iceland is small enough that this is
the whole country.

    python scripts/daily_queue.py iceland              # next 10, write results/queue/
    python scripts/daily_queue.py iceland --limit 3
    python scripts/daily_queue.py --dry-run            # all scoped countries, print only
    python scripts/daily_queue.py iceland --corpus github

Does not start any job. Print the Claude (tier 3) commands for the queue, and
one optional overnight local command only if nothing is already running.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from update_status import (  # noqa: E402
    ACCESSION_RE,
    ROOT,
    blocked_ids,
    load_corpus,
    manifest_ids,
)

ANN = ROOT / "annotations"
LOGS = ROOT / "results" / "logs"
QUEUE = ROOT / "results" / "queue"


def live_pxds() -> set[str]:
    """PXDs with a live Claude Code process or a JSONL that has no result event."""
    live: set[str] = set()
    try:
        out = subprocess.check_output(["pgrep", "-af", "sdrf-annotate PXD"], text=True)
    except subprocess.CalledProcessError:
        out = ""
    for line in out.splitlines():
        if "cursorsandbox" in line or "pgrep" in line:
            continue
        for tok in line.split():
            if ACCESSION_RE.match(tok) and tok.startswith("PXD"):
                live.add(tok)
    if not LOGS.exists():
        return live
    latest: dict[str, Path] = {}
    for path in LOGS.glob("PXD*.jsonl"):
        pxd = path.name.split(".")[0]
        if pxd not in latest or path.stat().st_mtime > latest[pxd].stat().st_mtime:
            latest[pxd] = path
    for pxd, path in latest.items():
        finished = False
        for line in path.read_text().splitlines():
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") == "result":
                finished = True
        if not finished:
            live.add(pxd)
    return live


def screen_verdicts(country: str, slug: str) -> dict[str, str]:
    tsv = ROOT / "results" / country / f"{slug}_screen.tsv"
    if not tsv.exists():
        return {}
    out: dict[str, str] = {}
    with tsv.open() as fh:
        for row in csv.reader(fh, delimiter="\t"):
            if not row or not ACCESSION_RE.match(row[0]):
                continue
            out[row[0]] = (row[1] if len(row) > 1 else "").strip().lower()
    return out


def classify(pxd: str, city: str, blocked: set[str], corpus: set[str],
             screen: dict[str, str], live: set[str]) -> tuple[str, str]:
    if (ANN / f"{pxd}.sdrf.tsv").exists():
        return "annotated", "SDRF already in annotations/"
    if pxd in blocked or (ANN / f"{pxd}.BLOCKED.md").exists():
        return "blocked", "blocked here"
    if pxd in corpus:
        return "in_corpus", "already in bigbio/sdrf-annotated-datasets — skip"
    if pxd in live:
        return "running", "local/Slurm job already in flight — do not start another"
    if screen:
        verdict = screen.get(pxd)
        if verdict == "include":
            return "include", "screened include"
        if verdict == "exclude":
            return "exclude", "screened exclude"
        if verdict == "uncertain":
            return "uncertain", "screened uncertain — not in the daily 10"
        return "unscreened", "not in the screen TSV"
    return "pending", f"{city}: no screen yet; queued as a candidate"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("country", nargs="?", help="limit to one country (default: all scoped)")
    ap.add_argument("--limit", type=int, default=10, help="max PXDs to queue (default 10)")
    ap.add_argument("--dry-run", action="store_true", help="print, do not write results/queue/")
    ap.add_argument("--corpus", choices=["local", "github"], default="local")
    args = ap.parse_args()

    cfg = yaml.safe_load((ROOT / "config.yml").read_text())
    wanted = args.country or None
    if wanted and wanted not in cfg["countries"]:
        sys.exit(f"unknown country: {wanted}")

    corpus, corpus_src = load_corpus(cfg, args.corpus)
    blocked = blocked_ids()
    live = live_pxds()
    today = dt.date.today().isoformat()

    rows = []  # (country, city, pxd, status, note)
    for country, cdata in cfg["countries"].items():
        if wanted and country != wanted:
            continue
        for slug, city in (cdata.get("cities") or {}).items():
            ids = manifest_ids(country, slug, city)
            if not ids:
                continue
            screen = screen_verdicts(country, slug)
            for pxd in ids:
                status, note = classify(pxd, slug, blocked, corpus, screen, live)
                rows.append((country, slug, pxd, status, note))

    queueable = {"include", "pending"}
    queued = [r for r in rows if r[3] in queueable][: args.limit]
    skipped = [r for r in rows if r[3] not in queueable]
    running = [r for r in rows if r[3] == "running"]

    label = wanted or "all"
    print(f"corpus: {len(corpus)} PXDs ({corpus_src})")
    print(f"{len(rows)} scoped PXDs  |  {len(queued)} in today's queue (limit {args.limit})  |  "
          f"{len(running)} already running")
    if queued:
        print("\nToday — annotate these with Claude (tier 3):")
        for country, slug, pxd, status, note in queued:
            print(f"  {pxd}  {country}/{slug}  {status}  {note}")
        print("\n    # in Claude Code, from the sdrf-skills plugin:")
        for *_, pxd, _, _ in queued:
            print(f"    /sdrf-skills:sdrf-annotate {pxd}")
    else:
        print("\nNothing to queue (all scoped PXDs are done, blocked, in the corpus, or running).")

    if running:
        print("\nAlready running (leave them; do not start a second local job):")
        for country, slug, pxd, _, note in running:
            print(f"  {pxd}  {country}/{slug}  {note}")

    leftover = [r for r in skipped if r[3] in {"in_corpus", "annotated", "blocked", "exclude", "uncertain"}]
    if leftover:
        print("\nSkipped:")
        for country, slug, pxd, status, note in leftover:
            print(f"  {pxd}  {country}/{slug}  {status}  {note}")

    if not running and queued:
        first = queued[0][2]
        print("\nOptional overnight local draft (only if the GPU is free — one PXD):")
        print(f"  NORDIC_BATCH=1 scripts/annotate_local.sh {first}")
        print("  # or Slurm, after the current job finishes:")
        if wanted:
            # array index is 1-based line number in that country's first queued city's manifest
            country, slug, pxd, _, _ = queued[0]
            manifest = ROOT / wanted / f"{slug}.txt"
            if manifest.exists():
                lines = [ln.strip() for ln in manifest.read_text().splitlines() if ln.strip()]
                if pxd in lines:
                    idx = lines.index(pxd) + 1
                    print(f"  sbatch --array={idx}-{idx}%1 scripts/annotate_slurm.sbatch {wanted}/{slug}.txt")
    elif running:
        print("\nGPU is busy — no overnight local start suggested.")

    if args.dry_run or not queued:
        return
    QUEUE.mkdir(parents=True, exist_ok=True)
    dest = QUEUE / f"{today}_{label}.txt"
    lines = [f"# daily queue {today} {label}  ({len(queued)} PXDs, cap {args.limit})"]
    for country, slug, pxd, status, note in queued:
        lines.append(f"{pxd}\t{country}/{slug}\t{status}\t{note}")
    dest.write_text("\n".join(lines) + "\n")
    print(f"\nwrote {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
