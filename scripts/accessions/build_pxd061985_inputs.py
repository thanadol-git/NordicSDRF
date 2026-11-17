"""Build evidence-linked input tables for the PXD061985 TMTpro heart cohort."""

import csv
import json
import re
from pathlib import Path


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD061985"
entries = json.loads((work / "files.json").read_text())
assert entries and all("PXD061985" in item.get("projectAccessions", []) for item in entries)
raw = [item["fileName"] for item in entries if item["fileName"].lower().endswith(".raw")]
assert len(raw) == len(set(raw)) == 24
raw.sort(key=lambda name: int(re.search(r"Fr(\d+)\.raw$", name).group(1)))
assert [int(re.search(r"Fr(\d+)\.raw$", name).group(1)) for name in raw] == list(range(1, 25))
(work / "raw-files.json").write_text(json.dumps(raw, indent=2) + "\n")

channels = {}
for line in (work / "PPCM_annotation.txt").read_text().splitlines():
    channel, sample = line.split()
    assert channel not in channels
    channels[channel] = sample
assert len(channels) == 16
assert list(channels.values()).count("Empty") == 1
assert {value for value in channels.values() if value != "Empty"} == {
    *(f"Ctrl{i}" for i in range(1, 7)),
    *(f"PPCM{i}" for i in range(1, 6)),
    *(f"NI{i}" for i in range(1, 5)),
}

rows = []
for channel, sample in channels.items():
    if sample == "Empty":
        source = ""
        cohort = ""
        disease = ""
        replicate = ""
    else:
        source = sample
        cohort = "control" if sample.startswith("Ctrl") else "PPCM" if sample.startswith("PPCM") else "NPCM"
        disease = ("normal" if cohort == "control" else
                   "peripartum cardiomyopathy" if cohort == "PPCM" else "cardiomyopathy")
        replicate = int(re.search(r"\d+$", sample).group())
    rows.append({
        "source name": source,
        "files": ",".join(raw),
        "label": "TMT" + channel,
        "characteristics[organism]": "Homo sapiens" if source else "",
        "characteristics[organism part]": "heart" if source else "",
        "characteristics[biological replicate]": replicate,
        "characteristics[disease]": disease,
        "characteristics[material type]": "tissue" if source else "",
        "characteristics[age]": "not available" if source else "",
        "characteristics[sex]": "female" if source else "",
        "characteristics[individual]": source,
        "characteristics[cohort]": cohort,
        "factor value[cohort]": cohort,
    })

with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=Orbitrap Eclipse;AC=MS:1003029"),
    ("comment[cleavage agent details]", "NT=Lys-C;AC=MS:1001309"),
    ("comment[dissociation method]", "NT=HCD;AC=MS:1000422"),
    ("comment[collision energy]", "35% NCE"),
    ("comment[reduction reagent]", "NT=Tris(2-carboxyethyl)phosphine (TCEP);AC=PRIDE:0000609"),
    ("comment[alkylation reagent]", "NT=Chloroacetamide (ClAA);AC=PRIDE:0000600"),
    ("comment[precursor mass tolerance]", "20 ppm"),
    ("comment[fragment mass tolerance]", "20 ppm"),
    ("comment[modification parameters]",
     "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed|"
     "NT=TMTpro;AC=UNIMOD:2016;TA=K;MT=Fixed|"
     "NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable|"
     "NT=Acetyl;AC=UNIMOD:1;PP=Protein N-term;MT=Variable|"
     "NT=TMTpro;AC=UNIMOD:2016;PP=Any N-term;MT=Variable"),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("column", "value"))
    writer.writerows(technical)
print(f"{len(raw)} RAW fractions; {len(rows) - 1} samples; {(len(rows) - 1) * len(raw)} expected rows")
