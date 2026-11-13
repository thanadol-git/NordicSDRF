# Copenhagen fourth 20 PXD batch

Selected on 2026-11-13 from confirmed Copenhagen candidates, excluding prior Copenhagen batches, existing local SDRFs and reports, and accessions in the live `bigbio/sdrf-annotated-datasets` corpus. The cohort is ordered by the sum of accession-scoped PRIDE `fileSizeBytes` for files categorised as RAW. The two previously identified processed-only RAW mislabels, PXD066727 and PXD066932, remain excluded. The selected cohort starts with PXD004341 (9,830,389,512 bytes) and ends with PXD052074 (17,368,244,462 bytes).

The [batch tracker](copenhagen_fourth20_batch.tsv) records each accession's annotation and review state. A RAW-labelled ZIP or 7z file may contain several acquisitions; its contents and sample map must be verified before annotation.

Initial evidence review began with PXD035661. Its 28-file draft passed parser validation, but independent review identified unsupported acquisition and replicate assumptions. See [PXD035661 evidence report](../../annotations/PXD035661.report.md). It is recorded as blocked; no unapproved SDRF is included in the committed batch.
