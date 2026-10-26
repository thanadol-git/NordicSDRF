# PXD003822-freshfrozen-phospho

Status: validated annotation; independent review pending.

- Title: Human AML patient samples, Method Optimization, LC-MSMS
- Lab: Frode S. Berven (PI) and Elise Aasebø (submitter), PROBE proteomics unit, Department of Biomedicine, University of Bergen, Bergen, Norway.
- Paper: Aasebø E, Mjaavatten O, Vaudel M, Farag Y, Selheim F, Berven F, Bruserud Ø, Hernandez-Valladares M. "Freezing effects on the acute myeloid leukemia cell proteome and phosphoproteome revealed using optimal quantitative workflows." J Proteomics 2016;145:214-225. doi:10.1016/j.jprot.2016.03.049, PMID 27107777. The paper is subscription-only: Europe PMC has no PMC copy, Unpaywall reports it as closed, and ScienceDirect returned HTTP 403. **Only the abstract was read.**
- Existing upstream annotation: none. `bigbio/sdrf-annotated-datasets` returned 404 for both `datasets/PXD003822` and `sandbox/PXD003822`.
- SDRF: `annotations/PXD003822-freshfrozen-phospho.sdrf.tsv`
- Rows: 16; columns: 37
- SHA-256: `70a2fa7643fdc5289c16423fb2bbee897c9a10939f82850c1ba47af8a692aba4`
- Evidence manifest: `annotations/PXD003822-freshfrozen-phospho.evidence.json`

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

Fresh vs frozen, super-SILAC phosphoproteome arm. There is one IMAC-enriched run per patient and storage state, 8 raw files in total. These files come from the same MaxQuant search as the proteome SDRF, in its Phospho (STY) parameter group.

| Source name (light) | individual | MaxQuant experiment | File |
|---|---|---|---|
| FF patient 1 fresh / frozen | FF_patient_1 | Exp_1A / Exp_1B | HR82_FRESH / HR82_FROZEN |
| FF patient 2 fresh / frozen | FF_patient_2 | Exp_2A / Exp_2B | 17_FRESH / 17_FROZEN |
| FF patient 3 fresh / frozen | FF_patient_3 | Exp_3A / Exp_3B | 23_FRESH / 23_FROZEN |
| FF patient 4 fresh / frozen | FF_patient_4 | Exp_4A / Exp_4B | FIL_FRESH / FIL_FROZEN |

- **Mapping source.** The file names state FRESH or FROZEN. `Search_FreshFrozen_SS/summary.txt` places each file in the matching patient experiment (Fraction 5 of Exp_nA/B) and searches it with Phospho (STY). The patient codes HR82, 17, 23 and FIL are carried in the assay names.
- **Biological replicate.** `characteristics[biological replicate]` is the patient number (1–4), shared by each patient's fresh and frozen samples. In the super-SILAC search the patient codes are HR82 = 1, 17 = 2, 23 = 3 and FIL = 4. The QC pool and the super-SILAC heavy standard are `pooled`, which the contract allows ("integer or pooled").
- **Enrichment.** `characteristics[enrichment process]` = `IMAC` (PRIDE:0000587, a child of EFO:0009090 enrichment process). The PRIDE text says the fresh/frozen study used IMAC phosphopeptide enrichment, and the raw-file folder is `2015-10-28_Orbitrapelite_FreshvsFrozen_phospho`.
- **Super-SILAC channel map (SILAC SDRFs).** Every SILAC run has two rows. `SILAC light` is the AML patient sample. `SILAC heavy` is the `super-SILAC spike-in standard`, a pooled heavy-labelled (Arg6/Lys8) reference.
  - This follows from the super-SILAC design named in the PRIDE record and in the abstract, together with MaxQuant's Labels0 (light, none) and Labels1 (Arg6;Lys8) for every file. It is the definition of a super-SILAC experiment, not an inference about individual channels.
  - The heavy rows have `characteristics[biological replicate]` = `pooled`, because the reference is a pool and not one biological source. The contract allows `integer or pooled`.
  - The heavy rows share one source name. Their `comment[technical replicate]` is numbered 1..N in sample-row order, so the (source, biological replicate, technical replicate, fraction) coordinate stays unique. This follows the convention used for the other super-SILAC datasets in this campaign (PXD001963, PXD003138). The numbering does not mean the heavy standard was prepared N separate times.
