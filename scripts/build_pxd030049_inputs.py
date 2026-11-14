"""Create builder inputs for the PXD030049 Caco-2 treatment experiment."""

import csv
import json
import re
from pathlib import Path


root = Path(__file__).resolve().parents[1]
work = root / "scratchpad/PXD030049"
items = json.loads((work / "files.json").read_text())
assert items and all("PXD030049" in item.get("projectAccessions", []) for item in items)
raw = sorted(item["fileName"] for item in items if item.get("fileCategory", {}).get("name") == "Associated raw file URI")
assert len(raw) == 15
(work / "raw_files.json").write_text(json.dumps(raw, indent=2) + "\n")

groups = {
    "Control": "DMSO vehicle control",
    "BaP": "50 uM benzo(a)pyrene for 24 h",
    "Eriodictyol_BaP": "20 uM eriodictyol and 50 uM benzo(a)pyrene for 24 h",
}
fields = [
    "source name", "files", "label", "technical replicate",
    "characteristics[organism]", "characteristics[organism part]",
    "characteristics[biological replicate]", "characteristics[disease]",
    "characteristics[age]", "characteristics[sex]", "characteristics[individual]",
    "characteristics[cell line]", "characteristics[cellosaurus accession]",
    "characteristics[cellosaurus name]", "factor value[treatment]",
]
samples = []
seen = set()
for name in raw:
    match = re.fullmatch(r"(Control|BaP|Eriodictyol_BaP)_([1-5])\.raw", name)
    assert match, name
    group, replicate = match.groups()
    seen.add((group, replicate))
    samples.append({
        "source name": name.removesuffix(".raw"),
        "files": name,
        "label": "label free sample",
        "technical replicate": 1,
        "characteristics[organism]": "Homo sapiens",
        "characteristics[organism part]": "colon",
        "characteristics[biological replicate]": 1,
        "characteristics[disease]": "colon adenocarcinoma",
        "characteristics[age]": "72Y",
        "characteristics[sex]": "male",
        "characteristics[individual]": "not available",
        "characteristics[cell line]": "Caco-2",
        "characteristics[cellosaurus accession]": "CVCL_0025",
        "characteristics[cellosaurus name]": "Caco-2",
        "factor value[treatment]": groups[group],
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
    ("comment[instrument]", "NT=Q Exactive HF;AC=MS:1002523"),
    ("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251"),
    ("comment[dissociation method]", "NT=beam-type collision-induced dissociation;AC=MS:1000422"),
    ("comment[precursor mass tolerance]", "6 ppm"),
    ("comment[fragment mass tolerance]", "20 ppm"),
    ("comment[reduction reagent]", "NT=Dithiothreitol (DTT);AC=PRIDE:0000608"),
    ("comment[alkylation reagent]", "NT=Iodoacetamide (IAA);AC=PRIDE:0000599"),
    ("comment[modification parameters]", "|".join([
        "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed",
        "NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable",
    ])),
    ("comment[ms1 scan range]", "300m/z-1800m/z"),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t")
    writer.writerow(["column", "value"])
    writer.writerows(technical)
print("mapped", len(samples), "RAW files")
