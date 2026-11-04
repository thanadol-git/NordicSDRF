# PXD002277-yeast-succinylation

Status: validated annotation; independent review pending.

## Description

- Dataset: PXD002277, "Lysine succinylation is a frequently occurring modification in prokaryotes and eukaryotes and extensively overlaps with acetylation".
- Lab: Chunaram Choudhary lab (submitter Brian T. Weinert), NNF Center for Protein Research, University of Copenhagen, Denmark.
- Paper: Weinert BT et al., Cell Rep. 2013;4(4):842-51, doi:10.1016/j.celrep.2013.07.024, PMID 23954790.
- Scope of this SDRF: the *Saccharomyces cerevisiae* lysine-succinylation sub-experiment, which corresponds to the deposited MaxQuant search `MaxQuant_output_files/yeast_succinylation/`. The deposit holds six separate MaxQuant searches (E. coli succinylation, yeast succinylation, HeLa succinylation, HeLa acetylation, mouse liver succinylation, mouse liver acetylation). Each search is annotated as its own SDRF, `PXD002277-<search>.sdrf.tsv`.

## SDRF

- Path: `annotations/PXD002277-yeast-succinylation.sdrf.tsv`
- Rows: 30 data rows (plus header), covering 14 RAW files.
- Columns: 34.
- SHA-256: `65586832081ecdbb4e200ec80b2335e781b6e395cb8ed8a46a3fc54ee5bed392`
- The file is byte-identical (`cmp`) to the validated build in the scratch folder (`yeast-succinylation/final.sdrf.tsv`).

## Templates and why

- `ms-proteomics` (v1.1.0) only. The study is DDA mass-spectrometry proteomics of a unicellular fungus. None of the organism templates (`human`, `vertebrates`, `invertebrates`, `plants`) fits *S. cerevisiae*, and no cell-line or clinical template applies. The SDRF declares the template in `comment[sdrf template]` as `NT=ms-proteomics;VV=v1.1.0`.

## Design and file mapping

The deposited yeast search covers two designs: one label-free succinylome and two triple-SILAC quantitative experiments.

### 1. Label-free succinylome (6 RAW files, 6 rows)

- Files `20120620_QE3_LC1_BTW_SA_Yeast40_succK_pH45/pH5/pH11.raw` are three SCX elution fractions of one succinyl-lysine-enriched yeast sample. They are ordered by elution pH as `comment[fraction identifier]` 1, 2 and 3.
- MaxQuant `summary.txt` gives Multiplicity 1 with no labels for these runs, so `comment[label]` is `label free sample`.
- The `...b.raw` files (`pH45b`, `pH5b`, `pH11b`) are re-injections of the same three fractions. The RAW headers show that the originals used the method `VYT\150min_3tunes_nolockmass_Iso2_Res35000_IT120.meth`, while the b-files used `BTW\BTW_120m_60ms_250ms2_.meth`, a 120 min method. The b-files therefore have the same source name and fraction identifiers as the originals, with `comment[technical replicate]` 2 (the originals are 1).
- All six rows have source name `PXD002277_Scer_succK_nonSILAC` and biological replicate 1.
- Genotype and growth condition, and their factor values, are `not available` because no source states them for this sample (see Limitations).

### 2. Triple-SILAC experiments (8 RAW files × 3 channels = 24 rows)

`List_of_RAW_files.xlsx` in the deposited MaxQuant zip marks these files "SILAC, as indicated in file name". MaxQuant `summary.txt` confirms Multiplicity 3 with `Labels1 = Lys4` and `Labels2 = Lys8` for every file. Combining the file-name tokens with the MaxQuant label order gives the channel map below.

| File set | SILAC light (Lys0) | SILAC medium (Lys4) | SILAC heavy (Lys8) |
|---|---|---|---|
| `..._sc_wtDEX0_wtGAL4_kgdGAL8_succK_SCX_01..04.raw` | wild type, glucose (`wtDEX0`) | wild type, galactose (`wtGAL4`) | kgd mutant, galactose (`kgdGAL8`) |
| `..._sc_wtDEX0_wtGAL4_lscGAL8_succK_SCX_01..04.raw` | wild type, glucose | wild type, galactose | lsc mutant, galactose |

