# PXD002277-HeLa-succinylation
Status: validated annotation; independent review pending.

## Dataset

- Title: *Lysine succinylation is a frequently occurring modification in prokaryotes and eukaryotes and extensively overlaps with acetylation*.
- Lab: Chunaram Choudhary, The NNF Center for Protein Research, University of Copenhagen (Copenhagen, Denmark); submitter Brian T. Weinert.
- Paper: Weinert BT, Schölz C, Wagner SA, Iesmantavicius V, Su D, Daniel JA, Choudhary C. *Cell Rep* 2013;4(4):842-51, doi:10.1016/j.celrep.2013.07.024, PMID 23954790. The full text and supplementary tables could not be retrieved (not in PMC or Europe PMC full text; cell.com and ScienceDirect returned HTTP 403; no repository copy found). Only the PubMed abstract and the MeSH headings were read.
- Not already annotated upstream: `bigbio/sdrf-annotated-datasets` `datasets/PXD002277` and `sandbox/PXD002277` both return 404.
- The deposit has 57 Thermo RAW files and one `MaxQuant_output_files.zip`. The zip holds six separate MaxQuant 1.2.7.1 searches (E. coli succinylation, yeast succinylation, HeLa succinylation, HeLa acetylation, mouse liver succinylation, mouse liver acetylation) plus `List_of_RAW_files.xlsx`, a submitter table that assigns every RAW file to a supplementary table and gives the SILAC channel map.

## Why the deposit is split into six SDRFs

The deposit covers four organisms, and the organism templates are mutually exclusive (`human` vs `vertebrates`; no template fits bacteria or yeast). Each organism, and each acyl modification, was searched separately in MaxQuant with its own FASTA and variable modifications. One SDRF per deposited MaxQuant search keeps `comment[modification parameters]` equal to that search. This SDRF covers the `hela_succinylation` search. The six SDRFs together cover all 57 RAW files, each exactly once. The sibling SDRFs are `PXD002277-Ecoli-succinylation`, `-yeast-succinylation`, `-HeLa-acetylation`, `-mouse-liver-succinylation` and `-mouse-liver-acetylation`.

## Output

- SDRF: `annotations/PXD002277-HeLa-succinylation.sdrf.tsv`
- 14 data rows x 44 columns, covering 10 RAW files.
- SHA-256: `0fd62d9d9aceeb1379d2fab983a8e76fec08eab367d11938aed9d845eb242946`
- Templates: `ms-proteomics` v1.1.0 + `human` v1.1.0 + `cell-lines` v1.1.0. All samples are the human HeLa cell line, so `human` (organism) and `cell-lines` (sample type) apply on top of the base `ms-proteomics` template.

## Design and file mapping

The `hela_succinylation` MaxQuant `summary.txt` lists exactly 10 RAW files. They form two groups.

**1. Label-free succinyl-lysine survey (6 RAW files, 6 rows).** Files `20120620_QE3_LC1_BTW_SA_HeLa40_succK_pH45/pH55/pH11` and their `b` counterparts. MaxQuant searched them with multiplicity 1 (no labels), so `comment[label]` = `label free sample`. `List_of_RAW_files.xlsx` assigns them to Table S4 with no SILAC note.
- Source: one sample, `PXD002277_HeLa_succK_labelfree` (biological replicate 1). `characteristics[treatment]` and `factor value[treatment]` = `not available`: no treatment is recorded for this survey sample.
- Fractions: the pH-step token in the file name gives the micro-SCX step. Fraction identifiers follow ascending elution pH: pH 4.5 = 1, pH 5.5 = 2, pH 11 = 3.
- Re-injections: the RAW headers show that the base files used the method `150min_3tunes_nolockmass_Iso2_Res35000_IT120.meth`, while each `b` file used a different method, `BTW_120m_60ms_250ms2_.meth` (120 min). The `b` files are therefore treated as re-injections of the same fraction: `comment[technical replicate]` = 1 for the base files and 2 for the `b` files, with the same fraction number.

