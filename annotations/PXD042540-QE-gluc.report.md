# PXD042540-QE-gluc

Status: validated local annotation; independent review pending. PR not created.

- Characterization of the biochemical activity and tumor-promoting role of the dual protein methyltransferase METL-13/METTL13 in Caenorhabditis elegans
- SDRF: `annotations/PXD042540-QE-gluc.sdrf.tsv`
- Rows: 1; columns: 33
- SHA-256: `f8db59135e4934e86aee995c562cbc439deaf3521faa4f25052cae6bba4a4bc0`
- Evidence manifest: `annotations/PXD042540-QE-gluc.evidence.json`
- Scope: One of 3 suffixed SDRFs for PXD042540 split by instrument/enzyme: QE-gluc

## Validation

- parse_sdrf validate-sdrf (ms-proteomics + invertebrates, --use_ols_cache_only): clean for all three files
- tools structure: OK
- tools check: CLEAN (13 terms verified each)
- File coverage: each of the 4 injections claimed exactly once (3 RAW + 1 .d.7z)

## Limitations

- Per-file genotype/strain (wild type N2 vs metl-13(tm6870) etc.) is not stated in PRIDE, file names or deposited files; strain, genotype, developmental stage and cell type set to 'not available'. No factor value column added.
- Biological replicate numbering is unknown; each injection is given biological replicate 1 as a placeholder, not evidence that they are independent animals.
- Dissociation method not stated in PRIDE/paper; set to 'not available'.
- Deposit was split by instrument and enzyme because the cleavage agent differs per injection (chymotrypsin vs Glu-C, taken from the PEAKS .mzid enzyme regex and file names Cym/GluC/Chymo) and the instrument differs (Q Exactive confirmed from RAW headers; timsTOF Pro from paper text and mzid ion mobility values).
- The enzyme for GC1 (timsTOF) is inferred from its mzid (Glu-C regex), file name 'GC'; acquisition method for the timsTOF run is recorded as DDA though not stated explicitly (PASEF details unknown).
- timsTOF data is a Bruker .d folder deposited as 210520_Engelfriet_GC1_698.d.7z; it is used as the data file name (not a RAW file) .
- Organism part 'whole body' follows PRIDE organismParts; the analysed material is an EEF-1A-enriched gel band from whole-animal extracts.
- Modifications/tolerances (15 ppm, 0.03 Da) come from the deposited PEAKS mzid files; propionamide (UNIMOD:24) is listed as variable as in the search; N-terminal methylations are protein N-terminal per mzid 'NT Protein' labels.
