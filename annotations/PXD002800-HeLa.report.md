# PXD002800-HeLa

Status: validated annotation; independent review pending.

- Dataset: "Improved functional annotation of posttranslationally modified proteins" (PXD002800), Choudhary group, Novo Nordisk Foundation Center for Protein Research, University of Copenhagen, Denmark (lab PI / submitter Brian Tate Weinert). PRIDE submission 2015-08-27, public 2020-07-01.
- Paper: Schölz C, Lyon D, Refsgaard JC, Jensen LJ, Choudhary C, Weinert BT. Avoiding abundance bias in the functional annotation of post-translationally modified proteins. Nat Methods 2015;12(11):1003-1004. PMID 26513550, doi:10.1038/nmeth.3621. PRIDE lists no reference; the paper was found by an Europe PMC author/title search (the accession itself returns no hit). The full text is paywalled with no PMC copy, but the **Supplementary Methods PDF** (Nature ESM) was readable and is the main protocol source together with the PRIDE protocol fields.
- Not previously annotated: `datasets/PXD002800` and `sandbox/PXD002800` both return 404 in bigbio/sdrf-annotated-datasets.
- SDRF: `annotations/PXD002800-HeLa.sdrf.tsv`, 40 rows x 48 columns.
- SHA-256: `80b6b6ca2843ca25548818f7358fe935d41d90512544921ce1351ea7da35a51a`
- Evidence manifest: `annotations/PXD002800-HeLa.evidence.json`
- Companion SDRF: `annotations/PXD002800-yeast.sdrf.tsv` (46 yeast runs).

## Why the deposit is split

The deposit contains two organisms (HeLa cells and *S. cerevisiae* BY4742) searched separately: `MaxQuant_output.zip` has one folder per organism (`HeLa/`, `Yeast/`), each with five independent MaxQuant 1.2.7.1 searches against an organism-specific FASTA (HUMAN20140123.fasta / YEAST.fasta). The two organisms also need different template sets (`human` + `cell-lines` vs. none for fungi). The split is by organism; all 86 RAW files are annotated (40 here, 46 in the yeast file).

## Templates

`ms-proteomics` v1.1.0 + `human` v1.1.0 + `cell-lines` v1.1.0: label-free DDA of the human HeLa cell line (ATCC CCL-2). No DIA, single-cell, clinical or other experiment layer applies.

## Design and file mapping

The study maps PTMs (lysine acetylation, succinylation, ubiquitylation via di-Gly remnant, phosphorylation) and the proteome of one cell type to correct GO-enrichment analyses for abundance bias. There is no treatment or disease contrast; the compared variable is the enrichment (which modified-peptide population was measured vs. the unenriched proteome).

- Source = HeLa x enrichment. `characteristics[biological replicate]` = 1 throughout (one sample per enrichment; Supplementary Methods describe one digest from which enrichments and the proteome aliquot were taken).
- `factor value[enrichment process]` mirrors `characteristics[enrichment process]`: `enrichment of phosphorylated protein` (EFO:0010806) for phospho runs; `sample enrichment` (EFO:0009106) for the acetyl-lysine, succinyl-lysine and di-Gly immunoaffinity enrichments; `not applicable` for the proteome runs.
- `comment[technical replicate]`: the `_s_` and `_vs_` files are the **same autosampler vials** injected twice with two instrument methods, `SENSITIVE_180min_125MS2_R35k...` and `VERY-SENSITIVE_180min_250MS2_R70k...` (RAW headers). They are written as technical replicate 1 (sensitive) and 2 (very sensitive). The yeast di-Gly `summary.txt` names the two MaxQuant experiments `sens` and `verysens`, which confirms the meaning of the tags.
- Fractions: SCX stage-tip fractions, numbered by the file-name `F` number and confirmed by sequential vial positions.