- Each file is one of four SCX fractions, given as `comment[fraction identifier]` 1–4 from the `SCX_0n` suffix. All 8 files are on QE4 with the method `BTW\1-9um_BTW_141min_120MS2_IW2.meth` (from the RAW headers).
- Assay names are `<raw file stem>-SILAC light|medium|heavy`.
- Source names identify each condition within each SILAC mix, for example `PXD002277_Scer_wild_type_glucose_kgdSILAC`.
- The wild-type glucose and wild-type galactose channels appear in both mixes. They are treated as independently grown cultures: biological replicate 1 in the kgd mix and 2 in the lsc mix. Each mutant has biological replicate 1.
- Label modifications: `NT=Label:2H(4);AC=UNIMOD:481;TA=K` (Lys4) and `NT=Label:13C(6)15N(2);AC=UNIMOD:259;TA=K` (Lys8), both variable, as in the MaxQuant multiplicity-3 search.

### Shared technical values

| Item | Value | Source |
|---|---|---|
| Instrument | Q Exactive (`MS:1001911`) | PRIDE record and RAW headers ("Q Exactive - Orbitrap MS"; units QE3 and QE4) |
| Acquisition | DDA | PRIDE sample-processing protocol |
| Dissociation | HCD, written as `NT=beam-type collision-induced dissociation;AC=MS:1000422` | PRIDE sample-processing protocol |
| MS2 analyzer | Orbitrap | PRIDE data-processing protocol ("orbitrap analyzer used for fragment scans") |
| Fractionation | SCX (`PRIDE:0000561`) | PRIDE sample-processing protocol ("micro-scale SCX chromatography") |
| Cleavage agent | Trypsin/P (`MS:1001313`) | MaxQuant `summary.txt` Protease column for every yeast RAW file |
| Mass tolerances | 6 ppm precursor, 20 ppm fragment | PRIDE data-processing protocol; `parameters.txt` "MS/MS tol. (FTMS) 20 ppm" |
| Fixed modification | Carbamidomethyl (C) | `parameters.txt` |
| Variable modifications | Oxidation (M), Acetyl (Protein N-term), succinyl-K (`UNIMOD:64`) | `summary.txt` |

### Post-processing

`sdrf-tools build` can emit only one value per `comment[modification parameters]` column. A small documented script, `scratchpad/PXD002277/postprocess.py`, therefore set the two SILAC label-modification cells to `not applicable` on the six label-free rows, matching their Multiplicity 1 search. A diff of the build output against the final file shows that exactly 12 cells changed (rows 1–6, columns 29 and 30) and nothing else.

### Factors

- `factor value[genotype]`: wild type, kgd mutant or lsc mutant.
- `factor value[growth condition]`: glucose or galactose.
- Both factors are `not available` on the six label-free rows.

## Validation

All runs on 2026-11-04 against the SDRF with the SHA-256 above.

| Command | Result |
|---|---|
| `timeout 900 /home/thanadol/Documents/GitHub/sdrf-skills/.venv/bin/parse_sdrf validate-sdrf --sdrf_file annotations/PXD002277-yeast-succinylation.sdrf.tsv --template ms-proteomics --use_ols_cache_only` | Exit 0 in about 10 s with "Everything seems to be fine. Well done." No errors and no warnings. |
| `cd /home/thanadol/Documents/GitHub/sdrf-skills && .venv/bin/python -m tools check <sdrf>` | Exit 0. 13 terms checked and 13 verified; 0 hallucinated, 0 label mismatches, 0 wrong ontology, 0 UNIMOD swaps. Status CLEAN. |

The previous run also recorded these results (`scratchpad/PXD002277/validation/`):

