# PXD004245-HeLa
Status: validated annotation; independent review pending.

**Dataset:** PXD004245, "ADP-ribosylation site analysis". Submitted by Michael Lund Nielsen, Novo Nordisk Foundation Center for Protein Research, University of Copenhagen, Copenhagen, Denmark. Paper: Martello R, Leutert M, Jungmichel S, *et al.*, "Proteome-wide identification of the endogenous ADP-ribosylome of mammalian cells and tissue", Nat Commun 2016;7:12917 (PMID 27686526, PMC5056437, doi:10.1038/ncomms12917).

The deposit holds two organisms that were searched separately, so it is split into two SDRFs. This file covers the 12 HeLa RAW files, which are all in the one deposited MaxQuant search (human FASTA). The 3 mouse liver RAW files are in `PXD004245-mouse-liver.sdrf.tsv`.

- **SDRF:** `annotations/PXD004245-HeLa.sdrf.tsv`
- **Size:** 21 data rows × 51 columns
- **SHA-256:** `698fcf18c2fc7230f879f2ce7e46a2e84097fcc009ec787595fa1b814b0e51fb`
- **Templates:** `ms-proteomics` v1.1.0, `human` v1.1.0, `cell-lines` v1.1.0. MS proteomics, human samples, all from the HeLa cell line. The acquisition is DDA (data-dependent), so `dia-acquisition` does not apply. These are cultured cells, not patients, so the clinical templates do not apply.

## Design and file mapping

There are four sub-experiments, all using HeLa cells and Af1521 macrodomain enrichment of ADP-ribosylated peptides after Lys-C/trypsin digestion and PARG treatment:

| Sub-experiment | RAW files | Label | Rows |
|---|---|---|---|
| Replicate enrichments, H2O2-treated HeLa | `..._Hela_PAR_PD_Rep1/2/3.raw` | label-free | 3 |
| SILAC H2O2 time course (0, 5, 10, 30, 60, 120 min) | `..._500uMH2O2_{0_min,5_min,10_min,30_min,1_h,2_h}.raw` | SILAC light + heavy | 12 |
| SILAC olaparib (1 µM, 10 µM) | `..._HeLaSILAC_Ola_{1uM,10uM}_104ms.raw` | SILAC light + heavy | 4 |
| SILAC occupancy (stoichiometry) | `..._HELA_SILAC_H2O2_occupancy.raw` | SILAC light + heavy | 2 |

**SILAC channels.** The deposited MaxQuant `peptides.txt` header has only `Intensity L` / `Intensity H` and `Ratio H/L` columns for the SILAC experiments, so these are duplex runs. The `PAR_PD Rep1–3` experiments have no L/H columns, so they are label-free. A sample of `msms.txt`, read by HTTP range requests at six offsets, shows the heavy-state peptides shifted by +8.014 Da per lysine and +10.008 Da per arginine. That makes heavy Lys8/Arg10 (`Label:13C(6)15N(2)` K, `Label:13C(6)15N(4)` R), which matches Supplementary Fig. 4a, "Heavy (K8, R10)". Channel conditions come from the paper:
- **Time course** (main text and Supplementary Fig. 4a): the light cells got 500 µM H2O2 for about 0 min (a few seconds) in every run. The heavy cells got 500 µM H2O2 for the time point in the file name.
- **Olaparib** (main text: "In two SILAC experiments, both light and heavy SILAC cells were treated with H2O2, while only light SILAC cells were treated with olaparib (1 μM or 10 μM)"): both light and heavy cells got H2O2. Only the light cells got olaparib (1 µM or 10 µM, per the file name).
- **Occupancy** (Supplementary Fig. 4d/e legend): the heavy cells were H2O2-treated for 10 min and the light cells were untreated.

