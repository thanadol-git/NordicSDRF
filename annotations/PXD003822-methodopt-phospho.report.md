# PXD003822-methodopt-phospho

Status: validated annotation; independent review pending.

- Title: Human AML patient samples, Method Optimization, LC-MSMS
- Lab: Frode S. Berven (PI) and Elise Aasebø (submitter), PROBE proteomics unit, Department of Biomedicine, University of Bergen, Bergen, Norway.
- Paper: Aasebø E, Mjaavatten O, Vaudel M, Farag Y, Selheim F, Berven F, Bruserud Ø, Hernandez-Valladares M. "Freezing effects on the acute myeloid leukemia cell proteome and phosphoproteome revealed using optimal quantitative workflows." J Proteomics 2016;145:214-225. doi:10.1016/j.jprot.2016.03.049, PMID 27107777. The paper is subscription-only: Europe PMC has no PMC copy, Unpaywall reports it as closed, and ScienceDirect returned HTTP 403. **Only the abstract was read.**
- Existing upstream annotation: none. `bigbio/sdrf-annotated-datasets` returned 404 for both `datasets/PXD003822` and `sandbox/PXD003822`.
- SDRF: `annotations/PXD003822-methodopt-phospho.sdrf.tsv`
- Rows: 84; columns: 37
- SHA-256: `58f420d32e16480816d52d5d0d9aff22f6b392c12dd662a73b0691abbe441691`
- Evidence manifest: `annotations/PXD003822-methodopt-phospho.evidence.json`

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

Method optimization, phosphopeptide-enrichment arm. All samples are FASP (SDS lysis) digests, single- or double-digested, enriched by IMAC, SIMAC or TiO2 (MOAC). That is 6 workflows × 2 deposited replicates = 12 MaxQuant experiments, covering 42 raw files.

| Source name (light) | Files per replicate (fraction order) |
|---|---|
| MO-phospho FASP double digestion IMAC | DD_L_IMAC, DD_L_IMAC_FT, DD_T_IMAC, DD_T_IMAC_FT |
| MO-phospho FASP double digestion SIMAC | DD_L_SIMAC, DD_L_SIMAC_FT, DD_L_SIMAC_MULTIP, DD_T_SIMAC, DD_T_SIMAC_FT, DD_T_SIMAC_MULTIP |
| MO-phospho FASP double digestion TiO2 (MOAC) | DD_L_TIO2, DD_L_TIO2_FT, DD_T_TIO2, DD_T_TIO2_FT |
| MO-phospho FASP single digestion IMAC | SD_IMAC, SD_IMAC_FT |
| MO-phospho FASP single digestion SIMAC | SD_SIMAC, SD_SIMAC_FT, SD_SIMAC_MULTIP |
| MO-phospho FASP single digestion TiO2 (MOAC) | SD_TIO2, SD_TIO2_FT |

Replicate 2 has the same files with a `_2` suffix (for example `DD_L_IMAC_2`, `DD_L_IMAC_FT_2`, `SD_TiO2_2`).

- **Mapping source.** The deposited `Search_MethodOptimization_SS-Phospho/summary.txt`. MaxQuant names the deposited files' experiments `2nd_rep_<DD|SD>_<IMAC|SIMAC|TiO2>` (un-suffixed files) and `3rd_rep_...` (`_2` files), with fraction numbers that give the order above.
- **Search files not deposited.** The search also lists 30 raw files that are not in the deposit:
  - the `1st_rep_*` experiments (`D6D7_*`, `D8D12_*`, `D9D10_*`, `S3S4_*`, `S8S9_*`);
  - the incubation-time variants `*_2H`, `*_3H` and `*_4H`.
  - The PRIDE text says "some raw files included in the result files were not used in the final experiment". Every deposited MaxQuant experiment is complete in the deposit, and no deposited file is left out.
- **Replicates.** MaxQuant's `2nd_rep` and `3rd_rep` become technical replicates 1 and 2 of one source per workflow, renumbered so they run from 1 (`sdrf-tools structure` requires this).
- **Fractions.** Each experiment's files are fractions of one enriched sample, in MaxQuant order:
  - `L`/`T` are the two eluates of the double digestion;
  - `FT` is the flow-through of the enrichment;
  - `MULTIP` is the SIMAC multiphosphorylated fraction. The search file names call the others `monop`.
- **Enrichment.** `characteristics[enrichment process]` = enrichment of phosphorylated protein (EFO:0010806) on all rows. The specific chemistry (IMAC, SIMAC, TiO2/MOAC) is in the factor value.
- **Super-SILAC channel map (SILAC SDRFs).** Every SILAC run has two rows. `SILAC light` is the AML patient sample. `SILAC heavy` is the `super-SILAC spike-in standard`, a pooled heavy-labelled (Arg6/Lys8) reference.
  - This follows from the super-SILAC design named in the PRIDE record and in the abstract, together with MaxQuant's Labels0 (light, none) and Labels1 (Arg6;Lys8) for every file. It is the definition of a super-SILAC experiment, not an inference about individual channels.
  - The heavy rows have `characteristics[biological replicate]` = `pooled`, because the reference is a pool and not one biological source. The contract allows `integer or pooled`.
  - The heavy rows share one source name. Their `comment[technical replicate]` is numbered 1..N in sample-row order, so the (source, biological replicate, technical replicate, fraction) coordinate stays unique. This follows the convention used for the other super-SILAC datasets in this campaign (PXD001963, PXD003138). The numbering does not mean the heavy standard was prepared N separate times.
