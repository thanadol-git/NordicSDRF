# PXD034174-venom

Status: validated local annotation; independent review pending. PR not created.

- PXD034174 - Physiological constraints dictate toxin spatial heterogeneity in snake venom glands (Kazandjian et al., BMC Biol 2022)
- SDRF: `annotations/PXD034174-venom.sdrf.tsv`
- Rows: 6; columns: 25
- SHA-256: `3753001b39bb5dcf75a9b731a4c7c87895228d8b8a142138fbc4bef278898e3e`
- Evidence manifest: `annotations/PXD034174-venom.evidence.json`
- Scope: 6 intact venom LC-MS runs: spat vs milked venom from H. haemachatus, N. nigricollis, N. pallida (TripleTOF 5600)

## Validation

- parse_sdrf validate-sdrf -t base: clean
- tools structure: OK
- tools check: CLEAN (5/5 terms)
- Data files: 6/6 .wiff claimed once

## Limitations

- PXD034174 is split into three SDRFs because it holds three unrelated assays: tryptic LC-MS/MS of venom gland section quarters (-tissue), intact-venom LC-MS of spat vs milked venom (-venom), and MALDI mass spectrometry imaging (-msi).
- Each .wiff is claimed once; the companion .wiff.scan files are not listed as data files. imzML files (IMAGE DATA) are companions of the .ibd files; only .ibd (RAW category) are claimed.
- File names say Nmoss/Nmos/n-moss (Naja mossambica); the paper and PRIDE name the animal Naja nigricollis (Tanzanian origin), so Naja nigricollis is used. n-mel is mapped to Naja subfulva (paper: non-spitting cobra N. subfulva; PRIDE organism list) - the abbreviation itself is not decoded by any deposited file.
- Sex, age, developmental stage and strain are not reported and are not included.
- 'postspit' is interpreted as milked venom (paper: milked samples extracted following spits); not stated verbatim in the file names. Biological replicate 1: one specimen per species.
- comment[proteomics data acquisition method] column omitted and base template declared (instead of ms-proteomics) because no PRIDE:0000659 term fits this assay; ms-proteomics would require a false value.
