# PXD069822-dataset2

Status: validated annotation; independent review pending.

- Dataset: PXD069822, Oslo University Hospital (NordicSDRF). "Intrinsic errors in mitochondrial translation trigger a decline in cell fitness". Sub-experiment dataset2: WT MEFs +/- CA, DIA (dia-PASEF folders contain diaSettings), DIA-NN 2.3.2 library-free.
- SDRF: `annotations/PXD069822-dataset2.sdrf.tsv`; rows: 10; columns: 36; SHA-256 `aead2f2bca170e7cfec5725f29725b34bc858ae8a389bd55d873b3d3e8813842`
- Evidence manifest: `annotations/PXD069822-dataset2.evidence.json`
- Scope: the project has three distinct experiments (dataset1 MEF DDA, dataset2 MEF DIA, dataset3 BMDM DIA) with different cells, acquisition and search software, so three SDRFs (PXD069822-dataset1/2/3) were written.
- Groups: WT MEF -CA x5, WT MEF +CA x5
- Templates: ms-proteomics, vertebrates, sample-metadata, dia-acquisition (v1.1.0/v1.1.0/v1.0.0/v1.1.0). sample-metadata supplies characteristics[treatment]; characteristics[genotype] is an extra column outside these templates (free text, accepted by the validator). Factors: genotype, treatment (chloramphenicol vs not applicable).
- Step 0.5: no directory for PXD069822 in sdrf-annotated-datasets (new annotation).

## Validation

- parse_sdrf validate-sdrf (--use_ols_cache_only for the DIA files): no errors.
- tools structure: OK. tools check: CLEAN.
- RAW coverage: 10 of 10 .d folders in LC-MS_dataset2.zip, each once.

## Limitations
- DIA window/isolation columns are not available (not read from the raw method files).
- Protocol says DIA-NN version 1.9.2 and 2.3.0; the dataset2 log is DIA-NN 2.3.2.
- Acquisition method written as the bare literal Data-independent acquisition because the dia-acquisition template validator rejects the NT=;AC= form (same workaround as other annotations in this repo).
- Publication: PRIDE lists no DOI/PMID/references; no paper was read. All claims come from the PRIDE record, the zip central directories, and the deposited search logs/mqpar.
- Dose of chloramphenicol: protocol gives "124M" (unclear unit), so no dose column.
- Disease, sex, strain and developmental stage are not available. Dissociation method and fragment tolerance not available.
- Trypsin/P (MS:1001313) used: mqpar says Trypsin/P and the protocol says "Trypsin without proline restriction". `tools reconcile` flags this against the record word "trypsin" (BLOCKER/MAJOR on dataset1); judged a false positive of the keyword match.
- Raw data are zip archives of Bruker .d folders (45-186 GB); only zip central directories were range-read. Data-file names are the .d folder names inside the zips.
