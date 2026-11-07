# PXD002277-HeLa-acetylation
Status: validated annotation; independent review pending.

## Description

- Dataset: PXD002277, "Lysine succinylation is a frequently occurring modification in prokaryotes and eukaryotes and extensively overlaps with acetylation".
- Lab: Chunaram Choudhary (with Brian T. Weinert), The NNF Center for Protein Research, University of Copenhagen, Copenhagen, Denmark.
- Paper: Weinert BT et al., Cell Rep 2013;4(4):842-51, doi:10.1016/j.celrep.2013.07.024, PMID 23954790.
- This SDRF covers one of six sub-experiments: the HeLa lysine-acetylome (anti-acetyllysine antibody enrichment, SCX fractionation, Q Exactive). The submitter's `List_of_RAW_files.xlsx` assigns these runs to Table S6 of the paper. It matches the deposited MaxQuant search `hela_acetylation`.
- The dataset is split into six SDRFs, one per deposited MaxQuant search. Each search has its own organism, FASTA and modification set: E. coli succinylation, yeast succinylation, HeLa succinylation, HeLa acetylation, mouse liver succinylation and mouse liver acetylation.

## Output

- SDRF: `/home/thanadol/Documents/GitHub/NordicSDRF/annotations/PXD002277-HeLa-acetylation.sdrf.tsv`
- Rows/columns: 8 data rows (plus header) x 40 columns.
- SHA-256: `7d7b25c10937ba5fb582c1b8158252f4cdd4fcf8bfc6cdaa8e2d484ca64d4af7`
- Built with `sdrf-tools build` from `scratchpad/PXD002277/HeLa-acetylation/samples.tsv` and `technical.tsv`. No post-processing was needed for this stem: `build.sdrf.tsv` and `final.sdrf.tsv` are byte-identical, and the annotations copy matches them.

## Templates and why

- `ms-proteomics` v1.1.0: base template for an MS proteomics run.
- `human` v1.1.0: the organism is Homo sapiens (human FASTA in `parameters.txt`: `F:\000-Fasta\HUMAN.fasta`).
- `cell-lines` v1.1.0: the sample is the HeLa cell line (run names `..._HeLa_acK_...`). The template requires the Cellosaurus columns.
- `dda-acquisition` is not declared. The acquisition method is written as `Data-dependent acquisition` (PRIDE:0000627), as the PRIDE protocol states ("data-dependent mode").

## Design and file mapping

- There is one biological source: a HeLa lysate enriched for acetyllysine peptides (`source name` `PXD002277_HeLa_acK`, biological replicate 1). It was SCX-fractionated into 4 fractions (F01-F04). Each fraction was injected twice, so there are 8 RAW files.
- The design is label-free. `List_of_RAW_files.xlsx` gives no SILAC note for any of these 8 files; SILAC notes appear only for the E. coli cobB, yeast kgd/lsc and HeLa NAM runs. MaxQuant `summary.txt` reports `Multiplicity` = 1 with no labels for every run. `comment[label]` is therefore `label free sample`.
- There is no factor value column. This sub-experiment is a single-condition site catalogue: one sample, no treatment or comparison, and the MaxQuant search has one experiment. The rules say to omit the factor column for a genuinely single-condition study.

| RAW file | fraction | technical replicate | LC-MS method (RAW header) |
|---|---|---|---|
| 20120903_QE4_LC7_BTW_SA_HeLa_acK_F01.raw | 1 | 1 | BTW_180min_acK |
| 20120903_QE4_LC7_BTW_SA_HeLa_acK_F02.raw | 2 | 1 | BTW_180min_acK |
| 20120903_QE4_LC7_BTW_SA_HeLa_acK_F03.raw | 3 | 1 | BTW_150min_acK |
| 20120903_QE4_LC7_BTW_SA_HeLa_acK_F04.raw | 4 | 1 | BTW_150min_acK |
| 20120903_QE4_LC7_BTW_SA_HeLa_acK_F01b.raw | 1 | 2 | BTW_150min_acK |
| 20120903_QE4_LC7_BTW_SA_HeLa_acK_F02b.raw | 2 | 2 | BTW_150min_acK |
| 20120903_QE4_LC7_BTW_SA_HeLa_acK_F03b.raw | 3 | 2 | BTW_120min_acK |
| 20120903_QE4_LC7_BTW_SA_HeLa_acK_F04b.raw | 4 | 2 | BTW_120min_acK |

