# PXD002318-labelfree

Status: validated annotation; independent review pending.

PRIDE title: "Multiple sclerosis resaerch: EAE and cuprizone mouse brain TMT and label-free proteomics" (sic). Proteomics Unit at the University of Bergen (PROBE), Bergen, Norway (lab PI Frode S. Berven; submitter Eystein Oveland). Paper: Oveland E et al., "Cuprizone and EAE mouse frontal cortex proteomics revealed proteins altered in multiple sclerosis", Sci Rep 2021 11(1):7174, DOI 10.1038/s41598-021-86191-5, PMID 33785790, PMC8010076.

- SDRF: `annotations/PXD002318-labelfree.sdrf.tsv`, 34 rows × 37 columns, 34 sources (individual mice), 34 RAW files
- SHA-256: `dbb1d1a14e8fe9a6163e337e52876982219c46ba99742f82978bc4855f7f3246`
- Companion SDRF (same deposit, TMT sub-experiment): `annotations/PXD002318-tmt.sdrf.tsv`
- Evidence manifest: `annotations/PXD002318-labelfree.evidence.json`; working files in `sdrf-skills/scratchpad/PXD002318/`

## Templates

`ms-proteomics` v1.1.0 (MS proteomics, DDA on an LTQ-Orbitrap Velos Pro) + `vertebrates` v1.1.0 (Mus musculus). No `dia-acquisition` (DDA per Supplementary Methods), no `cell-lines` (tissue), and no `clinical-metadata` (mouse models).

## Why the deposit is split into two SDRFs

The deposit holds a TMT sub-experiment (5 condition pools, fractionated, PD/SEQUEST/MS Amanda, TMT6plex fixed modifications, 0.05 Da fragment tolerance, CID+HCD) and a label-free sub-experiment (individual mice, unfractionated, Progenesis + SearchGUI/X!Tandem, 0.7 fragment tolerance, CID only). Their modifications, tolerances and labels differ, so each gets its own SDRF.

## Design and file mapping

- Mice: female C57BL/6, frontal cortex of the right hemisphere. Each mouse lysate was digested and run once (2.5 µg, 220 min run, 50 cm column), so there is one RAW file per mouse, all unfractionated.
- The RAW file name is the animal's random code, and it is used as `source name`. The group of each code comes from the deposited `Sampleoverviewlabel-freeandTMT.xlsx` (sheet "Label-free"), repeated in the paper's Supplementary Data 2 (`41598_2021_86191_MOESM5_ESM.xlsx`). Both the "Label free raw data files" sheet and the abundance-column headers of the "Label-free data" sheet list the same codes under the same groups.
- `characteristics[biological replicate]` is the animal's index within its group, as in the sheet's "Individual samples" column (e.g. CTR42d_3 → 3).

| group | animals (RAW file stems) | n | disease | sampling time |
|---|---|---|---|---|
| CTR-CPZ | CPZ_C1_ctr, C3, C4, C5, C6 | 5 | normal | 42 day |
| CTR-EAE | EAE_A1_ctr, C1, D1, E1, F1, B1 | 6 | normal | not available |
| CPZ-42d | CPZ_A4, A5, B4, B5, B6 | 5 | demyelinating disease | 42 day |
| EAE-16d | EAE_A3, B3, C3, D3, E3, F3 | 6 | experimental autoimmune encephalomyelitis | 16 day |
| EAE-32d | EAE_A2, A4, B2, B4, C2, C4, D2, D4, E2, E4, F2, F4 | 12 | experimental autoimmune encephalomyelitis | 32 day |

- Rows: 34, one per RAW file. Every label-free RAW file in the PRIDE file list (102 files over 2 API pages) is claimed exactly once. The other 63 RAW files are the TMT sub-experiment.
- Factors: `factor value[disease]` and `factor value[sampling time]`. Together they separate the five groups.

## Technical values

