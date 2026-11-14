"""Build PXD018721 inputs from its deposited filename key and PRIDE file list."""

import csv
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
work = root / "scratchpad/PXD018721"
items = json.loads((work / "files.json").read_text())
assert items and all("PXD018721" in item.get("projectAccessions", []) for item in items)
raw_names = sorted(item["fileName"] for item in items if item["fileName"].lower().endswith(".raw"))
assert len(raw_names) == 14 and len(set(raw_names)) == 14
key = (work / "Rawfilenamekey.txt").read_text()
for suffix in ("1686_01", "1686_02", "1687_01", "1687_02", "1688_01", "1688_02", "1689_01", "1689_02", "_1692", "_1693"):
    assert suffix in key
for suffix in ("Blnk_01", "Blnk_03", "Blnk_04", "Blnk_06"):
    assert suffix in key

fields = [
    "source name", "files", "label", "technical replicate",
    "characteristics[organism]", "characteristics[organism part]",
    "characteristics[biological replicate]", "characteristics[disease]",
    "characteristics[developmental stage]", "characteristics[strain or breed]",
    "characteristics[sex]", "characteristics[extraction method]",
    "factor value[extraction method]",
]
rows = []
for name in raw_names:
    if match := re.search(r"_Enamel_(HCl|TFA)_168[67]_(0[12])\.raw$", name):
        extraction, replicate = match.groups()
        replicate = int(replicate) + (2 if extraction == "TFA" else 0)
        source, organism, part, sex = "TNH2", "Homo", "tooth enamel", "not available"
    elif match := re.search(r"_E-blnk_(HCl|TFA)_168[89]_(0[12])\.raw$", name):
        extraction, replicate = match.groups()
        source, organism, part, sex = f"extraction_blank_{extraction}", "not applicable", "not applicable", "not applicable"
    elif match := re.search(r"_MS-blnk_(0[1346])\.raw$", name):
        replicate = "1"
        source, organism, part, sex = f"MS_blank_{match.group(1)}", "not applicable", "not applicable", "not applicable"
    elif match := re.search(r"_(169[23])\.raw$", name):
        extraction = "HCl" if match.group(1) == "1692" else "TFA"
        replicate = 1 if extraction == "HCl" else 2
        source, organism, part, sex = "medieval_reference_1952", "Homo sapiens", "tooth enamel", "male"
    else:
        raise AssertionError(name)
    blank = organism == "not applicable"
    rows.append({
        "source name": source,
        "files": name,
        "label": "label free sample",
        "technical replicate": int(replicate),
        "characteristics[organism]": organism,
        "characteristics[organism part]": part,
        "characteristics[biological replicate]": 1,
        "characteristics[disease]": "not applicable" if blank else "not available",
        "characteristics[developmental stage]": "not applicable" if blank else "not available",
        "characteristics[strain or breed]": "not applicable" if blank else "not available",
        "characteristics[sex]": sex,
        "characteristics[extraction method]": (
            "not applicable" if "MS_blank" in source else extraction
        ),
        "factor value[extraction method]": (
            "not applicable" if "MS_blank" in source else extraction
        ),
    })
assert len(rows) == 14
(work / "vendor_files.json").write_text(json.dumps(raw_names, indent=2) + "\n")
with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=Q Exactive HF-X;AC=MS:1002877"),
    ("comment[cleavage agent details]", "not applicable"),
    ("comment[dissociation method]", "NT=higher energy beam-type collision-induced dissociation;AC=MS:1000422"),
    ("comment[precursor mass tolerance]", "not available"),
    ("comment[fragment mass tolerance]", "not available"),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t")
    writer.writerow(["column", "value"])
    writer.writerows(technical)
print("mapped 4 TNH2, 2 medieval reference, 4 extraction blank, 4 MS blank RAW runs")
