# PXD029320-scms

Status: validated annotation; independent review pending. PR not created.

- Single-cell proteomics of OCI-AML8227 (LSC / PROG / BLAST), Orbitrap Eclipse + FAIMS, MS2 vs RTS-MS3 vs RETICLE at 500/750 ms
- SDRF: `annotations/PXD029320-scms.sdrf.tsv`
- Rows: 870; columns: 46
- SHA-256: `9b1a330d2bc764f671e9ef8c4e7d8f18e9cbb4f85c0154051aea4695d5a72bea`
- Evidence manifest: `annotations/PXD029320-scms.evidence.json`
- Scope: 58 June-2021 RAW files (6 methods x 9-10 runs), 16-plex TMTpro: 14 sorted single cells + TMT126 carrier per run, TMT127C unused (not emitted)
- Templates: ms-proteomics v1.1.0, human v1.1.0, single-cell v1.0.0 (PXD029320 deposits two distinct experiments, split into `PXD029320-scms` and `PXD029320-diluted`; no existing annotation found in sdrf-annotated-datasets, so this is new).

## Validation

- parse_sdrf validate-sdrf -t ms-proteomics -t human -t single-cell (online OLS): "Everything seems to be fine" (after fixing cell identifier charset in round 1).
- tools structure: OK. tools check: CLEAN (0 hallucinated). tools reconcile: all values agree with the record.
- RAW coverage: 58 files, each claimed exactly once by build.

## Design and provenance

- Channel map source: the paper's cited GitHub repository (bfurtwa/RETICLE), not PRIDE. PRIDE .pdStudy files list only the 16 TMTpro channels without sample names.
- Per run: file -> plate/sample (file_sample_mapping.txt); wells of that sample (sample_layout.txt); channel per well (balanced_channels_N.txt); gate per well (sort_layout.txt). 58 runs x (14 cells + carrier) = 870 rows; 812 single-cell sources plus one carrier source.
- Factors: `factor value[cell population]` (LSC = CD34+CD38-, PROG = CD34+CD38+, BLAST = CD34-, carrier) and `factor value[acquisition strategy]`, which is the compared technical variable of the paper.
- Technical: Orbitrap Eclipse, trypsin, DDA, TMTpro fixed on K and any N-term, Oxidation M, Acetyl and Met-loss protein N-term variable, 10 ppm; fragment tolerance 0.02 Da (MS2, RETICLE) or 0.6 Da (RTS-MS3); HCD 32% NCE (MS2, RETICLE), 45% NCE for the RTS-MS3 quant scan.

## Limitations and judgement calls

- Cell sources are named `<method>_P<plate>_<well>` and treated as distinct per method (a lysate is injected once); the repository facs_data files are byte-identical across methods, so whether physically separate plates were sorted per method is not stated.
- `characteristics[cell type]` is `not available`: LSC/PROG/BLAST are author gates with no exact CL term; the population is in the custom column `characteristics[cell population]` plus `enrichment marker`.
- organism part, age, sex, individual, ancestry: `not available` (patient-derived culture, no donor data in the deposit).
- The carrier is one pooled source; its technical replicate is the injection index 1..58 only to keep rows unique.
- Only the quantification scan dissociation is recorded; CID 30% LIT scans (RTS) are omitted since the column is single-valued.
- Search parameters come from PRIDE/paper prose; the 1-2 GB .msf/.pdResult files were not opened. Raw file headers not checked.
- One RETICLE_750 file is named `..._10_faulty.raw`; it is in the repository mapping, annotated like the rest.
- The custom columns `characteristics[cell population]` and factor `acquisition strategy` are not template columns; the validator accepted them.

