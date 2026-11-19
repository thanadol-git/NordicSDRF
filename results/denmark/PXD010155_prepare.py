#!/usr/bin/env python3
"""Prepare samples.tsv / technical.tsv for PXD010155 glyco and proteome subsets.

Channel map (Data S1 labels × deposited PD SEARCH ratios; T11 2000/2000 exact,
T2 1803/2000 exact for mono dose order):
  TMT126 = uninduced (0 ng/ml)
  TMT127..TMT130 = increasing dox doses
  TMT131 = HEK WT
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = json.loads((ROOT / "files.json").read_text())
for f in FILES:
    assert "PXD010155" in (f.get("projectAccessions") or []), f.get("fileName")

RAW = sorted(
    f["fileName"]
    for f in FILES
    if (f.get("fileCategory") or {}).get("value") == "RAW"
)
assert len(RAW) == 32, len(RAW)

GROUPS = {
    "T2_glyco": "171030_Fusion_LC2_John_Hek_WT_T2_inducer_Trypsin_TMT6plex_PNA_2h_ETD_HCD_High_pH",
    "T11_glyco": "171020_Fusion_LC2_John_Hek_WT_T11_inducer_Trypsin_TMT6plex_PNA_2h_ETD_HCD_High_pH",
    "T2_proteome": "171209_Fusion_LC2_John_Hek_WT_T2_inducer_Trypsin_TMT6plex_PNA_FT_Proteome_3h_HCD_High_pH",
    "T11_proteome": "171222_Fusion_LC2_John_Hek_WT_T11_inducer_Trypsin_TMT6plex_PNA_FT_Proteome_3h_HCD_High_pH",
}


def fractions(stem: str) -> list[str]:
    files = [f for f in RAW if f.startswith(stem + "_") and f.lower().endswith(".raw")]
    files = sorted(files, key=lambda n: int(n.rsplit("_", 1)[1].split(".", 1)[0]))
    assert [int(f.rsplit("_", 1)[1].split(".", 1)[0]) for f in files] == list(range(1, 9)), files
    return files


# channel -> (label, dose_ng_ml or None for WT marker)
T2_CHANNELS = [
    ("TMT126", "HEKindT2_0ng", "HEKindT2", "0 ng/ml", 1),
    ("TMT127", "HEKindT2_4ng", "HEKindT2", "4 ng/ml", 1),
    ("TMT128", "HEKindT2_8ng", "HEKindT2", "8 ng/ml", 1),
    ("TMT129", "HEKindT2_12ng", "HEKindT2", "12 ng/ml", 1),
    ("TMT130", "HEKindT2_16ng", "HEKindT2", "16 ng/ml", 1),
    ("TMT131", "HEKWT_T2plex", "HEK WT", "0 ng/ml", 1),
]
T11_CHANNELS = [
    ("TMT126", "HEKindT11_0ng", "HEKindT11", "0 ng/ml", 1),
    ("TMT127", "HEKindT11_2p5ng", "HEKindT11", "2.5 ng/ml", 1),
    ("TMT128", "HEKindT11_5ng", "HEKindT11", "5 ng/ml", 1),
    ("TMT129", "HEKindT11_7p5ng", "HEKindT11", "7.5 ng/ml", 1),
    ("TMT130", "HEKindT11_10ng", "HEKindT11", "10 ng/ml", 1),
    ("TMT131", "HEKWT_T11plex", "HEK WT", "0 ng/ml", 1),
]

HEAD = [
    "source name",
    "files",
    "label",
    "technical replicate",
    "characteristics[organism]",
    "characteristics[organism part]",
    "characteristics[cell type]",
    "characteristics[biological replicate]",
    "characteristics[disease]",
    "characteristics[age]",
    "characteristics[sex]",
    "characteristics[ancestry category]",
    "characteristics[individual]",
    "characteristics[cell line]",
    "characteristics[cellosaurus accession]",
    "characteristics[cellosaurus name]",
    "characteristics[passage number]",
    "characteristics[culture medium]",
    "characteristics[sample storage temperature]",
    "characteristics[enrichment process]",
    "factor value[genotype]",
    "factor value[doxycycline]",
]


def write_samples(path: Path, enrichment: str, groups: list[tuple[str, list]]) -> None:
    rows = []
    for stem, channels in groups:
        files = ",".join(fractions(stem))
        for label, source, genotype, dox, biorep in channels:
            rows.append(
                [
                    source,
                    files,
                    label,
                    "1",
                    "Homo sapiens",
                    "kidney",
                    "not available",
                    str(biorep),
                    "not available",
                    "not available",
                    "female",
                    "not available",
                    source,
                    "HEK293",
                    "CVCL_0045",
                    "HEK293",
                    "not available",
                    "not available",
                    "not available",
                    enrichment,
                    genotype,
                    dox,
                ]
            )
    with path.open("w", newline="") as out:
        w = csv.writer(out, delimiter="\t", lineterminator="\n")
        w.writerow(HEAD)
        w.writerows(rows)


def write_technical(path: Path, *, glyco: bool) -> None:
    mods = [
        "NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed",
        "NT=TMT6plex;AC=UNIMOD:737;TA=K;MT=Fixed",
        "NT=TMT6plex;AC=UNIMOD:737;PP=Any N-term;MT=Fixed",
        "NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable",
    ]
    if glyco:
        mods.append("NT=HexNAc;AC=UNIMOD:43;TA=S,T,Y;MT=Variable")
        dissociation = "NT=beam-type collision-induced dissociation;AC=MS:1000422"  # ETD added by expand_glyco_dissociation.py
    else:
        dissociation = "NT=beam-type collision-induced dissociation;AC=MS:1000422"

    rows = [
        ("comment[sdrf version]", "v1.1.0"),
        ("comment[sdrf annotation tool]", "manual curation"),
        (
            "comment[proteomics data acquisition method]",
            "NT=Data-dependent acquisition;AC=PRIDE:0000627",
        ),
        ("comment[instrument]", "NT=Orbitrap Fusion;AC=MS:1002416"),
        ("comment[cleavage agent details]", "NT=Trypsin;AC=MS:1001251"),
        ("comment[dissociation method]", dissociation),
        (
            "comment[fractionation method]",
            "NT=High-pH reversed-phase chromatography (hpHRP);AC=PRIDE:0000564",
        ),
        ("comment[precursor mass tolerance]", "6 ppm"),
        ("comment[fragment mass tolerance]", "0.02 Da"),
        ("comment[reduction reagent]", "NT=Dithiothreitol (DTT);AC=PRIDE:0000613"),
        ("comment[alkylation reagent]", "NT=Iodoacetamide (IAA);AC=PRIDE:0000599"),
        ("comment[modification parameters]", "|".join(mods)),
    ]
    with path.open("w", newline="") as out:
        w = csv.writer(out, delimiter="\t", lineterminator="\n")
        w.writerow(["column", "value"])
        w.writerows(rows)


def main() -> None:
    write_samples(
        ROOT / "glyco_samples.tsv",
        "glycopeptide enrichment",
        [
            (GROUPS["T2_glyco"], T2_CHANNELS),
            (GROUPS["T11_glyco"], T11_CHANNELS),
        ],
    )
    write_samples(
        ROOT / "proteome_samples.tsv",
        "not applicable",
        [
            (GROUPS["T2_proteome"], T2_CHANNELS),
            (GROUPS["T11_proteome"], T11_CHANNELS),
        ],
    )
    write_technical(ROOT / "glyco_technical.tsv", glyco=True)
    write_technical(ROOT / "proteome_technical.tsv", glyco=False)
    # raw-only files.json for build
    raw_files = [f for f in FILES if (f.get("fileCategory") or {}).get("value") == "RAW"]
    (ROOT / "raw_files.json").write_text(json.dumps(raw_files, indent=2) + "\n")
    print("wrote glyco/proteome samples+technical; raw_files", len(raw_files))


if __name__ == "__main__":
    main()
