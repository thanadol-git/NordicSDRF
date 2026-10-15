# PXD009302-apex

Status: validated local annotation; independent review pending. PR not created.

- PXD009302 - APEX2-FGF1 proximity labeling in RPE1 cells (Zhen et al. 2018) - apex runs
- SDRF: `annotations/PXD009302-apex.sdrf.tsv`
- Rows: 9; columns: 34
- SHA-256: `81b370a7845dbdf6311d38b3c3069de784dcece3c8baa9fa291f1a588cef79f8`
- Evidence manifest: `annotations/PXD009302-apex.evidence.json`
- Scope: Nine label-free runs P1408-P1418 (S1-S3 x 3).

## Validation

- parse_sdrf validate-sdrf with ms-proteomics, human, cell-lines (--use_ols_cache_only): 'Everything seems to be fine.'
- tools structure: OK
- tools check: 10 terms verified, 0 hallucinated, CLEAN
- RAW coverage: 9 of 9 apex raw files claimed once; P8838.raw in the shotgun SDRF; 10 of 10 deposited raw files covered in total.

## Limitations

- Biological meaning of sample groups S1, S2, S3 (e.g. APEX2-FGF1 vs FGF1 control, plus/minus heparin, time) is not given in PRIDE text or any deposited file; the paper full text could not be read (no open full text in Europe PMC). Therefore no treatment/factor columns were added and no factor value exists.
- Biological replicate numbers 1-3 follow the suffix of MaxQuant experiment names and are an assumption.
- P8838.raw (MaxQuant 1.6.1.0, fixed Carbamidomethyl, phospho search, acquired 2017) is annotated in the separate PXD009302-shotgun SDRF because its deposited search settings differ from those of P1408-P1418 (MaxQuant 1.4.0.5, 2015). The two zip archives contain MaxQuant tables only, no raw files; listings were made from the zip central directories and file names claimed are the ones deposited as .raw in PRIDE.
- Cell line identity hTERT-RPE1 is inferred from the 'RPE1' name via the Cellosaurus synonym; age 1Y and sex female are Cellosaurus values, not from the deposit. PRIDE also mentions U2OS-FGFR4 cells in the protocol, but none of the deposited runs could be assigned to U2OS-FGFR4.
- Tolerance conflict: protocol says MS/MS 6 ppm, deposited parameters.txt says 20 ppm (20 ppm used). Protocol prose says MaxQuant 1.4.0.8, parameters.txt says 1.4.0.5.
- Dissociation method, organism part, cell type, disease not available. Mass spectrometer is a Q Exactive Plus per RAW headers, whereas PRIDE lists Q Exactive.
- The deposited PXD009302_community_annotated.sdrf.tsv exists (all-not-available sample info, Q Exactive, no cell line); it was consulted but not reused.
- Paper not cited as a source because its full text was not read.
