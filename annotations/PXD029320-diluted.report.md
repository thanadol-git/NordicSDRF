# PXD029320-diluted

Status: validated annotation; independent review pending. PR not created.

- Multiplexed diluted standard (LSC / PROG / BLAST, 250 pg per channel) with 100- or 200-cell carrier, same acquisition methods
- SDRF: `annotations/PXD029320-diluted.sdrf.tsv`
- Rows: 390; columns: 47
- SHA-256: `5ab14d85e67a9fc286eb64bbb22bfc3645e10268f23498511a3eb770647d84b7`
- Evidence manifest: `annotations/PXD029320-diluted.evidence.json`
- Scope: 39 RAW files (36 in the 100x/200x series plus 3 April-2021 RETICLE close-out files), 16-plex TMTpro: 9 populated channels + TMT126 carrier, 6 channels empty (not emitted)
- Templates: ms-proteomics v1.1.0, human v1.1.0, single-cell v1.0.0 (PXD029320 deposits two distinct experiments, split into `PXD029320-scms` and `PXD029320-diluted`; no existing annotation found in sdrf-annotated-datasets, so this is new).

## Validation

- parse_sdrf validate-sdrf -t ms-proteomics -t human -t single-cell (online OLS): "Everything seems to be fine" (after fixing cell identifier charset in round 1).
- tools structure: OK. tools check: CLEAN (0 hallucinated). tools reconcile: all values agree with the record.
- RAW coverage: 39 files, each claimed exactly once by build.

## Design and provenance

- Channel map source: the paper's cited GitHub repository (bfurtwa/RETICLE), not PRIDE. PRIDE .pdStudy files list only the 16 TMTpro channels without sample names.
- Channel map from code/diluted_sample.ipynb: 127N BLAST1, 128N LSC1, 129N PROG1, 130C LSC2, 131N BLAST2, 131C PROG2, 132C BLAST3, 133N PROG3, 133C LSC3, 126 carrier; 127C, 128C, 129C, 130N, 132N, 134N empty. Carrier size (100 or 200 cell equivalents) from mapping.csv, stored in `characteristics[cells per well]` for carrier rows.
- 39 runs x 10 sources = 390 rows. Technical: as the scMS file plus Carbamidomethyl C fixed (paper: set for the diluted standard).
- Factors: `factor value[cell population]` and `factor value[acquisition strategy]`.

## Limitations and judgement calls

- The three April-2021 close-out files (`..._100c_2_2021041...`, `_maxpep10`, `_nocloseout`) are not in the repository mapping.csv; they are assumed to share the 100x layout (same TMTpro2 sample, 114 min gradient). The `_2_2021...` file carries no close-out label.
- Technical replicate is a global injection index 1..39 because each standard source is injected in every run.
- The standard channels are bulk-sorted peptide aliquots, so `cell identifier` is `not applicable`; the single-cell template was used to keep carrier-channel columns. `facs sorting mode` is `not available` for standard channels.
- Search parameters from PRIDE/paper prose, not from result files. Raw headers not checked.

