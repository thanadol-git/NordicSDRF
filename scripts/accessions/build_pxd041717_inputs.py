"""Build PXD041717 DNMT1 immunoprecipitation SDRF inputs."""

import csv
import json
from pathlib import Path


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD041717"
record = json.loads((work / "pride.json").read_text())
assert record["accession"] == "PXD041717"
entries = json.loads((work / "files.json").read_text())
assert entries and all("PXD041717" in x["projectAccessions"] for x in entries)
raw = {x["fileName"] for x in entries if x["fileName"].lower().endswith(".raw")}
assert len(raw) == 20

conditions = [
    ("siC", False, "non-targeting control"),
    ("siC", True, "non-targeting control"),
    ("siR", True, "RNF4"),
    ("siT", True, "TOPORS"),
    ("siD", True, "DNMT1"),
]
rows = []
for code, aza, target in conditions:
    for replicate in range(1, 5):
        suffix = f"_{code}{'_AZA' if aza else ''}_{replicate:02d}.raw"
        hits = [name for name in raw if name.endswith(suffix)]
        assert len(hits) == 1, suffix
        rows.append({
            "source name": f"{code}{'-AZA' if aza else ''}-{replicate:02d}",
            "files": hits[0],
            "label": "label free sample",
            "characteristics[organism]": "Homo sapiens",
            "characteristics[organism part]": "tibia",
            "characteristics[cell line]": "U2OS",
            "characteristics[cellosaurus accession]": "CVCL_0042",
            "characteristics[material type]": "cell line",
            "characteristics[disease]": "osteosarcoma",
            "characteristics[age]": "15Y",
            "characteristics[sex]": "female",
            "characteristics[biological replicate]": replicate,
            "characteristics[siRNA target]": target,
            "characteristics[5-AzadC treatment]": "5-AzadC for 30 min" if aza else "untreated",
            "characteristics[enrichment bait]": "DNMT1-trap beads",
            "factor value[siRNA target]": target,
            "factor value[5-AzadC treatment]": "5-AzadC for 30 min" if aza else "untreated",
        })
assert {row["files"] for row in rows} == raw
with (work / "samples.tsv").open("w", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
(work / "raw-files.json").write_text(json.dumps(sorted(raw), indent=2) + "\n")
technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=Orbitrap Exploris 480;AC=MS:1003028"),
    ("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251"),
    ("comment[label]", "label free sample"),
    ("comment[dissociation method]", "NT=beam-type collision-induced dissociation;AC=MS:1000422"),
    ("comment[collision energy]", "25 NCE"),
    ("comment[ms1 scan range]", "300m/z-1300m/z"),
    ("comment[reduction reagent]", "NT=Tris(2-carboxyethyl)phosphine (TCEP);AC=PRIDE:0000609"),
    ("comment[alkylation reagent]", "NT=Chloroacetamide (ClAA);AC=PRIDE:0000600"),
    ("comment[precursor mass tolerance]", "not available"),
    ("comment[fragment mass tolerance]", "not available"),
    ("comment[modification parameters]", "NT=Acetyl;AC=UNIMOD:1;PP=Protein N-term;MT=Variable|NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable|NT=GlyGly;AC=UNIMOD:121;TA=K;MT=Variable"),
]
with (work / "technical.tsv").open("w", newline="") as fh:
    writer = csv.writer(fh, delimiter="\t", lineterminator="\n")
    writer.writerow(("column", "value"))
    writer.writerows(technical)
print("PXD041717: five conditions x four independent replicates; 20 matched RAW files")
