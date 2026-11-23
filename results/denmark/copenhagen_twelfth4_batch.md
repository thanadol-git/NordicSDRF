# Copenhagen twelfth batch: 4 PXDs

Started 2026-11-23 on `copenhagen-12`, based on NordicSDRF `origin/main` (`599c700`). The [tracker](copenhagen_twelfth4_batch.tsv) lists the **last four** confirmed Copenhagen deposits with no local SDRF, BLOCKED file, or evidence report, and absent from BigBio `datasets/` + `sandbox/` (`upstream/main` `87f8fd2de`). They are the remaining giants by accession-scoped PRIDE RAW size (305–756 GB). Twenty-five other pending accessions already have local `*.report.md` evidence blockers and are not queued here.

`python scripts/batches/check_pxd_absent.py` passed CLEAR for all four on 2026-11-23. Each PXD still needs an evidence pass, validation, and independent adversarial review before contribution. `queued` does not imply an approved SDRF. A PRIDE RAW-category ZIP may contain multiple acquisitions and will be inspected before annotation.

| Order | Accession | RAW files | ~RAW size | Title |
|---|---|---:|---:|---|
| 1 | PXD004055 | 342 | 305 GB | Large-scale phosphorylation site interaction proteomics |
| 2 | PXD006361 | 4 | 327 GB | Proteomics Reveal Global Regulation of Protein SUMOylation by ATM and ATR Kinases during Replication |
| 3 | PXD003443 | 189 | 357 GB | Changes in proteome upon deletion of UBE2S/UBE2C in HCT116 cells |
| 4 | PXD005252 | 612 | 756 GB | Time-resolved analysis reveals rapid dynamics and broad scope of the CBP/p300 acetylome |
