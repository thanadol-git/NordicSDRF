# PXD054815-chop annotation report

## Result

Two label-free HeLa CHOP runs comparing LacZ control and ARHGEF17-AS1 M30 capture oligonucleotides.

- Rows: 2
- Columns: 36
- Unique acquisition files represented: 2
- Artifact SHA-256: `98ed79d558e4cee7e854879f58d643c5ffc3bdc0ff1d086757ad9d5e6a27523d`

## Validation

- `parse_sdrf validate-sdrf --skip-ontology`: PASS
- `parse_sdrf validate-sdrf --use_ols_cache_only`: PASS
- `sdrf-tools structure`: PASS
- `sdrf-tools check --offline`: CLEAN
- Exact deposited acquisition-file coverage for this artifact: PASS
- Independent adversarial review: PENDING; this artifact is annotated and validated but is not yet independently approved for PR

## Evidence limitations

- This artifact covers only the two label-free CHOP runs; the separate TMT IP arm is blocked pending its channel map.
- Project-level reconciliation reports TMT because the PRIDE record describes the mixed project globally; the two selected QEHF runs are explicitly identified as CHOP and processed label-free in the deposited sample sheet and protocol.
