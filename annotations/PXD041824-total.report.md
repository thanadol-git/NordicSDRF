# PXD041824-total annotation report

Status: validated local annotation; independent adversarial review passed; no pull request created.

## Outputs

- `annotations/PXD041824-total.sdrf.tsv` — 320 rows x 36 columns; SHA-256 `4e35cbe83bd7f17961892edd3bf9ae62bea2434e3f97aeb7168e4fe10dfb6c42`
- Evidence manifest: `annotations/PXD041824-total.evidence.json`
- Unique RAW files represented in this output: 20
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
