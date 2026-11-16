# Copenhagen sixth batch: 25 PXDs

Selected on 2026-11-16 from confirmed Copenhagen candidates, excluding the five earlier Copenhagen cohorts, local annotation or block records, the saved community-corpus list, and two previously identified processed-only RAW mislabels. The [tracker](copenhagen_sixth25_batch.tsv) orders 25 accessions by the sum of accession-scoped PRIDE file sizes for entries categorised as RAW. Every cached file-list entry was checked against its accession. `scripts/batches/select_copenhagen_sixth25.py` reproduces the selection and preserves tracker statuses on rerun.

The cohort runs from PXD017475 (21.81 GB RAW-labelled files) through PXD066033 (34.01 GB). RAW-labelled ZIP files may contain multiple vendor acquisitions; archive interiors and sample assignments must be verified before SDRF construction.

## Initial evidence review

### PXD017475

PRIDE lists 19 RAW files from two workflows: four MIR31HG oligonucleotide pull-down files dated 2016-06-17 and 15 secretome files dated 2016-08-12. The [linked paper](https://doi.org/10.1038/s41467-021-22746-4) and PRIDE sample protocol distinguish the workflows. Secretome proteins were digested with Lys-C followed by trypsin; pull-down material was digested with trypsin. The available repeated-cleavage builder can represent sequential digestion, but this accession also needs different enzyme values for its two arms. Filename-to-condition and replicate mapping is being checked. No SDRF has been written.

### PXD042430

The 14 Thermo RAW files are modern grouper-bone LC-MS/MS references. The [paper](https://onlinelibrary.wiley.com/doi/full/10.1002/ece3.10625) reports five *Epinephelus marginatus* and three each of *E. aeneus*, *E. caninus* and *E. costae*. Most RAW names contain a species name or specimen code, but the specimen `1082` requires an explicit key. The publisher's supplementary Data S1 link currently returns a cache miss, and the accession protocol is not locally cached. No SDRF has been written.

### PXD012573

The cached PRIDE description provides separate, complete 11-channel TMT maps for Fgf4/MEK-inhibition and analog-sensitive Erk2 experiments. The 24 RAW files are two sets of 12 fractions, and the PRIDE sample protocol specifies Lys-C followed by trypsin. The deposited MaxQuant output is listed as `txt.zip`, but its contents are not locally available; search modifications and tolerances remain to be verified before constructing the SDRF. No SDRF has been written.

### PXD026225

The [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC9074744/) and accession-scoped PRIDE record support 16 human runs (six basal TBC1D4 IP, six insulin-stimulated TBC1D4 IP and four IgG controls) and 10 mouse runs (five wild type and five TBC1D4 knockout). Separate [human](../../annotations/PXD026225-human.sdrf.tsv) and [mouse](../../annotations/PXD026225-mouse.sdrf.tsv) SDRFs cover all 26 RAW files and use their respective organism templates. The author-reported instrument, top-15 DDA acquisition and trypsin digestion are captured. Search modifications and tolerances are `not available` because the deposited MaxQuant archives are not locally accessible. Both SDRFs passed deterministic validation and fresh independent review, with matching hash-bound approval receipts. The mouse file has a minor offline ontology warning for the author-reported C57BL/6J strain. The repo-wide review gate still exits nonzero because many unrelated earlier annotations remain pending in its state; these two receipts are current.

### PXD043452

The [paper](https://pure.au.dk/ws/files/462582763/sciadv.adi2687.pdf) describes five technical 293T culture replicates for each PARP14 construct, with each lysate split between Af1521-linked and empty control beads. Two companion SDRFs, [Af1521](../../annotations/PXD043452-af1521.sdrf.tsv) and [control beads](../../annotations/PXD043452-beads.sdrf.tsv), preserve that shared source identity and cover all 20 accession-matched RAW files (10 each). Both use the `ms-proteomics`, `human`, and `cell-lines` templates, pass deterministic validation and independent review, and have current hash-bound approval receipts. The accessible paper supports the Orbitrap Exploris 480, data-dependent acquisition, and trypsin digestion. Search tolerances and modification settings remain `not available` because the deposited search archive was not accessible. Review noted one minor omission: the paper-supported HCD dissociation method is not recorded as a recommended comment column. The repo-wide gate still has unrelated pending files.

### PXD035353

The [paper](https://edoc.mdc-berlin.de/id/eprint/22057/1/22057oa.pdf) describes control-siRNA and TRESLIN-siRNA HeLa samples, each divided into eight high-pH reversed-phase fractions. The [SDRF](../../annotations/PXD035353.sdrf.tsv) covers all 16 accession-matched RAW files and records the Q Exactive HF-X, top-15 data-dependent acquisition, trypsin digestion, and the three stated MaxQuant modifications. Cellosaurus supports the HeLa cell-line metadata. Deterministic validation and independent review pass with a current hash-bound approval receipt. Review noted minor optional omissions for collision energy and culture medium. The repo-wide gate still has unrelated pending files.

### PXD041717

The 20 accession-scoped RAW filenames form five groups of four: siC untreated, and siC/siR/siT/siD with AZA. The [paper](https://www.nature.com/articles/s41594-024-01294-7.pdf) describes DNMT1 immunoprecipitation, four independent experiments, siRNAs targeting control, RNF4 and TOPORS, and 5-AzadC treatment. The [ProteomeXchange record](https://proteomecentral.proteomexchange.org/cgi/GetDataset?ID=PXD041717) lists Orbitrap Exploris 480. The exact meaning of the `siD` filename code and the accession-specific acquisition/search protocol have not been verified. No SDRF has been written; these labels will stay literal until a run-level key is found.

### PXD036512

The [paper](https://www.nature.com/articles/s41467-023-38793-y.pdf) and 64 accession-scoped RAW filenames support a 2 × 2 design in S2R+ *Drosophila* cells: DMSO or PARG inhibitor PDD00017273, with or without hydrogen peroxide. Each condition has four culture replicates, each acquired in four fractions. The [SDRF](../../annotations/PXD036512.sdrf.tsv) records all 64 files, the sequential Lys-C then Trypsin digestion, Af1521 macrodomain enrichment, and EThcD fragmentation on Orbitrap Fusion Lumos. The parser and structural checks pass, and fresh independent review approved the exact file hash. The parser warns that the precise enrichment phrase and Oregon-R strain do not resolve in its offline ontology cache. Search mass tolerances remain `not available`. The reviewer noted minor optional omissions for the high-pH fractionation method and donor developmental stage.
