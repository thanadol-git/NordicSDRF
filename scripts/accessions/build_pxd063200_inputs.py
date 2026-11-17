"""Build PXD063200 source and technical tables from deposited design and ZIP index."""

import csv
import json
import struct
from pathlib import Path


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD063200"
with (work / "experimental_design.txt").open(newline="") as handle:
    design = list(csv.DictReader(handle, delimiter="\t"))
assert len(design) == 12
assert {r["Grouping"] for r in design} == {"VMAT", "Control"}
assert sum(r["Grouping"] == "VMAT" for r in design) == 6

tail = (work / "raw-tail-128k.bin").read_bytes()
index = tail.find(b"PK\x01\x02")
names = []
while index >= 0 and tail[index:index + 4] == b"PK\x01\x02":
    header = struct.unpack_from("<IHHHHHHIIIHHHHHII", tail, index)
    name_len, extra_len, comment_len = header[10:13]
    names.append(tail[index + 46:index + 46 + name_len].decode("utf-8"))
    index += 46 + name_len + extra_len + comment_len
assert len(names) == 577
raw = sorted({name.removeprefix("raw/").removesuffix("/") for name in names
              if name.startswith("raw/") and name.endswith(".d/")})
assert len(raw) == 12
assert {r["MS file name"] + ".d" for r in design} == set(raw)
(work / "raw-files.json").write_text(json.dumps(raw, indent=2) + "\n")

rows = []
for entry in design:
    sample_id = entry["Analytical Sample ID"]
    group = entry["Grouping"]
    rows.append({
        "source name": sample_id,
        "files": entry["MS file name"] + ".d",
        "label": "label free sample",
        "characteristics[organism]": "Drosophila melanogaster",
        "characteristics[organism part]": "whole body",
        "characteristics[cell type]": "neuron",
        "characteristics[biological replicate]": 1,
        "characteristics[disease]": "not applicable",
        "characteristics[developmental stage]": "adult",
        "characteristics[strain or breed]": "not available",
        "characteristics[proximity-labeling construct]": "TurboID-VMAT" if group == "VMAT" else "free cytosolic TurboID",
        "characteristics[analytical sample ID]": sample_id,
        "factor value[proximity-labeling construct]": "TurboID-VMAT" if group == "VMAT" else "free cytosolic TurboID",
    })
with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=timsTOF Pro 2;AC=MS:1003230"),
    ("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251"),
    ("comment[precursor mass tolerance]", "10 ppm"),
    ("comment[fragment mass tolerance]", "40 ppm"),
    ("comment[reduction reagent]", "NT=Dithiothreitol (DTT);AC=PRIDE:0000608"),
    ("comment[alkylation reagent]", "NT=Chloroacetamide (ClAA);AC=PRIDE:0000600"),
    ("comment[modification parameters]", "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed|NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable|NT=Acetyl;AC=UNIMOD:1;PP=Protein N-term;MT=Variable"),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("column", "value"))
    writer.writerows(technical)
print("PXD063200: 12 acquisitions, 6 VMAT and 6 controls")
