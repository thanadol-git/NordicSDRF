# Copenhagen third 20 PXD batch

Selected on 2026-11-11 from confirmed entries in `copenhagen_candidates.tsv`. The cohort excludes the preceding 20, any accession already annotated in this repository, and accessions with an SDRF in the current `bigbio/sdrf-annotated-datasets` `main` tree. Size is the sum of accession-scoped PRIDE `fileSizeBytes` for files categorised as `RAW`. The ordered cohort and annotation state are in [copenhagen_third20_batch.tsv](copenhagen_third20_batch.tsv).

PXD066727 and PXD066932 are excluded from the size ranking for the same reason as in the preceding batch: their apparent RAW entries are processed `.mzML.quant` or ASCII spectral exports rather than acquisition files. This cohort begins at PXD045032 (5,102,221,864 bytes) and ends at PXD038362 (9,574,712,579 bytes).

## Annotation progress

Ten accessions are independently approved: PXD060336, PXD044835 (qualitative and quantitative subsets), PXD033732, PXD056295, PXD031272, PXD068323, PXD075502, PXD018051, PXD057401 (archaeological and standard-curve subsets), and PXD075443 (DDA and DIA subsets). Each approved SDRF passed the official parser and a hash-bound independent review. Together the two PXD057401 files account for all 59 PRIDE RAW acquisitions.

Ten accessions have explicit evidence blockers: PXD045032 (mouse ID–genotype map), PXD037269 (painting species assignment), PXD029885 (heterogeneous run-to-sample design map), PXD054499 (bear S1–S22 hibernation-state map), PXD028151 (TMT channel map), PXD047667 (acquisition method), PXD016395 (colony and acquisition maps), PXD019679 (digestion and replicate structure), PXD009298 (mock-up run map), and PXD038362 (S1–S6 genotype map). Each has an `annotations/<PXD>.report.md` evidence report. The TSV is the authoritative per-accession status list.
