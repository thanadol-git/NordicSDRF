# PXD002277-mouse-liver-succinylation

Status: validated annotation; independent review pending.

## Description

- Dataset: PXD002277, "Lysine succinylation is a frequently occurring modification in prokaryotes and eukaryotes and extensively overlaps with acetylation" (Weinert BT, Schölz C, Wagner SA, Iesmantavicius V, Su D, Daniel JA, Choudhary C; Cell Rep 2013;4(4):842-51; doi:10.1016/j.celrep.2013.07.024; PMID 23954790).
- Lab: Chunaram Choudhary, The NNF Center for Protein Research, University of Copenhagen, Copenhagen, Denmark. Submitter Brian Weinert.
- This SDRF covers one of the six MaxQuant searches in the deposit: lysine succinylation (succinyl-K) mapping in mouse liver tissue. It corresponds to Table S5 of the paper, according to the deposited `List_of_RAW_files.xlsx`. The other five searches are annotated in sibling SDRFs `PXD002277-{Ecoli-succinylation,yeast-succinylation,HeLa-succinylation,HeLa-acetylation,mouse-liver-acetylation}.sdrf.tsv`.

## SDRF

- Path: `annotations/PXD002277-mouse-liver-succinylation.sdrf.tsv`
- 8 rows (one per RAW file, label-free) x 32 columns
- SHA-256: `b8b7212c16baf925b1cbd2fe02cbd0bcd578ae1fbf4bd6082b6a8055957bf62c`
- Evidence manifest: `annotations/PXD002277-mouse-liver-succinylation.evidence.json`

## Templates and why

- `ms-proteomics` v1.1.0: mass spectrometry proteomics (DDA, Q Exactive).
- `vertebrates` v1.1.0: the sample is mouse (*Mus musculus*) liver tissue. Not `human` (non-human), not `cell-lines` (tissue, not a cell line), not `dia-acquisition` (DDA), no clinical or single-cell template.

## Design and file mapping

- Single condition: mouse liver tissue was digested, succinyl-lysine peptides were enriched with anti-succinyl-lysine antibody beads (PRIDE sample protocol: "polyclonal antibody beads (immunechem)") and fractionated by micro-scale SCX. This is a qualitative site-mapping experiment with no comparison, so the SDRF has no `factor value[...]` column.
- 8 RAW files, all in the deposited `mouse_liver_succinylation` MaxQuant search (`summary.txt` lists exactly these 8 raw files; Multiplicity 1, so label-free) and all assigned to Table S5 in `List_of_RAW_files.xlsx`. All 8 are in the PRIDE file list, and all are annotated.
- Two SCX series of 4 fractions each:
  - `20130322_QE4_LC6_BTW_SA_mm_liver_succK_SCX_01`, `_SCX_02_130323222057`, `_SCX_03` and `_SCX_04` are technical replicate 1, fractions 1-4.
  - `20130406_QE4_LC6_BTW_SA_mm_liver_succK_scx_1` to `_scx_4` are technical replicate 2, fractions 1-4.
  - Both series share `source name` `PXD002277_mouse_liver_succK` and biological replicate 1.
- Fraction numbers come from the file-name suffixes. The `_130323222057` suffix on SCX_02 looks like an Xcalibur acquisition timestamp; the RAW header records the same file name and the same method as its siblings, so the file is treated as fraction 2 of the first series.
- SILAC: `List_of_RAW_files.xlsx` holds the SILAC channel maps for the labelled sub-experiments of this deposit (*E. coli* and yeast), but it gives no labels for the mouse liver files. MaxQuant also ran this search with Multiplicity 1 and no labels, so `comment[label]` = `label free sample`.
- No b-files: elsewhere in the deposit, `...b.raw` files are re-injections acquired with a different 120 min method (`BTW_120m_60ms_250ms2_.meth` in the RAW headers). None exist in this sub-experiment. All 8 mouse liver succinylation RAW headers show `Q Exactive - Orbitrap MS` and method `1-9um_BTW_141min_120MS2_IW2.meth`.
- Instrument: Q Exactive (MS:1001911), from the RAW headers, the PRIDE record and the MaxQuant summary `Instrument` column.
- Search parameters:
  - The PRIDE data-processing protocol gives a 6 ppm parent / 20 ppm (HCD) fragment main search, "strict trypsin specificity" and up to 2 missed cleavages.
  - From `parameters.txt` / `summary.txt` (MaxQuant 1.2.7.1): `MS/MS tol. (FTMS)` 20 ppm, Protease `Trypsin/P`, max missed cleavages 2, fasta `MOUSE.fasta`.
  - Modifications: fixed Carbamidomethyl (C); variable Oxidation (M), Acetyl (Protein N-term) and succinyl-K, written as UNIMOD:4, 35, 1 and 64.
