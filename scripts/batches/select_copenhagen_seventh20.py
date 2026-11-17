"""Select Copenhagen's seventh cohort: 20 smallest remaining RAW deposits."""

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DENMARK = ROOT / "results/denmark"
OUT = DENMARK / "copenhagen_seventh20_batch.tsv"
EXCLUDE_RAW_MISLABELS = {"PXD066727", "PXD066932"}


def table(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


previous = {
    row["accession"]
    for path in DENMARK.glob("copenhagen_*_batch.tsv")
    if path != OUT
    for row in table(path)
}
corpus = set((DENMARK / "copenhagen_in_corpus.txt").read_text().splitlines())
local = {path.name[:9] for path in (ROOT / "annotations").glob("PXD*")}
current = {row["accession"]: row["annotation_status"] for row in table(OUT)} if OUT.exists() else {}

eligible = []
for candidate in table(DENMARK / "copenhagen_candidates.tsv"):
    accession = candidate["accession"]
    if candidate["verdict"] != "confirmed" or candidate["in_corpus"].strip() == "yes":
        continue
    if accession in previous | corpus | EXCLUDE_RAW_MISLABELS or (accession in local and accession not in current):
        continue
    path = ROOT / "scratchpad" / accession / "files.json"
    if not path.exists():
        raise SystemExit(f"missing accession-scoped PRIDE file list: {accession}")
    files = json.loads(path.read_text())
    if not files or not all(accession in item.get("projectAccessions", []) for item in files):
        raise SystemExit(f"nonmatching PRIDE file list: {accession}")
    raw = [item for item in files if item.get("fileCategory", {}).get("name") == "Associated raw file URI"]
    if raw:
        eligible.append((sum(item["fileSizeBytes"] for item in raw), accession, len(raw), candidate["title"]))

selected = sorted(eligible)[:20]
if len(selected) != 20:
    raise SystemExit(f"expected 20 eligible accessions; found {len(selected)}")

with OUT.open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(["batch_order", "accession", "pride_raw_bytes", "pride_raw_count", "annotation_status", "title"])
    for order, (size, accession, count, title) in enumerate(selected, 1):
        writer.writerow([order, accession, size, count, current.get(accession, "queued: evidence review"), title])
print(f"wrote {OUT}: {len(selected)} PXDs")
