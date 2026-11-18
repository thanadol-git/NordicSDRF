"""Build source and technical tables for the two PXD066033 arms."""

import csv
import json
from collections import Counter
from pathlib import Path


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD066033"
entries = json.loads((work / "files.json").read_text())
assert entries and all("PXD066033" in entry.get("projectAccessions", []) for entry in entries)
raw = {entry["fileName"] for entry in entries if entry["fileCategory"].get("value") == "RAW"}
assert len(raw) == 40

with (work / "run-map.tsv").open(newline="") as handle:
    mapping = list(csv.DictReader(handle, delimiter="\t"))
assert len(mapping) == 40 and {row["raw_file"] for row in mapping} == raw

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=Orbitrap Fusion Lumos;AC=MS:1002732"),
    ("comment[cleavage agent details]", "NT=Lys-C;AC=MS:1001309"),
    ("comment[dissociation method]", "NT=electron-transfer/higher-energy collision dissociation;AC=MS:1002631"),
    ("comment[reduction reagent]", "NT=Tris(2-carboxyethyl)phosphine (TCEP);AC=PRIDE:0000609"),
    ("comment[alkylation reagent]", "not applicable"),
    ("comment[precursor mass tolerance]", "not available"),
    ("comment[fragment mass tolerance]", "not available"),
    ("comment[modification parameters]", "NT=Acetyl;AC=UNIMOD:1;PP=Protein N-term;MT=Variable"),
    ("comment[modification parameters]", "NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable"),
    ("comment[modification parameters]", "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Variable"),
    ("comment[modification parameters]", "NT=ADP-Ribosyl;AC=UNIMOD:213;TA=C,D,E,H,K,R,S,T,Y;MT=Variable"),
]

for arm, count in (("cellular", 24), ("in-vitro", 16)):
    rows = []
    for item in mapping:
        if item["arm"].replace(" ", "-") != arm:
            continue
        genotype = item["sample_code"].removeprefix("invitro-")
        rep = int(item["replicate_code"])
        processing = "PARG" if item["processing_code"] == "parg" else "mock"
        source = f"{arm}-{genotype}-{item['HPF1_or_mock_code']}-{processing}-R{rep}"
        row = {
            "source name": source,
            "files": item["raw_file"],
            "label": "label free sample",
            "characteristics[organism]": "Homo sapiens",
            "characteristics[organism part]": "not applicable" if arm == "in-vitro" else "tibia",
            "characteristics[biological replicate]": rep if arm == "cellular" else 1,
            "characteristics[disease]": "not applicable" if arm == "in-vitro" else "osteosarcoma",
            "characteristics[material type]": "not available" if arm == "in-vitro" else "cell line",
            "characteristics[PARG processing]": processing,
            "comment[filename date code]": item["raw_file"].split("_", 1)[0],
            "factor value[PARG processing]": processing,
        }
        if arm == "cellular":
            row.update({
                "characteristics[age]": "15Y",
                "characteristics[sex]": "female",
                "characteristics[genotype code]": genotype,
                "factor value[genotype code]": genotype,
                "characteristics[cell line]": "U2OS",
                "characteristics[cellosaurus accession]": "CVCL_0042",
                "characteristics[cellosaurus name]": "U2OS",
                "characteristics[DNA damage treatment]": "hydrogen peroxide" if genotype == "HPF1ko" else "methyl methanesulfonate",
            })
        else:
            hp = item["HPF1_or_mock_code"]
            row["characteristics[run suffix]"] = item["replicate_code"]
            row["characteristics[PARP1 variant]"] = genotype
            row["factor value[PARP1 variant]"] = genotype
            row["characteristics[HPF1 addition]"] = "HPF1" if hp == "HPF1" else "mock"
            row["factor value[HPF1 addition]"] = row["characteristics[HPF1 addition]"]
        rows.append(row)
    assert len(rows) == count
    assert len({row["files"] for row in rows}) == count
    samples_path = work / f"{arm}-samples.tsv"
    with samples_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with (work / f"{arm}-technical.tsv").open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("column", "value"))
        writer.writerows(technical)
    (work / f"{arm}-raw-files.json").write_text(json.dumps(sorted(row["files"] for row in rows), indent=2) + "\n")
    print(arm, count, Counter((r.get("characteristics[genotype code]", r.get("characteristics[PARP1 variant]")), r["characteristics[PARG processing]"]) for r in rows))
