# PXD033068-eclipse

Status: validated annotation; independent review pending.

PRIDE title: "The chromatin-regulating CoREST complex is animal specific and essential for development in the cnidarian Nematostella vectensis". Department of Biological Sciences (Sars Centre), University of Bergen (lab PI Fabian Rentzsch); proteomics at PROBE. Paper: Gahan JM et al., BMC Biol 2022, PMID 35999597, DOI 10.1186/s12915-022-01385-1 (not read). Sibling: `PXD033068-qe`.

- SDRF: `annotations/PXD033068-eclipse.sdrf.tsv`, 6 rows × 36 columns
- SHA-256: `158c4f69c51b81851d2ee378983d7471dd0c569ce133790d53c8158efe95b23d`
- Evidence manifest: `annotations/PXD033068-eclipse.evidence.json`; working files in `sdrf-skills/scratchpad/PXD033068/`

## Templates
`ms-proteomics` v1.1.0 + `invertebrates` v1.1.0 (Nematostella vectensis planula, GFP-Trap immunoprecipitation, label-free DDA).

## Design and file mapping
Planula-stage embryos from wild-type or NvLsd1-GFP/GFP crosses; IP with GFP-Trap or binding-control agarose beads (PRIDE protocol). **Which tissue/bead combination defines the control IP is not stated** (control vs GFP samples = `Control_*` vs `GFP_*`/`NvLsd1GFP` files), so the sample label is `control IP` vs `NvLsd1-GFP IP`. Factor: `factor value[treatment]`. On-bead digestion (DTT/iodoacetamide, 2 ug trypsin).

Final Orbitrap Eclipse runs: `Eclipse_270821_JamesGahan_Control_1-3` and `…_GFP_1-3` (three replicates each).

## Technical values
Trypsin (Promega). Fixed Carbamidomethyl C (alkylation stated); other search parameters not stated (MaxQuant 1.6.14.0 for QE files, Proteome Discoverer 2.5/SEQUEST HT for Eclipse files): variable modifications, tolerances `not available`. HCD. Orbitrap Eclipse with FAIMS Pro (CV -45/-65 V), HCD NCE 30, isolation 4 m/z, 30 000 resolution; same peptide amount per sample.

## Validation
`sdrf-tools build`: 6 rows × 36 columns; `parse_sdrf validate-sdrf … --use_ols_cache_only`: 0 errors (warnings only for free-text terms absent from the ontologies); `check --offline` CLEAN; `structure` OK; `reconcile`: all values agree with the record.

## Limitations
- Strain/age/sex `not available`; `whole organism` and developmental stage `planula` from the protocol; NCBITaxon:45351. `reconcile` reports instrument mismatches because the PRIDE record lists only Q Exactive HF while the protocol also uses an Orbitrap Eclipse (both files are annotated with their own instrument).