**Replicate files were renamed on deposit.** The original acquisition paths in the RAW headers show the swap:
- Deposited `Rep1.raw` was acquired as `..._PAR_PD_2xSep-pak.raw`. That is MaxQuant experiment Rep1 in `experimentalDesignTemplate.txt`.
- Deposited `Rep2.raw` was acquired as `..._PAR_PD_normal.raw`, which is MaxQuant **Rep3**.
- Deposited `Rep3.raw` was acquired as `..._PAR_PD_Filter.raw`, which is MaxQuant **Rep2**.

`characteristics[biological replicate]` follows the MaxQuant experiment numbers. So deposited Rep2.raw is replicate 3 and deposited Rep3.raw is replicate 2. Assay names stay as the deposited file stems. All other deposited RAW names match their original acquisition names.

**Biological replicate numbering.** Independent samples are numbered from 1 within each condition, where a condition is the combination of treatment, sampling time, compound and dose:
- **H2O2 at 0 min:** 7 sources. These are the time-course 0-min heavy channel (1) and the six light reference channels, in file order (2–7).
- **H2O2 at 10 min, no olaparib:** 7 sources. These are label-free replicates 1–3, the time-course 10-min heavy channel (4), the olaparib heavy controls at 1 µM and 10 µM (5 and 6), and the occupancy heavy channel (7).
- **Every other condition** has one source, numbered 1.

**Factors.**
- `factor value[treatment]`: hydrogen peroxide vs untreated. Untreated is only the occupancy light channel.
- `factor value[sampling time]`: H2O2 exposure time, 0 to 120 minutes.
- `factor value[compound]`: olaparib vs `not applicable`.
- `factor value[dose]`: olaparib dose, 1 uM or 10 uM.

**Instrument (from the RAW headers; PRIDE says "Q Exactive"):** Q Exactive Plus (MS:1002634) for all HeLa runs except the occupancy run, which is Q Exactive HF (MS:1002523). The paper's Methods name both. The NCE from the RAW method headers is 30 for the Q Exactive Plus runs and 28 for the occupancy run.

**Search settings:**
- **Fixed modification:** Carbamidomethyl (C), from the deposited `parameters.txt` (MaxQuant 1.3.0.5).
- **Variable modifications:** Oxidation (M), Acetyl (protein N-term), and ADP-Ribosyl (UNIMOD:213, 541.06 Da) on K, R, D and E. The MaxQuant site tables `ADP ribose (KRDE)Sites` and `Oxidation (M)Sites` are listed in `parameters.txt`, and the paper's Methods confirm the full set.
- **SILAC labels:** Lys8 and Arg10 are written as variable modification parameters on the SILAC rows only.
- **Tolerances:** fragment 20 ppm (FTMS, `parameters.txt`); precursor 7 ppm (paper).
- **Digestion:** Lys-C then trypsin (paper), so there are two `comment[cleavage agent details]` columns.
- **Reagents:** DTT for reduction and chloroacetamide for alkylation (paper).

## Post-processing (after `sdrf-tools build`)

`scratchpad/PXD004245/postprocess.py` made two changes:
1. It inserted a second `comment[cleavage agent details]` column with `NT=Lys-C;AC=MS:1001309` next to Trypsin, because every sample was digested with Lys-C and then trypsin. `build` emits that column only once.
2. It set the two SILAC label modification cells to `not applicable` on the 3 label-free rows.

A diff check against the build output found that the only changes were the inserted column and those 6 cells.

## Validation