| Source | Files | Rows | Tech rep | Fractions | Instrument |
|---|---|---|---|---|---|
| HeLa acetyl-lysine enrichment | `20140131_..._hela_acK_s_F01-F04` | 4 | 1 | 1-4 (vials B05-B08) | Q Exactive |
| HeLa acetyl-lysine enrichment | `20140131_..._hela_acK_vs_F01-F04` | 4 | 2 | 1-4 (vials B05-B08) | Q Exactive |
| HeLa succinyl-lysine enrichment | `20140204_..._hela_suK_F01-F04` (VERY-SENSITIVE only) | 4 | 1 | 1-4 (C05-C08) | Q Exactive |
| HeLa diGly-lysine enrichment | `20140128_..._hela_gg_s_F01`, `_F01_140130015100`, `_F01_140130075744`, `_F01_140130140448` | 4 | 1 | 1-4 (H05-H08) | Q Exactive |
| HeLa diGly-lysine enrichment | `20140128_..._hela_gg_vs_F01`, `_F01_140129224719`, `_F01_140130045414`, `_F01_140130110108` | 4 | 2 | 1-4 (H05-H08) | Q Exactive |
| HeLa proteome | `20140205_..._hela_proteome_F01-F08` | 8 | 1 | 1-8 (E01-E08) | Q Exactive |
| HeLa phosphopeptide enrichment set 1 | `20140810_QE2_..._hela_phos_F11-F16` | 6 | 1 | 11-16 (A02-A07) | Q Exactive Plus |
| HeLa phosphopeptide enrichment set 2 | `20140829_QE2_..._hs_hela_phos2-2_F01-F06` | 6 | 1 | 1-6 (D02-D07) | Q Exactive Plus |

How the mapping was established:
- Run to enrichment: the MaxQuant search folders (`HeLa/Acetylation`, `Succinylation`, `Ubiquitylation`, `Phosphorylation`, `Proteome`) list exactly these RAW files in their `summary.txt`. Every deposited HeLa RAW file appears in exactly one search, and the file-name tokens (`acK`, `suK`, `gg`, `phos`, `proteome`) agree.
- di-Gly fractions: all eight HeLa di-Gly files are named `F01`. Xcalibur appended a timestamp to each duplicate name. The RAW-header sequence rows give vials H05, H06, H07, H08 for each method series (yeast di-Gly F01-F04 sit in H01-H04 of the same plate), so the files are ordered by vial as fractions 1-4.
- Instrument: RAW headers read `Q Exactive - Orbitrap MS` for the QE4 files and `Q Exactive Plus - Orbitrap MS` for all 12 QE2 phospho files. PRIDE lists only Q Exactive, so the RAW headers win.

## Technical values

- Acquisition: DDA (Top10, RAW method). HCD at NCE 27.5 in all 40 RAW headers, Orbitrap MS2.
- Digest: Lys-C, then trypsin (Supplementary Methods), written as two `comment[cleavage agent details]` columns: Trypsin (MS:1001251) and Lys-C (MS:1001309). The MaxQuant protease was Trypsin/P with 2 missed cleavages. In the HeLa acetyl search, 98.7% of unique target peptides end in K or R.
- Reduction / alkylation: DTT (PRIDE:0000608) / chloroacetamide (PRIDE:0000600).
- Fractionation: SCX (PRIDE:0000561), micro-SCX stage tips for the proteome and microtip SCX for the enriched peptides.
- Tolerances: precursor 6 ppm (main search) and fragment 20 ppm, from the Methods and `parameters.txt` (MS/MS tol. (FTMS) 20 ppm).
- Modifications, read from `parameters.txt` and `summary.txt` of each search:
  - In every search: Carbamidomethyl (C) fixed, plus Oxidation (M) and Acetyl (Protein N-term) variable.
  - Acetylation search: also Acetyl (K) and the custom MaxQuant modification `_prop (K)`. Its mass was computed from `evidence.txt` (e.g. ADKLAEEHSS observed 1141.5251 Da), giving +56.0262 Da on K, which is Propionyl (UNIMOD:58).
  - Succinylation search: Succinyl (K) (UNIMOD:64).
  - Ubiquitylation search: GlyGly (K), written as `GG` (UNIMOD:121).
  - Phosphorylation search: Phospho (STY) (UNIMOD:21).
  - Proteome search: no extra modification, so the two PTM slots are `not applicable`.

## Build and post-processing

