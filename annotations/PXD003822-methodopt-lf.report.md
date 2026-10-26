# PXD003822-methodopt-lf

Status: validated annotation; independent review pending.

- Title: Human AML patient samples, Method Optimization, LC-MSMS
- Lab: Frode S. Berven (PI) and Elise Aasebø (submitter), PROBE proteomics unit, Department of Biomedicine, University of Bergen, Bergen, Norway.
- Paper: Aasebø E, Mjaavatten O, Vaudel M, Farag Y, Selheim F, Berven F, Bruserud Ø, Hernandez-Valladares M. "Freezing effects on the acute myeloid leukemia cell proteome and phosphoproteome revealed using optimal quantitative workflows." J Proteomics 2016;145:214-225. doi:10.1016/j.jprot.2016.03.049, PMID 27107777. The paper is subscription-only: Europe PMC has no PMC copy, Unpaywall reports it as closed, and ScienceDirect returned HTTP 403. **Only the abstract was read.**
- Existing upstream annotation: none. `bigbio/sdrf-annotated-datasets` returned 404 for both `datasets/PXD003822` and `sandbox/PXD003822`.
- SDRF: `annotations/PXD003822-methodopt-lf.sdrf.tsv`
- Rows: 12; columns: 32
- SHA-256: `8f3ef15823aacfa20080d9f0e5a1ac4df46e271ffabaa9241ab72bda787e0fc0`
- Evidence manifest: `annotations/PXD003822-methodopt-lf.evidence.json`

## Why the deposit is split into six SDRFs

The PRIDE data-processing protocol describes five sub-datasets, and each has its own MaxQuant 1.5.2.8 search archive. Together they hold all 163 deposited raw files:

| SDRF | Search archive | Raw files | Quantification |
|---|---|---|---|
| `PXD003822-methodopt-lf` | `Search_MethodOptimization_LF.zip` | 12 | label-free |
| `PXD003822-methodopt-silac` | `Search_MethodOptimization_SS-Proteome.zip` | 66 | super-SILAC |
| `PXD003822-methodopt-phospho` | `Search_MethodOptimization_SS-Phospho.zip` | 42 | super-SILAC, phosphopeptide-enriched |
| `PXD003822-freshfrozen-lf` | `Search_FreshFrozen-LF.zip` | 11 | label-free |
| `PXD003822-freshfrozen-silac` | `Search_FreshFrozen_SS.zip` (proteome parameter group) | 24 | super-SILAC |
| `PXD003822-freshfrozen-phospho` | `Search_FreshFrozen_SS.zip` (phospho parameter group) | 8 | super-SILAC, IMAC-enriched |

The searches differ in label multiplicity and in variable modifications. Phospho (STY) was searched only for the enriched files, so one constant `comment[modification parameters]` set per file is only possible after splitting. `Search_FreshFrozen_SS.zip` is a single search with two parameter groups. In its `summary.txt`, the 24 proteome files have no Phospho and the 8 enriched files do, so it is split into a proteome SDRF and a phospho SDRF. Every raw file in the deposit appears in exactly one SDRF.

## Templates

`ms-proteomics` v1.1.0 and `human` v1.1.0.

- `ms-proteomics`: DDA LC-MS/MS on an Orbitrap Elite.
- `human`: the samples are cells from patients with acute myeloid leukemia (AML). The super-SILAC reference is a pool of human cells, and the search database was human Swiss-Prot.
- `oncology-metadata` and `clinical-metadata` were **not** used. This is a technical method study. The deposit and the abstract give no per-patient clinical, staging or treatment data, so those templates would only add columns of `not available`.
- `cell-lines` was not used. The study samples are primary patient cells, and the composition of the super-SILAC cell-line pool is not documented in the available evidence.
- `dia-acquisition` does not apply. The raw-file methods are top-10 or top-15 data-dependent CID scans.

## Design and file mapping

Method optimization, label-free arm. The study compares lysis and digestion workflows on AML patient cells. Each workflow was processed in duplicate: the PRIDE text says "All samples were processed in replicates".

| Source name | Factor value (`sample preparation protocol`) | Replicate 1 file(s) | Replicate 2 file(s) |
|---|---|---|---|
| MO-LF FASP double digestion | FASP (SDS lysis), double digestion | F_LFQ_1_ddig_Lys_new, F_LFQ_1_ddig_Trp | F_LFQ_2_ddig_Lys, F_LFQ_2_ddig_Trp |
| MO-LF FASP single digestion | FASP (SDS lysis), single digestion | F_LFQ_1_sdig_trp | F_LFQ_2_sdig_trp |
| MO-LF IsD-U double digestion | in-solution digestion, urea lysis (IsD-U), double digestion | IsD_LFQ_dd_1_150109164014 | IsD_LFQ_dd_2 |
| MO-LF IsD-U single digestion | in-solution digestion, urea lysis (IsD-U), single digestion | IsD_LFQ_sd_1 | IsD_LFQ_sd_2 |
| MO-LF IsD-G double digestion | in-solution digestion, guanidinium hydrochloride lysis (IsD-G), double digestion | LF-1 | LF-2 |