- `tools structure`: "Structure OK" (exit 0).
- Live OLS re-check: all ontology accessions resolved (`ols_check.txt`).
- `tools reconcile` reported one BLOCKER, `cleavage_agent_unsupported`. The PRIDE text says "strict trypsin specificity" and never names "Trypsin/P". The deposited MaxQuant `summary.txt` gives `Trypsin/P` as the protease for all 14 yeast RAW files, so the search-level value was kept. This should be adjudicated in review.

## Limitations
- **Revised after independent review:** (1) `assay name` is now one per RAW file (the per-channel `-SILAC light/medium/heavy` suffixes were removed); channels are distinguished by `comment[label]` and source name. (2) The wild-type glucose/galactose channels of the lsc mix are now biological replicate 1 (previously 2): no source states whether the two mixes used independent wild-type cultures or one lysate split between them (both acquired 20130322). They keep mix-specific source names (`..._kgdSILAC` / `..._lscSILAC`) so that each mix's channels stay distinct, without claiming n = 2.


- **Paper full text unavailable.** The Cell Reports article is not in PMC, and both cell.com and ScienceDirect returned 403. No repository copy was found. Only the PubMed abstract (PMID 23954790) and the PRIDE protocol texts were used, so no Methods or supplementary-table details from the paper could be checked.
- **SILAC channel map is inferred from file names plus the MaxQuant label order.** `List_of_RAW_files.xlsx` states only "SILAC, as indicated in file name". The map assumes `DEX0` means wild type on glucose in Lys0, `GAL4` means wild type on galactose in Lys4, and `kgdGAL8`/`lscGAL8` mean the mutant on galactose in Lys8. The `0/4/8` suffixes agree with the MaxQuant `Labels1 = Lys4` and `Labels2 = Lys8`.
- **Mutant identity is unresolved.** "kgd mutant" and "lsc mutant" are free-text abbreviations from the file names. The abstract mentions only "mutations that affected succinyl-CoA metabolism in the tricarboxylic acid cycle". The exact genes (α-ketoglutarate dehydrogenase subunits such as KGD1/KGD2, or succinyl-CoA ligase LSC1/LSC2) and the allele type (deletion or otherwise) are not available. The strain background is also not available.
- **Growth condition is inferred from file names.** "glucose" and "galactose" come from the `DEX`/`GAL` tokens. The abstract confirms only that "growth conditions" were varied. Media composition, carbon-source concentration and harvest time are not available.
- **Biological replicate numbering is an assumption.** Giving the wild-type channels of the two SILAC mixes replicates 1 and 2 assumes separately grown cultures. If one wild-type culture was shared between both mixes, these should be the same biological replicate.
- **Label-free sample conditions are unknown.** Genotype and growth condition are `not available` for this sample, which is likely a wild-type culture but no source says so. These six rows carry no factor information.
- **Fraction ordering.** The label-free SCX fractions are ordered by elution pH (4.5, then "5", then 11). The "pH5" token may stand for pH 5.5, as in the E. coli files (`pH55`), but this is unconfirmed. The SILAC fractions follow the `SCX_01..04` order.
- **Re-injections.** The b-files are treated as technical replicate 2 of the same fractions. This follows from the identical file stems and the different (120 min) instrument method in the RAW headers; no source explicitly describes them.
- **Reduction and alkylation reagents are `not available`.** Fixed carbamidomethyl-C implies iodo- or chloroacetamide alkylation, but no reagent is named.
- **Enrichment is not encoded as a column.** The anti-succinyl-lysine antibody enrichment ("polyclonal antibody beads (immunechem)", per the PRIDE protocol) has no dedicated column in this SDRF.
- **Cleavage agent.** Trypsin/P comes from the deposited MaxQuant output. The PRIDE prose says "strict trypsin specificity", and `tools reconcile` flags the difference (see Validation).
- **MaxQuant experiment grouping.** `summary.txt` lists experiments `EXP0`, `EXP1` and `EXP2` without a per-file Experiment column. This grouping was not used for the mapping, which relies on file names only.
- **Organism part and disease** are `not applicable` because the samples are unicellular yeast cultures.
