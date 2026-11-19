"""Rebuild PXD014342 from PRIDE RAW names and Welker et al. Extended Data Table 1."""

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = ROOT / "results/denmark/PXD014342_source_files.json"
OUTPUT = ROOT / "annotations/PXD014342.sdrf.tsv"
raw = sorted(
    f["fileName"] for f in json.loads(FILES.read_text())
    if f["fileCategory"]["value"] == "RAW"
)
assert len(raw) == 27 and len(raw) == len(set(raw))

columns = [
    "source name", "characteristics[organism]", "characteristics[organism part]",
    "characteristics[cell type]", "characteristics[biological replicate]",
    "characteristics[disease]", "characteristics[specimen identifier]",
    "characteristics[taxonomic identification]",
    "characteristics[archaeological site]", "characteristics[extraction method]",
    "assay name", "technology type", "comment[technical replicate]",
    "comment[data file]", "comment[sdrf version]", "comment[sdrf template]",
    "comment[sdrf annotation tool]", "comment[proteomics data acquisition method]",
    "comment[instrument]", "comment[cleavage agent details]",
    "comment[cleavage agent details]", "comment[label]", "comment[fraction identifier]",
    "comment[dissociation method]",
]

rows = []
counts = {}
for filename in raw:
    site = "Atapuerca" if filename.startswith("Atapuerca") else "Dmanisi"
    blank = "_Blank_" in filename
    tissue = "not applicable" if blank else ("tooth enamel" if "_Enamel_" in filename else "dentin")
    match = re.search(r"(?<!\d)(1069|1070|1138|1139|1140|1141|1142|1143|1386|1387|1388)(?!\d)", filename)
    assert match, filename
    tip = match.group(1)
    method = "3" if tip == "1387" else "2" if tip in {"1141", "1142", "1143"} else "1"
    specimen = "not applicable" if blank else ("ATD6-92" if site == "Atapuerca" else "D4163")
    source_name = f"{site}_{tip}_{'blank' if blank else tissue.replace(' ', '_')}_method{method}"
    counts[source_name] = counts.get(source_name, 0) + 1
    cleavage = (
        ["NT=Lys-C;AC=MS:1001309", "NT=Trypsin;AC=MS:1001251"]
        if method == "2" else ["NT=unspecific cleavage;AC=MS:1001955", "not applicable"]
    )
    instrument = (
        "NT=Orbitrap Fusion Lumos;AC=MS:1002732" if "_S_" in filename
        else "NT=Q Exactive HF;AC=MS:1002523"
    )
    rows.append([
        source_name,
        "not applicable" if blank else "Homo",
        tissue,
        "not applicable",
        "1",
        "not applicable",
        specimen,
        "not applicable" if blank else ("Homo antecessor" if site == "Atapuerca" else "Homo erectus"),
        site,
        f"method {method}",
        Path(filename).stem,
        "proteomic profiling by mass spectrometry",
        str(counts[source_name]),
        filename,
        "v1.1.0",
        "NT=ms-proteomics;VV=v1.1.0",
        "manual curation",
        "NT=Data-dependent acquisition;AC=PRIDE:0000627",
        instrument,
        *cleavage,
        "label free sample",
        "1",
        "NT=beam-type collision-induced dissociation;AC=MS:1000422",
    ])

OUTPUT.parent.mkdir(exist_ok=True)
with OUTPUT.open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(columns)
    writer.writerows(rows)
