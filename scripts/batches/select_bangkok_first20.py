"""Select bangkok-1: the 20 remaining Bangkok deposits with the fewest RAW files.

Pool: lists/thailand/bangkok.txt minus BigBio corpus (bangkok_in_corpus.txt) minus any
local annotation. RAW counts come from ProteomeCentral PROXI (compact result,
column "files (raw/total)"), cached in results/thailand/bangkok_proxi_counts.tsv because
the PRIDE API was unreachable from the annotation session. Deposits with 0 or unknown RAW
are excluded. Ties break on total file count, then accession.

Usage: python scripts/batches/select_bangkok_first20.py
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TH = ROOT / "results/thailand"
OUT = TH / "bangkok_first20_batch.tsv"

manifest = [l.strip() for l in (ROOT / "lists/thailand/bangkok.txt").read_text().splitlines() if l.startswith("PXD")]
corpus = set((TH / "bangkok_in_corpus.txt").read_text().split())
local = {p.name[:9] for p in (ROOT / "annotations").glob("PXD*")}
counts = {r["accession"]: r for r in csv.DictReader((TH / "bangkok_proxi_counts.tsv").open(), delimiter="\t")}
current = {r["accession"]: r["annotation_status"] for r in csv.DictReader(OUT.open(), delimiter="\t")} if OUT.exists() else {}

pool = []
for acc in manifest:
    if acc in corpus or (acc in local and acc not in current):
        continue
    r = counts.get(acc)
    if r is None:
        raise SystemExit(f"no PROXI count cached for {acc}")
    if not r["raw"].isdigit() or int(r["raw"]) == 0:
        continue
    pool.append((int(r["raw"]), int(r["total"]), acc, r["title"]))

selected = sorted(pool)[:20]
with OUT.open("w", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["batch_order", "accession", "raw_count", "total_files", "annotation_status", "title"])
    for i, (raw, total, acc, title) in enumerate(selected, 1):
        w.writerow([i, acc, raw, total, current.get(acc, "queued: evidence review"), title])
print(f"wrote {OUT.relative_to(ROOT)}: {len(selected)} of {len(pool)} eligible")
