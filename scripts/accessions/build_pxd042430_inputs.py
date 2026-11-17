"""Build PXD042430 modern-grouper LC-MS/MS inputs from Table S2."""

import csv
import json
import re
from collections import Counter
from pathlib import Path


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD042430"
record = json.loads((work / "pride.json").read_text())
assert record["accession"] == "PXD042430"
files = json.loads((work / "files.json").read_text())
assert all("PXD042430" in entry["projectAccessions"] for entry in files)
raw = sorted(entry["fileName"] for entry in files if entry["fileName"].endswith(".raw"))
assert len(raw) == 14
(work / "raw-files.json").write_text(json.dumps(raw, indent=2) + "\n")

# Thirteen sample IDs and identifications are in supplementary Table S2.
# CAN-2 is identified by its accession RAW name and the deposited CAN2 search
# archive, whose FASTA path explicitly names the Caninus species library.
species = {
    "1082": ("WLAp 1082", "Epinephelus aeneus"),
    "AEN1": ("AEN-1", "Epinephelus aeneus"),
    "AEN3": ("AEN-3", "Epinephelus aeneus"),
    "CAN1": ("CAN-1", "Epinephelus caninus"),
    "CAN2": ("CAN-2", "Epinephelus caninus"),
    "765": ("id765", "Epinephelus caninus"),
    "1003": ("id1003", "Epinephelus costae"),
    "ALE1": ("ALE-1", "Epinephelus costae"),
    "ALE4": ("ALE-4", "Epinephelus costae"),
    "711": ("id711", "Epinephelus marginatus"),
    "449": ("id449", "Epinephelus marginatus"),
    "GUA4": ("GUA-4", "Epinephelus marginatus"),
    "GUA7": ("GUA-7", "Epinephelus marginatus"),
    "GUA8": ("GUA-8", "Epinephelus marginatus"),
}

rows = []
replicate = Counter()
for filename in raw:
    matches = [code for code in species if re.search(rf"(?:_|-){code}(?:-|_|\.)", filename)]
    assert len(matches) == 1, (filename, matches)
    source, taxon = species[matches[0]]
    replicate[taxon] += 1
    rows.append({
        "source name": source,
        "files": filename,
        "label": "label free sample",
        "characteristics[organism]": taxon,
        "characteristics[organism part]": "bone",
        "characteristics[biological replicate]": replicate[taxon],
        "characteristics[pooled sample]": "not pooled",
        "characteristics[disease]": "not applicable",
        "characteristics[material type]": "tissue",
        "characteristics[developmental stage]": "not available",
        "characteristics[sex]": "not available",
        "factor value[organism]": taxon,
    })
assert set(species) == {code for filename in raw for code in species if re.search(rf"(?:_|-){code}(?:-|_|\.)", filename)}
assert replicate == {"Epinephelus marginatus": 5, "Epinephelus caninus": 3, "Epinephelus costae": 3, "Epinephelus aeneus": 3}

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
    ("comment[dissociation method]", "NT=beam-type collision-induced dissociation;AC=MS:1000422"),
    ("comment[collision energy]", "30% NCE"),
    ("comment[precursor mass tolerance]", "10 ppm"),
    ("comment[fragment mass tolerance]", "0.05 Da"),
    ("comment[modification parameters]", "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed|NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable|NT=Oxidation;AC=UNIMOD:35;TA=P;MT=Variable|NT=Acetyl;AC=UNIMOD:1;PP=Protein N-term;MT=Variable|NT=Deamidated;AC=UNIMOD:7;TA=N,Q;MT=Variable|NT=Gln->pyro-Glu;AC=UNIMOD:28;TA=Q;PP=Peptide N-term;MT=Variable|NT=Glu->pyro-Glu;AC=UNIMOD:27;TA=E;PP=Peptide N-term;MT=Variable"),
    ("comment[ms1 scan range]", "350m/z-1400m/z"),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("column", "value"))
    writer.writerows(technical)
print("PXD042430: 14 specimens and 14 distinct RAW files; species counts 5/3/3/3")
