"""Build accession-scoped SDRF input tables for PXD036512."""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD036512"
entries = json.loads((work / "files.json").read_text())
assert entries and all("PXD036512" in entry.get("projectAccessions", []) for entry in entries)
raw = [entry["fileName"] for entry in entries if entry["fileCategory"].get("value") == "RAW"]
assert len(raw) == len(set(raw)) == 64

groups = defaultdict(dict)
for name in raw:
    match = re.fullmatch(
        r"20201110_LUMOS1_LC4_SCL_SA_collab_S2R_(DMSO|PARGi)(_H2O2)?_R([1-4])_F([0-3])\.raw",
        name,
    )
    assert match, name
    inhibitor, peroxide, replicate, fraction = match.groups()
    key = inhibitor, bool(peroxide), int(replicate)
    assert int(fraction) not in groups[key]
    groups[key][int(fraction)] = name
assert len(groups) == 16 and all(set(fractions) == {0, 1, 2, 3} for fractions in groups.values())

fields = [
    "source name", "files", "label", "characteristics[organism]",
    "characteristics[organism part]", "characteristics[biological replicate]",
    "characteristics[disease]", "characteristics[material type]",
    "characteristics[developmental stage]", "characteristics[strain or breed]",
    "characteristics[cell line]", "characteristics[cellosaurus accession]",
    "characteristics[cellosaurus name]", "characteristics[enrichment process]",
    "characteristics[enrichment method]", "characteristics[PARG inhibitor]",
    "characteristics[oxidative stress]", "factor value[PARG inhibitor]",
    "factor value[oxidative stress]",
]
samples = []
for inhibitor, peroxide, replicate in sorted(groups):
    inhibitor_value = "PDD00017273" if inhibitor == "PARGi" else "DMSO vehicle"
    stress_value = "hydrogen peroxide" if peroxide else "untreated"
    samples.append({
        "source name": f"S2R-{inhibitor}-{'H2O2' if peroxide else 'control'}-R{replicate}",
        "files": ",".join(groups[(inhibitor, peroxide, replicate)][fraction] for fraction in range(4)),
        "label": "label free sample",
        "characteristics[organism]": "Drosophila melanogaster",
        "characteristics[organism part]": "embryo",
        "characteristics[biological replicate]": replicate,
        "characteristics[disease]": "normal",
        "characteristics[material type]": "cell line",
        "characteristics[developmental stage]": "not available",
        "characteristics[strain or breed]": "Oregon-R",
        "characteristics[cell line]": "S2R+",
        "characteristics[cellosaurus accession]": "CVCL_Z831",
        "characteristics[cellosaurus name]": "S2R+",
        "characteristics[enrichment process]": "enrichment of ADP-ribosylated peptides",
        "characteristics[enrichment method]": "Af1521 macrodomain affinity enrichment",
        "characteristics[PARG inhibitor]": inhibitor_value,
        "characteristics[oxidative stress]": stress_value,
        "factor value[PARG inhibitor]": inhibitor_value,
        "factor value[oxidative stress]": stress_value,
    })
with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(samples)

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=Orbitrap Fusion Lumos;AC=MS:1002732"),
    ("comment[cleavage agent details]", "NT=Lys-C;AC=MS:1001309"),
    ("comment[dissociation method]", "NT=electron-transfer/higher-energy collision dissociation;AC=MS:1002631"),
    ("comment[precursor mass tolerance]", "not available"),
    ("comment[fragment mass tolerance]", "not available"),
    ("comment[modification parameters]", "|".join((
        "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Variable",
        "NT=ADP-Ribosyl;AC=UNIMOD:213;TA=C,D,E,H,K,R,S,T,Y;MT=Variable",
    ))),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("column", "value"))
    writer.writerows(technical)
(work / "raw-files.json").write_text(json.dumps(sorted(raw), indent=2) + "\n")
print("16 cultures x 4 fractions = 64 RAW files")
