"""Create SDRF build tables for the accession-scoped PXD058287 BLG experiment."""

import csv
import json
import re
from pathlib import Path


root = Path(__file__).resolve().parents[1]
work = root / "scratchpad/PXD058287"
items = json.loads((work / "files.json").read_text())
assert items and all("PXD058287" in item.get("projectAccessions", []) for item in items)
raw = sorted(item["fileName"] for item in items if item.get("fileCategory", {}).get("name") == "Associated raw file URI")
assert len(raw) == 63
(work / "raw_files.json").write_text(json.dumps(raw, indent=2) + "\n")

fields = ["source name", "files", "label", "technical replicate", "characteristics[organism]", "characteristics[organism part]", "characteristics[biological replicate]", "characteristics[disease]", "characteristics[sampling time]", "characteristics[developmental stage]", "characteristics[sex]", "factor value[additive]", "factor value[sampling time]"]
conditions = {"": "none", "S": "glucose", "L": "octanoic acid", "LS": "glucose and octanoic acid"}
with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
    writer.writeheader()
    observed = set()
    for name in raw:
        blank = re.search(r"_BLG_BLANK_([1-3])\.raw$", name)
        match = re.search(r"_BLG_(?:(S|L|LS)_)?T(0|3|6|9|12)_([1-3])\.raw$", name)
        if blank:
            source = "method blank"
            time = "not available"
            additive = "not applicable"
            rep = int(blank.group(1))
        elif match:
            code, hour, rep_text = match.groups()
            additive = conditions[code or ""]
            time = f"{hour} hour"
            rep = int(rep_text)
            source = f"BLG {additive} {hour}h"
            observed.add((code or "", int(hour), rep))
        else:
            raise SystemExit(f"unmapped RAW: {name}")
        writer.writerow({"source name": source, "files": name, "label": "label free sample", "technical replicate": rep, "characteristics[organism]": "not applicable" if blank else "Bos taurus", "characteristics[organism part]": "not applicable" if blank else "not available", "characteristics[biological replicate]": 1, "characteristics[disease]": "not applicable", "characteristics[sampling time]": time, "characteristics[developmental stage]": "not applicable", "characteristics[sex]": "not applicable", "factor value[additive]": additive, "factor value[sampling time]": time})
assert len(observed) == 60

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=Q Exactive HF;AC=MS:1002523"),
    ("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251"),
    ("comment[dissociation method]", "not available"),
    ("comment[precursor mass tolerance]", "7 ppm"),
    ("comment[fragment mass tolerance]", "20 ppm"),
    ("comment[modification parameters]", "|".join([
        "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed",
        "NT=Deamidated;AC=UNIMOD:7;TA=N,Q;MT=Variable",
        "NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable",
    ])),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t")
    writer.writerow(["column", "value"])
    writer.writerows(technical)
