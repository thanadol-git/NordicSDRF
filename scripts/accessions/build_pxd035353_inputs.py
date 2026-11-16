"""Build accession-scoped SDRF inputs for PXD035353."""

import csv
import json
import re
from pathlib import Path


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD035353"
entries = json.loads((work / "files.json").read_text())
assert entries and all("PXD035353" in entry.get("projectAccessions", []) for entry in entries)
raw = [entry["fileName"] for entry in entries if entry["fileCategory"].get("value") == "RAW"]
assert len(raw) == len(set(raw)) == 16

groups = {"CTRL": {}, "48h": {}}
for name in raw:
    match = re.fullmatch(r"20190702_QE10_nLC0_FaCo_SA_AF13_library_(CTRL|48h)_F([1-8])(?:_20190704103024)?\.raw", name)
    assert match, name
    group, fraction = match.groups()
    fraction = int(fraction)
    assert fraction not in groups[group]
    groups[group][fraction] = name
assert all(set(fractions) == set(range(1, 9)) for fractions in groups.values())

fields = [
    "source name", "files", "label", "characteristics[organism]",
    "characteristics[organism part]", "characteristics[biological replicate]",
    "characteristics[disease]", "characteristics[material type]",
    "characteristics[age]", "characteristics[sex]", "characteristics[individual]",
    "characteristics[cell line]", "characteristics[cellosaurus accession]",
    "characteristics[cellosaurus name]", "characteristics[siRNA treatment]",
    "factor value[siRNA treatment]",
]
samples = []
for group, treatment in (("CTRL", "control siRNA"), ("48h", "TRESLIN siRNA, 48 h")):
    samples.append({
        "source name": f"HeLa-{group}",
        "files": ",".join(groups[group][number] for number in range(1, 9)),
        "label": "label free sample",
        "characteristics[organism]": "Homo sapiens",
        "characteristics[organism part]": "uterine cervix",
        "characteristics[biological replicate]": 1,
        "characteristics[disease]": "human papillomavirus-related cervical adenocarcinoma",
        "characteristics[material type]": "cell line",
        "characteristics[age]": "30Y6M",
        "characteristics[sex]": "female",
        "characteristics[individual]": "not applicable",
        "characteristics[cell line]": "HeLa",
        "characteristics[cellosaurus accession]": "CVCL_0030",
        "characteristics[cellosaurus name]": "HeLa",
        "characteristics[siRNA treatment]": treatment,
        "factor value[siRNA treatment]": treatment,
    })
with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(samples)

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=Q Exactive HF-X;AC=MS:1002877"),
    ("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251"),
    ("comment[precursor mass tolerance]", "not available"),
    ("comment[fragment mass tolerance]", "not available"),
    ("comment[modification parameters]", "|".join((
        "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed",
        "NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable",
        "NT=Acetyl;AC=UNIMOD:1;PP=Protein N-term;MT=Variable",
    ))),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("column", "value"))
    writer.writerows(technical)
(work / "raw-files.json").write_text(json.dumps(sorted(raw), indent=2) + "\n")
print("2 source rows, 8 fractions each, 16 RAW files")