- File-to-sample mapping uses `List_of_RAW_files.xlsx` (all 8 files are "Table S6"), the 8 raw files of the `hela_acetylation` MaxQuant `summary.txt`, and the RAW file names. All 8 deposited `HeLa_acK` RAW files are included. None are left out.
- The `b` files are treated as re-injections, i.e. technical replicate 2 of the same fraction. In this subset they were not all run with the 120 min method that the other sub-experiments' `b` files used. The RAW headers show that the first injections of F01/F02 used a 180 min method, the first injections of F03/F04 and the re-injections of F01/F02 used a 150 min method, and only the re-injections of F03/F04 used a 120 min method. Every `b` run used a method 30 min shorter than its first injection.
- Instrument: the RAW headers give "Q Exactive - Orbitrap MS" for all 8 files, which agrees with PRIDE (`NT=Q Exactive;AC=MS:1001911`). The `QE4_LC7` token in the file names is an in-house instrument/LC identifier.

### Values and sources

- Organism, organism part, cell line: Homo sapiens; uterine cervix (UBERON:0000002); HeLa. These come from the human FASTA and the run names. Cellosaurus CVCL_0030 gives "Derived from site: Uterus, cervix".
- Cell type: `epithelial cell` (CL:0000066). This is a conventional annotation for HeLa (see Limitations).
- Disease: `cervical adenocarcinoma` (MONDO:0005153). Cellosaurus gives NCIt C27677, "HPV-related endocervical adenocarcinoma".
- Age `30Y6M` and sex `female` come from Cellosaurus CVCL_0030 (`AG 30Y6M`, `SX Female`). These describe the donor of the cell line, not the experiment.
- Ancestry, passage number, culture medium and storage temperature are `not available`. They are not stated in any available source.
- Cleavage agent: `Trypsin/P` (MS:1001313), from the `summary.txt` `Protease` column. The PRIDE protocol says "strict trypsin specificity", up to 2 missed cleavages.
- Modifications come from `parameters.txt` and `summary.txt`: Carbamidomethyl (C) fixed; Oxidation (M), Acetyl (Protein N-term) and Acetyl (K) variable.
- Tolerances: precursor 6 ppm (PRIDE protocol: main search after a 20 ppm first search). Fragment 20 ppm (`parameters.txt` `MS/MS tol. (FTMS)` 20 ppm; the protocol agrees).
- Dissociation: HCD (`NT=beam-type collision-induced dissociation;AC=MS:1000422`), from the PRIDE protocol "higher energy C-trap dissociation (HCD)". MS2 analyzer: orbitrap. The Q Exactive has no other MS2 analyzer, and MaxQuant used the FTMS tolerance.
- Fractionation: `Strong cation-exchange chromatography (SCX)` (PRIDE:0000561), from the PRIDE protocol "immediately separated by micro-scale SCX chromatography".
- Reduction and alkylation reagents are `not available`. The fixed Carbamidomethyl search implies alkylation, but no reagent is named.

## Validation

Commands were run on 2026-11-04 against the SDRF at the SHA-256 above:

