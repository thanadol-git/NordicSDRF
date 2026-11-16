"""Build evidence-backed SDRF input tables for PXD043452."""

import csv
import json
import re
from collections import Counter
from pathlib import Path


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD043452"
accession = "PXD043452"
entries = json.loads((work / "files.json").read_text())
assert entries and all(accession in entry.get("projectAccessions", []) for entry in entries)
raw = sorted(entry["fileName"] for entry in entries if entry["fileCategory"].get("value") == "RAW")
assert len(raw) == len(set(raw)) == 20

fields = [
    "source name", "files", "label", "technical replicate",
    "characteristics[organism]", "characteristics[organism part]",
    "characteristics[biological replicate]", "characteristics[disease]",
    "characteristics[material type]", "characteristics[age]", "characteristics[sex]",
    "characteristics[individual]", "characteristics[cell line]",
    "characteristics[cellosaurus accession]", "characteristics[cellosaurus name]",
    "characteristics[PARP14 construct]", "characteristics[affinity capture]",
    "factor value[PARP14 construct]", "factor value[affinity capture]",
]
samples = []
groups = Counter()
for name in raw:
    match = re.fullmatch(
        r"20230613_EXPL7_LC4_JE_collab_ND-Ahel_P14_(WT|MD1)_(af1521|beads)_(0[1-5])\.raw",
        name,
    )
    assert match, name
    construct, capture, rep = match.groups()
    groups[(construct, capture)] += 1
    construct_value = "PARP14 wild type" if construct == "WT" else "PARP14 MD1 mutant"
    capture_value = "Af1521-linked beads" if capture == "af1521" else "empty control beads"
    samples.append({
        "source name": f"293T-PARP14-{construct}-{rep}",
        "files": name,
        "label": "label free sample",
        "technical replicate": int(rep),
        "characteristics[organism]": "Homo sapiens",
        "characteristics[organism part]": "kidney",
        "characteristics[biological replicate]": 1,
        "characteristics[disease]": "not applicable",
        "characteristics[material type]": "cell line",
        "characteristics[age]": "not available",
        "characteristics[sex]": "female",
        "characteristics[individual]": "not applicable",
        "characteristics[cell line]": "HEK293T",
        "characteristics[cellosaurus accession]": "CVCL_0063",
        "characteristics[cellosaurus name]": "HEK293T",
        "characteristics[PARP14 construct]": construct_value,
        "characteristics[affinity capture]": capture_value,
        "factor value[PARP14 construct]": construct_value,
        "factor value[affinity capture]": capture_value,
    })
assert groups == Counter({(construct, capture): 5 for construct in ("WT", "MD1") for capture in ("af1521", "beads")})

for capture in ("af1521", "beads"):
    subset = [sample for sample in samples if f"_{capture}_" in sample["files"]]
    assert len(subset) == 10
    with (work / f"{capture}-samples.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(subset)
    (work / f"{capture}-raw-files.json").write_text(json.dumps(sorted(sample["files"] for sample in subset), indent=2) + "\n")

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=Orbitrap Exploris 480;AC=MS:1003028"),
    ("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251"),
    ("comment[ms min charge]", "2"),
    ("comment[ms max charge]", "6"),
    ("comment[precursor mass tolerance]", "not available"),
    ("comment[fragment mass tolerance]", "not available"),
    ("comment[modification parameters]", "not available"),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("column", "value"))
    writer.writerows(technical)
print(f"{len(samples)} samples, {len(raw)} RAW files, {dict(groups)}")
