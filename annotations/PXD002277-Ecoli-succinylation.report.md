# PXD002277-Ecoli-succinylation
Status: validated annotation; independent review pending.

## Dataset

- Title: *Lysine succinylation is a frequently occurring modification in prokaryotes and eukaryotes and extensively overlaps with acetylation*.
- Lab: Chunaram Choudhary, The NNF Center for Protein Research, University of Copenhagen (Copenhagen, Denmark); submitter Brian T. Weinert.
- Paper: Weinert BT, Schölz C, Wagner SA, Iesmantavicius V, Su D, Daniel JA, Choudhary C. *Cell Rep* 2013;4(4):842-51, doi:10.1016/j.celrep.2013.07.024, PMID 23954790. Only the PubMed abstract and MeSH headings could be read (see Limitations).
- Not already annotated upstream: `bigbio/sdrf-annotated-datasets` `datasets/PXD002277` and `sandbox/PXD002277` both return 404.
- The deposit has 57 Thermo RAW files and one `MaxQuant_output_files.zip`. The zip holds six separate MaxQuant 1.2.7.1 searches (`E_coli_succinylation`, `yeast_succinylation`, `hela_succinylation`, `hela_acetylation`, `mouse_liver_succinylation`, `mouse_liver_acetylation`) plus `List_of_RAW_files.xlsx`, a submitter table that assigns every RAW file to a supplementary table and gives the SILAC channel notes.
- The deposit is split into six SDRFs, one per deposited MaxQuant search, because it spans four organisms (organism templates are mutually exclusive, and there is none for bacteria or yeast) and each organism and acyl type was searched separately with its own FASTA and modifications. This SDRF covers the `E_coli_succinylation` search. Together the six SDRFs cover all 57 RAW files exactly once.

## Output

- SDRF: `annotations/PXD002277-Ecoli-succinylation.sdrf.tsv`
- 17 data rows x 32 columns (13 RAW files; the 4 SILAC runs have one row per channel).
- SHA-256: `d2a620093984bc7a482a896e808775e453f2d290179e8380b3165c434b5a45ad`
- Templates: `ms-proteomics` v1.1.0 only. The organism is *Escherichia coli*; no organism template fits bacteria (`human` and `vertebrates` do not apply), so per project convention only the base MS template is declared.
- Factor: `factor value[genotype]` = `wild type` (4 rows) / `cobB mutant` (4 rows) on the SILAC runs; `not available` on the 9 label-free discovery rows, which have no stated comparison.

## Design and file mapping

The `E_coli_succinylation` `summary.txt` lists 13 raw files in two MaxQuant experiment groups, `NON-SILAC` (9 files, multiplicity 1) and `CobB` (4 files, multiplicity 2, `Labels1` = Lys8). The file set equals the PRIDE file list entries for these names, and the original acquisition path in each RAW header equals the deposited file name. `List_of_RAW_files.xlsx` assigns all 13 files to Supplementary Tables S1 and S2.

| Source name | RAW files | Label | Bio rep | Fractions | Tech rep |
|---|---|---|---|---|---|
| `PXD002277_Ecoli_succK_nonSILAC_exp1` | `20120618/20_..._EColi40_succK_pH45`, `pH55`, `pH11` | label free | 1 | 1 = pH 4.5, 2 = pH 5.5, 3 = pH 11 | 1 |
| `PXD002277_Ecoli_succK_nonSILAC_exp1` | same names with `b` suffix (`pH45b`, `pH55b`, `pH11b`) | label free | 1 | 1, 2, 3 | 2 |
| `PXD002277_Ecoli_succK_nonSILAC_exp2` | `20120705_QE4_LC3_BTW_SA_ec_succK_EXP2_F01`-`F03` | label free | 2 | 1-3 (file-name F number) | 1 |
| `PXD002277_Ecoli_BW25113_wild_type` | `20130128_..._ec_BW25113_wt-K8_cobB-K0_succK_pre-conjugate_F01`-`F04` | SILAC heavy | 1 | 1-4 | 1 |
| `PXD002277_Ecoli_BW25113_cobB` | same 4 files | SILAC light | 1 | 1-4 | 1 |

- **SILAC map.** `List_of_RAW_files.xlsx` notes "SILAC wt(H) cobb (L)" on all four `20130128` files; the file names say `wt-K8_cobB-K0`, and `summary.txt` has `Labels1` = Lys8 with empty `Labels0`. So wild type = heavy (Lys8), cobB = light (Lys0). Strain `BW25113` is from the file names; genotype `wild type` / `cobB mutant` from the xlsx note and file names.
- **`b` files = re-injections.** Each `b` file has the same name as its partner plus `b`. The RAW headers show the partners ran with `150min_3tunes_nolockmass_Iso2_Res35000_IT120.meth` and the `b` files with `BTW_120m_60ms_250ms2_.meth` (a 120 min method). They are recorded as technical replicate 2 of the same fraction and source; MaxQuant searched them as separate raw files in the same `NON-SILAC` experiment.
- **Label-free vs SILAC rows.** `summary.txt` multiplicity is 1 for the 9 label-free runs and 2 for the 4 SILAC runs. `sdrf-tools build` can emit only one value per modification column, so a documented post-processing step (`scratchpad/PXD002277/postprocess.py`) set the `Label:13C(6)15N(2)` modification column to `not applicable` on the 9 label-free rows only; nothing else changed.
- **Technical values.** Instrument `Q Exactive` (MS:1001911) from all 13 RAW headers (`Q Exactive - Orbitrap MS`), PRIDE and `summary.txt`. DDA (PRIDE:0000627) and HCD (`beam-type collision-induced dissociation`, MS:1000422) from the PRIDE protocol; MS2 analyzer orbitrap (MS:1000484). Cleavage agent `Trypsin/P` (MS:1001313) from `summary.txt` `Protease`. Modifications: fixed Carbamidomethyl C (`parameters.txt`); variable Oxidation M, Acetyl Protein N-term and MaxQuant `succinyl-K` written as `Succinyl` (UNIMOD:64, TA=K) (`summary.txt`); Lys8 = `Label:13C(6)15N(2)` (UNIMOD:259) on SILAC rows. Tolerances: precursor 6 ppm (PRIDE protocol: "searched with a mass tolerance of 6 ppm for parent ions"), fragment 20 ppm (`parameters.txt` `MS/MS tol. (FTMS)` and the protocol). Fractionation: SCX (PRIDE:0000561), because the protocol says enriched peptides were "immediately separated by micro-scale SCX chromatography".

