# PXD002800-yeast

Status: validated annotation; independent review pending.

- Dataset: "Improved functional annotation of posttranslationally modified proteins" (PXD002800), Choudhary group, Novo Nordisk Foundation Center for Protein Research, University of Copenhagen, Denmark (lab PI / submitter Brian Tate Weinert). PRIDE submission 2015-08-27, public 2020-07-01.
- Paper: Schölz C, Lyon D, Refsgaard JC, Jensen LJ, Choudhary C, Weinert BT. Avoiding abundance bias in the functional annotation of post-translationally modified proteins. Nat Methods 2015;12(11):1003-1004. PMID 26513550, doi:10.1038/nmeth.3621. PRIDE lists no reference; the paper was found by an Europe PMC author/title search. The full text is paywalled with no PMC copy, but the **Supplementary Methods PDF** (Nature ESM) was readable.
- Not previously annotated: `datasets/PXD002800` and `sandbox/PXD002800` both return 404 in bigbio/sdrf-annotated-datasets.
- SDRF: `annotations/PXD002800-yeast.sdrf.tsv`, 46 rows x 35 columns.
- SHA-256: `7198c908b770033afcfaeefbe435c213cd38e7beb9bdeabd3fdfe38ccd6abbc5`
- Evidence manifest: `annotations/PXD002800-yeast.evidence.json`
- Companion SDRF: `annotations/PXD002800-HeLa.sdrf.tsv` (40 HeLa runs). The deposit splits by organism: there are separate MaxQuant searches per organism (`MaxQuant_output/Yeast/` vs `HeLa/`, separate FASTA files), and the template sets differ. See the HeLa report.

## Templates

`ms-proteomics` v1.1.0 only. The sample is wild-type *Saccharomyces cerevisiae*, a fungus; no organism template (`human`, `vertebrates`, `invertebrates`, `plants`) fits. It is label-free DDA, so no experiment layer applies. `characteristics[strain or breed]` (GENO:0000112, a spec term) was added to record BY4742.

## Design and file mapping

The study maps lysine acetylation, succinylation, ubiquitylation (di-Gly remnant) and phosphorylation, plus the proteome, in yeast. There is no treatment contrast; the compared variable is the enrichment.

- Source = yeast x enrichment. `characteristics[biological replicate]` = 1 throughout. The Supplementary Methods describe one culture (BY4742 in synthetic complete medium, harvested at OD600 ~0.5) and one digest, from which enrichments and the proteome aliquot were taken.
- `factor value[enrichment process]` mirrors `characteristics[enrichment process]`: `enrichment of phosphorylated protein` (EFO:0010806); `sample enrichment` (EFO:0009106) for acetyl-lysine, succinyl-lysine and di-Gly immunoaffinity enrichments; `not applicable` for the proteome.
- `comment[technical replicate]`: the `_s_` and `_vs_` files share autosampler vials (RAW headers) and differ only by instrument method, `SENSITIVE_..._125MS2_R35k` vs `VERY-SENSITIVE_..._250MS2_R70k`. They are written as technical replicate 1 (sensitive) and 2 (very sensitive). The yeast di-Gly `summary.txt` names the two experiments `sens` and `verysens`.
- Phospho: the `ip1_s` and `ip1_vs` files are the same vials (F01-F06). The `ip2_s` files sit in different vials (F07-F12), so `ip2` is a distinct phospho sample and gets its own source.

| Source | Files | Rows | Tech rep | Fractions (vials) |
|---|---|---|---|---|
| yeast acetyl-lysine enrichment | `20140131_..._sc_acK_s_F01-F04` | 4 | 1 | 1-4 (B01-B04) |
| yeast acetyl-lysine enrichment | `20140131_..._sc_acK_vs_F01-F04` | 4 | 2 | 1-4 (B01-B04) |
| yeast succinyl-lysine enrichment | `20140204_..._sc_suK_F01-F04` (VERY-SENSITIVE only) | 4 | 1 | 1-4 (C01-C04) |
| yeast diGly-lysine enrichment | `20140128_..._sc_gg_s_F01-F04` | 4 | 1 | 1-4 (H01-H04) |
| yeast diGly-lysine enrichment | `20140128_..._sc_gg_vs_F01-F04` | 4 | 2 | 1-4 (H01-H04) |
| yeast proteome | `20140205_..._sc_proteome_F01-F08` | 8 | 1 | 1-8 (D01-D08) |
| yeast phosphopeptide enrichment ip1 | `20140207_..._sc_phos_ip1_s_F01-F06` | 6 | 1 | 1-6 (F01-F06) |
| yeast phosphopeptide enrichment ip1 | `20140207_..._sc_phos_ip1_vs_F01-F06` | 6 | 2 | 1-6 (F01-F06) |
| yeast phosphopeptide enrichment ip2 | `20140207_..._sc_phos_ip2_s_F01-F06` (SENSITIVE only) | 6 | 1 | 1-6 (F07-F12) |

