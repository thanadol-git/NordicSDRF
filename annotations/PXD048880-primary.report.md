# PXD048880-primary annotation report

## Result

Fifty-four DDA runs from three patient-derived glioblastoma cultures across oxygen condition and surfaceome/endocytome enrichment.

- Rows: 54
- Columns: 44
- Deposited acquisition files represented: 54
- Artifact SHA-256: `f4ce51e1aacef9f68296b02f4ba69d757cf1d9c505b10229e9e4be082f704f98`

## Validation

- `parse_sdrf validate-sdrf --skip-ontology`: PASS
- `sdrf-tools structure`: PASS
- `sdrf-tools check --offline`: CLEAN
- Record reconciliation: PASS with one explained false-positive control-arm warning.
- Independent adversarial review: PENDING; this artifact is a draft and is not PR-ready

## Evidence limitations

- Patient-derived culture names have no Cellosaurus record; accession and demographic fields are not available.
- The reconciler's control-arm disease warning is a false positive: normoxia is an oxygen control, not a non-glioblastoma biological control.
