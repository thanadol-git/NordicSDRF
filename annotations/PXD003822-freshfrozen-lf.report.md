# PXD003822-freshfrozen-lf

Status: validated annotation; independent review pending.

- Title: Human AML patient samples, Method Optimization, LC-MSMS
- Lab: Frode S. Berven (PI) and Elise Aasebø (submitter), PROBE proteomics unit, Department of Biomedicine, University of Bergen, Bergen, Norway.
- Paper: Aasebø E, Mjaavatten O, Vaudel M, Farag Y, Selheim F, Berven F, Bruserud Ø, Hernandez-Valladares M. "Freezing effects on the acute myeloid leukemia cell proteome and phosphoproteome revealed using optimal quantitative workflows." J Proteomics 2016;145:214-225. doi:10.1016/j.jprot.2016.03.049, PMID 27107777. The paper is subscription-only: Europe PMC has no PMC copy, Unpaywall reports it as closed, and ScienceDirect returned HTTP 403. **Only the abstract was read.**
- Existing upstream annotation: none. `bigbio/sdrf-annotated-datasets` returned 404 for both `datasets/PXD003822` and `sandbox/PXD003822`.
- SDRF: `annotations/PXD003822-freshfrozen-lf.sdrf.tsv`
- Rows: 11; columns: 33
- SHA-256: `92066e73b316503c00288625a126d1fdf0ef1eeed7190302228b44a8d9859f0e`
- Evidence manifest: `annotations/PXD003822-freshfrozen-lf.evidence.json`

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

Fresh vs frozen, label-free arm. Four AML patients each give a freshly lysed sample (A) and a liquid-nitrogen-stored sample (B). There are also 3 QC runs of a mix of all samples. The workflow is FASP single digestion, per the PRIDE text ("By using the best working methods (FASP single digested ...").

| Source name | individual | sample storage | File |
|---|---|---|---|
| FF patient 1 fresh / frozen | FF_patient_1 | freshly lysed / liquid nitrogen storage | 20151016_AML-FF1-A / -FF1-B |
| FF patient 2 fresh / frozen | FF_patient_2 | ... | 20151016_AML-FF2-A / -FF2-B |
| FF patient 3 fresh / frozen | FF_patient_3 | ... | 20151016_AML-FF3-A / -FF3-B |
| FF patient 4 fresh / frozen | FF_patient_4 | ... | 20151016_AML-FF4-A / -FF4-B |
| FF QC pool | pooled | pooled (mix of all samples) | 20151016_AML-FF_QC1, _QC2, _QC3 (technical replicates 1–3) |

- **Mapping source.** The deposited `Search_FreshFrozen-LF/summary.txt`, which names the experiments `1-A` … `4-B` and `QC1`–`QC3`. The PRIDE text describes "four fresh/frozen pairs and 3 quality controls (QC), which was a mix of all samples".
- **A = fresh, B = frozen.** In the super-SILAC fresh/frozen search, the enriched files `HR82_FRESH`, `17_FRESH`, … sit in MaxQuant experiments `Exp_1A`, `Exp_2A`, …, and the `*_FROZEN` files in `Exp_1B`, … . That establishes A = fresh and B = frozen for the `FF<n><A|B>` naming. Applying the same rule to the label-free `FF<n>-<A|B>` files is an inference from the shared naming scheme (see Limitations).
- **Biological replicate.** `characteristics[biological replicate]` is the patient number (1–4), shared by each patient's fresh and frozen samples. In the super-SILAC search the patient codes are HR82 = 1, 17 = 2, 23 = 3 and FIL = 4. The QC pool and the super-SILAC heavy standard are `pooled`, which the contract allows ("integer or pooled").
- **Factor.** `factor value[sample storage]`, which mirrors `characteristics[sample storage]` (free text; this column is outside the human/ms-proteomics templates).
- **Row count.** 11 files × 1 row = 11 rows.

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

Previous SHA-256: `73b98b8563bb38a2d56eeb2ce43c3880096e2d0b91074573fc8de0d3cd927349`. The independent review returned FAIL with one important finding, which this round addresses.

