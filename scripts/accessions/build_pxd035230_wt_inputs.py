"""Build the paper-described WT phosphoproteomics arm of PXD035230."""

import csv
import json
import re
from collections import Counter
from pathlib import Path


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD035230"
entries = json.loads((work / "files.json").read_text())
assert entries and all("PXD035230" in entry.get("projectAccessions", []) for entry in entries)
raw = sorted(e["fileName"] for e in entries if e["fileCategory"].get("value") == "RAW")
assert len(raw) == len(set(raw)) == 36
pattern = re.compile(
    r"20191129_QE7_EVO4_AKP_EPIC_XS_Kollias_Greece_WT([1-3])"
    r"(?:_TNF(5|15|30))?(_GLK1h)?_Phos500ug_\d{2}\.raw"
)
wt = []
groups = Counter()
for name in raw:
    if "_WT" not in name:
        continue
    match = pattern.fullmatch(name)
    assert match, name
    rep, tnf, drug = match.groups()
    tnf_value = f"{tnf} min" if tnf else "0 min"
    drug_value = "GLK1h" if drug else "GLK absent"
    groups[(tnf_value, drug_value)] += 1
    wt.append({
        "source name": f"WT-SF-R{rep}-TNF{tnf or '0'}-{'GLK1h' if drug else 'GLK-absent'}",
        "files": name,
        "label": "label free sample",
        "characteristics[organism]": "Mus musculus",
        "characteristics[organism part]": "synovium",
        "characteristics[cell type]": "fibroblast",
        "characteristics[biological replicate]": int(rep),
        "characteristics[disease]": "normal",
        "characteristics[material type]": "cell",
        "characteristics[developmental stage]": "not available",
        "characteristics[strain or breed]": "not available",
        "characteristics[sex]": "not available",
        "characteristics[enrichment process]": "phosphopeptide enrichment",
        "characteristics[enrichment method]": "TiIMAC-HP beads",
        "characteristics[TNF stimulation]": tnf_value,
        "characteristics[GLK condition]": drug_value,
        "factor value[TNF stimulation]": tnf_value,
        "factor value[GLK condition]": drug_value,
    })
assert len(wt) == 24 and set(groups.values()) == {3} and len(groups) == 8
fields = list(wt[0])
with (work / "wt-samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(wt)
technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "Data-independent acquisition"),
    ("comment[instrument]", "NT=Orbitrap Exploris 480;AC=MS:1003028"),
    ("comment[cleavage agent details]", "NT=Lys-C;AC=MS:1001309"),
    ("comment[reduction reagent]", "NT=Tris(2-carboxyethyl)phosphine (TCEP);AC=PRIDE:0000609"),
    ("comment[alkylation reagent]", "NT=Chloroacetamide (ClAA);AC=PRIDE:0000600"),
    ("comment[precursor mass tolerance]", "not available"),
    ("comment[fragment mass tolerance]", "not available"),
    ("comment[modification parameters]", "NT=Phospho;AC=UNIMOD:21;TA=S,T,Y;MT=Variable"),
]
with (work / "wt-technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("column", "value"))
    writer.writerows(technical)
(work / "wt-raw-files.json").write_text(json.dumps(sorted(row["files"] for row in wt), indent=2) + "\n")
print("WT arm:", len(wt), "RAW files in", len(groups), "groups")
