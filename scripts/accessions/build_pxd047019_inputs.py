"""Build evidence-backed PXD047019 sample and technical tables."""

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


root = Path(__file__).resolve().parents[2]
work = root / "scratchpad/PXD047019"
record = json.loads((work / "pride.json").read_text())
assert record["accession"] == "PXD047019"
files = json.loads((work / "files.json").read_text())
assert all("PXD047019" in item["projectAccessions"] for item in files)
raw = {item["fileName"] for item in files if item["fileName"].lower().endswith(".raw")}
assert len(raw) == 90
(work / "raw-files.json").write_text(json.dumps(sorted(raw), indent=2) + "\n")

with (work / "run-map.tsv").open(newline="") as handle:
    runs = list(csv.DictReader(handle, delimiter="\t"))
assert len(runs) == 90 and {row["raw_file"] for row in runs} == raw
grouped = defaultdict(list)
for row in runs:
    assert row["genotype_code"] in {"C", "RKO", "HKO"}
    assert int(row["fraction"]) in range(1, 7)
    grouped[(row["genotype_code"], int(row["biological_replicate"]))].append(row)
assert len(grouped) == 15
assert Counter(code for code, _ in grouped) == {"C": 5, "RKO": 5, "HKO": 5}

samples = []
for (code, replicate), group in sorted(grouped.items()):
    group.sort(key=lambda row: int(row["fraction"]))
    assert [int(row["fraction"]) for row in group] == list(range(1, 7))
    assert len({row["genotype"] for row in group}) == 1
    assert len({row["pooled_testes_per_replicate"] for row in group}) == 1
    genotype = group[0]["genotype"]
    samples.append({
        "source name": f"{code}-{replicate:02d}",
        "files": ",".join(row["raw_file"] for row in group),
        "label": "label free sample",
        "characteristics[organism]": "Mus musculus",
        "characteristics[organism part]": "testis",
        "characteristics[biological replicate]": replicate,
        "characteristics[pooled sample]": "pooled",
        "characteristics[disease]": "not applicable",
        "characteristics[material type]": "tissue",
        "characteristics[developmental stage]": "not available",
        "characteristics[sex]": "male",
        "characteristics[enrichment antibody]": "8A2 anti-SUMO2/3 antibody",
        "characteristics[genotype]": genotype,
        "factor value[genotype]": genotype,
    })

with (work / "samples.tsv").open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(samples[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(samples)

technical = [
    ("comment[sdrf version]", "v1.1.0"),
    ("comment[sdrf annotation tool]", "manual curation"),
    ("comment[proteomics data acquisition method]", "NT=Data-dependent acquisition;AC=PRIDE:0000627"),
    ("comment[instrument]", "NT=Orbitrap Exploris 480;AC=MS:1003028"),
    ("comment[cleavage agent details]", "NT=Lys-C;AC=MS:1001309|NT=Asp-N;AC=MS:1001304"),
    ("comment[dissociation method]", "NT=beam-type collision-induced dissociation;AC=MS:1000422"),
    ("comment[collision energy]", "25 NCE"),
    ("comment[precursor mass tolerance]", "not available"),
    ("comment[fragment mass tolerance]", "not available"),
    ("comment[reduction reagent]", "NT=Tris(2-carboxyethyl)phosphine (TCEP);AC=PRIDE:0000609"),
    ("comment[alkylation reagent]", "NT=Chloroacetamide (ClAA);AC=PRIDE:0000600"),
    ("comment[modification parameters]", "NT=Acetyl;AC=UNIMOD:1;PP=Protein N-term;MT=Variable|NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable|NT=Gln->pyro-Glu;AC=UNIMOD:28;TA=Q;PP=Peptide N-term;MT=Variable|NT=SUMOylation (DVFQQQTGG);MM=960.4301;TA=K;MT=Variable"),
    ("comment[ms1 scan range]", "500m/z-1500m/z"),
]
with (work / "technical.tsv").open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow(("column", "value"))
    writer.writerows(technical)
print("PXD047019: 15 pooled samples; 90 matched RAW fractions")
