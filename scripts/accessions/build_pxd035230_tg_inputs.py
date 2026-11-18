"""Build the separately coded Tg phosphoproteomics arm of PXD035230."""

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
    r"20191130_QE7_EVO4_AKP_EPIC_XS_Kollias_Greece_Tg([1-3])"
    r"(?:_GLK(1|8|24)h)?_Phos500ug_\d{2}\.raw"
)
samples = []
groups = Counter()
for name in raw:
    if "_Tg" not in name:
        continue
    match = pattern.fullmatch(name)
    assert match, name
    rep, time = match.groups()
    code = f"GLK{time}h" if time else "GLK absent"
    groups[code] += 1
    samples.append({
        "source name": f"Tg-SF-R{rep}-{code.replace(' ', '-')}",
        "files": name,
        "label": "label free sample",
        "characteristics[organism]": "Mus musculus",
        "characteristics[organism part]": "synovium",
        "characteristics[cell type]": "fibroblast",
        "characteristics[biological replicate]": int(rep),
        "characteristics[disease]": "not available",
        "characteristics[material type]": "cell",
        "characteristics[developmental stage]": "not available",
        "characteristics[strain or breed]": "not available",
        "characteristics[sex]": "not available",
        "characteristics[genotype filename code]": "Tg",
        "characteristics[enrichment process]": "not available",
        "characteristics[enrichment method]": "TiIMAC-HP beads",
        "characteristics[GLK condition]": code,
        "factor value[GLK condition]": code,
    })
assert len(samples) == 12 and groups == Counter({k: 3 for k in ("GLK absent", "GLK1h", "GLK8h", "GLK24h")})
with (work / "tg-samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(samples[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(samples)
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
with (work / "tg-technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("column", "value"))
    writer.writerows(technical)
(work / "tg-raw-files.json").write_text(json.dumps(sorted(row["files"] for row in samples), indent=2) + "\n")
print("Tg arm:", len(samples), "RAW files in", len(groups), "coded groups")
