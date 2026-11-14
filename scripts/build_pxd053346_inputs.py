"""Build PXD053346 inputs from the deposited design and RAW ZIP directory."""

import csv
import json
import struct
from pathlib import Path

root = Path(__file__).resolve().parents[1]
work = root / "scratchpad/PXD053346"
data = (work / "raw_tail.bin").read_bytes()
pos = 0
members = []
while (index := data.find(b"PK\x01\x02", pos)) >= 0:
    if index + 46 > len(data):
        break
    n, e, c = struct.unpack_from("<HHH", data, index + 28)
    members.append(data[index + 46:index + 46 + n].decode())
    pos = index + 46 + n + e + c
runs = {part.split("/")[1] for part in members if part.startswith("raw/") and len(part.split("/")) > 1 and part.split("/")[1].endswith(".d")}
assert len(runs) == 12, runs
(work / "vendor_files.json").write_text(json.dumps(sorted(runs), indent=2) + "\n")

fields = [
    "source name", "files", "label", "technical replicate",
    "characteristics[organism]", "characteristics[organism part]",
    "characteristics[biological replicate]", "characteristics[disease]",
    "characteristics[cell line]", "characteristics[cellosaurus accession]",
    "characteristics[cellosaurus name]", "characteristics[age]",
    "characteristics[sex]", "factor value[INTS6 status]", "factor value[treatment]",
]
with (work / "experimental_design.txt").open(newline="") as handle:
    design = list(csv.DictReader(handle, delimiter="\t"))
assert len(design) == 12
seen = {}
samples = []
for item in design:
    group = item["Grouping"].strip()
    genotype, treatment = group.split("_", 1)
    run = item["Raw file"] + ".d"
    assert run in runs, run
    seen[group] = seen.get(group, 0) + 1
    samples.append({
        "source name": item["Experiment"],
        "files": run,
        "label": "label free sample",
        "technical replicate": 1,
        "characteristics[organism]": "Homo sapiens",
        "characteristics[organism part]": "kidney",
        "characteristics[biological replicate]": seen[group],
        "characteristics[disease]": "normal",
        "characteristics[cell line]": "HEK293",
        "characteristics[cellosaurus accession]": "CVCL_U427",
        "characteristics[cellosaurus name]": "Flp-In-T-REx-293",
        "characteristics[age]": "not available",
        "characteristics[sex]": "female",
        "factor value[INTS6 status]": genotype,
        "factor value[treatment]": treatment,
    })
assert set(seen.values()) == {3} and len(seen) == 4
with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
    writer.writeheader()
    writer.writerows(samples)

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=timsTOF Pro;AC=MS:1003005"),
    ("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251"),
    ("comment[dissociation method]", "not available"),
    ("comment[reduction reagent]", "NT=Dithiothreitol (DTT);AC=PRIDE:0000608"),
    ("comment[alkylation reagent]", "NT=Chloroacetamide (ClAA);AC=PRIDE:0000600"),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t")
    writer.writerow(["column", "value"])
    writer.writerows(technical)
print("mapped 12/12 vendor RAW directories")
