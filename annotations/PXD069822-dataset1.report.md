# PXD069822-dataset1

Status: validated annotation; independent review pending.

- Dataset: PXD069822, Oslo University Hospital (NordicSDRF). "Intrinsic errors in mitochondrial translation trigger a decline in cell fitness". Sub-experiment dataset1: MEFs, DDA (dda-PASEF), MaxQuant 2.4.7.0.
- SDRF: `annotations/PXD069822-dataset1.sdrf.tsv`; rows: 16; columns: 33; SHA-256 `73084bf932941ac053e5ef99c443595ebb9dd85d85ab67ac73174d339d2b69ae`
- Evidence manifest: `annotations/PXD069822-dataset1.evidence.json`
- Scope: the project has three distinct experiments (dataset1 MEF DDA, dataset2 MEF DIA, dataset3 BMDM DIA) with different cells, acquisition and search software, so three SDRFs (PXD069822-dataset1/2/3) were written.
- Groups: WT untreated x5 (WT1-5; WT2 injected twice -> 2 technical replicates), PolgD257A no CA x5 (CA-1..5), PolgD257A + CA x5 (CA+1..5)
- Templates: ms-proteomics, vertebrates, sample-metadata (v1.1.0/v1.1.0/v1.0.0). sample-metadata supplies characteristics[treatment]; characteristics[genotype] is an extra column outside these templates (free text, accepted by the validator). Factors: genotype, treatment (chloramphenicol vs not applicable).
- Step 0.5: no directory for PXD069822 in sdrf-annotated-datasets (new annotation).

## Validation

- parse_sdrf validate-sdrf (--use_ols_cache_only for the DIA files): no errors.
- tools structure: OK. tools check: CLEAN.
- RAW coverage: 16 of 16 .d folders in LC-MS_files_dataset1.zip, each once.

## Limitations
- Genotype of the CA-/CA+ runs (PolgD257A) and of WT1-5 (wild type, no chloramphenicol) is inferred from file names plus the PRIDE protocol (dataset1 = Polg wt or PolgD257A +/- CA); no deposited sample table maps names to genotype.
- WT2_Slot2-24_1_1345.d and WT2_Slot2-24_1_1351.d share a name; treated as two injections (technical replicates 1 and 2) of one sample. The mqpar lists both under separate experiment names.
- The protocol lists carbamyl (N-term) as a variable modification but mqpar_dataset1.xml (authoritative) has only Carbamidomethyl (C) fixed, Oxidation (M) and Acetyl (Protein N-term) variable; the SDRF follows mqpar.
- Fragment tolerance not stated for MaxQuant TOF search (not available).
- Publication: PRIDE lists no DOI/PMID/references; no paper was read. All claims come from the PRIDE record, the zip central directories, and the deposited search logs/mqpar.
- Dose of chloramphenicol: protocol gives "124M" (unclear unit), so no dose column.
- Disease, sex, strain and developmental stage are not available. Dissociation method and fragment tolerance not available.
- Trypsin/P (MS:1001313) used: mqpar says Trypsin/P and the protocol says "Trypsin without proline restriction". `tools reconcile` flags this against the record word "trypsin" (BLOCKER/MAJOR on dataset1); judged a false positive of the keyword match.
- Raw data are zip archives of Bruker .d folders (45-186 GB); only zip central directories were range-read. Data-file names are the .d folder names inside the zips.
