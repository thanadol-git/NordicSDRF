"""Build PXD067969 SDRF inputs from the deposited design and ZIP directory."""

import csv
import json
import struct
from collections import defaultdict
from pathlib import Path


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD067969"
with (work / "experimental_design.txt").open(newline="") as handle:
    design = list(csv.DictReader(handle, delimiter="\t"))
assert len(design) == 18

tail = (work / "raw-tail-128k.bin").read_bytes()
index = tail.find(b"PK\x01\x02")
names = []
while index >= 0 and tail[index:index + 4] == b"PK\x01\x02":
    header = struct.unpack_from("<IHHHHHHIIIHHHHHII", tail, index)
    name_len, extra_len, comment_len = header[10:13]
    names.append(tail[index + 46:index + 46 + name_len].decode("utf-8"))
    index += 46 + name_len + extra_len + comment_len
assert len(names) == 705
raw = sorted({name.split("/")[1] for name in names if name.startswith("raw/") and ".d/" in name})
assert len(raw) == 18
assert set(raw) == {row["File Name"] + ".d" for row in design}
(work / "raw-files.json").write_text(json.dumps(raw, indent=2) + "\n")

groups = defaultdict(int)
rows = []
for entry in design:
    group = entry["Grouping"]
    assert group in {"IP_untreated", "IP_no", "IP_60", "ctrl_untreated", "ctrl_no", "ctrl_60"}
    groups[group] += 1
    capture = "4H8 antibody" if group.startswith("IP_") else "unconjugated beads"
    condition = {"untreated": "untreated", "no": "H2O2, no recovery", "60": "H2O2, 60 min recovery"}[group.split("_", 1)[1]]
    rows.append({
        "source name": entry["Experiment"],
        "files": entry["File Name"] + ".d",
        "label": "label free sample",
        "characteristics[organism]": "Homo sapiens",
        "characteristics[organism part]": "cell culture",
        "characteristics[biological replicate]": groups[group],
        "characteristics[disease]": "normal",
        "characteristics[material type]": "cell line",
        "characteristics[age]": "not available",
        "characteristics[sex]": "female",
        "characteristics[individual]": "not applicable",
        "characteristics[cell line]": "Flp-In-T-REx-293",
        "characteristics[cellosaurus accession]": "CVCL_U427",
        "characteristics[cellosaurus name]": "Flp-In-T-REx-293",
        "characteristics[oxidative stress condition]": condition,
        "characteristics[affinity capture]": capture,
        "characteristics[deposited group]": group,
        "factor value[oxidative stress condition]": condition,
        "factor value[affinity capture]": capture,
    })
assert set(groups.values()) == {3}
with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=timsTOF Pro;AC=MS:1003005"),
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
print("PXD067969: 18 ZIP acquisitions and six deposited groups of three")
