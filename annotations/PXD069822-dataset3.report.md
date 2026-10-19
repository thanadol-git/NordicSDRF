# PXD069822-dataset3

Status: validated annotation; independent review pending.

- Dataset: PXD069822, Oslo University Hospital (NordicSDRF). "Intrinsic errors in mitochondrial translation trigger a decline in cell fitness". Sub-experiment dataset3: Bone marrow-derived macrophages, DIA, DIA-NN 1.9.2 library-free.
- SDRF: `annotations/PXD069822-dataset3.sdrf.tsv`; rows: 14; columns: 36; SHA-256 `7025d5a0c0c49e9277c41ebe85bba8ae7bd8660831f92bf7b84930832f69b770`
- Evidence manifest: `annotations/PXD069822-dataset3.evidence.json`
- Scope: the project has three distinct experiments (dataset1 MEF DDA, dataset2 MEF DIA, dataset3 BMDM DIA) with different cells, acquisition and search software, so three SDRFs (PXD069822-dataset1/2/3) were written.
- Groups: WT BMDM x5 (untreated), PolgD257A BMDM no CA x5, PolgD257A BMDM + CA x4 (CA2-5; no CA1 file deposited)
- Templates: ms-proteomics, vertebrates, sample-metadata, dia-acquisition (v1.1.0/v1.1.0/v1.0.0/v1.1.0). sample-metadata supplies characteristics[treatment]; characteristics[genotype] is an extra column outside these templates (free text, accepted by the validator). Factors: genotype, treatment (chloramphenicol vs not applicable).
- Step 0.5: no directory for PXD069822 in sdrf-annotated-datasets (new annotation).

## Validation

- parse_sdrf validate-sdrf (--use_ols_cache_only for the DIA files): no errors.
- tools structure: OK. tools check: CLEAN.
- RAW coverage: 14 of 14 .d folders in LC-MS_files_dataset3.zip, each once.

## Limitations
- Precursor tolerance is not available: the PRIDE protocol says 15 ppm for datasets 2 and 3 but the dataset3 DIA-NN log shows automatic mass-accuracy optimisation (about 12-13 ppm).
- "MUT" is read as PolgD257A homozygous from the protocol; "10wk" in file names suggests 10-week-old animals but no age/sex/strain is stated, so these stay not available.
- DIA window/isolation columns not available.
- Acquisition method written as bare literal (see dataset2).
- Publication: PRIDE lists no DOI/PMID/references; no paper was read. All claims come from the PRIDE record, the zip central directories, and the deposited search logs/mqpar.
- Dose of chloramphenicol: protocol gives "124M" (unclear unit), so no dose column.
- Disease, sex, strain and developmental stage are not available. Dissociation method and fragment tolerance not available.
- Trypsin/P (MS:1001313) used: mqpar says Trypsin/P and the protocol says "Trypsin without proline restriction". `tools reconcile` flags this against the record word "trypsin" (BLOCKER/MAJOR on dataset1); judged a false positive of the keyword match.
- Raw data are zip archives of Bruker .d folders (45-186 GB); only zip central directories were range-read. Data-file names are the .d folder names inside the zips.
