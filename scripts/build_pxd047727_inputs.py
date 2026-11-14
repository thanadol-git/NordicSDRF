"""Create PXD047727 plant IP-MS builder inputs from accession-scoped RAW names."""

import csv
import json
import re
import struct
from pathlib import Path


root = Path(__file__).resolve().parents[1]
work = root / "scratchpad/PXD047727"
items = json.loads((work / "files.json").read_text())
assert items and all("PXD047727" in x.get("projectAccessions", []) for x in items)
archives = sorted(x["fileName"] for x in items if x.get("fileCategory", {}).get("name") == "Associated raw file URI")
assert len(archives) == 15 and all(x.endswith(".d.zip") for x in archives)
vendor_dirs = {}
for archive in archives:
    tail = work / f"{archive}.tail.bin"
    if archive == "NKS1_RFP_Rep1.d.zip":
        tail = work / "nks1_raw_tail.bin"
    data = tail.read_bytes()
    pos = 0
    names = []
    while (index := data.find(b"PK\x01\x02", pos)) >= 0:
        if index + 46 > len(data):
            break
        name_length, extra_length, comment_length = struct.unpack_from("<HHH", data, index + 28)
        names.append(data[index + 46:index + 46 + name_length].decode())
        pos = index + 46 + name_length + extra_length + comment_length
    roots = {name.split("/")[0] for name in names if name.split("/")[0].endswith(".d")}
    assert len(roots) == 1, (archive, roots)
    vendor_dirs[archive] = roots.pop()
(work / "vendor_files.json").write_text(json.dumps(list(vendor_dirs.values()), indent=2) + "\n")

groups = {
    "NKS1_RFP": ("NKS1-mRFP", "RFP-Trap"),
    "ST_RFP": ("ST-mRFP Golgi-marker control", "RFP-Trap"),
    "Col0_RFPTrap": ("untagged Col-0 control", "RFP-Trap"),
    "QUA1_GFP": ("QUA1-GFP", "GFP-Trap"),
    "Col_0_GFPTrap": ("untagged Col-0 control", "GFP-Trap"),
}
fields = [
    "source name", "files", "label", "technical replicate",
    "characteristics[organism]", "characteristics[organism part]",
    "characteristics[biological replicate]", "characteristics[disease]",
    "characteristics[developmental stage]", "characteristics[strain or breed]",
    "factor value[bait]", "factor value[affinity reagent]",
]
seen = set()
samples = []
for archive in archives:
    match = re.fullmatch(r"(.+)_Rep([1-3])\.d\.zip", archive)
    assert match, archive
    group, replicate = match.groups()
    assert group in groups, group
    seen.add((group, replicate))
    bait, reagent = groups[group]
    samples.append({
        "source name": f"{group}_plant{replicate}",
        "files": vendor_dirs[archive],
        "label": "label free sample",
        "technical replicate": 1,
        "characteristics[organism]": "Arabidopsis thaliana",
        "characteristics[organism part]": "leaf",
        "characteristics[biological replicate]": replicate,
        "characteristics[disease]": "not applicable",
        "characteristics[developmental stage]": "not available",
        "characteristics[strain or breed]": "Col-0",
        "factor value[bait]": bait,
        "factor value[affinity reagent]": reagent,
    })
assert len(seen) == 15
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
print("mapped 15/15 RAW archives to vendor .d names")
