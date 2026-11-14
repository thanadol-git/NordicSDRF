"""Build accession-scoped SDRF inputs for the 18 PXD067831 timsTOF runs."""

import csv
import json
import re
import struct
from pathlib import Path


root = Path(__file__).resolve().parents[1]
work = root / "scratchpad/PXD067831"
entries = json.loads((work / "files.json").read_text())
assert all("PXD067831" in e.get("projectAccessions", []) for e in entries)
assert any(e["fileName"] == "raw.zip" for e in entries)

tail = (work / "raw_tail.bin").read_bytes()
zip_names = []
cursor = 0
while (index := tail.find(b"PK\x01\x02", cursor)) >= 0:
    if index + 46 > len(tail):
        break
    name_len, extra_len, comment_len = struct.unpack_from("<HHH", tail, index + 28)
    zip_names.append(tail[index + 46:index + 46 + name_len].decode("utf-8"))
    cursor = index + 46 + name_len + extra_len + comment_len
vendor_dirs = {name.removeprefix("raw/").removesuffix("/") for name in zip_names if re.fullmatch(r"raw/[^/]+\.d/", name)}
assert len(vendor_dirs) == 18

with (work / "experimental_design.txt").open(newline="") as handle:
    design = list(csv.DictReader(handle, delimiter="\t"))
assert len(design) == 18
assert {row["File Name"] + ".d" for row in design} == vendor_dirs

fields = [
    "source name", "files", "label", "technical replicate",
    "characteristics[organism]", "characteristics[organism part]",
    "characteristics[biological replicate]", "characteristics[disease]",
    "characteristics[age]", "characteristics[sex]", "characteristics[individual]",
    "characteristics[cell line]", "characteristics[cellosaurus accession]",
    "characteristics[cellosaurus name]", "factor value[stress state]",
    "factor value[FLAG bait]",
]
mapping = {"unt": "untreated", "no_rec": "15 min 1 mM H2O2", "60min": "60 min recovery after H2O2"}
samples = []
seen = set()
for row in design:
    group = row["Grouping"]
    state_code, bait = group.rsplit("_", 1)
    assert state_code in mapping and bait in ("control", "flag")
    replicate = sum(1 for sample in samples if sample["source name"] == group) + 1
    assert replicate <= 3
    seen.add((state_code, bait, replicate))
    samples.append({
        "source name": group,
        "files": row["File Name"] + ".d",
        "label": "label free sample",
        "technical replicate": 1,
        "characteristics[organism]": "Homo sapiens",
        "characteristics[organism part]": "not applicable",
        "characteristics[biological replicate]": replicate,
        "characteristics[disease]": "not applicable",
        "characteristics[age]": "not available",
        "characteristics[sex]": "not available",
        "characteristics[individual]": "not available",
        "characteristics[cell line]": "HEK293",
        "characteristics[cellosaurus accession]": "CVCL_0045",
        "characteristics[cellosaurus name]": "HEK293",
        "factor value[stress state]": mapping[state_code],
        "factor value[FLAG bait]": "RPB3-3xFLAG" if bait == "flag" else "control",
    })
assert len(seen) == 18
with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
    writer.writeheader()
    writer.writerows(samples)
(work / "vendor_files.json").write_text(json.dumps(sorted(vendor_dirs), indent=2) + "\n")

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=timsTOF Pro;AC=MS:1003005"),
    ("comment[cleavage agent details]", "NT=Trypsin/P;AC=MS:1001313"),
    ("comment[dissociation method]", "not available"),
    ("comment[precursor mass tolerance]", "10 ppm"),
    ("comment[fragment mass tolerance]", "40 ppm"),
    ("comment[modification parameters]", "|".join([
        "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed",
        "NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable",
        "NT=Acetyl;AC=UNIMOD:1;PP=Protein N-term;MT=Variable",
    ])),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t")
    writer.writerow(["column", "value"])
    writer.writerows(technical)
print("mapped 18/18 vendor .d directories")
