"""Select the next Singapore batch: the 20 remaining deposits with the fewest RAW files.

Pool: lists/singapore/singapore.txt minus BigBio corpus (singapore_in_corpus.txt) minus any
local annotation minus accessions already in bigbio sandbox/ (passed as a file of accessions).
RAW counts come from ProteomeCentral PROXI, cached in results/singapore/singapore_proxi_counts.tsv
(PRIDE API unreachable from the annotation session). Deposits with 0 or unknown RAW are excluded.
Ties break on total file count, then accession.

Usage: python scripts/batches/select_singapore_batch.py BATCH_TSV [bigbio_sandbox_accessions.txt] [N=20]
  e.g. ... results/singapore/singapore_batch2.tsv /tmp/bbsand.txt  (singapore-1 wrote singapore_first20_batch.tsv)
"""
import csv, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SG = ROOT / "results/singapore"

manifest = [l.strip() for l in (ROOT / "lists/singapore/singapore.txt").read_text().splitlines() if l.startswith("PXD")]
corpus = set((SG / "singapore_in_corpus.txt").read_text().split())
local = {p.name[:9] for p in (ROOT / "annotations").glob("PXD*")}
OUT = ROOT / sys.argv[1]
sandbox = set(Path(sys.argv[2]).read_text().split()) if len(sys.argv) > 2 else set()
counts = {r["accession"]: r for r in csv.DictReader((SG / "singapore_proxi_counts.tsv").open(), delimiter="\t")}

pool = []
for acc in dict.fromkeys(manifest):
    if acc in corpus or acc in local or acc in sandbox:
        continue
    r = counts.get(acc)
    if r is None:
        raise SystemExit(f"no PROXI count cached for {acc}")
    if not r["raw"].isdigit() or int(r["raw"]) == 0:
        continue
    total = int(r["total"]) if r["total"].isdigit() else 10**6
    pool.append((int(r["raw"]), total, acc, r["instrument"], r["title"]))

N = int(sys.argv[3]) if len(sys.argv) > 3 else 20
selected = sorted(pool)[:N]
with OUT.open("w", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["batch_order", "accession", "raw_count", "total_files", "instrument", "annotation_status", "title"])
    for i, (raw, total, acc, inst, title) in enumerate(selected, 1):
        w.writerow([i, acc, raw, total, inst, "queued", title])
print(f"wrote {OUT.relative_to(ROOT)}: {len(selected)} of {len(pool)} eligible")
