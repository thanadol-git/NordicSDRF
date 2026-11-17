"""Build PXD076695 tables from the deposited design and accession RAW list."""

import csv
import json
from collections import defaultdict
from pathlib import Path


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD076695"
files = json.loads((work / "files.json").read_text())
assert all("PXD076695" in entry["projectAccessions"] for entry in files)
raw = {entry["fileName"] for entry in files if entry["fileName"].lower().endswith(".raw")}
assert len(raw) == 60
with (work / "experimental_design.txt").open(newline="") as handle:
    design = list(csv.DictReader(handle, delimiter="\t"))
assert len(design) == 61
extra = {entry["Raw file"] + ".raw" for entry in design} - raw
assert extra == {"20240506_ASC1_NEO1_PRI_DDA_uPAC50cm_60min_X1687_P0190_R1206_GelB_S01_3uL.raw"}
assert raw <= {entry["Raw file"] + ".raw" for entry in design}
(work / "raw-files.json").write_text(json.dumps(sorted(raw), indent=2) + "\n")

groups = defaultdict(int)
rows = []
for entry in design:
    filename = entry["Raw file"] + ".raw"
    if filename not in raw:
        continue
    group = entry["Grouping"]
    assert group in {"DCM", "ICM", "CONTROL"}
    groups[group] += 1
    disease = {"DCM": "dilated cardiomyopathy", "ICM": "ischemic cardiomyopathy", "CONTROL": "normal"}[group]
    rows.append({
        "source name": entry["Sample ID"],
        "files": filename,
        "label": "label free sample",
        "characteristics[organism]": "Homo sapiens",
        "characteristics[organism part]": "heart",
        "characteristics[biological replicate]": groups[group],
        "characteristics[disease]": disease,
        "characteristics[material type]": "tissue",
        "characteristics[age]": "not available",
        "characteristics[sex]": "not available",
        "characteristics[cardiac sampling site]": "interventricular septum",
        "characteristics[deposited sample ID]": entry["Sample ID"],
        "factor value[disease]": disease,
    })
assert dict(groups) == {"DCM": 19, "ICM": 24, "CONTROL": 17}
with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=Orbitrap Exploris 480;AC=MS:1003028"),
    ("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251"),
    ("comment[collision energy]", "30% NCE"),
    ("comment[precursor mass tolerance]", "4.5 ppm"),
    ("comment[fragment mass tolerance]", "20 ppm"),
    ("comment[reduction reagent]", "NT=Tris(2-carboxyethyl)phosphine (TCEP);AC=PRIDE:0000609"),
    ("comment[alkylation reagent]", "NT=Chloroacetamide (ClAA);AC=PRIDE:0000600"),
    ("comment[modification parameters]", "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed|NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable|NT=Acetyl;AC=UNIMOD:1;PP=Protein N-term;MT=Variable|NT=Acetyl;AC=UNIMOD:1;TA=K;MT=Variable|NT=Phospho;AC=UNIMOD:21;TA=S,T,Y;MT=Variable"),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("column", "value"))
    writer.writerows(technical)
print("PXD076695:", len(rows), "RAW rows,", dict(groups), "; extra design row absent from RAW list:", extra)