**2. SILAC nicotinamide experiment (4 RAW files, 8 rows).** Files `20130307_QE4_LC6_CHS_SA_Hela_NAM_Succinyl_01` to `_04`. MaxQuant searched them with multiplicity 2 and `Labels1` = `Arg10;Lys8` (light channel unlabelled). `List_of_RAW_files.xlsx` gives the channel map: "SILAC, nicotinamide (H), control (L) *SILAC data not used for this study".
- Heavy channel: `PXD002277_HeLa_nicotinamide`, `comment[label]` = `SILAC heavy`, `characteristics[treatment]` and `factor value[treatment]` = `nicotinamide`.
- Light channel: `PXD002277_HeLa_control`, `comment[label]` = `SILAC light`, treatment and factor = `control`.
- Each RAW file appears twice (one row per channel); `assay name` = `<run>-SILAC heavy` / `<run>-SILAC light`.
- Fractions: the trailing number `_01` to `_04` is used as the fraction identifier 1-4. All four runs used the same method (`1-9um_CHS_141min_120MS2_IW2.meth`). Technical replicate = 1.
- SILAC labels are written as variable modifications on these rows only: Lys8 = `Label:13C(6)15N(2)` (UNIMOD:259, K), Arg10 = `Label:13C(6)15N(4)` (UNIMOD:267, R).

**Factor value:** `factor value[treatment]` takes the values `nicotinamide` (4 rows), `control` (4 rows) and `not available` (6 label-free rows).

**Post-processing:** `sdrf-tools build` can only emit one value per modification column, so the two SILAC label columns were first filled on every row. `scratchpad/PXD002277/postprocess.py` then set those two columns to `not applicable` on the 6 label-free rows. A diff of the build output against the final file confirmed that only these 12 cells changed.

## Technical values and sources

- Instrument: `Q Exactive` (MS:1001911). All 10 RAW headers (HTTP range read of the first 64 KB) say `Q Exactive - Orbitrap MS`, and the original acquisition path in each header equals the deposited file name. This agrees with PRIDE and the `summary.txt` `Instrument` column.
- Acquisition: DDA (PRIDE:0000627). The PRIDE protocol says "data-dependent mode".
- Dissociation: HCD, written `NT=beam-type collision-induced dissociation;AC=MS:1000422` (PRIDE protocol: "higher energy C-trap dissociation (HCD)"). MS2 analyzer: orbitrap (MS:1000484). The Q Exactive has no other MS2 analyzer, and MaxQuant used the FTMS MS/MS tolerance.
- Cleavage agent: `Trypsin/P` (MS:1001313), from the `summary.txt` `Protease` column. The PRIDE data-processing text says "strict trypsin specificity".
- Modifications: `parameters.txt` `Fixed modifications` = Carbamidomethyl (C) (UNIMOD:4). The `summary.txt` `Variable modifications` are Oxidation (M) (UNIMOD:35), Acetyl (Protein N-term) (UNIMOD:1), and the custom `succinyl-K`, written as `Succinyl` (UNIMOD:64, TA=K).
- Tolerances: precursor `6 ppm` (PRIDE data-processing protocol: main search 6 ppm after a 20 ppm first search). Fragment `20 ppm` (`parameters.txt` `MS/MS tol. (FTMS)` 20 ppm; the protocol also says 20 ppm).
- Fractionation: `Strong cation-exchange chromatography (SCX)` (PRIDE:0000561). The PRIDE protocol says that after enrichment, peptides were "immediately separated by micro-scale SCX chromatography".
- Reduction and alkylation reagents: `not available`.
- Cell line: HeLa, Cellosaurus `CVCL_0030`. Organism part `uterine cervix`, cell type `epithelial cell`, disease `cervical adenocarcinoma`, sex `female` and age `30Y6M` come from the Cellosaurus record. The PubMed MeSH headings include "Hela Cells".
- Enrichment: the protocol says succinylated peptides were enriched with polyclonal antibody beads (ImmuneChem). `characteristics[enrichment process]` is omitted because no term under EFO:0009090 covers acyl-lysine immunoaffinity enrichment. The closest PRIDE term, `antibody enrichment` (PRIDE:0000954), is not under that parent. The enrichment is still visible in the file names and the `Succinyl` variable modification.

## Validation

Run on 2026-11-04 against the SDRF with the SHA-256 above (unchanged since it was validated on 2026-11-03):

