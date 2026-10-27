# PXD013363-lysc-gluc

Status: validated annotation; independent review pending.

Same deposit as `PXD013363-lysc` (see its report for the study, paper, SILAC design and file mapping). This file is the sequential Lys-C then Glu-C digest arm.

- SDRF: `annotations/PXD013363-lysc-gluc.sdrf.tsv`, 64 rows × 41 columns (SUMO1/SUMO2 × 4 replicates × {KGG pull-down, flow-through} × 2 technical replicates × light/heavy)
- SHA-256: `505dc37956a05183caf7c74f1756ebcc3596ef9bdc5962430aba619d65536a6f`
- Evidence manifest: `annotations/PXD013363-lysc-gluc.evidence.json`

## Specifics
- Files (Readme): `SILAC-CCD-S<1,2>-GLUC-<A-D>` (KGG pull-down) and `CCD-S<1,2>-GluCKGG-FT-<A-D>` (flow-through), each present twice (plain and timestamped = technical replicate 1 and 2); 32 RAW files, no fractionation.
- Light = aldosterone, heavy = vehicle (PRIDE protocol), as in the companion.
- **Two `comment[cleavage agent details]` columns** (Lys-C and Glu-C) were written by post-processing the `build` output (the contract treats the column as single-valued, so `build` keeps only the first). `parse_sdrf` accepts the repeated column. Reviewers should decide whether to keep both or only the final protease.
- Modifications, instrument and other technical values identical to the Lys-C file.

## Validation
`parse_sdrf validate-sdrf` (cache-only OLS): 0 errors, same 3 term warnings as the companion. `check --offline` CLEAN, `structure` OK. `reconcile` still reports the Glu-C finding because it reads only the first cleavage column.

## Limitations
As in the Lys-C report (tolerances, dissociation, dose, passage not available; His-SUMO in source name only).
