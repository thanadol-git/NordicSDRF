# Copenhagen seventh batch: 20 PXDs

Started on 2026-11-17 on branch `codex/copenhagen-seventh20`. The [tracker](copenhagen_seventh20_batch.tsv) selects the 20 smallest remaining RAW-labelled deposits among confirmed Copenhagen candidates. It excludes earlier Copenhagen batches, the saved community-corpus list, existing local annotation and block records, and two deposits previously identified as processed-only RAW mislabels. The selection uses accession-scoped PRIDE file lists and verifies every listed file belongs to its PXD. `scripts/batches/select_copenhagen_seventh20.py` reproduces the selection and keeps statuses on rerun.

The cohort ranges from PXD011937 (34.36 GB, 32 RAW files) to PXD042172 (44.68 GB, 23 RAW files). ZIP-labelled entries need archive-interior checks before they can be counted as acquisitions.

## Annotation progress

### PXD011937 — blocked after two independent reviews

The [PRIDE record](https://www.ebi.ac.uk/pride/archive/projects/PXD011937), [paper](https://doi.org/10.1093/nar/gkz510), deposited MaxQuant summary and inspected RAW headers support a 96-row draft across 32 files, four eight-fraction experiments and three SILAC channels. The pilot light-channel condition is explicitly `not available`. The initial review led to stronger disease and instrument evidence. The second review found that `HeLa S3` is not recognized in the required CLO/BTO/EFO cell-line ontology set. The draft is [blocked](../../annotations/PXD011937.BLOCKED.md) pending resolution; it is not approved.

### PXD064417 — blocked after two independent reviews

The [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12804880/), deposited sample key and MaxQuant summary support a 22-row draft covering 21 enamel samples and one laboratory blank. The second review objected to assigning a biological replicate number to the blank, while the current SDRF contract requires an integer there. The draft is [blocked](../../annotations/PXD064417.BLOCKED.md) pending a schema-compatible convention or a decision to omit the blank; it is not approved.

### PXD051333 — approved after independent review

The PRIDE archive lists one 37.72 GB `Raw_files.zip`, but its verified ZIP index contains 12 Bruker `.d` acquisitions. The [run inventory](PXD051333_run_inventory.tsv), derived from the ZIP directory and each Bruker `SampleInfo.xml`, identifies nine peptidome and three proteome acquisitions. The [paper](https://doi.org/10.1016/j.ab.2025.115837) and PRIDE record describe rat precision-cut lung-slice supernatants processed for both endpoints. Run-specific deposited pepXML search headers support a [three-run proteome SDRF](../../annotations/PXD051333-proteome.sdrf.tsv). They also show two peptidome search-setting groups: six BE/BA runs without fixed cysteine modification and three GA runs with fixed cysteine carbamidomethylation. Separate [BE/BA](../../annotations/PXD051333-peptidome-be-ba.sdrf.tsv) and [GA](../../annotations/PXD051333-peptidome-ga.sdrf.tsv) SDRFs cover them. All three files pass deterministic validation and hash-bound independent review. The processed-file list names `160101a_BE1_1_4205`, `160101b_BE2_1_4206`, `160101b_GE2_1_4197`, and `180101_GA1_1_5604`, whose acquisition directories are absent from `Raw_files.zip`; they are excluded. No solvent, condition, donor, or replicate relationship is asserted without run-level evidence.

### PXD024397 — blocked after two independent reviews

The accession-scoped PRIDE file list has 26 `.raw` acquisitions: 20 `A`–`J` reconstruction runs (`large` and `small`), three painting micro-samples (`1BP`, `1GL`, `2YP`), and three processing blanks. The deposited file-description key confirms each mapping. The [paper](https://doi.org/10.1038/s41598-022-14109-w) and its supplement describe the materials; deposited RAW headers support run-specific Q Exactive HF and HF-X instruments. The [26-row draft](../../scratchpad/PXD024397/draft.sdrf.tsv) passes official validation, structure and offline ontology checks. The first independent review identified composite painting samples incorrectly assigned a single organism, which was corrected. The second review found `characteristics[biological replicate]=0` on three blanks conflicts with the active template's integer-starting-at-1 semantics, despite passing the validator. The draft is [blocked](../../annotations/PXD024397.BLOCKED.md) pending a schema-compatible blank convention or a documented decision to exclude blanks; it has no approval receipt.

### PXD029644 — outside current proteomics SDRF scope

The [PRIDE record](https://www.ebi.ac.uk/pride/archive/projects/PXD029644) and [paper](https://doi.org/10.1021/acs.analchem.1c05068) identify a released O-glycan profiling experiment, not protein or peptide analysis. Its 71 `.raw` files are glycomics acquisitions; the installed template set has no glycomics SDRF template. The accession is [held](../../annotations/PXD029644.BLOCKED.md) without an SDRF rather than assigning false proteomics metadata.

### PXD012235 — BUB3 and cell-derived BUB1B approved; bead-only controls blocked

The [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6443202/) and deposited MaxQuant archives identify 12 Venus-Bub3 affinity-purification RAW files across four HeLa conditions and three technical repeats per condition. The first independent review of the [BUB3 SDRF](../../annotations/PXD012235-bub3.sdrf.tsv) found unsupported `nocodazole` treatment; that column was removed. The rebuilt file passes official validation and hash-bound independent review, and has been committed. The [BUB1B cell-derived SDRF](../../annotations/PXD012235-bub1b-cells.sdrf.tsv) covers 21 runs from HeLa, HAP1, and RPE1 groups. Its first review found a stale HAP1 donor age and missing disease, which were corrected from the current Cellosaurus record. The rebuilt file passes official validation and hash-bound independent review, and has been committed. Three bead-only BUB1B controls remain [blocked](../../annotations/PXD012235.BLOCKED.md) because the active human template has no truthful biological-replicate value for acellular controls. The accession is not fully covered.

### PXD074599 — approved after independent review

The [paper](https://www.nature.com/articles/s41375-026-03122-x), supplementary methods and TMT sample key, and deposited MaxQuant settings support separate [proteome](../../annotations/PXD074599-proteome.sdrf.tsv) and [phosphoproteome](../../annotations/PXD074599-phospho.sdrf.tsv) SDRFs. Together they cover all 116 accession-scoped RAW runs. Both passed official validation and hash-bound independent review and were committed separately.

### PXD032328 — mIMCD-3 fractions approved; remainder in progress

The [publication](https://pmc.ncbi.nlm.nih.gov/articles/PMC10214176/) gives the six-channel TMT clone map for mIMCD-3 wild-type and TMEM260 knockout cells. The [Fusion](../../annotations/PXD032328-mimcd3-fusion.sdrf.tsv) and [Lumos](../../annotations/PXD032328-mimcd3-lumos.sdrf.tsv) SDRFs each cover four high-pH fractions and 24 sample-channel rows. Their accession-scoped RAW mapping, instrument, HCD and ETciD methods, and clone labels passed official validation and hash-bound independent review. They were committed separately. The deposited fraction-3 HCD search file supported modifications but not search tolerances across all eight RAW files, so shared tolerance fields were omitted. The other 49 RAW runs remain to be interpreted and annotated.

### PXD058085 — blocked after two independent review rounds

The deposited `MSfiles.xlsx` and both RAW ZIP indexes map 10 liver and 10 mesenteric artery Bruker acquisitions. The [PRIDE protocol](https://www.ebi.ac.uk/pride/archive/projects/PXD058085) specifies a Trypsin/LysC digestion mix. The first independent reviews found that encoding only Lys-C omitted trypsin; the second reviews found that two repeated cleavage-agent columns violate the active template's single-value cardinality. Both drafts pass deterministic validation but have no approval receipt. The [block record](../../annotations/PXD058085.BLOCKED.md) preserves the conflict and draft locations. The artery workbook and Bruker metadata both label the last two treated runs `mA_P4`, so no fifth treated biological sample is inferred.

### PXD070197 — blocked after first independent review

The depositor SDRF maps 24 mouse dermal-fibroblast runs across OTULIN genotype, TNF time, pull-down, and three biological replicates. The [block record](../../annotations/PXD070197.BLOCKED.md) documents correction of 12 deposit filename typos and the unresolved digestion reagent. Peptide termini suggest trypsin, but neither the project protocol nor the accessible publication source directly names it. Independent review rejected that inferred reagent. No SDRF was approved or committed.

### PXD034924 — approved after independent review

The [33-row histone PTM SDRF](../../annotations/PXD034924.sdrf.tsv) covers every accession-scoped RAW file. The depositor experimental design and Table S2 identify four comparison blocks and their replicates. The [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC10114496/) identifies HeLa S3 cells, PRM on Q Exactive HF, trypsin digestion and 5 ppm precursor tolerance. Its human cell-line evidence resolves a conflicting mouse organism field in the PRIDE project record. The first independent review identified missing donor disease and cervix origin; these were corrected. The second review approved the final hash. Repository-wide gate output still includes unrelated pending artifacts, but the PXD034924 hash itself is approved. The SDRF and evidence were committed as `144ee53`.

### PXD013140 — approved after independent review

The [71-row recombinant-enzyme SDRF](../../annotations/PXD013140.sdrf.tsv) maps all accession-scoped RAW files to 61 GLA and 10 GBA sheets in the depositor's Figure 2 and Figure 4 workbooks. The [paper](https://doi.org/10.1038/s41467-019-09809-3) and Supplementary Tables 2–3 identify the human proteins produced in Chinese hamster ovary cells, clone gene edits and parental lines. Methods support chymotrypsin, Orbitrap Fusion, top-five data-dependent HCD and the MS1 scan range. The 5 ppm glycopeptide composition-assignment value was not treated as a peptide search tolerance. Official cached-ontology validation, structure, record reconciliation, and offline checks passed. A fresh independent review approved SHA-256 `8826827f71556b2e981517e6406029b1ca057baba0f5666e0e8a34e39d98ba49`. The repository-wide gate still reports unrelated pending artifacts; this SDRF's hash-bound approval is recorded.

### PXD042321 — held for sample and method mapping

The deposited file list has 102 RAW files; `SampletoData.csv` maps 94, including 16 acellular blanks. Eight 4EDTA files lack rows in that map. The [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC10603084/) reports trypsin, Lys-C and mixed Lys-C/Trypsin methods, plus several uncertain specimen taxa. The [hold record](../../annotations/PXD042321.BLOCKED.md) documents the unresolved run, digest and blank mapping. No SDRF has been produced.

### PXD010527 — held after first independent review

The depositor's design table maps all 33 RAW files. A 20-run draft for four complete five-fraction WT and mutant SPOP pull-down groups passed official validation. Independent review rejected its DDA acquisition annotation because the [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6182143/) and PRIDE protocol do not state the mode. The [hold record](../../annotations/PXD010527.BLOCKED.md) identifies the evidence needed before further review. No SDRF was approved.

### PXD016522 — held after first independent review

The [paper](https://doi.org/10.1093/gigascience/giz152) and PRIDE protocol identify one giant-squid mantle sample, Q Exactive and top-12 DDA. A 41-run draft covered every RAW file and passed deterministic validation, but the A/B/E/Off-Gel filename series cannot be assigned to biological sources or fractions from the available documentation. Independent review also found that the protocol's “tryptic peptides” phrase does not directly identify the digest reagent. The [hold record](../../annotations/PXD016522.BLOCKED.md) preserves the review findings. No SDRF was approved.

### PXD042172 — glycopeptide subset approved after independent review

The [eight-row glycopeptide SDRF](../../annotations/PXD042172-glycopeptides.sdrf.tsv) covers the flow-through and eluate files for duplicate total-cell-lysate and cell-surface preparations of N/TERT-1 keratinocytes. The [paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC10688226/) supports the preparation, trypsin digest, Orbitrap Fusion Lumos and DDA HCD settings; [Cellosaurus](https://www.cellosaurus.org/CVCL_CW92) supports the human cell-line identity. All eight RAW names match the accession file list. Official validation passed with one cell-line ontology warning because N/TERT-1 is absent from the validator's CLO/BTO/EFO lookup. Structure and offline checks passed, and fresh independent review approved SHA-256 `3a7568cbf16b63e27aaf20003710e731449e4d0b5d61dabe8f1082a0dfec0730`. The other 15 RAW files comprise nine in-depth DIA proteomics runs with a mixed Lys-C/Trypsin digest and six released-glycan runs outside the installed proteomics template's scope; these remain unannotated.

### PXD071605 — held for TMT channel mapping

The accession has 30 RAW runs: 20 input fractions, five acetyl-enriched pools and five phospho-enriched pools. The [paper](https://doi.org/10.1111/nph.71214) identifies three biological replicates of wild-type and `rak1-1` moss, but does not map those six samples to the six TMT reporter channels. The [hold record](../../annotations/PXD071605.BLOCKED.md) identifies the deposited result file that may contain the missing map. No SDRF has been produced.