- `timeout 900 .venv/bin/parse_sdrf validate-sdrf --sdrf_file PXD002277-HeLa-succinylation.sdrf.tsv --template ms-proteomics --use_ols_cache_only`: "Everything seems to be fine. Well done.", exit 0, no errors or warnings.
- Same command with `--template human`: same result, exit 0, no errors or warnings.
- Same command with `--template cell-lines`: same result, exit 0, no errors or warnings.
- `.venv/bin/python -m tools check`: exit 0, CLEAN. It checked 17 terms and found 0 hallucinated terms, 0 label mismatches, 0 wrong-ontology terms and 0 UNIMOD swaps.
- From the earlier run on 2026-11-03: `tools structure` reported "Structure OK", exit 0. `tools reconcile` raised two flags, explained below:
  - `run_names_name_a_cell_line` on `characteristics[organism part]`: expected for a cell-line SDRF. `uterine cervix` is the tissue of origin of HeLa, as the `cell-lines` template asks.
  - `cleavage_agent_unsupported`: see Limitations.
- Live OLS (ols4) checks confirmed MS:1001911, MS:1001313, MS:1000422, MS:1000484, PRIDE:0000627, PRIDE:0000561, UNIMOD:4, UNIMOD:35, UNIMOD:1, UNIMOD:64, UNIMOD:259, UNIMOD:267, NCBITaxon:9606, UBERON:0000002, CL:0000066, MONDO:0005153, CHEBI:17154 (nicotinamide) and EFO:0001461 (control).
- Independent adversarial review: not run (out of scope for this producer run).

## Limitations
- **Revised for consistency with the sibling HeLa-acetylation file:** `characteristics[ancestry category]` set to `African American` (HANCESTRO:0568) from Cellosaurus CVCL_0030.

- **Revised for consistency after review of the sibling yeast file:** `assay name` is now one per RAW file (the per-channel `-SILAC light/heavy` suffixes were removed), as the spec requires for multiplexed runs; channels are distinguished by `comment[label]` and source name.


- **Paper not read.** The full text and Tables S1-S10 were unavailable (HTTP 403 at the publisher; no PMC or repository copy). Only the PubMed abstract and MeSH headings were read. Every sample fact comes from the PRIDE record, the deposited MaxQuant `summary.txt`/`parameters.txt`, the submitter's `List_of_RAW_files.xlsx`, the RAW file names, the RAW headers and Cellosaurus.
- **SILAC channel map (deposited table).** Heavy = nicotinamide and light = control come from `List_of_RAW_files.xlsx`. The Arg10/Lys8 heavy labels come from `summary.txt` `Labels1`. The submitter notes that the SILAC data were "not used for this study". The nicotinamide dose, duration and culture conditions are not stated anywhere available.
- **Label-free survey treatment (unavailable).** No treatment or condition is recorded for the 2012 label-free HeLa sample, so its treatment and factor value are `not available`. Whether it shares a lysate with the SILAC experiment is unknown. The two groups are recorded as separate sources, each with biological replicate 1.
- **Re-injections (`b` files; inference from RAW headers).** The `b` files are read as technical replicate 2 of the same SCX fraction. They have the same name plus `b`, the same acquisition date, and a different 120 min method (`BTW_120m_60ms_250ms2_.meth`) versus 150 min for the base runs. MaxQuant lists them as separate raw files. No document states this explicitly.
- **Fraction order (inference from file names).** pH-step runs are numbered by ascending elution pH (4.5, 5.5, 11). NAM runs `_01` to `_04` are assumed to be four SCX fractions of the pooled heavy/light sample, based on the PRIDE SCX statement and the sequential numbering. The fraction pH values for these runs are not given.
- **Cleavage agent.** `Trypsin/P` rests on the deposited search settings and the PRIDE "strict trypsin specificity" statement. The sample-preparation text does not name the digest reagent, so `sdrf-tools reconcile` raises `cleavage_agent_unsupported`. A peptide C-terminus check would not be independent here, because a Trypsin/P search only returns K/R-terminated peptides.
- **Reduction and alkylation reagents** = `not available`. Alkylation is implied by the fixed Carbamidomethyl (C) search, but the reagents are not stated.
- **Ancestry, passage number, culture medium and sample storage temperature** = `not available`; they are not stated in any available source.
- **Cell-line characteristics** (organism part, cell type, disease, sex, age) come from the Cellosaurus HeLa record (CVCL_0030), not from the study.
- **Enrichment column omitted** (no fitting ontology term under EFO:0009090; see Technical values).
