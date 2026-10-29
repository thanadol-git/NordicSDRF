# PXD024197-proteome

Status: validated annotation; independent review pending.

PRIDE title: "Pre and post ATRA/VP treatment proteomic and phophoproteomic profiling of AML responders and non-responders". University of Bergen (lab PI Øystein Bruserud). Paper: Hernandez-Valladares M et al., Cancers 2021, PMID 33946813, PMC8125016 (open access). Companion deposit PXD024110 (pre-treatment samples of the same patients). Sibling: `PXD024197-phospho`.

- SDRF: `annotations/PXD024197-proteome.sdrf.tsv`, 180 rows × 36 columns
- SHA-256: `870560f2b364f9f1a77a36d4590e1b9afead462fd4f73256bf2588cd367ac6bc`
- Evidence manifest: `annotations/PXD024197-proteome.evidence.json`; working files in `sdrf-skills/scratchpad/PXD024197/`

## Templates
`ms-proteomics` v1.1.0 + `human` v1.1.0 + `clinical-metadata` v1.1.0 + `oncology-metadata` v1.1.0 (primary AML cells, super-SILAC spike-in).

## Design and file mapping
Serial samples of AML patients in the ATRA-VP-TP study (`AT<n>` codes): pre-treatment (`pre`/`PRE`), `T1` and `T2`. The paper collects samples at day 3 (3D) and day 8 (8D) of that study; **T1 = day 3 and T2 = day 8 is inferred from the file codes and the paper text** (no table links the codes). Proteome files `AT<n>-<pre|T1|T2>_x1..3` = three high-pH fractions (fraction identifiers 1-3; `AT14-T1_x1_re` and `AT7-T2_X2_re` are the only files for their fractions) and phospho files `AT<n>_<PRE|T1|T2>[_AGAIN]` (IMAC). Super-SILAC: two label rows per file (`SILAC light` patient cells, `SILAC heavy` super-SILAC standard) as separate sources. 120 RAW files: 90 proteome fractions, 29 phospho, and `P134.raw` (undescribed, not annotated here; it also exists in PXD024110). The 40 `pre` files are byte-identical (same checksums) to those of PXD024110 and are annotated here too. Factor: `factor value[sampling time]` (0/3/8 day).
**Patient response group, sex and age are `not available`: the file codes are not mapped to the paper's patient IDs (R1…/NR1…).**

## Technical values
Q Exactive HF; trypsin (FASP); deposited mqpar.xml/Phospho (STY) Sites.txt: fixed Carbamidomethyl C, variable protein N-term Acetyl and Oxidation M (phospho adds Phospho STY); first search 20 ppm, main search 4.5 ppm. Fragment tolerance and dissociation not stated.

## Validation
`sdrf-tools build`: 180 rows × 36 columns; `parse_sdrf validate-sdrf … --use_ols_cache_only`: 0 errors (warnings only for free-text terms absent from the ontologies); `check --offline` CLEAN; `structure` OK; `reconcile`: all values agree with the record.

## Limitations
- Response group/sex/age/study details not assignable per patient (see above). The ATRA-VP-AraC patients (`VA` codes) appear only in PXD024110.
- `reconcile` reports Trypsin as unsupported by the PRIDE text; mqpar.xml lists Trypsin.
- Disease `acute myeloid leukemia`; cell type `leukemic blast`.
