# PXD069402-interactomeB-dda annotation report

## Result

50 bacterial DDA AP-MS and spectral-library runs from interactome B.

- Rows: 50
- Columns: 28
- Unique acquisition files represented: 50
- Artifact SHA-256: `80e3a5c524e0dfab33b2a23cf38576ed1518ebe1bb28acc189062e2e205fb92d`

## Validation

- `parse_sdrf validate-sdrf --skip-ontology`: PASS
- `sdrf-tools structure`: PASS
- `sdrf-tools check --offline`: CLEAN
- Exact deposited acquisition-file coverage: PASS
- Record reconciliation: PASS
- Independent adversarial review: PENDING; this artifact is annotated and validated but not yet independently approved for PR

## Evidence limitations

- Library fraction identifiers are preserved in the prey-fraction factor rather than inferred as technical fractions of a single source.
- Search modifications and fixed tolerances are not explicit in the accessible record.
