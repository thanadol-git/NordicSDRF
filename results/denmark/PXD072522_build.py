"""Rebuild PXD072522 SDRF from depositor metadata and PRIDE RAW inventory."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
METADATA = ROOT / "results/denmark/PXD072522_source_metadata.txt"
FILES = ROOT / "results/denmark/PXD072522_source_files.json"
OUTPUT = ROOT / "annotations/PXD072522.sdrf.tsv"

with METADATA.open(encoding="utf-16") as handle:
    metadata = list(csv.DictReader(handle, delimiter="\t"))
raw_files = {
    entry["fileName"]
    for entry in json.loads(FILES.read_text())
    if entry["fileCategory"]["value"] == "RAW"
}
assert len(metadata) == len(raw_files) == 36
assert {row[".raw file name"] for row in metadata} == raw_files

columns = [
    "source name",
    "characteristics[organism]",
    "characteristics[organism part]",
    "characteristics[cell type]",
    "characteristics[biological replicate]",
    "characteristics[disease]",
    "characteristics[specimen identifier]",
    "characteristics[taxonomic identification]",
    "characteristics[archaeological site]",
    "characteristics[demineralization buffer]",
    "assay name",
    "technology type",
    "comment[technical replicate]",
    "comment[data file]",
    "comment[sdrf version]",
    "comment[sdrf template]",
    "comment[sdrf annotation tool]",
    "comment[proteomics data acquisition method]",
    "comment[instrument]",
    "comment[cleavage agent details]",
    "comment[label]",
    "comment[fraction identifier]",
]

rows = []
for source in metadata:
    filename = source[".raw file name"]
    stem = Path(filename).stem
    material = source["Material Type"]
    specimen = source["Specimen ID"]
    blank = material == "Blank"
    organism = (
        "not applicable" if blank else
        "Homo" if source["Taxonomic identity"] == "Homo sp." else
        "Mammalia" if source["Taxonomic identity"] == "Stegodon" else
        source["Taxonomic identity"]
    )
    tissue = "not applicable" if blank else ("tooth enamel" if material == "Enamel" else "dentin")
    instrument = (
        "NT=Orbitrap Fusion Lumos;AC=MS:1002732"
        if filename.startswith("25SY")
        else "NT=Orbitrap Exploris 480;AC=MS:1003028"
    )
    cleavage = (
        "NT=Trypsin;AC=MS:1001251"
        if material == "Dentine" or (blank and "Dentine blank" in source["Taxonomic identity"])
        else "NT=unspecific cleavage;AC=MS:1001955"
    )
    technical_replicate = stem.rsplit("_S", 1)[-1] if "_DDA_S" in stem else "1"
    preparation = source["Injection ID"].split("-S", 1)[0] if filename.startswith("25SY") else ""
    row = {
        "source name": (
            f"{specimen}_{source['Injection ID']}" if blank else
            f"{specimen}_{material.lower()}_{preparation}" if preparation else
            f"{specimen}_{material.lower()}"
        ),
        "characteristics[organism]": organism,
        "characteristics[organism part]": tissue,
        "characteristics[cell type]": "not applicable",
        "characteristics[biological replicate]": "1",
        "characteristics[disease]": "not applicable",
        "characteristics[specimen identifier]": specimen,
        "characteristics[taxonomic identification]": source["Taxonomic identity"],
        "characteristics[archaeological site]": source["Site"],
        "characteristics[demineralization buffer]": source["Demin buffer"],
        "assay name": stem,
        "technology type": "proteomic profiling by mass spectrometry",
        "comment[technical replicate]": technical_replicate,
        "comment[data file]": filename,
        "comment[sdrf version]": "v1.1.0",
        "comment[sdrf template]": "NT=ms-proteomics;VV=v1.1.0",
        "comment[sdrf annotation tool]": "manual curation",
        "comment[proteomics data acquisition method]": "NT=Data-dependent acquisition;AC=PRIDE:0000627",
        "comment[instrument]": instrument,
        "comment[cleavage agent details]": cleavage,
        "comment[label]": "label free sample",
        "comment[fraction identifier]": "1",
    }
    rows.append(row)

OUTPUT.parent.mkdir(exist_ok=True)
with OUTPUT.open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=columns, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
