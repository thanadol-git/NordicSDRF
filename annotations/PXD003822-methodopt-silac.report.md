# PXD003822-methodopt-silac

Status: validated annotation; independent review pending.

- Title: Human AML patient samples, Method Optimization, LC-MSMS
- Lab: Frode S. Berven (PI) and Elise Aasebø (submitter), PROBE proteomics unit, Department of Biomedicine, University of Bergen, Bergen, Norway.
- Paper: Aasebø E, Mjaavatten O, Vaudel M, Farag Y, Selheim F, Berven F, Bruserud Ø, Hernandez-Valladares M. "Freezing effects on the acute myeloid leukemia cell proteome and phosphoproteome revealed using optimal quantitative workflows." J Proteomics 2016;145:214-225. doi:10.1016/j.jprot.2016.03.049, PMID 27107777. The paper is subscription-only: Europe PMC has no PMC copy, Unpaywall reports it as closed, and ScienceDirect returned HTTP 403. **Only the abstract was read.**
- Existing upstream annotation: none. `bigbio/sdrf-annotated-datasets` returned 404 for both `datasets/PXD003822` and `sandbox/PXD003822`.
- SDRF: `annotations/PXD003822-methodopt-silac.sdrf.tsv`
- Rows: 132; columns: 36
- SHA-256: `0215377cc060fd30b966b51e556cc251acd1c89ec8e33f2e70ed7bbad1ecda96`
- Evidence manifest: `annotations/PXD003822-methodopt-silac.evidence.json`

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

Method optimization, super-SILAC proteome arm: 11 workflows, each in duplicate. That makes 22 MaxQuant experiments and 66 raw files.

| Source name (light) | Fractionation | Files per replicate |
|---|---|---|
| MO-SILAC FASP double digestion | none | 2 (`_ddig_Lys`, `_ddig_Trp` eluates) |
| MO-SILAC FASP single digestion | none | 1 |
| MO-SILAC FASP single digestion SDB-RPS | SDB-RPS ("MM", mixed-mode), 3 fractions | 3 (x1, x2, bufX) |
| MO-SILAC FASP single digestion SCX | SCX, 6 fractions | 6 (x1–x5, bufX) |
| MO-SILAC IsD-U double digestion | none | 1 |
| MO-SILAC IsD-U single digestion | none | 1 |
| MO-SILAC IsD-U single digestion SDB-RPS | SDB-RPS, 3 fractions | 3 |
| MO-SILAC IsD-U single digestion SCX | SCX, 6 fractions | 6 |
| MO-SILAC IsD-G double digestion | none | 1 (`SS-1`, `SS-2`) |
| MO-SILAC IsD-G double digestion SDB-RPS | SDB-RPS, 3 fractions | 3 |
| MO-SILAC IsD-G double digestion SCX | SCX, 6 fractions | 6 |

- **Mapping source.** The deposited `Search_MethodOptimization_SS-Proteome/summary.txt`. Its Experiment names (`F_SILAC_SCX_Sdig_1`, `IsD-U_SILAC_MM_Sdig_2`, `IsD-G_SILAC_SCX_Ddig_1`, …) give the lysis method, the digestion scheme, the fractionation and the replicate. This is how the `SS_*` files are identified as IsD-G (guanidinium) double-digested; their file names alone do not say so.
- **Fraction order.** MaxQuant's Fraction numbers set the order: bufX is last (for example 301/302/303 = x1/x2/bufX and 401–406 = x1–x5/bufX).
- **Fractionation method.** SCX is PRIDE:0000561. SDB-RPS is written as `mixed mode chromatography` (MS:1003586), because the PRIDE text says SDB-RPS is "also referred to as mixed-mode" and the PRIDE fractionation branch has no mixed-mode term. Unfractionated rows are `not applicable`.
- **Replicates.** The `_1`/`_2` suffixes become technical replicates 1 and 2 of one source per workflow, with biological replicate 1 (light rows).
- **Super-SILAC channel map (SILAC SDRFs).** Every SILAC run has two rows. `SILAC light` is the AML patient sample. `SILAC heavy` is the `super-SILAC spike-in standard`, a pooled heavy-labelled (Arg6/Lys8) reference.
  - This follows from the super-SILAC design named in the PRIDE record and in the abstract, together with MaxQuant's Labels0 (light, none) and Labels1 (Arg6;Lys8) for every file. It is the definition of a super-SILAC experiment, not an inference about individual channels.
  - The heavy rows have `characteristics[biological replicate]` = `pooled`, because the reference is a pool and not one biological source. The contract allows `integer or pooled`.
  - The heavy rows share one source name. Their `comment[technical replicate]` is numbered 1..N in sample-row order, so the (source, biological replicate, technical replicate, fraction) coordinate stays unique. This follows the convention used for the other super-SILAC datasets in this campaign (PXD001963, PXD003138). The numbering does not mean the heavy standard was prepared N separate times.
- **Factor.** `factor value[sample preparation protocol]`: lysis, digestion and fractionation as free text. Heavy rows are `not applicable`.
- **Row count.** 66 files × 2 SILAC channels = 132 rows.

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

Previous SHA-256: `ac753b511b04e0a5659e899df3e7970ca9292b9d7a95eea0bc95e3fb876b95e0`. The independent review returned FAIL with one important finding, which this round addresses.

