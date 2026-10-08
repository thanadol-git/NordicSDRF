# PXD015078-supernatant

Status: validated local annotation; independent review pending. PR not created.

- GUN1 and chloroplast transit peptides (PXD015078): soluble extracts of 6-day-old Arabidopsis Col-0 and gun1-102 seedlings, +/- lincomycin, Q Exactive HF; University of Turku (Aro lab) with CNR Italy.
- SDRF: `annotations/PXD015078-supernatant.sdrf.tsv`
- Rows: 12; columns: 35
- SHA-256: `628edb72c9307c5b19f5ffbd8f4ef78f2a93870793953d42cb7d3769978f3ce6`
- Evidence manifest: `annotations/PXD015078-supernatant.evidence.json`
- Scope: 12 RAW files: 4 groups x 3 biological replicates; label-free DDA.

## Validation

- `parse_sdrf validate-sdrf -t ms-proteomics -t plants --use_ols_cache_only`: passed (free-text ontology warnings only).
- `sdrf-tools structure`: OK; `tools check`: clean.

## Limitations

- Subset of PXD015078 split by instrument and modification set; the two files together claim all 36 RAW files exactly once.
- Lincomycin concentration not recorded; 'no lincomycin' is free text. Seedling age (6 days after sowing) is in growth condition; developmental stage is `not available` (no resolvable EFO term).
- Col-0 is the background of gun1-102 (PRIDE text).
- The deposited *_semi.msf files are semi-tryptic re-searches of the same RAW files and add no rows.