- **Mapping source.** The deposited `Search_MethodOptimization_LF/summary.txt`. Its MaxQuant Experiment names (`F_LFQ_1_DD`, `F_LFQ_1_SD`, `IsD_U_LFQ_DD_1`, `IsD_U_LFQ_SD_1`, `IsD_G_LFQ_DD_1`, and the `_2` versions) assign every file to a workflow and replicate. This matters most for `LF-1`/`LF-2`, whose file names say nothing about the workflow; MaxQuant names them `IsD_G_LFQ_DD_1/2`.
- **Replicates.** Replicates 1 and 2 are written as `comment[technical replicate]` 1 and 2 of one source per workflow, because they are duplicate preparations of the workflow. `characteristics[biological replicate]` = 1.
- **Fractions.** In the FASP double digestion, the two eluates (`_Lys`, `_Trp`) are fractions 1 and 2 of one sample, in MaxQuant fraction order (10/11 and 30/31). Every other workflow is one unfractionated run.
- **Factor.** `factor value[sample preparation protocol]`. A free-text label is used because no ontology term covers lysis buffer combined with digestion scheme.
- **Row count.** 12 files × 1 label-free row = 12 rows.

## Technical values (all SDRFs)

- **Instrument**: `Orbitrap Elite` (MS:1001910).
  - PRIDE says "LTQ Orbitrap Elite". The embedded instrument method in the raw-file header reads "Orbitrap Elite MS" with tune file `Elite_nano`. The acquisition folders are named `..._OrbitrapElite_...` and the method names specify 240K resolution, which a Velos Pro cannot reach.
  - The headers also contain an "Orbitrap Velos Pro" string in the audit/header block. I treated it as a legacy device-name field, not the model.
  - Eight raw files spanning all six sub-experiments were checked, using an HTTP range read of the first 3 MB of each.
- **Acquisition**: DDA (PRIDE:0000627). In the sampled headers, MS1 is FTMS (300–2000 m/z) and MS2 is ITMS CID at normalized collision energy 35.0. The phospho runs use a top-15 CID method with multistage activation (`53b-TOP15nCID-MSA`).
  - This gives `comment[dissociation method]` = collision-induced dissociation (MS:1000133), `comment[collision energy]` = 35 NCE, and `comment[ms2 mass analyzer]` = linear ion trap (MS:1000291).
- **Fragment mass tolerance**: 0.6 Da, the MaxQuant `MS/MS tol. (ITMS)` in each `parameters.txt`. MS2 was in the ion trap.
- **Precursor mass tolerance**: omitted. The deposited `parameters.txt` (MaxQuant 1.5) does not report it, and no `mqpar.xml` was deposited.
- **Cleavage agents** (two `comment[cleavage agent details]` columns): every row has two columns, set per data file. They follow the peptide C-terminal residue pattern in the deposited MaxQuant `evidence.txt`: unique non-decoy, non-contaminant sequences per raw file, computed by `scratchpad/PXD003822/cterm.py`.
  - **FASP double-digestion Lys-C eluate** (`*_ddig_Lys*`, `DD_L_*`): `Lys-C` (MS:1001309) | `not applicable`. In these runs 92–97% of peptides end in K and 30–56% contain an uncleaved R not before P, which is a Lys-C digest.
  - **FASP double-digestion trypsin eluate** (`*_ddig_Trp`, `DD_T_*`): `Trypsin` | `not applicable`. 60–71% of peptides end in R, which is tryptic.
  - **In-solution double digestion, one run per digest** (MaxQuant experiments `IsD_U_LFQ_DD_*`, `IsD_G_LFQ_DD_*`, `IsD-U_SILAC_Ddig_*`, `IsD-G_SILAC_*Ddig_*`): `Lys-C` | `Trypsin`. One run saw both enzymes. In the unfractionated runs, the K-terminal share is 0.53–0.61 and the uncleaved-R share is 0.16–0.30. Both are higher than in the urea in-solution single digests (0.49 and 0.14). Lys-C is recorded first because the FASP double digests show Lys-C eluting before trypsin. The in-solution order is not stated in the evidence I could read.
  - **Single digestion**: `Trypsin` | `not applicable`.
  - MaxQuant searched every file with Trypsin/Specific (`summary.txt`). That is the search setting, not the digest; Lys-C peptides ending in K are still matched under trypsin specificity.
  - `sdrf-tools build` writes one cleavage column from `technical.tsv` and cannot vary it within one sample row's fractions. The per-file values and the second column are therefore set by `scratchpad/PXD003822/postprocess_cleavage.py`, which is documented and diff-verified (see Repair round).
- **Modifications**: from `parameters.txt` (fixed) and `summary.txt` (variable and labels).
  - Fixed: Carbamidomethyl (C).
  - Variable: Acetyl (Protein N-term) and Oxidation (M), plus Phospho (STY) in the phospho SDRFs only.
  - Super-SILAC heavy labels Arg6 = Label:13C(6) (UNIMOD:188) on R and Lys8 = Label:13C(6)15N(2) (UNIMOD:259) on K. These are encoded as Variable, which is the `sdrf-tools search-params` output for a MaxQuant SILAC search.
