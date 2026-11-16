"""Build accession-scoped SDRF inputs for painting-ground proteomics PXD035899."""

import csv
import json
import re
from pathlib import Path


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD035899"
files = json.loads((work / "files.json").read_text())
assert files and all("PXD035899" in item.get("projectAccessions", []) for item in files)
raw = sorted(item["fileName"] for item in files if item["fileCategory"].get("value") == "RAW")
assert len(raw) == len(set(raw)) == 15
header_instruments = json.loads((work / "raw-header-instruments.json").read_text())
assert set(header_instruments) == set(raw)

painting_codes = {
    "A": "KMS1671", "B": "KMS1663", "C": "KMS6439", "D": "KMS255",
    "E": "KMS1662", "F": "KMS1667", "G": "KMS6177", "H": "KMS3793",
    "I": "KMS1081", "J": "KS114",
}
model_terms = {
    "Q Exactive HF": "NT=Q Exactive HF;AC=MS:1002523",
    "Q Exactive HF-X": "NT=Q Exactive HF-X;AC=MS:1002877",
}

fields = [
    "source name", "files", "label", "technical replicate",
    "characteristics[organism]", "characteristics[organism part]",
    "characteristics[biological replicate]", "characteristics[material type]",
    "characteristics[run role]", "characteristics[painting code]",
    "characteristics[sampled material]", "comment[instrument]",
]
samples = []
seen_j = 0
for filename in raw:
    blank = re.fullmatch(r"Blank_(\d+)\.raw", filename)
    painting = re.fullmatch(r"([A-J])_(KMS\d+|KS\d+)_(\d+)\.raw", filename)
    assert bool(blank) ^ bool(painting), filename
    if blank:
        run = blank.group(1)
        source = f"extraction-blank-{run}"
        code = "not applicable"
        material = "laboratory extraction blank"
        sample_type = "laboratory negative control"
        technical_replicate = 1
    else:
        letter, code, run = painting.groups()
        assert painting_codes[letter] == code
        source = f"painting-{letter}-{code}"
        material = "painting ground layer and underlying canvas"
        sample_type = "study sample"
        if letter == "J":
            seen_j += 1
            technical_replicate = seen_j
        else:
            technical_replicate = 1
    instrument = model_terms[header_instruments[filename]["model"]]
    samples.append({
        "source name": source,
        "files": filename,
        "label": "label free sample",
        "technical replicate": technical_replicate,
        "characteristics[organism]": "not applicable",
        "characteristics[organism part]": "not applicable",
        "characteristics[biological replicate]": 1,
        "characteristics[material type]": "not applicable",
        "characteristics[run role]": sample_type,
        "characteristics[painting code]": code,
        "characteristics[sampled material]": material,
        "comment[instrument]": instrument,
    })
assert seen_j == 2
with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(samples)

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[cleavage agent details]", "NT=Lys-C;AC=MS:1001309"),
    ("comment[dissociation method]", "NT=beam-type collision-induced dissociation;AC=MS:1000422"),
    ("comment[collision energy]", "28% NCE"),
    ("comment[precursor mass tolerance]", "4.5 ppm"),
    ("comment[fragment mass tolerance]", "20 ppm"),
    ("comment[reduction reagent]", "NT=Tris(2-carboxyethyl)phosphine (TCEP);AC=PRIDE:0000609"),
    ("comment[alkylation reagent]", "NT=Chloroacetamide (ClAA);AC=PRIDE:0000600"),
    ("comment[modification parameters]", "|".join((
        "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed",
        "NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable",
        "NT=Deamidated;AC=UNIMOD:7;TA=N,Q;MT=Variable",
        "NT=Gln->pyro-Glu;AC=UNIMOD:28;TA=Q;PP=Any N-term;MT=Variable",
        "NT=Glu->pyro-Glu;AC=UNIMOD:27;TA=E;PP=Any N-term;MT=Variable",
        "NT=Oxidation;AC=UNIMOD:35;TA=P;MT=Variable",
        "NT=Acetyl;AC=UNIMOD:1;PP=Protein N-term;MT=Variable",
    ))),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("column", "value"))
    writer.writerows(technical)
(work / "raw-files.json").write_text(json.dumps(raw, indent=2) + "\n")
print("10 paintings (11 runs) plus 4 blanks = 15 RAW files")
