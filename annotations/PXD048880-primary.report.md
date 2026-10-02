# PXD048880-primary annotation report

## Result

Fifty-four DDA runs from three patient-derived glioblastoma cultures across oxygen condition and surfaceome/endocytome enrichment.

- Rows: 54
- Columns: 45
- Deposited acquisition files represented: 54
- Artifact SHA-256: `0f68d880c7e73bce1b09b485c60effb187fedb82be1b6b83ec083986e3bde890`

## Validation

- `parse_sdrf validate-sdrf --skip-ontology`: PASS
- `sdrf-tools structure`: PASS
- `sdrf-tools check --offline`: CLEAN
- Record reconciliation: PASS with one explained false-positive control-arm warning.
- Independent adversarial review: PENDING; this artifact is a draft and is not PR-ready

## Evidence limitations

- Patient-derived culture names have no Cellosaurus record; accession and demographic fields are not available.
- The reconciler's control-arm disease warning is a false positive: normoxia is an oxygen control, not a non-glioblastoma biological control.