- **Factor.** `factor value[sample storage]`: freshly lysed or liquid nitrogen storage. Heavy rows are `not applicable`.
- **Row count.** 8 files × 2 SILAC channels = 16 rows.

## Technical values (all SDRFs)

- **Instrument**: `Orbitrap Elite` (MS:1001910).
  - PRIDE says "LTQ Orbitrap Elite". The embedded instrument method in the raw-file header reads "Orbitrap Elite MS" with tune file `Elite_nano`. The acquisition folders are named `..._OrbitrapElite_...` and the method names specify 240K resolution, which a Velos Pro cannot reach.
  - The headers also contain an "Orbitrap Velos Pro" string in the audit/header block. I treated it as a legacy device-name field, not the model.
  - Eight raw files spanning all six sub-experiments were checked, using an HTTP range read of the first 3 MB of each.
- **Acquisition**: DDA (PRIDE:0000627). In the sampled headers, MS1 is FTMS (300–2000 m/z) and MS2 is ITMS CID at normalized collision energy 35.0. The phospho runs use a top-15 CID method with multistage activation (`53b-TOP15nCID-MSA`).
  - This gives `comment[dissociation method]` = collision-induced dissociation (MS:1000133), `comment[collision energy]` = 35 NCE, and `comment[ms2 mass analyzer]` = linear ion trap (MS:1000291).
- **Fragment mass tolerance**: 0.6 Da, the MaxQuant `MS/MS tol. (ITMS)` in each `parameters.txt`. MS2 was in the ion trap.
- **Precursor mass tolerance**: omitted. The deposited `parameters.txt` (MaxQuant 1.5) does not report it, and no `mqpar.xml` was deposited.
- **Cleavage agent**: Trypsin (MS:1001251). This sub-dataset is FASP single digestion: the PRIDE text says "By using the best working methods (FASP single digested ...". `summary.txt` gives Enzyme = Trypsin, mode Specific, for every annotated raw file.
- **Modifications**: from `parameters.txt` (fixed) and `summary.txt` (variable and labels).
  - Fixed: Carbamidomethyl (C).
  - Variable: Acetyl (Protein N-term) and Oxidation (M), plus Phospho (STY) in the phospho SDRFs only.
  - Super-SILAC heavy labels Arg6 = Label:13C(6) (UNIMOD:188) on R and Lys8 = Label:13C(6)15N(2) (UNIMOD:259) on K. These are encoded as Variable, which is the `sdrf-tools search-params` output for a MaxQuant SILAC search.
- **Labels**: the SILAC sub-experiments have MaxQuant multiplicity 2, with Labels0 = light and Labels1 = Arg6;Lys8. The label-free ones have multiplicity 1.

## Repair round (after independent review)

Previous SHA-256: `015a0844b234370a730e518e984be0de59fa8d2d94fe402d48eb0bd84026a620`. The independent review returned FAIL with one important finding, which this round addresses.

- **Finding:** `characteristics[biological replicate]` was 1 for all four patients within each condition, so patients were not distinguished as biological replicates.
- **Change:** biological replicate is now the patient number (1–4) for both fresh and frozen samples, and `pooled` for the 8 super-SILAC heavy rows. This was changed in `samples.tsv` and rebuilt with `sdrf-tools build`, with no post-processing. A diff against the previous SDRF confirmed that only the listed cells changed.
- Minor finding: `characteristics[enrichment process]` changed from the generic `enrichment of phosphorylated protein` to `IMAC` (PRIDE:0000587).
- **One combined search.** `PXD003822-freshfrozen-silac` (24 proteome files) and `PXD003822-freshfrozen-phospho` (8 IMAC files) come from one combined MaxQuant search, `Search_FreshFrozen_SS.zip`. It is split by parameter group: the phospho group searches Phospho (STY) and the proteome group does not.

