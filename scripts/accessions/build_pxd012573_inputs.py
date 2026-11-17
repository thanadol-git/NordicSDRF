"""Build source and run tables for the two PXD012573 TMT11 experiments."""

import csv
import json
from pathlib import Path


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD012573"
entries = json.loads((work / "files.json").read_text())
assert entries and all("PXD012573" in entry.get("projectAccessions", []) for entry in entries)
raw = sorted(e["fileName"] for e in entries if e["fileCategory"].get("value") == "RAW")
assert len(raw) == len(set(raw)) == 24
fgf = sorted(n for n in raw if "FGF4_MEKi_12fracs" in n)
analog = sorted(n for n in raw if "AnalogSENS_12fracs" in n)
assert len(fgf) == len(analog) == 12
(work / "raw-files.json").write_text(json.dumps(raw, indent=2) + "\n")
assert [n.rsplit("_", 1)[-1] for n in fgf] == [f"{i:02d}.raw" for i in range(1, 13)]
assert [n.rsplit("_", 1)[-1] for n in analog] == [f"{i:02d}.raw" for i in range(1, 13)]

channels = ["TMT126", "TMT127N", "TMT127C", "TMT128N", "TMT128C",
            "TMT129N", "TMT129C", "TMT130N", "TMT130C", "TMT131N", "TMT131C"]
fgf_design = [
    ("DMSO", "unstimulated", 1), ("DMSO", "unstimulated", 2), ("DMSO", "unstimulated", 3),
    ("DMSO", "FGF4", 1), ("DMSO", "FGF4", 2), ("DMSO", "FGF4", 3),
    ("PD0325901", "FGF4", 1), ("PD0325901", "FGF4", 2), ("PD0325901", "FGF4", 3),
    ("PD0325901", "unstimulated", 1), ("PD0325901", "unstimulated", 2),
]
analog_design = [
    ("DMSO", "non-induced", 1), ("DMSO", "non-induced", 2), ("DMSO", "non-induced", 3),
    ("DMSO", "4OHT-induced", 1), ("DMSO", "4OHT-induced", 2), ("DMSO", "4OHT-induced", 3),
    ("1-NM-PP1", "4OHT-induced", 1), ("1-NM-PP1", "4OHT-induced", 2), ("1-NM-PP1", "4OHT-induced", 3),
    ("PD0325901", "4OHT-induced", 1), ("PD0325901", "4OHT-induced", 2),
]
rows = []
for arm, files, design in (("FGF4/MEK", fgf, fgf_design), ("analog-sensitive ERK2", analog, analog_design)):
    for channel, (pretreatment, stimulus, replicate) in zip(channels, design, strict=True):
        rows.append({
            "source name": f"{arm.replace('/', '-').replace(' ', '-')}-{pretreatment}-{stimulus}-R{replicate}",
            "files": ",".join(files),
            "label": channel,
            "characteristics[organism]": "Mus musculus",
            "characteristics[organism part]": "not applicable",
            "characteristics[cell type]": "embryonic stem cell",
            "characteristics[biological replicate]": replicate,
            "characteristics[disease]": "not applicable",
            "characteristics[material type]": "cell line",
            "characteristics[developmental stage]": "not available",
            "characteristics[strain or breed]": "not available",
            "characteristics[sex]": "not available",
            "characteristics[experiment arm]": arm,
            "characteristics[pretreatment]": pretreatment,
            "characteristics[stimulation]": stimulus,
            "factor value[experiment arm]": arm,
            "factor value[pretreatment]": pretreatment,
            "factor value[stimulation]": stimulus,
        })
assert len(rows) == 22
with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=Q Exactive HF-X;AC=MS:1002877"),
    ("comment[cleavage agent details]", "NT=Lys-C;AC=MS:1001309"),
    ("comment[reduction reagent]", "NT=Tris(2-carboxyethyl)phosphine (TCEP);AC=PRIDE:0000609"),
    ("comment[alkylation reagent]", "NT=Chloroacetamide (ClAA);AC=PRIDE:0000600"),
    ("comment[precursor mass tolerance]", "not available"),
    ("comment[fragment mass tolerance]", "not available"),
    ("comment[modification parameters]", "not available"),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("column", "value"))
    writer.writerows(technical)
print(f"{len(rows)} sources; {len(raw)} RAW files; {len(rows) * 12} expected SDRF rows")