- **Finding:** `characteristics[biological replicate]` was 1 for all four patients within each condition, so patients were not distinguished as biological replicates.
- **Change:** biological replicate is now the patient number (1–4) for both fresh and frozen samples, and `pooled` for the 3 QC-pool rows. This was changed in `samples.tsv` and rebuilt with `sdrf-tools build`, with no post-processing. A diff against the previous SDRF confirmed that only the listed cells changed.

## Validation

All commands were run from the sdrf-skills checkout, one at a time.

- `timeout 900 .venv/bin/parse_sdrf validate-sdrf -s /home/thanadol/Documents/GitHub/NordicSDRF/annotations/PXD003822-freshfrozen-lf.sdrf.tsv -t ms-proteomics -t human --use_ols_cache_only`
  - Round 1: 4 errors: "Value 'FF patient N' does not match required pattern" in `characteristics[individual]`, where the identifier validator does not allow spaces.
  - Round 2, after changing the value to `FF_patient_N` in `samples.tsv` and rebuilding: 0 errors and 0 warnings.
  - Repair round: 0 errors and 0 warnings.
- `.venv/bin/python -m tools structure <sdrf>`: OK (acquisition, template declaration and column order are consistent).
- `.venv/bin/python -m tools check <sdrf>`: CLEAN. All controlled terms were verified against OLS, with no UNIMOD swaps and no label mismatches.
- `.venv/bin/python -m tools reconcile <sdrf> --record scratchpad/PXD003822/project.json --accession PXD003822`: see below.
  - BLOCKER `cleavage_agent_unsupported` (Trypsin). The PRIDE prose does not name the enzyme, but the deposited MaxQuant `summary.txt` gives Enzyme = Trypsin (Specific) for every file, so it was kept.
  - BLOCKER `labelled_annotated_as_label_free`. This fires because PRIDE registers SILAC as one of the project's two quantification methods. This sub-dataset is explicitly the label-free arm: the PRIDE protocol text names it a label-free dataset, and its MaxQuant search has multiplicity 1 with no labels. `label free sample` was kept.

## Limitations

- **A/B = fresh/frozen in the label-free files** is inferred. The evidence is the identical `FF<n>A/B` naming of the super-SILAC fresh/frozen files, where MaxQuant pairs Exp_nA with the `*_FRESH` phospho file and Exp_nB with `*_FROZEN`. No label-free file says FRESH or FROZEN explicitly.
- **Patient numbering across label-free and super-SILAC** (FF_patient_1 to 4) assumes that `AML-FF1` in the label-free runs is the same patient as `AML-SS-FF1A/B` in the SILAC runs. This also rests only on the shared naming scheme. The SILAC phospho files give patient codes HR82 (1), 17 (2), 23 (3) and FIL (4).
- **QC pool.** QC1–QC3 are encoded as three technical replicates (injections) of one pooled source. Whether they were three injections of one mix or three separate mixes is not stated.
- **Cleavage agent.** `reconcile` flags Trypsin as unsupported because the PRIDE prose never names the enzyme. The value comes from the deposited MaxQuant `summary.txt` (Trypsin, Specific, every file), and the fresh/frozen arm used FASP single digestion, so it was kept.
- **Paper not read.** The J Proteomics paper is closed access, so only the abstract, the PRIDE protocol text and the deposited MaxQuant files were used. Any detail that lives only in the paper's Methods is absent or marked `not available`. This includes patient demographics, cell isolation (blood or bone marrow, density-gradient or not), the super-SILAC cell-line composition, enzyme amounts and digestion times, reduction/alkylation reagents, LC gradient and precursor tolerance.
- **Organism part and cell type** are `not available`. The abstract says only "AML cells" and "cell lysates from patients with AML". PRIDE's dropdown lists CL:0000055 "non-terminally differentiated cell", which is obsolete in CL (the suggested replacement is progenitor cell, CL:0011026), so it was not used. Blood versus bone marrow origin is not stated in the evidence I could read.
- **Age, sex and ancestry** are `not available` (ancestry omitted). No per-patient table was available.
- **Precursor mass tolerance** is not recorded, because MaxQuant 1.5 `parameters.txt` does not report it.
- **Instrument.** The model is `Orbitrap Elite`, from the method text and folder names. One header field says "Orbitrap Velos Pro" (see Technical values). Only 8 of 163 raw files were range-read. The other files' CID/ion-trap settings are assumed to be the same, because they share the five method templates and the same MaxQuant ITMS tolerance.
