# PXD069402-interactomeB-dia annotation report

## Result

24 bacterial DIA AP-MS runs from interactome B.

- Rows: 24
- Columns: 32
- Unique acquisition files represented: 24
- Artifact SHA-256: `5629e65b440ff88700e3fb8b5d9d49a2ccb9be4a96ef7a0dd1e047f85f43e937`

## Validation

- `parse_sdrf validate-sdrf --skip-ontology`: PASS
- `sdrf-tools structure`: PASS
- `sdrf-tools check --offline`: CLEAN
- Exact deposited acquisition-file coverage: PASS
- Record reconciliation: PASS
- Independent adversarial review: PENDING; this artifact is annotated and validated but not yet independently approved for PR

## Evidence limitations

- The stepped 25.5/27/30 NCE method cannot be represented in the template's single scalar collision-energy field and is left not available.
- Search modifications and fixed tolerances are not explicit in the accessible record.
