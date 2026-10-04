# PXD041824-phospho annotation report

Status: validated local annotation; independent adversarial review passed; no pull request created.

## Outputs

- `annotations/PXD041824-phospho.sdrf.tsv` — 224 rows x 36 columns; SHA-256 `6f50b7245e9d193d196ea205fefd30da2f30c4fb648de5cf474f716bdfc1cb57`
- Evidence manifest: `annotations/PXD041824-phospho.evidence.json`
- Unique RAW files represented in this output: 14
- Templates: ms-proteomics, human, cell-lines

## Evidence and design

- Deposited total-proteome and phosphoproteome workbooks provide the TMTpro channel assignments and experimental conditions; the publication identifies the measured line as CLB-Bar.
- Publication: DOI 10.1073/pnas.2315242121
- Any deposited community SDRF was excluded from the evidence used to create this annotation.

## Validation

- `parse_sdrf validate-sdrf` passed with the declared template union and `--skip-ontology`.
- `python -m tools structure` passed.
- `python -m tools check --offline` returned no hallucinated accessions, ontology-family errors, label mismatches, or UNIMOD swaps.
- Dataset-level RAW-file coverage is exact, with no missing or extra acquisition files across split outputs where applicable.

## Limitations

- The reconciliation helper misreads a mouse-model mention as the measured organism; PRIDE structured organism metadata and the human database/search evidence identify the measured neuroblastoma cells as human.
