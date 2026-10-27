# PXD043021-mrmhr

Status: validated annotation; independent review pending.

Same deposit as `PXD043021-swath`. Targeted MRM-HR validation of six samples: three control (C1-C3) and three butanol-treated (T1-T3) cultures (PRIDE protocol).

- SDRF: `annotations/PXD043021-mrmhr.sdrf.tsv`, 6 rows × 29 columns
- SHA-256: `f31cfc558cbf2a9c16a8d235f1c179df51772120296413cae0059f1bbf96a5e6`
- Evidence manifest: `annotations/PXD043021-mrmhr.evidence.json`

Files `MRMHR_2ug_<Control_C|Butanol_T><1-3>.wiff`, one per sample. Acquisition method is written as Parallel reaction monitoring (PRIDE:0000629): MRM-HR is a TripleTOF targeted product-ion scan method (paper Fig. 7 / Table S8) with no exact PRIDE term, so PRM is the closest descendant of PRIDE:0000659 - **a judgement call for the reviewer**. The relation between the six MRM-HR cultures and the 12 SWATH samples (new cultures or aliquots) is not stated, so they are separate sources. Same instrument, enzyme assumption, MMTS modification and caveats as the SWATH file. Validation: `parse_sdrf` 0 errors (3 text warnings), `check` CLEAN, `structure` OK; `reconcile` Trypsin BLOCKER as above.
