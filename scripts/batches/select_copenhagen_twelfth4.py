"""Select Copenhagen's twelfth cohort: the last untouched confirmed deposits (no local SDRF/BLOCKED/report).

Ranks by accession-scoped PRIDE RAW-file size. Expects scratchpad/<PXD>/files.json
from the paginated v2 projects/{PXD}/files endpoint.
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DENMARK = ROOT / "results/denmark"
OUT = DENMARK / "copenhagen_twelfth4_batch.tsv"
ANN = ROOT / "annotations"


def acc_from(name: str) -> str:
    return name.split(".")[0].split("-")[0]


def local_touched() -> set[str]:
    out = set()
    for path in ANN.glob("PXD*"):
        a = acc_from(path.name)
        if path.name.endswith((".sdrf.tsv", ".BLOCKED.md", ".report.md")) or ".report." in path.name:
            out.add(a)
    return out


def bigbio_corpus(repo: Path) -> set[str]:
    text = subprocess.check_output(
        ["git", "-C", str(repo), "ls-tree", "-r", "--name-only", "upstream/main"], text=True)
    return {m.group(1) for m in re.finditer(r"(?:datasets|sandbox)/(PXD\d{6})/", text)}


def main() -> None:
    touched = local_touched()
    corpus = bigbio_corpus(ROOT / "../sdrf-annotated-datasets")
    titles = {}
    confirmed = []
    with (DENMARK / "copenhagen_candidates.tsv").open(newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            if row["verdict"] == "confirmed":
                confirmed.append(row["accession"])
                titles[row["accession"]] = row.get("title", "")
    manifest = {ln.strip() for ln in (ROOT / "lists/denmark/copenhagen.txt").read_text().splitlines()
                if ln.strip().startswith("PXD")}
    eligible = []
    for accession in confirmed:
        if accession not in manifest or accession in touched or accession in corpus:
            continue
        path = ROOT / "scratchpad" / accession / "files.json"
        if not path.exists():
            raise SystemExit(f"missing scratchpad/{accession}/files.json")
        files = json.loads(path.read_text())
        raw = [i for i in files if (i.get("fileCategory") or {}).get("name") == "Associated raw file URI"]
        eligible.append((sum(int(i.get("fileSizeBytes") or 0) for i in raw), accession, len(raw), titles[accession]))
    selected = sorted(eligible)
    with OUT.open("w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["batch_order", "accession", "pride_raw_bytes", "pride_raw_count", "annotation_status", "title"])
        for order, (size, accession, count, title) in enumerate(selected, 1):
            w.writerow([order, accession, size, count, "queued: evidence review", title])
    print(f"wrote {OUT}: {len(selected)} PXDs")


if __name__ == "__main__":
    main()
