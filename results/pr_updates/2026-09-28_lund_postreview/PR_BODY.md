## Post-review corrections for 19 Lund SDRFs

These annotations were merged before an independent adversarial review (sdrf-skills `sdrf-adversarial-review`) had finished. That review failed several of the merged files, including six from an earlier batch (PXD021241, PXD023244, PXD023708, PXD024448, PXD024508, PXD026371). This PR replaces them with the versions that passed: no blocker or important findings, minor notes only. All changed files are my own earlier contributions. No rows are added or removed, and every file keeps the same RAW-file mapping.

### Changes to every file: HCD term
Every file with a dissociation column (all except PXD021241, which has none) changes `comment[dissociation method]` from `NT=higher energy beam-type collision-induced dissociation;AC=MS:1002481` to `NT=beam-type collision-induced dissociation;AC=MS:1000422`. The SDRF-Proteomics README says: "the canonical accession is MS:1000422 … Do not use PRIDE:0000590 or MS:1002481."

### Changes to individual datasets

| Dataset (merged PR) | What was wrong | Evidence | New value |
|---|---|---|---|
| PXD021241 | Repeated seminal-plasma samples of a bull could only be told apart by source name, and the sampling season (the design's Batch 1/2/3) was missing. | deposited `first_cohort_design.tsv`; abstract: "sampled across three seasons" | Adds `characteristics[individual]` = bull and `comment[sample preparation batch]` = design batch 1/2/3 |
| PXD023244 | `disease = normal` on 35 rows of wound fluid from surgical patients (post-mastectomy drainage, skin-graft dressings) | paper Methods | `not available`; infected dressings stay `staphylococcal infection` |
| PXD023708 (`-dda`/`-dia`) | `190411_DDA_B414_nr2b.raw` was put in the DDA file because of its name, but its RAW header names the DIA method (and it is DIA-sized, with a Spectronaut .htrms). The pyroglutamate modification was the Gln form, but PRIDE and the paper say "N-term Glu to pyroglutamic acid". | RAW headers of all 135 files; PRIDE/paper Methods | The file moves to `-dia` (DDA 65 / DIA 70 rows). Modification becomes `Glu->pyro-Glu` (UNIMOD:27, E). |
| PXD024448 | Biological replicate was `1` for all 105 men. Infertile patients had `compound = not applicable` although Table 1b reports current medication for some. The phenotype contained a curator note. | paper Table 1b; file names | Biological replicate = subject number within group (healthy 1–30, infertile 1–75). Compound = `not available` for infertile patients. Phenotype = `man investigated for infertility`. Technical replicates are numbered in file order. |
| PXD024508 | Trypsin was missing (the protocol uses Lys-C then trypsin). The cells' α-syn A53T-GFP overexpression was not recorded. The HeLa QC row had no Cellosaurus ID. | paper Methods; PRIDE: "HEK293T overexpressing alpha-synucleinA53T-GFP", "treated 48 hours" | Second cleavage-agent column = Trypsin. Adds genetic modification / genotype / exposure duration 48 hour. HeLa = CVCL_0030. |
| PXD026371 | `modification parameters = not available`, although the samples were alkylated with iodoacetamide and PRIDE lists iodoacetamide-derivatized residues | PRIDE protocol and PTM list | Carbamidomethyl C, fixed |
| PXD021394 (#1025) | `sex = female` for all 24 tumours. The paper's "collected from women" refers to sample set 1 (21 specimens), but these 24 tumours are set 2, from a separate 109-sample study that does not state sex. | De Marchi et al., J Proteome Res 2021 (PMC8155562), Patients section | `sex = not available`. Adds `characteristics[clinical data]` = ER/PgR status and IntClust from the deposited `Sample.information.xlsx`. |
| PXD023075 (#1026) | HCD term only | spec README | — |
| PXD024286 (#1030) | HD rows had `sex = male`, but the donor codes in the file names (HD1, HD4, HDKP, …) cannot be matched to the paper's HD1–HD10 table, and that table lists HD4 as female. Biological replicate was `1` for every donor. | paper donor table; PRIDE file names | `sex = not available`. Biological replicate = donor number within its disease group; fibroblast and iN samples from the same donor share it. |
| PXD026690 (#1067) | Used `factor value[sampling date]`, which is not a spec column, with US-format dates. | spec | `characteristics[collection date]` and `factor value[collection date]` in ISO 8601 (e.g. 2019-07-18) |
| PXD027173 (#1068) | Control phenotype was free text: "control (no AD pathology)". | — | `control` |
| PXD027259 (#1069) | Ages used an unsupported `…Y6M` form. Brain-metastasis rows carried the primary tumour's stage. | Table S1 and its README sheet (ages given in half-years) | Whole-year age ranges covering each reported age; metastasis rows use age at brain-metastasis diagnosis. Metastasis rows now have `disease staging = stage IV` (distant, M1 disease). |
| PXD029028 (#1075) | Biological replicate was `1` for all four donors. The library SDRF had no cell-line columns. | design / paper | Biological replicate: FL4=1, FL5=2, FL11=3, FL12=4. The `-dda-library` file gains cell line and Cellosaurus columns (Sai2 CVCL_A5DT, HFL1 CVCL_0298; `not applicable` for primary cells) and drops the free-text phenotype column. |
| PXD029135 (#1070) | Biological replicate was `1` for every donor. | file names RC1…RC11 | Biological replicate = donor number (1–10), shared across the conditions each donor contributes to |
| PXD029805 (#1076), `-dda`/`-dia` | Disease for NCI-H841, DMS 114, NCI-H196 and NCI-H1341 had been replaced with later Cellosaurus reclassifications that no saved evidence supported. Organism part mixed tumour organ with metastatic site. | paper Table 1, PRIDE, sdrf-skills cell-line snapshot, Cellosaurus API records | Disease = small cell lung carcinoma, as in the paper and PRIDE. Organism part = `lung` for every line; the metastatic site stays in `sampling site`. SW1271 sampling site = lung and cell type = epithelial cell. Adds `characteristics[culture medium]` = RPMI 1640 (Methods; `not available` for the three reference lines) and `comment[lc batch]` = MS batch 1/2 from the deposited design sheet, because the paper batch-corrects. |
| PXD029821 (#1077), `-dda`/`-dia` | Same disease, SW1271, culture medium and batch issues as PXD029805 | same | Same fixes; organism part stays `culture medium` (conditioned media) |
| PXD030043 (#1071) | Developmental stage was `embryo` although the embryos are timed at E14.5. Sex was `not available` although the paper states the pools used equal numbers of male and female mice. | Methods: "equal numbers of male and female mice"; "Adult mice … 10–20 weeks old" | `embryonic day 14.5` (EFO:0002565), `sex = pooled`, adds `characteristics[age]` = 10W-20W for the adult rows |
| PXD032285 (#1073), PXD032369 (#1074) | SUM44PE disease was too generic. Cell type was `not available`. No cell-line factor although the cell line is the studied variable. Precursor tolerance was missing. | Cellosaurus; paper Methods | `invasive lobular breast carcinoma`, `epithelial cell`, adds `factor value[cell line]` and `comment[precursor mass tolerance]` = 4.5 ppm |

PXD021245, PXD026661 and PXD032213 are unchanged, because the merged files already match the reviewed versions.

### Validation
- `parse_sdrf validate-sdrf --use_ols_cache_only`: passed for every file, with warnings only (free-text phenotypes, cell-line short names, `pooled`, `RPMI 1640` label).
- `.github/scripts/sdrf_review.py --baseline <main>`: run locally on all 23 changed files.
- `git diff --name-status`: every change is `M` under the 19 accession folders above; no file is added or deleted.
- Independent adversarial review: PASS for each file at exactly the content in this PR (review reports are hash-bound).

### Sources
PRIDE project pages for each accession, the publications cited in each merged PR, the deposited design sheets (PXD029805/PXD029821: `SCLC_Experimental_design_cell_*.xlsx`; PXD021394: `Sample.information.xlsx`) and Cellosaurus.

Annotation and review were agent-assisted (sdrf-skills); I checked the evidence for every change above.
