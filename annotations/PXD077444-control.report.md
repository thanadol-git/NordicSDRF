# PXD077444-control

Status: validated annotation; independent review pending.

PRIDE title: "Context-Dependent Release of HMGB1: Cell Death Mode, Cell type and LPS Stress Drive Monomer and Heterocomplex Formation". Department of Biomedicine / Norwegian University (Harris lab; PRIDE lists University of Bergen proteomics, PROBE). Paper: Pechiappan H et al., Mol Med 2026, PMID 42067772 (not read). Sibling: `PXD077444-ip`.

- SDRF: `annotations/PXD077444-control.sdrf.tsv`, 1 rows × 37 columns
- SHA-256: `ced013cd2db27cdd8ebc00d4ae6e93d63da497b20ed4d3015264c38c71ec9ade`
- Evidence manifest: `annotations/PXD077444-control.evidence.json`; working files in `sdrf-skills/scratchpad/PXD077444/`

## Templates
`ms-proteomics` v1.1.0 + `dia-acquisition` v1.1.0 (no organism/cell-line template: acellular control).

## Design and file mapping
`13_Bead_CTRL.raw`: Opti-MEM media-only control incubated with the anti-FLAG magnetic beads and processed like the IP samples (the PRIDE processing protocol subtracts this background from the IP samples). It contains no cell material, so it is a separate SDRF without the cell-line columns (organism/cell line `not applicable`).

## Technical values
Same instrument and DIA method as the IP samples (Orbitrap Eclipse, DIA/FAIMS/HCD; Spectronaut).

## Validation
`sdrf-tools build`: 1 rows × 37 columns; `parse_sdrf validate-sdrf … --use_ols_cache_only`: 0 errors (warnings only for free-text terms absent from the ontologies); `check --offline` CLEAN; `structure` OK; `reconcile`: all values agree with the record.

## Limitations
- The control is not a biological sample; organism is `not applicable`.
