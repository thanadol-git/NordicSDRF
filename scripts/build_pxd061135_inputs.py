"""Generate PXD061135 SDRF builder inputs from the deposited run workbook."""

import csv
import json
from pathlib import Path

import openpyxl


root = Path(__file__).resolve().parents[1]
work = root / "scratchpad/PXD061135"
entries = json.loads((work / "files.json").read_text())
assert entries and all("PXD061135" in e.get("projectAccessions", []) for e in entries)
raw = {e["fileName"] for e in entries if e.get("fileCategory", {}).get("name") == "Associated raw file URI"}
misclassified_raw = "20240130_EXPL5_EVO7_FH_SA_HeLa_5ng_sRNG_Pton_fdsm2_03.raw"
assert any(e["fileName"] == misclassified_raw and e["fileCategory"]["name"] == "Search engine output file URI" for e in entries)
raw.add(misclassified_raw)
assert len(raw) == 121

sheet = openpyxl.load_workbook(work / "Annotation-extended.xlsx", read_only=True, data_only=True).active
records = list(sheet.values)
headers = records[0]
mapped = {}
for values in records[1:]:
    if not values[0]:
        continue
    row = dict(zip(headers, values))
    filename = row["R.FileName"] + ("" if str(row["R.FileName"]).endswith(".raw") else ".raw")
    # The workbook repeats _02 for replicate 1 and 2; the deposit has _01/_02/_03.
    if filename == "20240130_EXPL5_EVO7_FH_SA_HeLa_50ng_sRNG_Pton_fdsm0_02.raw" and row["Replicate"] == 1:
        filename = filename.replace("_02.raw", "_01.raw")
    if filename not in raw:
        continue  # Workbook also includes pilot runs absent from this deposit.
    assert filename not in mapped, filename
    assert filename.endswith(f"_{int(row['Replicate']):02d}.raw") or "_8min_" in filename, filename
    mapped[filename] = row
assert set(mapped) == raw, sorted(raw - set(mapped))

fields = [
    "source name", "files", "label", "technical replicate",
    "characteristics[organism]", "characteristics[organism part]",
    "characteristics[biological replicate]", "characteristics[disease]",
    "characteristics[age]", "characteristics[sex]", "characteristics[individual]",
    "characteristics[cell line]", "characteristics[cellosaurus accession]",
    "characteristics[cellosaurus name]", "factor value[acquisition setting]",
]
groups = {"dda": [], "dia": [], "dia-blank": []}
for filename, row in sorted(mapped.items()):
    gradient = row["Gradient"]
    group = "dda" if gradient == "8min" else "dia"
    assert gradient in ("8min", "5min")
    blank = row["Amount"] == "0ng"
    if blank:
        group = "dia-blank"
    setting = str(row["EXP"])
    source = f"HeLa S3 digest {gradient} {row['Amount']} {setting} MS2-{row['MS/MS_Resolution']}"
    if blank:
        source = "zero-load method control"
    sample = {
        "source name": source,
        "files": filename,
        "label": "label free sample",
        "technical replicate": int(row["Replicate"]),
        "characteristics[organism]": "not applicable" if blank else "Homo sapiens",
        "characteristics[organism part]": "not applicable" if blank else "cervix",
        "characteristics[biological replicate]": 1,
        "characteristics[disease]": "not applicable" if blank else "cervical adenocarcinoma",
        "characteristics[age]": "not available",
        "characteristics[sex]": "not applicable" if blank else "female",
        "characteristics[individual]": "not applicable" if blank else "not available",
        "characteristics[cell line]": "" if blank else "HeLa S3",
        "characteristics[cellosaurus accession]": "" if blank else "CVCL_0058",
        "characteristics[cellosaurus name]": "" if blank else "HeLa S3",
        "factor value[acquisition setting]": setting,
    }
    groups[group].append(sample)

for group, samples in groups.items():
    assert len(samples) == {"dda": 72, "dia": 48, "dia-blank": 1}[group], (group, len(samples))
    cols = [x for x in fields if not (group == "dia-blank" and x in (
        "characteristics[cell line]", "characteristics[cellosaurus accession]", "characteristics[cellosaurus name]"))]
    with (work / f"{group}_samples.tsv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cols, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(samples)
    (work / f"{group}_files.json").write_text(json.dumps([s["files"] for s in samples], indent=2) + "\n")
    technical = [
        ("comment[sdrf version]", "v1.1.0"),
        ("comment[sdrf annotation tool]", "manual curation"),
        # Installed dia-acquisition validator accepts the plain DIA label only.
        ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627" if group == "dda" else "Data-independent acquisition"),
        ("comment[instrument]", "NT=Orbitrap Exploris 480;AC=MS:1003028"),
        ("comment[dissociation method]", "NT=beam-type collision-induced dissociation;AC=MS:1000422"),
    ]
    if group == "dia-blank":
        technical.append(("comment[cleavage agent details]", "not applicable"))
    else:
        # The linked paper describes the acquired DDA material as a HeLa
        # tryptic digest and the DIA material as HeLa tryptic peptides.
        technical.append(("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251"))
    with (work / f"{group}_technical.tsv").open("w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["column", "value"])
        writer.writerows(technical)

print({k: len(v) for k, v in groups.items()})
