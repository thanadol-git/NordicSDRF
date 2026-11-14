"""Build PXD044685 input tables from its deposited experimental design."""

import csv
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[1]
work = root / "scratchpad/PXD044685"
files = json.loads((work / "files.json").read_text())
assert files and all("PXD044685" in item.get("projectAccessions", []) for item in files)
raw_names = {item["fileName"] for item in files if item["fileName"].lower().endswith(".raw")}
assert len(raw_names) == 42
with (work / "experimental_design.txt").open(newline="") as handle:
    design = list(csv.DictReader(handle, delimiter="\t"))
assert len(design) == 42
assert {row["raw file name"] + ".raw" for row in design} == raw_names
counts = Counter(row["Biological Sample ID"] for row in design)
assert len(counts) == 21 and set(counts.values()) == {2}

fields = [
    "source name", "files", "label", "technical replicate",
    "characteristics[organism]", "characteristics[organism part]",
    "characteristics[biological replicate]", "characteristics[disease]",
    "characteristics[developmental stage]", "characteristics[strain or breed]",
    "characteristics[sex]", "characteristics[sample group]",
    "factor value[sample group]",
]
rows = []
for record in design:
    sample = record["Biological Sample ID"].strip()
    species = record["Spcies"].strip()
    if species.startswith("Ursus americanus"):
        organism = "Ursus americanus"
        group = sample[0]
        assert group in {"C", "H"}
        biological = int(sample[1])
    else:
        assert species.startswith("Ictidomys tridecemlineatus")
        organism = "Ictidomys tridecemlineatus"
        group = next(prefix for prefix in ("IBA", "Top", "TA") if sample.startswith(prefix))
        biological = int(sample[len(group)])
    rows.append({
        "source name": sample,
        "files": record["raw file name"].strip() + ".raw",
        "label": "label free sample",
        "technical replicate": 1,
        "characteristics[organism]": organism,
        "characteristics[organism part]": "skeletal muscle fiber",
        "characteristics[biological replicate]": biological,
        "characteristics[disease]": "not available",
        "characteristics[developmental stage]": "not available",
        "characteristics[strain or breed]": "not available",
        "characteristics[sex]": "not available",
        "characteristics[sample group]": group,
        "factor value[sample group]": group,
    })
assert len(rows) == 42
grouped = {}
for row in rows:
    source = row["source name"]
    if source not in grouped:
        grouped[source] = row.copy()
    else:
        assert all(row[key] == grouped[source][key] for key in fields if key != "files")
        grouped[source]["files"] += "," + row["files"]
assert len(grouped) == 21 and all(len(row["files"].split(",")) == 2 for row in grouped.values())
(work / "vendor_files.json").write_text(json.dumps(sorted(raw_names), indent=2) + "\n")
with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
    writer.writeheader()
    writer.writerows(grouped.values())

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=Orbitrap Ascend;AC=MS:1003356"),
    ("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251"),
    ("comment[modification parameters]", "NT=Phospho;AC=UNIMOD:21;TA=S,T,Y;MT=Variable|NT=Acetyl;AC=UNIMOD:1;TA=K;MT=Variable"),
    ("comment[dissociation method]", "NT=higher energy beam-type collision-induced dissociation;AC=MS:1000422"),
    ("comment[precursor mass tolerance]", "not available"),
    ("comment[fragment mass tolerance]", "not available"),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t")
    writer.writerow(["column", "value"])
    writer.writerows(technical)
print("mapped 42 RAW files to 21 biological sample IDs, with two gel-band fractions per ID")