- Instrument: Orbitrap Velos Pro (MS:1003096), from "LTQ-Orbitrap Velos Pro" in the Methods. The PRIDE dropdown says LTQ Orbitrap Velos.
- Acquisition: DDA, top 7. Dissociation: CID (MS:1000133) at NCE 40% (`40% NCE`), fragments read in the linear ion trap (MS:1000291). MS1 300–2000 m/z in the Orbitrap. All from the Supplementary Methods, "Orbitrap LC-MS of label-free samples".
- Digestion: Trypsin (porcine, Promega), reduction with DTT, alkylation with iodoacetamide (Supplementary Methods, "Protein digestion and peptide clean-up").
- Search, from the PRIDE data-processing protocol and Supplementary Methods (SearchGUI v1.8.9 / X!Tandem, PeptideShaker v0.17.3): Carbamidomethyl (C) fixed, Oxidation (M) variable, precursor 10 ppm, fragment 0.7. No search parameter file was deposited; the label-free xlsx files are Progenesis exports.

## Validation

- `sdrf-tools build ... -t ms-proteomics -t vertebrates`: wrote 34 rows × 37 columns.
- `sdrf-tools reconcile --record pride.json --accession PXD002318`: 1 finding, `BLOCKER labelled_annotated_as_label_free (comment[label])`, triggered because the record also registers TMT as a quantification method. **This finding is a false positive for this file.** The project registers both "MS1 intensity based label-free quantification" and "TMT". The TMT runs are annotated with TMT channels in `PXD002318-tmt.sdrf.tsv` (where reconcile reports no disagreement). The 34 runs here are individual-mouse label-free runs according to the deposited sample sheet, Supplementary Data 2 and the Methods.
- `sdrf-tools structure`: OK. `sdrf-tools check --offline`: CLEAN (9 terms checked, 0 hallucinated, 0 UNIMOD swaps).
- `timeout 900 parse_sdrf validate-sdrf -s PXD002318-labelfree.sdrf.tsv -t ms-proteomics -t vertebrates --use_ols_cache_only`: exit 0, **0 errors**, 1 warning: `Term: C57BL/6 in column 'characteristics[strain or breed]', is not found in the given ontology list ncbitaxon`. Strain is free text in the contract.
- One validation round only; no fixes were needed.

## Limitations

- **CTR-EAE count and timepoint.** The paper's label-free Methods say CTR-EAE N = 5, and the main Methods say EAE controls (N = 5) were sacrificed at p.i. day 32. But 6 `EAE_*1_ctr` RAW files are deposited, and the deposited sheet and Supplementary Data 2 list all 6 (CTR36d_1–6, "CTR for EAE, 36 days"), with abundance columns for all 6. All 6 are annotated. `sampling time` is `not available` for them because day 32 and day 36 conflict.
- **Sampling time reference differs by model.** CPZ and CTR-CPZ count days on diet (6 weeks = 42 days); EAE counts days post-immunisation.
- **Disease for cuprizone mice.** `demyelinating disease` (MONDO:0002562) is used. Cuprizone-induced demyelination was confirmed histologically (Supplementary Fig. 1), and no more specific ontology term exists. Cuprizone is not in NCIT/EFO, so no `characteristics[treatment]` column is written. The PRIDE dropdown disease "multiple sclerosis" was not used: these are mouse models.
- **Developmental stage `adult`** is inferred from "eight-week-old female mice" (CPZ and EAE induction; the CPZ controls came from the same randomised group). The EAE controls' age is not stated; they are assumed to belong to the same cohort.
- **Fragment tolerance unit.** The Methods give "fragment mass tolerance of 0.7" without a unit. `0.7 Da` is written because the fragments were read in the linear ion trap and X!Tandem fragment tolerances are set in Da.
- **Group labels from file names are not used alone.** The `_ctr` suffix and the CPZ_/EAE_ prefix separate controls from treated animals. The EAE-16d vs EAE-32d split (row 3 vs rows 2/4 of each cage letter) comes only from the deposited sheet and Supplementary Data 2, which agree.
- Raw files were not opened (no techsdrf run). Instrument, acquisition and tolerances come from the Methods.
