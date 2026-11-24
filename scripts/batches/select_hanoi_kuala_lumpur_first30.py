"""Select the hanoi-kuala-lumpur-1 cohort: every confirmed Hanoi and Kuala Lumpur deposit that has
no local SDRF / BLOCKED / report file and is absent from BigBio datasets/ (sandbox/ hits are kept
but flagged, so the curator decides).

Usage: python scripts/batches/select_hanoi_kuala_lumpur_first30.py --bigbio-repo ../sdrf-annotated-datasets
"""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANN = ROOT / "annotations"
CITIES = [("vietnam", "hanoi"), ("malaysia", "kuala_lumpur")]


def local_touched() -> set[str]:
    out = set()
    for path in ANN.glob("PXD*"):
        if path.name.endswith((".sdrf.tsv", ".BLOCKED.md", ".report.md")):
            out.add(path.name.split(".")[0].split("-")[0])
    return out


def bigbio(repo: Path) -> dict[str, str]:
    text = subprocess.check_output(["git", "-C", str(repo), "ls-tree", "-r", "--name-only", "HEAD"], text=True)
    hits: dict[str, str] = {}
    for m in re.finditer(r"^(datasets|sandbox)/(PXD\d{6})/", text, re.M):
        hits.setdefault(m.group(2), m.group(1))
        if m.group(1) == "datasets":
            hits[m.group(2)] = "datasets"
    return hits


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bigbio-repo", type=Path, default=ROOT / "../sdrf-annotated-datasets")
    args = ap.parse_args()
    touched = local_touched()
    corpus = bigbio(args.bigbio_repo)
    for country, city in CITIES:
        manifest = [ln.strip() for ln in (ROOT / f"lists/{country}/{city}.txt").read_text().splitlines()
                    if ln.strip().startswith("PXD")]
        titles = {r["accession"]: r["title"] for r in csv.DictReader(
            (ROOT / f"results/{country}/{city}_candidates.tsv").open(newline=""), delimiter="\t")}
        local_corpus = set((ROOT / f"results/{country}/{city}_in_corpus.txt").read_text().split())
        rows = []
        for acc in manifest:
            if acc in touched or acc in local_corpus or corpus.get(acc) == "datasets":
                continue
            rows.append([acc, corpus.get(acc, ""), titles.get(acc, "")])
        n = len(rows)
        out = ROOT / f"results/{country}/{city}_first{n}_batch.tsv"
        with out.open("w", newline="") as fh:
            w = csv.writer(fh, delimiter="\t", lineterminator="\n")
            w.writerow(["batch_order", "accession", "bigbio_hit", "annotation_status", "title"])
            for i, (acc, hit, title) in enumerate(rows, 1):
                w.writerow([i, acc, hit, "queued: evidence review", title])
        print(f"wrote {out.relative_to(ROOT)}: {n} PXDs")


if __name__ == "__main__":
    main()