`samples.tsv` and `technical.tsv` were written in `scratchpad/PXD002800/` and expanded with `sdrf-tools build -t ms-proteomics -t human -t cell-lines`. `build` cannot write different values into the cells of a repeated column or repeat a non-multiple column. So `scratchpad/PXD002800/postprocess.py` then:
1. replaced the placeholders in modification-parameter columns 4-5 with each search's PTM-specific modifications (table above);
2. inserted a second `comment[cleavage agent details]` column (Lys-C) after the first;
3. set `comment[fraction identifier]` of `hela_phos_F11-F16` to 11-16, the submitter's numbering.

`scratchpad/PXD002800/diffcheck.py` confirmed that only these cells changed: 6 fraction cells, 80 modification cells, and the inserted column.

## Validation

- `timeout 900 parse_sdrf validate-sdrf -s PXD002800-HeLa.sdrf.tsv -t ms-proteomics -t human -t cell-lines --use_ols_cache_only`: exit 0, "Everything seems to be fine. Well done." (0 errors, 0 warnings).
- `sdrf-tools check`: exit 0, 24 terms checked, 24 verified, CLEAN.
- `sdrf-tools structure`: OK.
- `sdrf-tools reconcile --record pride.json --accession PXD002800`: exit 0, with one MAJOR `cleavage_agent_incomplete (missing Lys-C)`. This is a false positive: the tool reads one value of the repeated column, and Lys-C is declared in the second `comment[cleavage agent details]` column. Round 1 also raised a BLOCKER `run_names_name_a_cell_line` for `organism part = uterine cervix`. It was fixed in the tables: `organism part` is now `not applicable` and `sampling site` is `uterine cervix`, following `cellline.md`. The file was then rebuilt and re-validated (round 2).

## Limitations
- **Revised after independent review:** the acetyl-lysine, succinyl-lysine and diGly-lysine enrichments previously shared the generic EFO term `sample enrichment` in `characteristics[enrichment process]` and `factor value[enrichment process]`, which merged three experimental groups into one factor level. They now carry distinct free-text values (`enrichment of acetyl-lysine peptides`, `enrichment of succinyl-lysine peptides`, `enrichment of diglycine-lysine (ubiquitin remnant) peptides`); no specific EFO/PRIDE terms exist under EFO:0009090, and `parse_sdrf` reports these as warnings only.


- **Paper**: the full text is paywalled. Protocol facts come from the Supplementary Methods PDF and the PRIDE protocol fields; there is no per-sample table.
- **Enrichment process term**: no EFO/PRIDE term exists for acetyl-lysine, succinyl-lysine or di-Gly peptide immunoaffinity enrichment. These rows use the generic `sample enrichment` (EFO:0009106, a child of EFO:0009090), so the factor column alone does not separate those three sets. The source name and the PTM-specific `comment[modification parameters]` column do.
- **Biological replicate**: biological replicate is 1 for every source (inferred). Whether enrichments came from separate cultures is not documented.
- **HeLa phospho sets**: phospho set 1 (2014-08-10, vials A02-A07) and set 2 (`hs_hela_phos2-2`, 2014-08-29, vials D02-D07) are separate preparations searched together. Their relationship (replicate culture vs. second enrichment) is undocumented, so they are separate sources, each with biological replicate 1.
- **Fraction numbers 11-16**: set 1 keeps the file-name fraction numbers 11-16 (file names plus sequential vials). Fractions 1-10 of that series are not in the deposit.
- **Two MS methods**: SENSITIVE (MS2 35k, 125 ms) and VERY-SENSITIVE (MS2 70k, 250 ms) re-injections are encoded only as technical replicates 1 and 2, because SDRF has no instrument-method column. The HeLa succinyl runs exist only with the VERY-SENSITIVE method.
- **Cell-line fields**: sampling site, disease, cell type, sex, age (30Y6M) and ancestry (African American) are Cellosaurus CVCL_0030 donor facts, not study measurements. The identity HeLa ATCC CCL-2 comes from the Supplementary Methods.
- **Not available**: passage number, sample storage temperature and individual. Culture medium is DMEM (Supplementary Methods).
- **Collision energy**: 27.5 NCE from the RAW method blocks (all files).
- **Propionyl (K)**: identified from evidence masses. It is a search-space modification; no chemical propionylation step is described.