- `timeout 900 parse_sdrf validate-sdrf -s PXD004245-HeLa.sdrf.tsv -t ms-proteomics -t human -t cell-lines --use_ols_cache_only`: exit 0, 0 errors, 1 warning. The warning is that `untreated` in `characteristics[treatment]` is not in NCIT/EFO. A live OLS exact search finds no plain "untreated" term either, but the sample-metadata template recommends `untreated` for controls, so it was kept.
- `sdrf-tools check`: CLEAN (21/21 terms verified), exit 0.
- `sdrf-tools structure`: OK.
- `sdrf-tools score`: 100/100.
- `sdrf-tools reconcile` reported three blockers. All three were checked against the evidence and kept:
  1. *Run names name a cell line, not the annotated tissue.* `organism part` = `uterine cervix` is HeLa's tissue of origin (Cellosaurus CVCL_0030). The spec allows the tissue of origin in `organism part` for cell lines, and `characteristics[cell line]` = HeLa.
  2. *Trypsin is not named in the record.* The paper's Methods say "endoproteinase Lys-C … and modified sequencing grade trypsin", and `parameters.txt` has `Special AAs KR`.
  3. *A labelled method is annotated as label-free.* Only the three `PAR_PD` replicate runs are label-free, as `peptides.txt` shows (no L/H intensity columns for experiments Rep1–3), and `msms.txt` has labelling state 0 only for those files. All SILAC runs are annotated as SILAC light/heavy.

## Limitations
- **Revised after independent review:** the H2O2 concentration is now recorded. `characteristics[compound]` / `characteristics[dose]` (and the mirrored factor values) are `hydrogen peroxide` / `500 uM` on rows 1-15 (label-free triplicate and SILAC time course; the paper states 500 µM for both, and the file names say 500uMH2O2); `hydrogen peroxide` / `not available` on rows 17, 19 and 21 (olaparib-experiment controls and occupancy heavy; concentration not stated); olaparib rows 16 and 18 keep compound `olaparib` with its dose (H2O2 exposure is recorded in `characteristics[treatment]`, since a single compound/dose column cannot hold both); untreated row 20 unchanged.

- **Post-processing (before review):** `assay name` set to one value per RAW file (per-channel `-SILAC light/heavy` suffixes from `build` removed), as the spec requires for multiplexed runs; channels are distinguished by `comment[label]`.


- **H2O2 exposure for some samples is inferred.** The 10-minute exposure for the label-free replicates, the olaparib experiments and the occupancy heavy channel comes from the general Methods statement ("Cells were stimulated with H2O2 for 10 min"). The occupancy 10 min is also stated in the Supplementary Fig. 4d/e legend. The 500 µM concentration is explicit only for the time course and the benchmark replicates, so the dose of H2O2 is not written in any column. The olaparib pre-incubation time is not given.
- **Light reference channels may not be independent.** Each time-course run has its own light reference source, numbered as separate biological replicates. The paper does not say whether these came from separate cultures or one shared light batch.
- **Label-free replicates may not be biological replicates.** The original names (2xSep-pak, Filter, normal) suggest the three differ in peptide clean-up. The paper calls them "replicate enrichment experiments" (Supplementary Data 1, "triplicate HeLa analyses"; Fig. 1e legend: "two biological replicate analyses"). Whether they come from independent cultures is not stated.
- **Donor values are from Cellosaurus CVCL_0030.** Cell-line donor age, sex, ancestry, disease and developmental stage are not from the paper.
- **The culture medium is generalised.** The paper says DMEM or SILAC DMEM; both are written as "Dulbecco's Modified Eagle Medium".
- **The enrichment step has no column.** There is no EFO/PRIDE child of EFO:0009090 for ADP-ribosylated peptide (Af1521 macrodomain) enrichment, so `characteristics[enrichment process]` is omitted and the enrichment is described only here.
- **The precursor tolerance (7 ppm) is from the paper.** `parameters.txt` does not report it.
- **Deposited search output covers runs that are not in the deposit.** The MaxQuant output includes experiments with no deposited RAW file (Input_5/10/15/20mg, SILAC_8/14mg, noCL, TNKSi). Those are not annotated. Every deposited HeLa RAW file is annotated.
- **PRIDE's disease field is wrong.** PRIDE lists the disease as "brain cancer" (DOID:1319). That contradicts HeLa's origin (cervical adenocarcinoma) and was not used.
- **ETD runs are not in the deposit.** The paper's ETD data on an Orbitrap Fusion Lumos (Supplementary Data 2) have no deposited RAW files.
