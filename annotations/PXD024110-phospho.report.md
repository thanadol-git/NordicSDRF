# PXD024110-phospho

Status: validated annotation; independent review pending.

PRIDE title: "Responder and non-responder proteomic and phosphoproteomic profiles to ATRA/Valproic acid before treatment". Department of Biomedicine / Department of Clinical Science, University of Bergen (lab PI Øystein Bruserud). Paper: Hernandez-Valladares M et al., Cancers 2021, PMID 33946813, PMC8125016 (open access; Methods read). Companion deposit with pre/post-treatment samples: PXD024197. Sibling: `PXD024110-proteome`.

- SDRF: `annotations/PXD024110-phospho.sdrf.tsv`, 55 rows × 39 columns
- SHA-256: `0df3e074d877a2c5bc15c7941045b1956c06859c891a2dae3f33f018d443b556`
- Evidence manifest: `annotations/PXD024110-phospho.evidence.json`; working files in `sdrf-skills/scratchpad/PXD024110/`

## Templates
`ms-proteomics` v1.1.0 + `human` v1.1.0 + `clinical-metadata` v1.1.0 + `oncology-metadata` v1.1.0 (primary AML cells from patients; super-SILAC spike-in).

## Design and file mapping
Pre-treatment peripheral-blood AML cells from patients enrolled in two ATRA/valproic acid studies (ATRA-VP-TP and ATRA-VP-AraC; paper). File names `AT<n>-pre_x1..3` / `VA<n>-pre_x1..3` (proteome, three high-pH fractions at 10%, 17.5% and 50% ACN; fraction identifiers 1-3) and `AT<n>_PRE[_AGAIN]` / `VA<n>_PRE[_AGAIN]` (IMAC phosphopeptide-enriched sample). Each sample was mixed with the AML super-SILAC mix (paper): written as two label rows per file, `SILAC light` = patient cells and `SILAC heavy` = super-SILAC standard (separate sources). 28 patients have proteome runs and 27 phospho runs. `P134.raw` is not described anywhere; it is annotated as an unassigned phospho-type run (no source information). **The patient codes `AT`/`VA` are kept verbatim; whether `AT` = ATRA-VP-TP and `VA` = ATRA-VP-AraC study is not stated, and the mapping from file codes to the paper's patient IDs (R1…, NR1…; Table 1 with sex, age, response) is not given, so each patient's response group, sex and age are `not available` here.** This is the main loss: the published responder vs non-responder factor cannot be assigned.

## Technical values
Q Exactive HF (PRIDE and paper; 195 min gradients for some fractions). Trypsin (FASP). Deposited mqpar.xml (proteome): fixed Carbamidomethyl C; variable Acetyl (protein N-term) and Oxidation M; first search 20 ppm, main search 4.5 ppm, 2 missed cleavages, multiplicity 2. Phospho file adds Phospho STY (the deposit includes Phospho (STY) Sites.txt). Fragment tolerance and dissociation not stated.

## Validation
`sdrf-tools build`: 55 rows × 39 columns; `parse_sdrf validate-sdrf … --use_ols_cache_only`: 0 errors (warnings only for free-text terms absent from the ontologies); `check --offline` CLEAN; `structure` OK; `reconcile`: all values agree with the record.

## Limitations
- Response group, sex, age, FAB class etc. `not available` for every patient (see above). Disease `acute myeloid leukemia`; cell type `leukemic blast` (primary AML cells; the preparation of the cells (density gradient, not purified) was not read in detail).
- `sampling time` `0 day` = before the start of treatment.
- `reconcile` reports Trypsin as unsupported by the PRIDE text; mqpar.xml lists Trypsin.