How the mapping was established:
- Run to enrichment: the MaxQuant search folders `Yeast/Acetylation`, `Succinylation`, `Ubiquitylation`, `Phosphorylation` and `Proteome` list exactly these RAW files in `summary.txt`, and the file-name tokens agree.
- Re-injections and distinct samples: autosampler vial and instrument-method name from range-read RAW headers.
- Instrument: Q Exactive (MS:1001911). The RAW headers read `Q Exactive - Orbitrap MS` for all 46 yeast files, consistent with PRIDE and `summary.txt`.

## Technical values

Same protocol and settings as the HeLa file (shared Supplementary Methods; MaxQuant 1.2.7.1, identical `parameters.txt` apart from the FASTA file and site tables):
- DDA, Top10; HCD at NCE 27.5 (all 46 RAW headers); Orbitrap MS2.
- Lys-C then trypsin, written as two `comment[cleavage agent details]` columns: Trypsin (MS:1001251) and Lys-C (MS:1001309). The MaxQuant protease was Trypsin/P with 2 missed cleavages.
- DTT / chloroacetamide; SCX fractionation (PRIDE:0000561); precursor 6 ppm, fragment 20 ppm.
- Modifications:
  - In every search: Carbamidomethyl (C) fixed; Oxidation (M) and Acetyl (Protein N-term) variable.
  - Acetylation search: Acetyl (K) (UNIMOD:1) and Propionyl (K) (UNIMOD:58). The latter is MaxQuant's custom `_prop (K)`, +56.0262 Da on K, mass computed from the HeLa acetyl `evidence.txt` of the same modification set.
  - Succinylation search: Succinyl (K) (UNIMOD:64).
  - Ubiquitylation search: GG (K) (UNIMOD:121).
  - Phosphorylation search: Phospho (STY) (UNIMOD:21).
  - Proteome search: `not applicable` in the two PTM slots.

## Build and post-processing

The SDRF was built with `sdrf-tools build -t ms-proteomics` from `scratchpad/PXD002800/samples_yeast.tsv` and `technical.tsv`. `scratchpad/PXD002800/postprocess.py` then filled the per-search PTM modification columns and inserted the second (Lys-C) `comment[cleavage agent details]` column. `diffcheck.py` confirmed only those cells changed: 92 modification cells and the inserted column. No fraction numbers were changed in this file.

## Validation

- `timeout 900 parse_sdrf validate-sdrf -s PXD002800-yeast.sdrf.tsv -t ms-proteomics --use_ols_cache_only`: exit 0, "Everything seems to be fine. Well done." (0 errors, 0 warnings).
- `sdrf-tools check`: exit 0, 19 terms checked, 19 verified, CLEAN.
- `sdrf-tools structure`: OK.
- `sdrf-tools reconcile --record pride.json --accession PXD002800`: exit 0, with one MAJOR `cleavage_agent_incomplete (missing Lys-C)`. This is a false positive: the tool reads one value of the repeated column, and Lys-C is declared in the second `comment[cleavage agent details]` column.

## Limitations
- **Revised after independent review:** the acetyl-lysine, succinyl-lysine and diGly-lysine enrichments previously shared the generic EFO term `sample enrichment` in `characteristics[enrichment process]` and `factor value[enrichment process]`, merging three groups into one factor level. They now carry distinct free-text values (`enrichment of acetyl-lysine peptides`, `enrichment of succinyl-lysine peptides`, `enrichment of diglycine-lysine (ubiquitin remnant) peptides`); no specific EFO/PRIDE terms exist under EFO:0009090, and `parse_sdrf` reports these as warnings only.


- **Paper**: the full text is paywalled. Facts come from the Supplementary Methods PDF and the PRIDE protocol fields; there is no per-sample table.
- **Enrichment process term**: acetyl-lysine, succinyl-lysine and di-Gly immunoaffinity enrichments use the generic `sample enrichment` (EFO:0009106) because no specific term exists. They are distinguished by source name and by the PTM-specific `comment[modification parameters]` column.
- **Biological replicate**: biological replicate is 1 for every source (inferred, one culture/digest described).
- **Phospho ip1/ip2**: these are two separate phospho samples (distinct vials). What `ip1`/`ip2` denote (e.g. which IP flow-through they derive from) is not documented. They are distinct sources, each with biological replicate 1.
- **Two MS methods**: SENSITIVE and VERY-SENSITIVE re-injections are encoded only as technical replicates 1 and 2. The succinyl runs exist only with VERY-SENSITIVE, and phospho `ip2` only with SENSITIVE.
- **Not encoded**: culture medium (synthetic complete, US Biological) and growth phase (mid-exponential, OD600 ~0.5) are documented but have no column in `ms-proteomics` alone.
- **Organism**: species-level *Saccharomyces cerevisiae* (NCBITaxon:4932, as in PRIDE). The strain is BY4742 (an S288C derivative) per the Supplementary Methods.
- **Organism part, cell type, disease**: `not applicable` (a unicellular wild-type culture).
- **Collision energy**: 27.5 NCE from the RAW method blocks.
