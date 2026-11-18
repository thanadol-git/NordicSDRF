"""Prepare accession-scoped SDRF inputs from PXD053351's deposited design."""

import csv
import json
from collections import defaultdict
from pathlib import Path


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD053351"
with (work / "run-map.tsv").open(newline="") as handle:
    run_map = list(csv.DictReader(handle, delimiter="\t"))
assert len(run_map) == 12
assert {row["deposited_grouping"] for row in run_map} == {
    "6_CTRL", "6_dTAG", "6A_CTRL", "6A_dTAG"
}
assert len({row["raw_file"] for row in run_map}) == 12

counts = defaultdict(int)
rows = []
for entry in run_map:
    group = entry["deposited_grouping"]
    cohort, treatment_code = group.rsplit("_", 1)
    treatment = "DMSO" if treatment_code == "CTRL" else "dTAG"
    counts[group] += 1
    rows.append({
        "source name": entry["analytical_sample_id"],
        "files": entry["raw_file"],
        "label": "label free sample",
        "characteristics[organism]": "Homo sapiens",
        "characteristics[organism part]": "cell culture",
        "characteristics[biological replicate]": counts[group],
        "characteristics[disease]": "not available",
        "characteristics[material type]": "cell line",
        "characteristics[age]": "not available",
        "characteristics[sex]": "not available",
        "characteristics[individual]": "not applicable",
        "characteristics[cell line]": "Flp-In-T-REx-293",
        "characteristics[cellosaurus accession]": "CVCL_U427",
        "characteristics[cellosaurus name]": "Flp-In-T-REx-293",
        "characteristics[treatment]": treatment,
        "characteristics[deposited cohort code]": cohort,
        "factor value[treatment]": treatment,
    })
assert set(counts.values()) == {3}
with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
(work / "raw-files.json").write_text(json.dumps(sorted(row["raw_file"] for row in run_map), indent=2) + "\n")

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=timsTOF Pro;AC=MS:1003005"),
    ("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251"),
    ("comment[precursor mass tolerance]", "not available"),
    ("comment[fragment mass tolerance]", "not available"),
    ("comment[reduction reagent]", "NT=Dithiothreitol (DTT);AC=PRIDE:0000608"),
    ("comment[alkylation reagent]", "NT=Chloroacetamide (ClAA);AC=PRIDE:0000600"),
    ("comment[modification parameters]", "not available"),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("column", "value"))
    writer.writerows(technical)
print("PXD053351: 12 acquisitions in four deposited groups of three")
