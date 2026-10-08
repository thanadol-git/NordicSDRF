# PXD015078-ftsh

Status: validated local annotation; independent review pending. PR not created.

- GUN1 and chloroplast transit peptides (PXD015078): hwFtsH and mFtsH SDS-PAGE bands of 6-day-old Arabidopsis Col-0 and gun1-102 seedlings, +/- lincomycin, Q Exactive; University of Turku (Aro lab) with CNR Italy.
- SDRF: `annotations/PXD015078-ftsh.sdrf.tsv`
- Rows: 24; columns: 35
- SHA-256: `9b635e5f07549e4040a039ac722302bb1a3d4d883c1c532d80a715f08d8e6cd7`
- Evidence manifest: `annotations/PXD015078-ftsh.evidence.json`
- Scope: 24 RAW files: 4 groups x 2 bands x 3 injections (plain, FtsH2 inclusion list, FtsH5 inclusion list); label-free DDA.

## Validation

- `parse_sdrf validate-sdrf -t ms-proteomics -t plants --use_ols_cache_only`: passed (free-text ontology warnings only).
- `sdrf-tools structure`: OK; `tools check`: clean.

## Limitations

- Subset of PXD015078 split by instrument and modification set; the two files together claim all 36 RAW files exactly once.
- Lincomycin concentration not recorded; 'no lincomycin' is free text. Seedling age (6 days after sowing) is in growth condition; developmental stage is `not available` (no resolvable EFO term).
- Col-0 is the background of gun1-102 (PRIDE text).
- The deposited *_semi.msf files are semi-tryptic re-searches of the same RAW files and add no rows.
- The inclusion-list injections are encoded only as technical replicates 2 and 3.
