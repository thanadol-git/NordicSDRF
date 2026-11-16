"""Recreate the two sample tables for PXD026225 from accession-scoped PRIDE files."""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PXD = "PXD026225"
WORK = ROOT / "scratchpad" / PXD
files = json.loads((WORK / "files.json").read_text())
assert files and all(PXD in item.get("projectAccessions", []) for item in files)
raw = sorted(item["fileName"] for item in files if item["fileCategory"]["name"] == "Associated raw file URI")
assert len(raw) == 26 and len(set(raw)) == 26

human = [name for name in raw if "_mouse_" not in name]
mouse = [name for name in raw if "_mouse_" in name]
assert len(human) == 16 and len(mouse) == 10


def write_tsv(path, columns, rows):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


common = {
    "characteristics[organism part]": "skeletal muscle",
    "characteristics[material type]": "tissue",
    "characteristics[developmental stage]": "adult",
    "label": "label free sample",
}

human_rows = []
groups = defaultdict(list)
for name in human:
    if "_IgG_CTR_" in name:
        match = re.search(r"_IgG_CTR_(BASAL|INS)_?(\d+)\.raw$", name)
        antibody = "IgG control"
    else:
        match = re.search(r"_(BASAL|INS)_(\d+)\.raw$", name)
        antibody = "TBC1D4"
    assert match, name
    condition, code = match.groups()
    groups[(condition, antibody)].append((code, name))
assert {key: len(value) for key, value in groups.items()} == {
    ("BASAL", "TBC1D4"): 6, ("INS", "TBC1D4"): 6,
    ("BASAL", "IgG control"): 2, ("INS", "IgG control"): 2,
}
for (condition, antibody), members in sorted(groups.items()):
    for biological_replicate, (code, name) in enumerate(sorted(members, key=lambda x: int(x[0])), 1):
        human_rows.append({
            "source name": f"human-{condition.lower()}-{antibody.lower().replace(' ', '-')}-{code}",
            "files": name,
            **common,
            "characteristics[organism]": "Homo sapiens",
            "characteristics[biological replicate]": biological_replicate,
            "characteristics[disease]": "normal",
            "characteristics[sex]": "male",
            "factor value[insulin stimulation]": "basal" if condition == "BASAL" else "insulin-stimulated",
            "factor value[immunoprecipitation]": antibody,
        })

mouse_rows = []
mouse_groups = defaultdict(list)
for name in mouse:
    match = re.search(r"_mouse_(WT|D4KO)_S(\d+)\.raw$", name)
    assert match, name
    genotype, sample_number = match.groups()
    mouse_groups[genotype].append((int(sample_number), name))
assert {key: len(value) for key, value in mouse_groups.items()} == {"WT": 5, "D4KO": 5}
for genotype, members in sorted(mouse_groups.items()):
    for biological_replicate, (sample_number, name) in enumerate(sorted(members), 1):
        mouse_rows.append({
            "source name": f"mouse-{genotype}-S{sample_number}",
            "files": name,
            **common,
            "characteristics[organism]": "Mus musculus",
            "characteristics[biological replicate]": biological_replicate,
            "characteristics[disease]": "not applicable",
            "characteristics[strain or breed]": "C57BL/6J",
            "characteristics[sex]": "female",
            "characteristics[genotype]": "wild type" if genotype == "WT" else "TBC1D4 knockout",
            "factor value[genotype]": "wild type" if genotype == "WT" else "TBC1D4 knockout",
        })

technical = [
    {"column": "comment[sdrf version]", "value": "v1.1.0"},
    {"column": "comment[sdrf annotation tool]", "value": "manual curation"},
    {"column": "comment[proteomics data acquisition method]", "value": "NT=Data-dependent acquisition;AC=PRIDE:0000627"},
    {"column": "comment[instrument]", "value": "NT=Q Exactive HF-X;AC=MS:1002877"},
    {"column": "comment[cleavage agent details]", "value": "NT=Trypsin;AC=MS:1001251"},
    {"column": "comment[precursor mass tolerance]", "value": "not available"},
    {"column": "comment[fragment mass tolerance]", "value": "not available"},
    {"column": "comment[modification parameters]", "value": "not available"},
]

for arm, names, rows in (("human", human, human_rows), ("mouse", mouse, mouse_rows)):
    (WORK / f"{arm}-raw-files.json").write_text(json.dumps(names, indent=2) + "\n")
    columns = ["source name", "files", "label", "characteristics[organism]", "characteristics[organism part]",
               "characteristics[biological replicate]", "characteristics[disease]", "characteristics[material type]",
               "characteristics[developmental stage]", "characteristics[strain or breed]", "characteristics[sex]",
               "characteristics[genotype]"]
    columns += [key for key in rows[0] if key.startswith("factor value[")]
    write_tsv(WORK / f"{arm}-samples.tsv", columns, rows)
    write_tsv(WORK / f"{arm}-technical.tsv", ["column", "value"], technical)
    print(f"{arm}: {len(rows)} samples, {len(names)} RAW files")