## Validation

- `timeout 900 .venv/bin/parse_sdrf validate-sdrf --sdrf_file annotations/PXD002277-Ecoli-succinylation.sdrf.tsv --template ms-proteomics --use_ols_cache_only`: "Everything seems to be fine. Well done.", exit 0, no errors or warnings (re-run 2026-11-04 on the SDRF with the SHA-256 above).
- `cd sdrf-skills && .venv/bin/python -m tools check annotations/PXD002277-Ecoli-succinylation.sdrf.tsv`: exit 0, Status CLEAN (12 terms checked, 12 verified, 0 hallucinated, 0 label mismatches, 0 wrong ontology, 0 UNIMOD swaps).
- Earlier run (2026-11-03): `sdrf-tools structure` "Structure OK", exit 0. `sdrf-tools reconcile` raised one `cleavage_agent_unsupported` flag for Trypsin/P (see Limitations).
- Live OLS (ols4) lookups confirmed MS:1001911, MS:1001313, MS:1000422, MS:1000484, PRIDE:0000627, PRIDE:0000561, UNIMOD:4, UNIMOD:35, UNIMOD:1, UNIMOD:64, UNIMOD:259 and NCBITaxon:562.
- Independent adversarial review: not run (out of scope for this producer run).

## Limitations
- **Post-processing (consistency with sibling files):** `assay name` set to one value per RAW file (per-channel `-SILAC light/heavy` suffixes removed), as the spec requires for multiplexed runs.


- **Paper full text unavailable; PubMed abstract only.** The paper is not in PMC/Europe PMC full text; cell.com and ScienceDirect returned HTTP 403, and no repository copy was found. The Methods and Supplementary Tables S1-S10 were not read. Every sample fact comes from the PRIDE record, the deposited MaxQuant output (`summary.txt`, `parameters.txt`), `List_of_RAW_files.xlsx`, the RAW file names and the RAW headers.
- **Label-free runs: strain, genotype and growth condition not stated.** The 9 `NON-SILAC` runs carry `strain or breed`, `genotype` and `factor value[genotype]` = `not available`. The search FASTA is "Escherichia coli (strain K12)", but that only says what was searched, not which strain was grown.
- **Biological replicate grouping (file-name inference).** `EColi40_succK` runs (June 2012, QE3) and `ec_succK_EXP2` runs (July 2012, QE4) are recorded as two independent samples (biological replicates 1 and 2) based on the `EXP2` token and the different dates and instruments; no document states what differed between them. The SILAC wild-type and cobB samples are biological replicate 1 within each genotype.
- **Fraction order (inference).** pH-step runs are numbered by ascending elution pH (4.5, 5.5, 11); F-numbered runs follow the file-name number.
- **Re-injections (`b` files).** Read as technical replicate 2 of the same fraction from the file-name pattern and the different 120 min method in the RAW header; no document states this explicitly.
- **`cobB mutant` wording.** The xlsx says "cobb (L)" and the file name `cobB-K0`; the exact allele (for example a deletion) is not stated, so the generic `cobB mutant` is used.
- **SILAC label column on light rows.** The `Label:13C(6)15N(2)` variable modification is present on both heavy and light rows of the SILAC runs because both channels come from the same multiplicity-2 search; `comment[label]` distinguishes the channels. Only Lys8 was configured (no Arg label).
- **Cleavage agent.** `Trypsin/P` is the deposited search setting; the PRIDE text says "strict trypsin specificity" in the data-processing section but does not name the digest reagent in sample preparation, so `sdrf-tools reconcile` raises `cleavage_agent_unsupported`. A peptide C-terminus check is not independent here, because a Trypsin/P search can only return K/R-terminated peptides.
- **Reduction/alkylation reagents** = `not available`: alkylation is implied by the fixed Carbamidomethyl C search, but the reagents are not stated.
- **Enrichment not encoded as a column.** Succinyl-lysine peptides were enriched with polyclonal antibody beads (ImmuneChem) per the PRIDE protocol; `characteristics[enrichment process]` is omitted because no accepted term fits. The enrichment is visible in the file names and the Succinyl variable modification.
- **Process note.** A repository-wide text search during the original annotation run inadvertently printed lines from other accessions' scratch directories. Nothing from them was used as evidence for this dataset.
