"""Build PXD040213 palaeoproteomics inputs from its deposited file map."""

import csv
import io
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
work = root / "scratchpad/PXD040213"
items = json.loads((work / "files.json").read_text())
assert items and all("PXD040213" in item.get("projectAccessions", []) for item in items)
raw_names = {item["fileName"] for item in items if item.get("fileCategory", {}).get("name") == "Associated raw file URI"}
assert len(raw_names) == 17
description_by_run_id = {}
with (work / "README-FileDescription.txt").open(encoding="utf-16", newline="") as handle:
    for row in csv.DictReader(io.StringIO(handle.read()), delimiter="\t"):
        name = row["File name"]
        if not name.endswith(".raw"):
            continue
        run_id = name.removesuffix(".raw").rsplit("_", 1)[-1]
        desc = row["Description"].strip()
        match = re.fullmatch(r"Raw file for Pongo sample (.+)", desc)
        if match:
            description_by_run_id[run_id] = (match.group(1), False)
        else:
            assert desc == "Blank control", (name, desc)
            description_by_run_id[run_id] = ("extraction_blank_" + run_id, True)
mapping = {name: description_by_run_id[name.removesuffix(".raw").rsplit("_", 1)[-1]] for name in raw_names}
assert len(description_by_run_id) == 17 and set(mapping) == raw_names
assert sum(blank for _, blank in mapping.values()) == 2
(work / "vendor_files.json").write_text(json.dumps(sorted(raw_names), indent=2) + "\n")

fields = [
    "source name", "files", "label", "technical replicate",
    "characteristics[organism]", "characteristics[organism part]",
    "characteristics[biological replicate]", "characteristics[disease]",
    "characteristics[developmental stage]", "characteristics[strain or breed]",
    "characteristics[sex]",
]
rows = []
for name in sorted(raw_names):
    source, blank = mapping[name]
    rows.append({
        "source name": source,
        "files": name,
        "label": "label free sample",
        "technical replicate": 1,
        "characteristics[organism]": "not applicable" if blank else "Pongo sp.",
        "characteristics[organism part]": "not applicable" if blank else "tooth enamel",
        "characteristics[biological replicate]": 1,
        "characteristics[disease]": "not applicable" if blank else "not available",
        "characteristics[developmental stage]": "not applicable" if blank else "not available",
        "characteristics[strain or breed]": "not applicable" if blank else "not available",
        "characteristics[sex]": "not applicable" if blank else "not available",
    })
with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=Orbitrap Exploris 480;AC=MS:1003028"),
    ("comment[cleavage agent details]", "not applicable"),
    ("comment[dissociation method]", "NT=higher energy beam-type collision-induced dissociation;AC=MS:1000422"),
    ("comment[precursor mass tolerance]", "4.5 ppm"),
    ("comment[fragment mass tolerance]", "20 ppm"),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t")
    writer.writerow(["column", "value"])
    writer.writerows(technical)
print("mapped 15 specimen runs and 2 extraction blank runs")