- **Finding:** every row said Trypsin, but `F_SILAC_1_ddig_Lys` and `F_SILAC_2_ddig_Lys` are Lys-C digests: 96.6% and 96.7% of peptides end in K, and 48% contain an uncleaved R. The paired `_Trp` runs are 62% R-terminal.
- **Change:** there are now two cleavage columns. The 2 Lys-C eluate files (4 rows) are Lys-C | not applicable. The 22 in-solution double-digest files (44 rows) are Lys-C | Trypsin; MaxQuant names them `IsD-U_SILAC_Ddig_*`, `IsD-G_SILAC_Ddig_*`, `IsD-G_SILAC_MM_Ddig_*` and `IsD-G_SILAC_SCX_Ddig_*`, so this covers the fractionated IsD-G runs too. All other rows are Trypsin | not applicable.
- **Method:** `scratchpad/PXD003822/postprocess_cleavage.py` runs on the `build` output. It (1) sets the existing cleavage column per data file and (2) inserts a second `comment[cleavage agent details]` column directly after it. It asserts that every built row had Trypsin, and it checks each assignment against the C-terminal statistics. It then confirms that dropping both cleavage columns gives back the build output minus its one cleavage column, cell for cell. A diff against the previous SDRF confirmed that the only changes are listed here. The SDRF was never hand-edited.
- `characteristics[biological replicate]` on the super-SILAC heavy rows went from `1` to `pooled`, for consistency with the fresh/frozen SDRFs and because the reference is a pool. This was changed in `samples.tsv` and rebuilt.

## Validation

All commands were run from the sdrf-skills checkout, one at a time.

- `timeout 900 .venv/bin/parse_sdrf validate-sdrf -s /home/thanadol/Documents/GitHub/NordicSDRF/annotations/PXD003822-methodopt-silac.sdrf.tsv -t ms-proteomics -t human --use_ols_cache_only`
  - Round 1: 0 errors and 1 warning: "Term: NT=mixed mode chromatography;AC=MS:1003586 in column 'comment[fractionation method]', is not found in the given ontology list pride". The term exists in live OLS (PSI-MS); the warning only concerns the PRIDE-only list, see Limitations.
  - Repair round, on the post-processed file: 0 errors and the same 1 warning (mixed mode chromatography not in the PRIDE list).
- `.venv/bin/python -m tools structure <sdrf>`: OK (acquisition, template declaration and column order are consistent).
- `.venv/bin/python -m tools check <sdrf>`: CLEAN. All controlled terms were verified against OLS, with no UNIMOD swaps and no label mismatches.
- `.venv/bin/python -m tools reconcile <sdrf> --record scratchpad/PXD003822/project.json --accession PXD003822`: see below.
  - BLOCKER `cleavage_agent_unsupported` (Lys-C, Trypsin). The PRIDE prose names no enzyme. Both are kept on the peptide-terminus evidence described under Technical values.

## Limitations

- **Same AML material across workflows** is not stated, so `individual` = not available and `pooled sample` = not available for the light rows. The replicates are encoded as technical replicates, which is an interpretation (see the label-free method-optimization report).
- **SDB-RPS term.** `mixed mode chromatography` (MS:1003586) is outside the PRIDE list the validator expects, which produces 1 warning. The term is accurate for SDB-RPS. The alternative was `not available`, which would discard known information.
- **Super-SILAC standard.** Its composition (which heavy-labelled cell lines) is not in the evidence. The heavy rows therefore carry `pooled sample` = pooled, `individual` = pooled, `material type` = cell line (SILAC metabolic labelling requires cultured cells), `disease` = not available and `cell type` = not available.
- **Cleavage agent.** The Lys-C/trypsin split is evidenced by the deposited peptide data and the eluate tags in the file names. The paper's Methods were not read, so enzyme ratios and digestion times are unknown. For the in-solution double digests, the second enzyme is identified only from the peptide termini (a raised K-terminal and uncleaved-R share). `reconcile` flags Lys-C and Trypsin as unsupported because the PRIDE prose names no enzyme.
- **Paper not read.** The J Proteomics paper is closed access, so only the abstract, the PRIDE protocol text and the deposited MaxQuant files were used. Any detail that lives only in the paper's Methods is absent or marked `not available`. This includes patient demographics, cell isolation (blood or bone marrow, density-gradient or not), the super-SILAC cell-line composition, enzyme amounts and digestion times, reduction/alkylation reagents, LC gradient and precursor tolerance.
- **Organism part and cell type** are `not available`. The abstract says only "AML cells" and "cell lysates from patients with AML". PRIDE's dropdown lists CL:0000055 "non-terminally differentiated cell", which is obsolete in CL (the suggested replacement is progenitor cell, CL:0011026), so it was not used. Blood versus bone marrow origin is not stated in the evidence I could read.
- **Age, sex and ancestry** are `not available` (ancestry omitted). No per-patient table was available.
- **Precursor mass tolerance** is not recorded, because MaxQuant 1.5 `parameters.txt` does not report it.
- **Instrument.** The model is `Orbitrap Elite`, from the method text and folder names. One header field says "Orbitrap Velos Pro" (see Technical values). Only 8 of 163 raw files were range-read. The other files' CID/ion-trap settings are assumed to be the same, because they share the five method templates and the same MaxQuant ITMS tolerance.