- Dissociation: HCD (MS:1000422), per the PRIDE protocol. MS2 analyzer: orbitrap (Q Exactive; FTMS MS/MS tolerance used).
- Fractionation: SCX (PRIDE:0000561), per the PRIDE protocol and the `SCX` file names.
- Enrichment (anti-succinyl-lysine antibody) is not encoded as a column; see the PRIDE protocol.

## Validation

All results below are for the SDRF with SHA-256 `b8b7212c...f62c`, run on 2026-11-04 from `/home/thanadol/Documents/GitHub/sdrf-skills`:

- `timeout 900 .venv/bin/parse_sdrf validate-sdrf --sdrf_file <sdrf> --template ms-proteomics --use_ols_cache_only`: exit 0, "Everything seems to be fine. Well done." No errors and no warnings.
- `timeout 900 .venv/bin/parse_sdrf validate-sdrf --sdrf_file <sdrf> --template vertebrates --use_ols_cache_only`: exit 0, no errors and no warnings.
- `.venv/bin/python -m tools check <sdrf>`: exit 0, CLEAN (12 terms checked, 12 verified, 0 hallucinated, 0 label mismatches, 0 wrong ontology, 0 UNIMOD swaps).
- `.venv/bin/python -m tools structure <sdrf>`: exit 0, "Structure OK".
- `.venv/bin/python -m tools reconcile --record <PRIDE project JSON> --accession PXD002277 <sdrf>`: exit 1, one BLOCKER, `cleavage_agent_unsupported`. The PRIDE record never names Trypsin/P as a digest reagent. See Limitations; the SDRF was not changed.
- Earlier (2026-11-03), all ontology accessions used in the six PXD002277 SDRFs were checked against live OLS; all resolved, including MS:1001911, MS:1001313, MS:1000422, MS:1000484, PRIDE:0000627, PRIDE:0000561 and UNIMOD:4/35/1/64.

## Limitations
- **Revised after independent review:** the 2013-03-22 and 2013-04-06 SCX series were previously technical replicates 1 and 2 of one source. Evidence points to two separately prepared series (each enrichment was 'immediately separated by micro-scale SCX'; runs 15 days apart; different file naming `SCX_0n` vs `scx_n`; different autosampler pickup/loading volumes 5/9 vs 6/12 µl in the RAW headers). Whether they come from the same liver lysate or different animals is not stated in any accessible source (paper full text blocked). Each series is now its own source (`... series 1` / `... series 2`), both biological replicate 1 and technical replicate 1, so neither a re-injection nor independent animals is claimed.


- **Paper full text unavailable.** The paper is not in PMC, cell.com and ScienceDirect returned 403, and no repository copy was found. Only the PubMed abstract (PMID 23954790) and the PRIDE protocols were read. Nothing below was checked against the paper's Methods.
- **Cleavage agent.** The SDRF has `NT=Trypsin/P;AC=MS:1001313`, taken from the MaxQuant search enzyme (`summary.txt` Protease = Trypsin/P). The PRIDE protocol says only "strict trypsin specificity" and does not name the digest reagent. `sdrf-tools reconcile` reports this as a BLOCKER (`cleavage_agent_unsupported`). If the reviewer prefers the reagent rather than the search rule, the plain `Trypsin` (MS:1001251) would be the alternative. Left unchanged per instructions.
- **Biological vs technical replicate (inference).** The two SCX series (acquired 2013-03-22 and 2013-04-06) are encoded as technical replicates 1 and 2 of one source, with biological replicate 1. Nothing available states whether they came from the same liver lysate or enrichment, separate enrichments, or different mice. If they were different animals, they should be biological replicates 1 and 2 with distinct source names.
- **Fraction identity (file names).** Fraction numbers 1-4 come from the file-name suffixes (`SCX_01..04`, `scx_1..4`). The SCX elution order is assumed from the numbering.
- **Sample metadata not available.** Strain, sex, developmental stage/age and disease are `not available`. The PRIDE record, the abstract and the PubMed MeSH headings (only "Mice"/"Animals") do not state them. Disease is probably healthy/normal, but this is not stated.
- **Reduction/alkylation reagents** are `not available` (not named in the PRIDE protocol). Carbamidomethyl (C) is kept as a fixed modification because it was set in the search.
- **Precursor tolerance** of 6 ppm is from the PRIDE data-processing protocol text. No `mqpar.xml` was deposited, and MaxQuant 1.2.7.1 `parameters.txt` does not list the main-search tolerance.
- **Organism part** `liver` comes from PRIDE (`BTO:0000759 Liver`), the abstract ("mouse liver tissue") and the `mm_liver` file names. The liver lobe and any perfusion or other tissue handling are unknown.
- **Annotator-defined values.** `source name` `PXD002277_mouse_liver_succK` is an annotator identifier, not a deposited sample ID. The RAW headers contain no sample names.
