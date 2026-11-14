"""Create builder inputs for the six PXD056651 Bruker acquisitions."""

import csv
import json
import re
from pathlib import Path


root = Path(__file__).resolve().parents[1]
work = root / "scratchpad/PXD056651"
entries = json.loads((work / "files.json").read_text())
assert entries and all("PXD056651" in e.get("projectAccessions", []) for e in entries)
archives = sorted(
    e["fileName"] for e in entries
    if e.get("fileCategory", {}).get("name") == "Associated raw file URI"
)
assert len(archives) == 6 and all(a.endswith(".d.zip") for a in archives)

base_fields = [
    "source name", "files", "label", "technical replicate",
    "characteristics[organism]", "characteristics[organism part]",
    "characteristics[biological replicate]", "characteristics[disease]",
    "characteristics[age]", "characteristics[sex]",
    "characteristics[individual]",
    "factor value[subcellular fraction]",
]
samples = {"cyto": [], "ribo": []}
vendor_files = {"cyto": [], "ribo": []}
for archive in archives:
    match = re.fullmatch(r"(.+_(cyto|ribo)([123]))\.d\.zip", archive)
    assert match, archive
    stem, group, number = match.groups()
    vendor = stem + ".d"
    # The ZIP central directory was inspected with an HTTP range request for
    # each archive; in all six, the vendor directory equals this archive stem.
    tail = (work / f"{archive}.tail").read_bytes()
    assert vendor.encode() + b"/" in tail, archive
    vendor_files[group].append(vendor)
    sample = {
        "source name": f"{group}{number}",
        "files": vendor,
        "label": "label free sample",
        "technical replicate": 1,
        "characteristics[organism]": "Homo sapiens",
        "characteristics[organism part]": "not available",
        "characteristics[biological replicate]": 1,
        "characteristics[disease]": "not available",
        "characteristics[age]": "not available",
        "characteristics[sex]": "not available",
        "characteristics[individual]": "not available",
        "factor value[subcellular fraction]": "ribosome" if group == "ribo" else "cytosol",
    }
    if group == "ribo":
        sample.update({
            "characteristics[organism part]": "kidney",
            "characteristics[cell line]": "HEK293",
            "characteristics[cellosaurus accession]": "CVCL_0045",
            "characteristics[cellosaurus name]": "HEK293",
        })
    samples[group].append(sample)

for group in ("cyto", "ribo"):
    assert len(samples[group]) == 3 and len(vendor_files[group]) == 3
    (work / f"{group}_vendor_files.json").write_text(json.dumps(vendor_files[group], indent=2) + "\n")
    fields = base_fields[:]
    if group == "ribo":
        fields[-1:-1] = [
            "characteristics[cell line]", "characteristics[cellosaurus accession]",
            "characteristics[cellosaurus name]",
        ]
    with (work / f"{group}_samples.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(samples[group])

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=timsTOF Pro 2;AC=MS:1003230"),
    ("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251"),
    ("comment[dissociation method]", "not available"),
    ("comment[precursor mass tolerance]", "not available"),
    ("comment[fragment mass tolerance]", "not available"),
    ("comment[ms1 scan range]", "100m/z-1700m/z"),
    ("comment[ms2 scan range]", "100m/z-1700m/z"),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t")
    writer.writerow(["column", "value"])
    writer.writerows(technical)
print("mapped", sum(map(len, samples.values())), "vendor directories from", len(archives), "ZIPs")
