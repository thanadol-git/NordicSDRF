"""Build PXD065658 SDRF tables from the deposited MS file overview and ZIP index."""

import csv
import json
import struct
from collections import Counter
from pathlib import Path

import openpyxl


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD065658"
files = json.loads((work / "files.json").read_text())
assert all("PXD065658" in item["projectAccessions"] for item in files)
assert {item["fileName"] for item in files if item["fileName"].lower().endswith(".zip")} == {"AllRawFiles.zip"}

book = openpyxl.load_workbook(work / "MSFilesOverview.xlsx", read_only=True, data_only=True)
assert book.sheetnames == ["Sheet1"]
overview = list(book.active.values)
assert overview[0] == ("File name", "Group") and len(overview) == 21
samples = [(path.strip().split("\\")[-1], group) for path, group in overview[1:]]

tail = (work / "raw-tail-256k.bin").read_bytes()
index = tail.find(b"PK\x01\x02")
entries = []
while index >= 0 and tail[index:index + 4] == b"PK\x01\x02":
    header = struct.unpack_from("<IHHHHHHIIIHHHHHII", tail, index)
    name_len, extra_len, comment_len = header[10:13]
    entries.append(tail[index + 46:index + 46 + name_len].decode("utf-8"))
    index += 46 + name_len + extra_len + comment_len
assert len(entries) == 520
raw = sorted({name.split("/")[0] for name in entries if name.endswith("analysis.tdf")})
assert len(raw) == 20
assert set(raw) == {filename for filename, _ in samples}
(work / "raw-files.json").write_text(json.dumps(raw, indent=2) + "\n")

rows = []
for filename, group in samples:
    strain_code, age_code = group.split()
    assert strain_code in {"SHR", "WKY"} and age_code in {"30w", "40w"}
    source = filename.split("_")[0]
    assert source.startswith(strain_code)
    replicate = int(source[len(strain_code):])
    strain = "spontaneously hypertensive rat" if strain_code == "SHR" else "Wistar-Kyoto rat"
    age = "30W" if age_code == "30w" else "40W"
    rows.append({
        "source name": source,
        "files": filename,
        "label": "label free sample",
        "characteristics[organism]": "Rattus norvegicus",
        "characteristics[organism part]": "cerebral artery",
        "characteristics[biological replicate]": replicate,
        "characteristics[disease]": "hypertension" if strain_code == "SHR" else "normal",
        "characteristics[material type]": "tissue",
        "characteristics[developmental stage]": "adult",
        "characteristics[strain or breed]": strain,
        "characteristics[sex]": "male",
        "characteristics[age]": age,
        "factor value[strain or breed]": strain,
        "factor value[age]": age,
    })
assert Counter(group for _, group in samples) == {"SHR 30w": 5, "SHR 40w": 7, "WKY 30w": 4, "WKY 40w": 4}
with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "Data-independent acquisition"),
    ("comment[instrument]", "NT=timsTOF Pro;AC=MS:1003005"),
    ("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251|NT=Lys-C;AC=MS:1001309"),
    ("comment[precursor mass tolerance]", "not available"),
    ("comment[fragment mass tolerance]", "not available"),
    ("comment[reduction reagent]", "NT=Tris(2-carboxyethyl)phosphine (TCEP);AC=PRIDE:0000609"),
    ("comment[alkylation reagent]", "NT=Chloroacetamide (ClAA);AC=PRIDE:0000600"),
    ("comment[modification parameters]", "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed|NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable"),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("column", "value"))
    writer.writerows(technical)
print("PXD065658: 20 matched acquisitions; four groups 5/7/4/4")
