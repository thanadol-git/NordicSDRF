# PXD026942-IPTL

Status: validated local annotation; independent review pending. PR not created.

- PXD026942: Comparison of LFQ and IPTL for protein identification and relative quantification (Jurkat E6.1) - IPTL runs
- SDRF: `annotations/PXD026942-IPTL.sdrf.tsv`
- Rows: 16; columns: 39
- SHA-256: `e5d8e0da5b8cff4b0b05dc2f4ac7d1730dce41cc16151f5661385a7b82a40865`
- Evidence manifest: `annotations/PXD026942-IPTL.evidence.json`
- Scope: IPTL RAW files only (8 files)

## Validation

- parse_sdrf validate-sdrf -t ms-proteomics -t human -t cell-lines --use_ols_cache_only: only warning is Cellosaurus recommended name not in CLO/BTO/EFO list for characteristics[cell line].
- tools structure: OK
- tools check: CLEAN
- RAW coverage exact: 8 RAW files, 16 rows.

## Limitations

- organism part, disease, passage number, culture medium set to not available (paper does not give ontology-ready values; Cellosaurus tissue/disease not copied).
- Age 14Y and sex male come from Cellosaurus, not from the paper.
- All 8 injections are replicates of one prepared sample per the paper; technical replicate numbers follow file-name order 1-8 (no deposited mapping beyond file names).
- Deposit split into -LFQ and -IPTL SDRFs because label and modification sets differ; the two share the same cell material. Reduction/alkylation reagent columns omitted (optional).
- Arg-d4 (SILAC) has no matching Unimod entry used in the deposited search; only Label:2H(4) on K is declared; the Mascot custom mod IsobaricSILAC_Lct (-0.0013 Da on KR) is not represented.
- Dimethyl and Dimethyl:2H(4) at Any N-term are inferred from Mascot custom modification mass deltas; the dat headers only name them IsobaricSILAC_*.
- The deposit holds no archives; only the two Mascot .dat files are non-RAW. SILAC d4 pair labelled "SILAC heavy" although d4 is a medium-type label; the crosswise dimethyl IPTL labeling of the pair is not a separate label column.
- Mascot headers were read by HTTP range (first 60 kB) only; the full .dat files were not parsed.
