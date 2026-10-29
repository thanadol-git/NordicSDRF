# PXD018034-lumos-dia

Status: validated annotation; independent review pending.

PRIDE title: "Maturation kinetics of a multiprotein complex revealed by metabolic labeling". Department of Biological Sciences, University of Bergen (lab PI Evgeny Onischenko). Paper: Onischenko E et al., Cell 2020 (PMID 33333025; closed access, not read).

- SDRF: `annotations/PXD018034-lumos-dia.sdrf.tsv`, 257 rows x 33 columns
- SHA-256: `695ddbc8552ab9c5ffc57372776a3c3c9b9af52554674f613c4b62e220a51aba`
- Evidence manifest: `annotations/PXD018034-lumos-dia.evidence.json`; working files in `sdrf-skills/scratchpad/PXD018034/`
- Sibling SDRFs from the same deposit (split by instrument and acquisition mode): `PXD018034-qe-dia`, `PXD018034-lumos-dia`, `PXD018034-lumos-dda`, `PXD018034-lumos-prm`.

## Design and file mapping (deposited table)
The deposit contains `SampleAnnotation.xlsx` mapping every one of the 190 RAW files to instrument (QE / Lumos), mode (DIA / DDA / PRM), bait, time point, replicate and condition; all 190 are used across the four SDRFs. Yeast (Saccharomyces cerevisiae) nucleoporins (MLP1, NSP1, NUP1, NUP57, NUP82, NUP84, NUP85, NUP133, NUP159, NUP188) carried a ZZ tag; cells were shifted from light to heavy lysine medium and the tagged complexes were pulled down at 0/30/60/90 (MLP1 also 120/150) min, SDS-PAGE, in-gel trypsin digestion (PRIDE protocol). Each time-course DIA file contains a light (pre-existing) and a heavy (newly synthesised) channel: written as two rows per file (`SILAC light`/`SILAC heavy`) with separate sources `<bait>_<t>_r<n>_light/_heavy`; files that contain only light material (zero-time controls, mock ZZ bait, light-only mixing controls) have an empty-source heavy row. Factor: `factor value[sampling time]` (minutes after the shift).

## Technical values and limitations
Trypsin (PRIDE protocol). Instrument: the PRIDE protocol names Q Exactive Plus **or** Orbitrap Lumos; the sheet assigns QE or Lumos per file (written as Q Exactive Plus MS:1002634 / Orbitrap Fusion Lumos MS:1002732; the Lumos reading is the PRIDE dropdown "Orbitrap Fusion Lumos"; reconcile's `instrument_contradicted` finding on the Lumos files is a false positive caused by the protocol naming both). Search modifications are not stated in the PRIDE text and the Comet/Mascot/iProphet parameters were not read: `not available` (the heavy lysine isotope form is also not stated, so no label modification is written). Dissociation, tolerances and DIA window scheme not stated: `not available`. Strain, growth conditions, tag details and the SDS-PAGE excision are not recorded. Disease/organism part/cell type `not applicable`. `characteristics[enrichment process]` is free text (`ZZ-tag affinity pulldown of <bait>, in-gel digest`).
**Sheet vs file names:** for NSP1 the sheet assigns file `…_32_NSP1_t90_r2` to t60 replicate 3 and `…_35_NSP1_t60_r3` to t90 replicate 2, contradicting the file names; the deposited sheet is followed.
Validation: `build` OK; `parse_sdrf validate-sdrf … --use_ols_cache_only` 0 errors (warnings only on free-text treatment/enrichment terms); `check --offline` CLEAN; `structure` OK.

## This file
Lumos DIA: 10-bait ZZ time courses (t0/30/60/90, three replicates; 120 files), 13 MLP1 control pulldowns and 4 mock ZZ-bait pulldowns (`190813_..._Mlp1Pro_S-TEV-ZZ_1-4`, zero time point).
