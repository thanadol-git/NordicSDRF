# PXD048892-human annotation report

## Result

Eighteen human wound-fluid peptidomics acquisitions mapped to participant, wound, collection day, and infection group.

- Rows: 18
- Columns: 30
- Deposited acquisition files represented: 18
- Artifact SHA-256: `917fd7bfa9bd88c80948be641781542444b54c8bfcd6dc48f15082de42fb5610`

## Validation

- `parse_sdrf validate-sdrf --skip-ontology`: PASS
- `sdrf-tools structure`: PASS
- `sdrf-tools check --offline`: CLEAN
- Record reconciliation: PASS after evidence review; the remaining no-cleavage warning is a reconciler false positive for endogenous peptidomics.
- Independent adversarial review: PENDING; this artifact is a draft and is not PR-ready

## Evidence limitations

- Age and sex are not available at sample level.
- Bruker .d acquisitions are deposited as one ZIP per sample and are represented by the deposited ZIP filename.
- The reconciler misreads not applicable cleavage as an unsupported enzyme; this is endogenous peptidomics with no digestion.