```
cd /home/thanadol/Documents/GitHub/sdrf-skills
timeout 900 .venv/bin/parse_sdrf validate-sdrf --sdrf_file <sdrf> --template ms-proteomics --use_ols_cache_only   # exit 0, "Everything seems to be fine. Well done." (0 errors, 0 warnings)
timeout 900 .venv/bin/parse_sdrf validate-sdrf --sdrf_file <sdrf> --template human --use_ols_cache_only           # exit 0, "Everything seems to be fine. Well done." (0 errors, 0 warnings)
timeout 900 .venv/bin/parse_sdrf validate-sdrf --sdrf_file <sdrf> --template cell-lines --use_ols_cache_only      # exit 0, "Everything seems to be fine. Well done." (0 errors, 0 warnings)
.venv/bin/python -m tools check <sdrf>                                                                           # exit 0, 15/15 terms verified, Status CLEAN
```

Earlier runs on 2026-11-03 (logs in `scratchpad/PXD002277/validation/`) gave the same results:
- `tools structure` reported "Structure OK".
- A live OLS4 lookup resolved every accession used here: MS:1001911, MS:1001313, MS:1000422, MS:1000484, PRIDE:0000627, PRIDE:0000561, UNIMOD:4, UNIMOD:35, UNIMOD:1, NCBITaxon:9606, UBERON:0000002, CL:0000066 and MONDO:0005153.
- `tools reconcile` raised two heuristic flags. Both were reviewed and kept as annotated:
  - `run_names_name_a_cell_line` (organism part). The run names name HeLa, a cell line. That is expected: the `cell-lines` template records the cell line in `characteristics[cell line]` and the anatomical origin in `organism part`.
  - `cleavage_agent_unsupported`. The PRIDE sample-prep text does not name the protease. Trypsin/P comes from the deposited search settings and the "strict trypsin specificity" statement.

No independent adversarial review has been run.

## Limitations
- **Revised after independent review:** `characteristics[ancestry category]` set to `African American` (HANCESTRO:0568) from Cellosaurus CVCL_0030 ('Population: African American'), the same source as the donor age and sex.


- **Paper full text unavailable.** The publisher (Cell Press/ScienceDirect) returned HTTP 403. The paper is not in PMC and no repository copy was found. Only the PubMed abstract (PMID 23954790) was read. Methods and Table S6 were not seen. Every sample fact comes from the PRIDE record, the deposited MaxQuant output (`parameters.txt`, `summary.txt`), the submitter's `List_of_RAW_files.xlsx`, the RAW file names and the RAW headers (range-read).
- **Single biological sample (inference).** One HeLa acetylome preparation is assumed, because all 8 runs share one name stem, one acquisition date and one MaxQuant experiment. Whether F01-F04 came from one enrichment or from pooled enrichments is not documented.
- **Fraction numbers** come from the `F01`-`F04` tokens in the file names. The SCX elution conditions are not documented.
- **Re-injections (`b` files) = technical replicate 2 (inference).** They share the name plus `b`, the acquisition date series and the MaxQuant search, and each was acquired with a method 30 min shorter than its first injection (180 to 150 min or 150 to 120 min, per the RAW headers). No document says explicitly that they are re-injections of the same fraction.
- **Cell type `epithelial cell`** is the usual HeLa annotation (Cellosaurus describes HeLa as a cancer cell line from a cervical adenocarcinoma). It is not stated by the submitters.
- **Age/sex** are Cellosaurus donor values for HeLa, not experimental metadata.
- **Cleavage agent Trypsin/P** rests on the search settings and the "strict trypsin specificity" protocol text. The digest reagent is not named in the sample-preparation text. Checking peptide C-termini would not be independent, because a Trypsin/P search can only return K/R-terminated peptides.
- **Reduction/alkylation reagents, culture medium, passage number, storage temperature, ancestry:** `not available`. None is stated in any available source.
- **Enrichment** (anti-acetyllysine antibody beads, ImmuneChem, per the PRIDE protocol) is not encoded in a column. No term under the `characteristics[enrichment process]` parent fits. It is visible only from the `acK` run names and the Acetyl (K) variable modification.
- **Precursor tolerance 6 ppm** is the main-search value from the PRIDE protocol. MaxQuant 1.2.7.1 `parameters.txt` does not list it.
