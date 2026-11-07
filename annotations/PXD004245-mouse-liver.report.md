# PXD004245-mouse-liver
Status: validated annotation; independent review pending.

**Dataset:** PXD004245, "ADP-ribosylation site analysis". Submitted by Michael Lund Nielsen, Novo Nordisk Foundation Center for Protein Research, University of Copenhagen, Copenhagen, Denmark. The mouse liver samples were prepared at the University of Zurich (Hottiger lab). Paper: Martello R, Leutert M, Jungmichel S, *et al.*, Nat Commun 2016;7:12917 (PMID 27686526, PMC5056437, doi:10.1038/ncomms12917).

This file covers the 3 mouse liver RAW files. The 12 HeLa RAW files are in `PXD004245-HeLa.sdrf.tsv`. The deposit is split because the organisms differ, the organism templates are mutually exclusive (`human` vs `vertebrates`), and the liver runs are not part of the deposited human MaxQuant search.

- **SDRF:** `annotations/PXD004245-mouse-liver.sdrf.tsv`
- **Size:** 3 data rows × 37 columns
- **SHA-256:** `9054b1d2239810202752d73180aba102e153fff5a35e291e2bbf0a1d02449f80`
- **Templates:** `ms-proteomics` v1.1.0 and `vertebrates` v1.1.0. The samples are MS proteomics of *Mus musculus* tissue, acquired by DDA.

## Design and file mapping

The three liver samples come from three mice, one per RAW file:

| Deposited file | Original name (from the RAW header) | Source | Biological replicate |
|---|---|---|---|
| `20150916_002_Liver_Rep1.raw` | `20150916_002_Liver1_unt.raw` | mouse 1 liver | 1 |
| `20150916_003_Liver_Rep2.raw` | `20150916_003_Liver2_unt.raw` | mouse 2 liver | 2 |
| `20150916_004_Liver_Rep3.raw` | `20150916_004_Liver3_unt.raw` | mouse 3 liver | 3 |

The paper says: "Three C57BL/6 mice were killed before their livers were collected", and the samples are "Male 9-week-old C57BL/6 mice" (Methods). The animal-study note gives the strain as C57BL/6J. All runs are label-free (the paper describes no labelling for tissue) and untreated (original file names end in `_unt`, and the paper calls them "normal mouse liver samples"). The sample preparation was "processed as described for the HeLa cells": Lys-C then trypsin digestion, PARG treatment, and Af1521 enrichment.

This is a single-condition study, so there is **no `factor value[...]` column**. The three livers are biological replicates of untreated tissue and nothing is compared.

**Instrument:** the RAW headers say Q Exactive HF (MS:1002523), with NCE 28 in the method header. PRIDE lists only "Q Exactive".

## Validation

- `timeout 900 parse_sdrf validate-sdrf -s PXD004245-mouse-liver.sdrf.tsv -t ms-proteomics -t vertebrates --use_ols_cache_only`: exit 0, 0 errors, 2 warnings:
  - `untreated` (`characteristics[treatment]`) is not found in NCIT/EFO. It was kept because the template recommends `untreated` for controls.
  - `C57BL/6J` (`characteristics[strain or breed]`) is not found in NCBITaxon. That column is free text per the contract.
- `sdrf-tools check`: CLEAN (15/15 terms verified), exit 0.
- `sdrf-tools structure`: OK.
- `sdrf-tools score`: 95/100. The only issue is "No factor value columns", which is expected for a single-condition design.
- `sdrf-tools reconcile` reported three blockers. All three were checked against the evidence and kept:
  1. *Organism contradicted (Mus musculus).* The PRIDE record's `organisms` and `sampleAttributes` list Mus musculus (NEWT:10090) together with human, and the paper describes mouse liver.
  2. *Trypsin is not named in the record.* The paper's Methods describe a Lys-C plus trypsin digestion, applied to liver "as described for the HeLa cells".
  3. *A labelled method is annotated as label-free.* SILAC applies only to the HeLa experiments, and the liver tissue was not labelled.

## Post-processing

`scratchpad/PXD004245/postprocess.py` inserted a second `comment[cleavage agent details]` column (`NT=Lys-C;AC=MS:1001309`) next to Trypsin. A diff against the `build` output found no other cell changed.

## Limitations

- **Search settings are taken from the paper and the HeLa search.** No search output for the liver runs is deposited: the deposited MaxQuant output uses `HUMAN.fasta` and does not include the liver files. Modifications (Carbamidomethyl C fixed; Oxidation M, Acetyl protein N-term and ADP-Ribosyl KRDE variable) and tolerances (precursor 7 ppm, fragment 20 ppm) come from the paper's general "Identification of peptides and proteins" Methods. The mouse search database is not stated.
- **Sex, age and strain** are from the paper's Methods, at cohort level ("Male 9-week-old"). They are applied to all three animals. `developmental stage` = `adult` is inferred from the age of 9 weeks.
- **Disease is inferred.** `disease` = `normal` comes from the paper's description of "normal mouse liver samples" and the untreated wild-type animals. PRIDE's "brain cancer" (DOID:1319) has no support and was not used.
- **Animal identity comes from file names.** The mapping of mouse number to file uses the deposited and original file names (`Liver1/2/3`). No per-animal table exists.
- **The enrichment step has no column.** There is no EFO/PRIDE term for ADP-ribosylated peptide (Af1521) enrichment, so `characteristics[enrichment process]` is omitted.