## Validation

All commands were run from the sdrf-skills checkout, one at a time.

- `timeout 900 .venv/bin/parse_sdrf validate-sdrf -s /home/thanadol/Documents/GitHub/NordicSDRF/annotations/PXD003822-freshfrozen-phospho.sdrf.tsv -t ms-proteomics -t human --use_ols_cache_only`
  - Round 1: 4 errors (`characteristics[individual]` 'FF patient N' does not match the identifier pattern).
  - Round 2, after changing the value to `FF_patient_N` and rebuilding: 0 errors and 0 warnings.
  - Repair round: 0 errors and 0 warnings.
- `.venv/bin/python -m tools structure <sdrf>`: OK (acquisition, template declaration and column order are consistent).
- `.venv/bin/python -m tools check <sdrf>`: CLEAN. All controlled terms were verified against OLS, with no UNIMOD swaps and no label mismatches.
- `.venv/bin/python -m tools reconcile <sdrf> --record scratchpad/PXD003822/project.json --accession PXD003822`: see below.
  - BLOCKER `cleavage_agent_unsupported` (Trypsin). The PRIDE prose does not name the enzyme, but the deposited MaxQuant `summary.txt` gives Enzyme = Trypsin (Specific) for every file, so it was kept.

## Limitations

- **Patient numbering** FF_patient_1 to 4 links each phospho file to the proteome SDRF via the shared MaxQuant experiment (Exp_n). The link to the label-free FF runs is by naming scheme only.
- **Enrichment chemistry.** IMAC comes from the PRIDE protocol text ("IMAC phosphopeptide enrichment" for the fresh/frozen comparison). No deposited file states it per run.
- **Super-SILAC standard.** Its composition (which heavy-labelled cell lines) is not in the evidence. The heavy rows therefore carry `pooled sample` = pooled, `individual` = pooled, `material type` = cell line (SILAC metabolic labelling requires cultured cells), `disease` = not available and `cell type` = not available.
- **Cleavage agent.** `reconcile` flags Trypsin as unsupported because the PRIDE prose never names the enzyme. The value comes from the deposited MaxQuant `summary.txt` (Trypsin, Specific, every file), and the fresh/frozen arm used FASP single digestion, so it was kept.
- **Paper not read.** The J Proteomics paper is closed access, so only the abstract, the PRIDE protocol text and the deposited MaxQuant files were used. Any detail that lives only in the paper's Methods is absent or marked `not available`. This includes patient demographics, cell isolation (blood or bone marrow, density-gradient or not), the super-SILAC cell-line composition, enzyme amounts and digestion times, reduction/alkylation reagents, LC gradient and precursor tolerance.
- **Organism part and cell type** are `not available`. The abstract says only "AML cells" and "cell lysates from patients with AML". PRIDE's dropdown lists CL:0000055 "non-terminally differentiated cell", which is obsolete in CL (the suggested replacement is progenitor cell, CL:0011026), so it was not used. Blood versus bone marrow origin is not stated in the evidence I could read.
- **Age, sex and ancestry** are `not available` (ancestry omitted). No per-patient table was available.
- **Precursor mass tolerance** is not recorded, because MaxQuant 1.5 `parameters.txt` does not report it.
- **Instrument.** The model is `Orbitrap Elite`, from the method text and folder names. One header field says "Orbitrap Velos Pro" (see Technical values). Only 8 of 163 raw files were range-read. The other files' CID/ion-trap settings are assumed to be the same, because they share the five method templates and the same MaxQuant ITMS tolerance.
