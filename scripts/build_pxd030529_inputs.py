"""Create accession-scoped SDRF build inputs from the PXD030529 deposit and supplement."""

import csv
import json
from pathlib import Path


root = Path(__file__).resolve().parents[1]
work = root / "scratchpad/PXD030529"
files = json.loads((work / "files.json").read_text())
raw = [x for x in files if x.get("fileCategory", {}).get("name") == "Associated raw file URI"]
assert len(raw) == 8 and all("PXD030529" in x.get("projectAccessions", []) for x in raw)

groups = {
    "exploris": [x for x in raw if "EXPL2" in x["fileName"]],
    "fyrkat": [x for x in raw if "QE5" in x["fileName"]],
}
assert all(len(group) == 4 for group in groups.values())

mapping = {
    "F1.raw": ("Hvilehøj C4273-97 fragment 19", "Castor"),
    "F2.raw": ("Hvilehøj C4273-97 fragment 1", "Ovis aries"),
    "F3.raw": ("Hvilehøj C4273-97 fragment 60", "Sciuridae"),
    "F8.raw": ("Bjerringhøj AdC143", "Castor"),
    "GuHCl_fyrkat.raw": ("Fyrkat D158-1966 GuHCl", "Mustela sp."),
    "Urea_fyrkat.raw": ("Fyrkat D158-1966 Urea", "Mustelidae"),
    "GuHCl_BK.raw": ("Fyrkat GuHCl preparation blank", "not applicable"),
    "Urea_BK.raw": ("Fyrkat Urea preparation blank", "not applicable"),
}
fields = ["source name", "files", "label", "characteristics[organism]", "characteristics[organism part]", "characteristics[biological replicate]", "characteristics[disease]", "characteristics[developmental stage]", "characteristics[sex]"]
for group_name, group in groups.items():
    (work / f"{group_name}_files.json").write_text(json.dumps([x["fileName"] for x in group], indent=2) + "\n")
    with (work / f"{group_name}_samples.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        for file in sorted(group, key=lambda x: x["fileName"]):
            name = file["fileName"]
            source, organism = next(value for suffix, value in mapping.items() if name.endswith(suffix))
            blank = name.endswith("_BK.raw")
            writer.writerow({"source name": source, "files": name, "label": "label free sample", "characteristics[organism]": organism, "characteristics[organism part]": "not applicable" if blank else "hair", "characteristics[biological replicate]": 1, "characteristics[disease]": "not applicable", "characteristics[developmental stage]": "not applicable" if blank else "not available", "characteristics[sex]": "not applicable" if blank else "not available"})
    technical = [
        ("comment[sdrf version]", "v1.1.0"),
        ("comment[sdrf annotation tool]", "manual curation"),
        ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
        ("comment[instrument]", "NT=Orbitrap Exploris 480;AC=MS:1003028" if group_name == "exploris" else "NT=Q Exactive HF-X;AC=MS:1002877"),
        ("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251"),
        ("comment[dissociation method]", "NT=beam-type collision-induced dissociation;AC=MS:1000422"),
        ("comment[modification parameters]", "|".join([
            "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed",
            "NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable",
            "NT=Acetyl;AC=UNIMOD:1;PP=Protein N-term;MT=Variable",
            "NT=Deamidated;AC=UNIMOD:7;TA=N,Q;MT=Variable",
            "NT=Gln->pyro-Glu;AC=UNIMOD:28;PP=Any N-term;TA=Q;MT=Variable",
            "NT=Glu->pyro-Glu;AC=UNIMOD:27;PP=Any N-term;TA=E;MT=Variable",
        ])),
    ]
    with (work / f"{group_name}_technical.tsv").open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["column", "value"])
        writer.writerows(technical)