- **Factor.** `factor value[sample preparation protocol]`, for example "FASP (SDS lysis), double digestion, SIMAC phosphopeptide enrichment". Heavy rows are `not applicable`.
- **Row count.** 42 files × 2 SILAC channels = 84 rows.

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

Previous SHA-256: `a303d9e6511706d20a32e68a82ce9f1496dc9a9740b16353a99f26ded64c404f`. The independent review returned FAIL with one important finding, which this round addresses.

- **Finding:** every row said Trypsin, but the 14 `DD_L_*` runs are Lys-C digests: 92–96% of peptides end in K, and 30–56% contain an uncleaved R. The 14 `DD_T_*` runs are 60–71% R-terminal.
- **Change:** there are now two cleavage columns. The 14 `DD_L_*` files (28 rows) are Lys-C | not applicable. The 14 `DD_T_*` files and the 14 single-digest `SD_*` files are Trypsin | not applicable.
- **Method:** `scratchpad/PXD003822/postprocess_cleavage.py` runs on the `build` output. It (1) sets the existing cleavage column per data file and (2) inserts a second `comment[cleavage agent details]` column directly after it. It asserts that every built row had Trypsin, and it checks each assignment against the C-terminal statistics. It then confirms that dropping both cleavage columns gives back the build output minus its one cleavage column, cell for cell. A diff against the previous SDRF confirmed that the only changes are listed here. The SDRF was never hand-edited.
- `characteristics[biological replicate]` on the super-SILAC heavy rows went from `1` to `pooled`, for consistency with the fresh/frozen SDRFs and because the reference is a pool. This was changed in `samples.tsv` and rebuilt.

## Validation

All commands were run from the sdrf-skills checkout, one at a time.

- `timeout 900 .venv/bin/parse_sdrf validate-sdrf -s /home/thanadol/Documents/GitHub/NordicSDRF/annotations/PXD003822-methodopt-phospho.sdrf.tsv -t ms-proteomics -t human --use_ols_cache_only`
  - Round 1: 0 errors and 0 warnings. `sdrf-tools structure` then flagged `technical-replicate-not-contiguous`: the replicates were first numbered 2/3 after MaxQuant's `2nd_rep`/`3rd_rep`.
  - Round 2, after renumbering to 1/2 in `samples.tsv` and rebuilding: 0 errors and 0 warnings.
  - Repair round, on the post-processed file: 0 errors and 0 warnings.
- `.venv/bin/python -m tools structure <sdrf>`: OK (acquisition, template declaration and column order are consistent).
- `.venv/bin/python -m tools check <sdrf>`: CLEAN. All controlled terms were verified against OLS, with no UNIMOD swaps and no label mismatches.
- `.venv/bin/python -m tools reconcile <sdrf> --record scratchpad/PXD003822/project.json --accession PXD003822`: see below.
  - BLOCKER `cleavage_agent_unsupported` (Lys-C, Trypsin). The PRIDE prose names no enzyme. Both are kept on the peptide-terminus evidence described under Technical values.

## Limitations

- **Flow-through files** (`*_FT`) are the material not retained by the enrichment step. The term "enrichment of phosphorylated protein" describes the workflow the sample went through, not each file's phospho content.
- **Replicate renumbering.** Technical replicates 1 and 2 correspond to MaxQuant `2nd_rep` and `3rd_rep`. The `1st_rep` raw files were not deposited.
- **Same AML material** across workflows is not stated, so `individual` = not available.
- **Super-SILAC standard.** Its composition (which heavy-labelled cell lines) is not in the evidence. The heavy rows therefore carry `pooled sample` = pooled, `individual` = pooled, `material type` = cell line (SILAC metabolic labelling requires cultured cells), `disease` = not available and `cell type` = not available.
- **Cleavage agent.** The Lys-C/trypsin split is evidenced by the deposited peptide data and the eluate tags in the file names. The paper's Methods were not read, so enzyme ratios and digestion times are unknown. For the in-solution double digests, the second enzyme is identified only from the peptide termini (a raised K-terminal and uncleaved-R share). `reconcile` flags Lys-C and Trypsin as unsupported because the PRIDE prose names no enzyme.
- **Paper not read.** The J Proteomics paper is closed access, so only the abstract, the PRIDE protocol text and the deposited MaxQuant files were used. Any detail that lives only in the paper's Methods is absent or marked `not available`. This includes patient demographics, cell isolation (blood or bone marrow, density-gradient or not), the super-SILAC cell-line composition, enzyme amounts and digestion times, reduction/alkylation reagents, LC gradient and precursor tolerance.
- **Organism part and cell type** are `not available`. The abstract says only "AML cells" and "cell lysates from patients with AML". PRIDE's dropdown lists CL:0000055 "non-terminally differentiated cell", which is obsolete in CL (the suggested replacement is progenitor cell, CL:0011026), so it was not used. Blood versus bone marrow origin is not stated in the evidence I could read.
- **Age, sex and ancestry** are `not available` (ancestry omitted). No per-patient table was available.
- **Precursor mass tolerance** is not recorded, because MaxQuant 1.5 `parameters.txt` does not report it.
- **Instrument.** The model is `Orbitrap Elite`, from the method text and folder names. One header field says "Orbitrap Velos Pro" (see Technical values). Only 8 of 163 raw files were range-read. The other files' CID/ion-trap settings are assumed to be the same, because they share the five method templates and the same MaxQuant ITMS tolerance.
