# PXD009302-shotgun

Status: validated local annotation; independent review pending. PR not created.

- PXD009302 - APEX2-FGF1 proximity labeling in RPE1 cells (Zhen et al. 2018) - shotgun run
- SDRF: `annotations/PXD009302-shotgun.sdrf.tsv`
- Rows: 1; columns: 35
- SHA-256: `d413aad28376ff7ca65ece9ab1aa9e6c0a079568482f5169681fa4ce8135dc03`
- Evidence manifest: `annotations/PXD009302-shotgun.evidence.json`
- Scope: One label-free run P8838.

## Validation

- parse_sdrf validate-sdrf with ms-proteomics, human, cell-lines (--use_ols_cache_only): 'Everything seems to be fine.'
- tools structure: OK
- tools check: 10 terms verified, 0 hallucinated, CLEAN
- RAW coverage: P8838.raw claimed once.

## Limitations

- Nothing in PRIDE text describes how P8838 was prepared (e.g. whether it is phospho-enriched, which cells or treatment); the paper full text could not be read, so only cell line, instrument and search settings are annotated.
- Cell line hTERT-RPE1 inferred from RPE1 name via Cellosaurus synonym; age 1Y and sex female are Cellosaurus values.
- Split from the nine apex runs because the deposited search settings differ (phospho, carbamidomethyl, MaxQuant 1.6.1.0 vs 1.4.0.5). Zip archives contain MaxQuant tables only; no raw file names were taken from search outputs other than those deposited as .raw.
- Dissociation method and precursor tolerance not available. Paper not cited as a source because its full text was not read.
