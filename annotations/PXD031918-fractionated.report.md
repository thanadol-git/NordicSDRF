# PXD031918-fractionated

Status: validated annotation; independent review pending.

PRIDE title: "Comparison of in-solution and SP3 sample processing workflows on HeLa cell samples". Department of Biomedicine, University of Bergen (lab PI Maria Hernandez-Valladares / Frode Berven). Paper: Neset L et al., Molecules 2022, PMID 35684327, PMC9181984 (open access; Methods read; the human plasma part of the paper is not in this deposit). Sibling: `PXD031918-unfract`.

- SDRF: `annotations/PXD031918-fractionated.sdrf.tsv`, 30 rows × 37 columns
- SHA-256: `641680e9163ebae8623167b8ed57ad0d6f6dc0946504a92b03417f5b541d879f`
- Evidence manifest: `annotations/PXD031918-fractionated.evidence.json`; working files in `sdrf-skills/scratchpad/PXD031918/`

## Templates
`ms-proteomics` v1.1.0 + `human` v1.1.0 + `cell-lines` v1.1.0 (HeLa, label-free DDA, Orbitrap Eclipse with FAIMS).

## Design and file mapping
Three sample-processing workflows on HeLa cells, read from the file names: `IsD_Gua` (in-solution digestion, guanidine hydrochloride lysis), `SP3_Gua` (SP3, guanidine hydrochloride lysis) and `SP3_SDS` (SP3, SDS lysis, "extrawash" = two extra 80% ethanol washes, paper). Dates in names (`291021`, `251121`, `221121`, `091221`) are used as `comment[sample preparation batch]`; they are assumed to be preparation/acquisition days. Factor: `factor value[treatment]` = workflow. The mapping of replicates is **inferred from file names** (no sample sheet; PD `.msf` files not opened).

Fractionated runs (30 RAW, high-pH reversed-phase fractionation): for each workflow and each of two replicates (batches `221121` and `091221`) five fraction files (`…_A5-A9`, `…_B2-B6[_REP]`, `…_C9…D12`, `…_D1…E3`, `…_B51…B91`). The letters/numbers are plate positions; **fraction identifiers 1-5 are assigned by order of the position, not stated**. 6 sources x 5 files.

## Technical values
Orbitrap Eclipse + FAIMS Pro (CVs -45/-65/-80 V), MS1 375-1500 m/z, HCD NCE 30, isolation 4 m/z (paper Methods, 180 or 120 min gradients). Trypsin (paper). Proteome Discoverer 2.5 Sequest HT with default settings (modifications and tolerances not stated: `not available`). Only five fractions per replicate are deposited.

## Validation
`sdrf-tools build`: 30 rows × 37 columns; `parse_sdrf validate-sdrf … --use_ols_cache_only`: 0 errors (warnings only for free-text terms absent from the ontologies); `check --offline` CLEAN; `structure` OK; `reconcile`: all values agree with the record.

## Limitations
- Cell line HeLa written as parental HeLa CVCL_0030 (variant not stated); age/sex/disease from Cellosaurus.
- Replicate identities are inferred from names; batches differ between the unfractionated sets and the fractionated sets.
