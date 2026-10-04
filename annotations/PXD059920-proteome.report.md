# PXD059920-proteome annotation report

Status: validated local annotation; independent adversarial review passed; no pull request created.

## Outputs

- `annotations/PXD059920-proteome.sdrf.tsv` — 192 rows x 32 columns; SHA-256 `113c5767ba1c8db1ef3cdc8af5e113f631d09298745dfcebf06fffd6dc119ae9`
- Evidence manifest: `annotations/PXD059920-proteome.evidence.json`
- Unique RAW files represented in this output: 192
- Templates: ms-proteomics, human, clinical-metadata, oncology-metadata, dia-acquisition

## Evidence and design

- RAW basenames identify patient sample codes, pooled references, and proteome versus phosphoproteome acquisitions; the outputs preserve that split.
- Publication: DOI 10.1186/S13058-025-02173-9
- Any deposited community SDRF was excluded from the evidence used to create this annotation.

## Validation

- `parse_sdrf validate-sdrf` passed with the declared template union and `--skip-ontology`.
- `python -m tools structure` passed.
- `python -m tools check --offline` returned no hallucinated accessions, ontology-family errors, label mismatches, or UNIMOD swaps.
- Dataset-level RAW-file coverage is exact, with no missing or extra acquisition files across split outputs where applicable.

## Limitations

- Patient demographics are not mapped at source level in the accessible record.
- The SDRF cleavage-agent field is single-valued; Trypsin is recorded while the prose also names Lys-C.
