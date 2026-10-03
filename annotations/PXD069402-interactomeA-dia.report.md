# PXD069402-interactomeA-dia annotation report

## Result

27 human plasma/saliva DIA AP-MS runs from interactome A.

- Rows: 27
- Columns: 37
- Unique acquisition files represented: 27
- Artifact SHA-256: `f747a367c10908ab9ee5b643c97bce158f1263b23e7e5e710120ad751ba5c5f5`

## Validation

- `parse_sdrf validate-sdrf --skip-ontology`: PASS
- `sdrf-tools structure`: PASS
- `sdrf-tools check --offline`: CLEAN
- Exact deposited acquisition-file coverage: PASS
- Record reconciliation: PASS
- Independent adversarial review: PENDING; this artifact is annotated and validated but not yet independently approved for PR

## Evidence limitations

- The commercial pooled plasma and saliva products do not have donor-level demographics.
- Search modifications and fixed tolerances are not explicit in the accessible record.
