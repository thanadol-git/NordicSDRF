# PXD002277-mouse-liver-acetylation

Status: validated annotation; independent review pending.

## Description

- Dataset: PXD002277, "Lysine succinylation is a frequently occurring modification in prokaryotes and eukaryotes and extensively overlaps with acetylation".
- Lab: Chunaram Choudhary lab, The NNF Center for Protein Research, University of Copenhagen, Copenhagen, Denmark (submitter Brian T. Weinert).
- Paper: Weinert BT et al., Cell Rep 2013;4(4):842-51, doi:10.1016/j.celrep.2013.07.024, PMID 23954790.
- This SDRF covers one of six SDRFs for the deposit: the acetyl-lysine (acK) enrichment from mouse liver, which was deposited as its own MaxQuant search (`mouse_liver_acetylation`). `List_of_RAW_files.xlsx` assigns these runs to Supplementary Table S7.

## SDRF

- Path: `annotations/PXD002277-mouse-liver-acetylation.sdrf.tsv`
- Rows: 4 data rows (4 RAW files, one row each); 32 columns.
- SHA-256: `d099c92c1c0cd76aa1fca2f66c19442ccd4d4ab573af79e98474c778122a5805`
- Factor value columns: none. All four files are SCX fractions of a single label-free acetyl-lysine enrichment from mouse liver, so there is no varying condition to record.

## Templates and why

- `ms-proteomics` (v1.1.0): mass-spectrometry proteomics data.
- `vertebrates` (v1.1.0): the organism is *Mus musculus* (a non-human vertebrate). `human` and `cell-lines` do not apply to a tissue sample, so this SDRF does not use them.

## Design and file mapping

- The deposit has 57 Thermo RAW files and one `MaxQuant_output_files.zip`. The zip contains six separate MaxQuant 1.2.7.1 searches, each with its own FASTA and modification set, plus `List_of_RAW_files.xlsx`. One SDRF per deposited search keeps `comment[modification parameters]` identical to that search.
- The `mouse_liver_acetylation` search (`summary.txt`) contains exactly four RAW files, `20130412_QE4_LC6_BTW_mm_liver_acK_F01` to `_F04`. All four are in the PRIDE file list, and `List_of_RAW_files.xlsx` assigns all four to Table S7.
- Labelling: label free. The xlsx Notes column is empty for these files, so they have no SILAC channel map (unlike the E. coli, yeast and HeLa-NAM runs). In `summary.txt`, Multiplicity is 1 and Labels0 is empty.
- Fractions: `comment[fraction identifier]` 1 to 4 follows the `F01` to `F04` tokens in the file names. The PRIDE protocol says that enriched peptides were "immediately separated by micro-scale SCX chromatography".
- Re-injections: this search has no `b`-suffixed files. Elsewhere in the deposit, `b`-files are re-injections acquired with a different (120 min) method, but none belong to this search.
- RAW headers (HTTP range read of the first 64 KB) show the same instrument for all four files ("Q Exactive - Orbitrap MS") and the same method (`1-9um_BTW_141min_120MS2_IW2.meth`). The original acquisition paths match the deposited file names, so the files were not renamed. The headers contain no sample names.
- Source and replicates: there is one source (`PXD002277_mouse_liver_acK`), with `characteristics[biological replicate]` = 1 and `comment[technical replicate]` = 1. All four fractions come from the same enrichment.
- Search settings: the cleavage agent is Trypsin/P (`summary.txt` Protease column; the protocol states "strict trypsin specificity" and up to 2 missed cleavages). Carbamidomethyl (C) is a fixed modification. Variable modifications are Oxidation (M), Acetyl (Protein N-term) and Acetyl (K) (`summary.txt`). The precursor tolerance is 6 ppm and the fragment tolerance is 20 ppm (PRIDE protocol: main search 6 ppm after a 20 ppm first search; `parameters.txt` MS/MS tol. (FTMS) = 20 ppm). Acquisition is DDA with HCD fragmentation and an Orbitrap MS2 analyzer (PRIDE protocol).
- The SDRF was built with `sdrf-tools build`. The resumed run confirmed that the copy in `annotations/` is byte-identical to the validated scratch build (`final.sdrf.tsv`).

## Validation

All commands were run on 2026-11-04 against the SDRF with the SHA-256 above.

| Command | Result |
|---|---|
| `timeout 900 .venv/bin/parse_sdrf validate-sdrf --sdrf_file <sdrf> --template ms-proteomics --use_ols_cache_only` | exit 0, "Everything seems to be fine. Well done." (no errors, no warnings) |
| `timeout 900 .venv/bin/parse_sdrf validate-sdrf --sdrf_file <sdrf> --template vertebrates --use_ols_cache_only` | exit 0, "Everything seems to be fine. Well done." (no errors, no warnings) |
| `.venv/bin/python -m tools check <sdrf>` | exit 0; 12 terms checked, 12 verified, 0 hallucinated, 0 label mismatches, 0 wrong ontology, 0 UNIMOD swaps; status CLEAN |

From the earlier run (2026-11-03): `tools structure` reported "Structure OK", and a live OLS lookup confirmed every accession used here (MS:1001911, MS:1001313, MS:1000422, MS:1000484, PRIDE:0000627, PRIDE:0000561, UNIMOD:4, UNIMOD:35, UNIMOD:1, NCBITaxon:10090, UBERON:0002107). `tools reconcile` raised one flag, `cleavage_agent_unsupported` (Trypsin/P). See Limitations.

## Limitations

- **Paper full text unavailable.** The Cell Reports article was not reachable (cell.com and ScienceDirect returned 403, it is not in PMC, and no repository copy was found). Only the PubMed abstract, the PRIDE project record and the deposited MaxQuant files were used. Mouse-specific methods (strain, sex, age, diet, number of animals pooled) could not be checked.
- **Sex, strain, developmental stage = `not available`.** The PubMed MeSH headings list only "Mice" and "Animals", and the PRIDE record does not state these attributes.
- **Disease = `not available`.** No source states the health status or treatment of the mice. They were probably untreated wild-type animals, but this was not asserted.
- **Single biological source (inference).** The four files are treated as SCX fractions of one acK enrichment, based on a shared date and run prefix, consecutive `F01` to `F04` numbering, a single MaxQuant search, and one supplementary table. If the paper pooled several animals or used separate livers per fraction set, the deposit does not show it. It is also unknown whether the same liver lysate was used for the mouse succinylation runs, so that SDRF uses a separate source name.
- **Fraction order (file names).** Fraction identifiers follow the `Fnn` file-name tokens. The SCX salt or pH step for each fraction is not recorded.
- **Cleavage agent.** Trypsin/P comes from the deposited search settings and the protocol's "strict trypsin specificity". The sample-preparation text does not name the digest reagent, so `sdrf-tools reconcile` raises `cleavage_agent_unsupported`. Checking peptide C-termini would not be independent evidence here, because a Trypsin/P search can only return K/R-terminated peptides.
- **Reduction and alkylation reagents = `not available`.** Carbamidomethyl (C) is a fixed modification in the search, so the samples were alkylated, but the record does not name the reagents.
- **Enrichment is not a column.** The anti-acetyl-lysine antibody enrichment ("polyclonal antibody beads (ImmuneChem)" in the protocol) appears only in the source name and in the Acetyl (K) modification. It is not encoded as a separate enrichment column.