- **Labels**: the SILAC sub-experiments have MaxQuant multiplicity 2, with Labels0 = light and Labels1 = Arg6;Lys8. The label-free ones have multiplicity 1.

## Repair round (after independent review)

Previous SHA-256: `dafd84557fe70903b2921fe63c9cc8b9350c6025ca2c578a1bafd8a86a960eef`. The independent review returned FAIL with one important finding, which this round addresses.

- **Finding:** every row said Trypsin, but `F_LFQ_1_ddig_Lys_new` and `F_LFQ_2_ddig_Lys` are Lys-C digests. I verified this from the deposited `evidence.txt`: 96.8% and 96.5% of their peptides end in K, and 47% and 44% contain an uncleaved R. The paired `_Trp` runs are 60% R-terminal.
- **Change:** there are now two cleavage columns. The 2 Lys-C eluate rows are Lys-C | not applicable. The 4 in-solution double-digest rows (`IsD_LFQ_dd_*`, `LF-1`, `LF-2`) are Lys-C | Trypsin. All other rows are Trypsin | not applicable.
- **Method:** `scratchpad/PXD003822/postprocess_cleavage.py` runs on the `build` output. It (1) sets the existing cleavage column per data file and (2) inserts a second `comment[cleavage agent details]` column directly after it. It asserts that every built row had Trypsin, and it checks each assignment against the C-terminal statistics. It then confirms that dropping both cleavage columns gives back the build output minus its one cleavage column, cell for cell. A diff against the previous SDRF confirmed that the only changes are listed here. The SDRF was never hand-edited.

## Validation

All commands were run from the sdrf-skills checkout, one at a time.

- `timeout 900 .venv/bin/parse_sdrf validate-sdrf -s /home/thanadol/Documents/GitHub/NordicSDRF/annotations/PXD003822-methodopt-lf.sdrf.tsv -t ms-proteomics -t human --use_ols_cache_only`
  - Round 1: 0 errors and 0 warnings ("Everything seems to be fine").
  - Repair round, on the post-processed file: 0 errors and 0 warnings.
- `.venv/bin/python -m tools structure <sdrf>`: OK (acquisition, template declaration and column order are consistent).
- `.venv/bin/python -m tools check <sdrf>`: CLEAN. All controlled terms were verified against OLS, with no UNIMOD swaps and no label mismatches.
- `.venv/bin/python -m tools reconcile <sdrf> --record scratchpad/PXD003822/project.json --accession PXD003822`: see below.
  - BLOCKER `cleavage_agent_unsupported` (Lys-C, Trypsin). The PRIDE prose names no enzyme. Both are kept on the peptide-terminus evidence described under Technical values.
  - BLOCKER `labelled_annotated_as_label_free`. This fires because PRIDE registers SILAC as one of the project's two quantification methods. This sub-dataset is explicitly the label-free arm: the PRIDE protocol text names it a label-free dataset, and its MaxQuant search has multiplicity 1 with no labels. `label free sample` was kept.

## Limitations

- **Same AML material across workflows?** The abstract says "AML patient samples". Whether all workflows used one patient, several patients or a pooled lysate is not stated, so `individual` = not available. Each workflow is its own source, so no shared identity is asserted.
- **Replicates as technical.** Encoding the duplicates as technical replicates is an interpretation of "processed in replicates". If they came from different patients, they would be biological replicates instead.
- **Cleavage agent.** The Lys-C/trypsin split is evidenced by the deposited peptide data and the eluate tags in the file names. The paper's Methods were not read, so enzyme ratios and digestion times are unknown. For the in-solution double digests, the second enzyme is identified only from the peptide termini (a raised K-terminal and uncleaved-R share). `reconcile` flags Lys-C and Trypsin as unsupported because the PRIDE prose names no enzyme.
- **Paper not read.** The J Proteomics paper is closed access, so only the abstract, the PRIDE protocol text and the deposited MaxQuant files were used. Any detail that lives only in the paper's Methods is absent or marked `not available`. This includes patient demographics, cell isolation (blood or bone marrow, density-gradient or not), the super-SILAC cell-line composition, enzyme amounts and digestion times, reduction/alkylation reagents, LC gradient and precursor tolerance.
- **Organism part and cell type** are `not available`. The abstract says only "AML cells" and "cell lysates from patients with AML". PRIDE's dropdown lists CL:0000055 "non-terminally differentiated cell", which is obsolete in CL (the suggested replacement is progenitor cell, CL:0011026), so it was not used. Blood versus bone marrow origin is not stated in the evidence I could read.
- **Age, sex and ancestry** are `not available` (ancestry omitted). No per-patient table was available.
- **Precursor mass tolerance** is not recorded, because MaxQuant 1.5 `parameters.txt` does not report it.
- **Instrument.** The model is `Orbitrap Elite`, from the method text and folder names. One header field says "Orbitrap Velos Pro" (see Technical values). Only 8 of 163 raw files were range-read. The other files' CID/ion-trap settings are assumed to be the same, because they share the five method templates and the same MaxQuant ITMS tolerance.
