"""Build the two separately processed proteomics arms of PXD017475."""

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "scratchpad/PXD017475"
record = json.loads((WORK / "pride.json").read_text())
assert record["accession"] == "PXD017475"
entries = json.loads((WORK / "files.json").read_text())
assert entries and all("PXD017475" in e["projectAccessions"] for e in entries)
raw = {e["fileName"] for e in entries if e["fileName"].lower().endswith(".raw")}
assert len(raw) == 19


def file_for(suffix):
    hits = [name for name in raw if name.endswith("_" + suffix + ".raw")]
    assert len(hits) == 1, (suffix, hits)
    return hits[0]


def write_arm(arm, rows, technical):
    folder = WORK / arm
    folder.mkdir(exist_ok=True)
    with (folder / "samples.tsv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with (folder / "technical.tsv").open("w", newline="") as fh:
        writer = csv.writer(fh, delimiter="\t", lineterminator="\n")
        writer.writerow(("column", "value"))
        writer.writerows(technical)
    (folder / "files.json").write_text(json.dumps([r["files"] for r in rows], indent=2) + "\n")


common = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=Q Exactive HF;AC=MS:1002523"),
    ("comment[ms1 scan range]", "300m/z-1700m/z"),
]

secretome = []
conditions = {"A": "control proliferating", "B": "control senescent", "C": "MIR31HG-depleted senescent"}
for n in range(1, 4):
    for letter in "ABC":
        suffix = f"{(n - 1) * 3 + ord(letter) - ord('A') + 1}_{n}{letter}"
        secretome.append({
            "source name": f"secretome-{n}{letter}",
            "files": file_for(suffix),
            "label": "label free sample",
            "characteristics[organism]": "Homo sapiens",
            "characteristics[cell line]": "BJ ER:BRAF",
            "characteristics[material type]": "cell line",
            "characteristics[biological replicate]": n,
            "characteristics[disease]": "normal",
            "characteristics[experimental condition]": conditions[letter],
            "factor value[experimental condition]": conditions[letter],
        })
assert len(secretome) == 9
write_arm("secretome", secretome, common + [
    ("comment[precursor mass tolerance]", "7 ppm"),
    ("comment[fragment mass tolerance]", "20 ppm"),
    ("comment[cleavage agent details]", "NT=Lys-C;AC=MS:1001309|NT=Trypsin;AC=MS:1001251"),
    ("comment[reduction reagent]", "NT=Dithiothreitol (DTT);AC=PRIDE:0000599"),
    ("comment[alkylation reagent]", "not available"),
    ("comment[modification parameters]", "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed|NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable|NT=Acetyl;AC=UNIMOD:1;PP=Protein N-term;MT=Variable|NT=Deamidated;AC=UNIMOD:7;TA=N,Q;MT=Variable"),
])

pulldown = []
for target, codes in (("luciferase control", ["3Ctrl1", "4Ctrl2", "Cm1_vs2", "Cm2_vs2", "Cm3_vs2"]),
                      ("MIR31HG", ["5MIR31_1", "6MIR31_2", "M1_vs2", "M2_vs2", "M3_vs2"])):
    for n, code in enumerate(codes, 1):
        pulldown.append({
            "source name": f"pulldown-{target.replace(' ', '-')}-{n}",
            "files": file_for(code),
            "label": "label free sample",
            "characteristics[organism]": "Homo sapiens",
            "characteristics[cell line]": "BJ ER:BRAF",
            "characteristics[material type]": "cell line",
            "characteristics[biological replicate]": n,
            "characteristics[disease]": "normal",
            "characteristics[senescence status]": "senescent",
            "characteristics[senescence induction]": "4-hydroxytamoxifen (1 uM, 72 h)",
            "characteristics[crosslinking]": "UV 254 nm",
            "characteristics[enrichment oligo target]": target,
            "factor value[enrichment oligo target]": target,
        })
assert len(pulldown) == 10
write_arm("pulldown", pulldown, common + [
    ("comment[precursor mass tolerance]", "not available"),
    ("comment[fragment mass tolerance]", "not available"),
    ("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251"),
    ("comment[reduction reagent]", "NT=Dithiothreitol (DTT);AC=PRIDE:0000599"),
    ("comment[alkylation reagent]", "NT=Iodoacetamide (IAA);AC=PRIDE:0000598"),
    ("comment[modification parameters]", "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed|NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable|NT=Acetyl;AC=UNIMOD:1;PP=Protein N-term;MT=Variable"),
])
assert {r["files"] for r in secretome + pulldown} == raw
print("PXD017475: 9 secretome and 10 pull-down RAW files mapped")
