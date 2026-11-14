"""Build inputs for two instrument-specific PXD031280 pigment SDRFs."""

import csv
import json
from pathlib import Path


root = Path(__file__).resolve().parents[1]
work = root / "scratchpad/PXD031280"
items = json.loads((work / "files.json").read_text())
assert items and all("PXD031280" in item.get("projectAccessions", []) for item in items)
raw = {item["fileName"] for item in items if item.get("fileCategory", {}).get("name") == "Associated raw file URI"}
assert len(raw) == 6

groups = {
    "2016": {
        "RedSample_2016files_928.raw": ("red paint IN2795", "red", 1),
        "YellowSample_2016files_929.raw": ("yellow paint IN2795", "yellow", 1),
        "Blank_930.raw": ("2016 batch protocol blank", "not applicable", 1),
    },
    "2021": {
        "RedSample_2021files_1944_2.raw": ("red paint IN2795", "red", 1),
        "YellowSample_2021files_1945_2.raw": ("yellow paint IN2795", "yellow", 1),
        "Blank_1943.raw": ("2021 batch protocol blank", "not applicable", 1),
    },
}
assert raw == set().union(*(set(group) for group in groups.values()))

fields = ["source name", "files", "label", "technical replicate", "characteristics[organism]", "characteristics[organism part]", "characteristics[biological replicate]", "characteristics[disease]", "factor value[paint color]"]
for group_name, mapping in groups.items():
    (work / f"{group_name}_files.json").write_text(json.dumps(sorted(mapping), indent=2) + "\n")
    with (work / f"{group_name}_samples.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        for filename, (source, color, replicate) in mapping.items():
            writer.writerow({"source name": source, "files": filename, "label": "label free sample", "technical replicate": replicate, "characteristics[organism]": "not applicable", "characteristics[organism part]": "not applicable", "characteristics[biological replicate]": 1, "characteristics[disease]": "not applicable", "factor value[paint color]": color})
    technical = [
        ("comment[sdrf version]", "v1.1.0"),
        ("comment[sdrf annotation tool]", "manual curation"),
        ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
        ("comment[instrument]", "NT=Q Exactive HF;AC=MS:1002523" if group_name == "2016" else "NT=Orbitrap Exploris 480;AC=MS:1003028"),
        ("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251"),
        ("comment[dissociation method]", "NT=beam-type collision-induced dissociation;AC=MS:1000422"),
        ("comment[modification parameters]", "|".join([
            "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed",
            "NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable",
            "NT=Acetyl;AC=UNIMOD:1;PP=Protein N-term;MT=Variable",
            "NT=Deamidated;AC=UNIMOD:7;TA=N,Q;MT=Variable",
            "NT=Gln->pyro-Glu;AC=UNIMOD:28;PP=Any N-term;TA=Q;MT=Variable",
            "NT=Glu->pyro-Glu;AC=UNIMOD:27;PP=Any N-term;TA=E;MT=Variable",
            "NT=Oxidation;AC=UNIMOD:35;TA=P;MT=Variable",
        ])),
    ]
    with (work / f"{group_name}_technical.tsv").open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["column", "value"])
        writer.writerows(technical)
