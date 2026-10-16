# PXD005931-standards

Status: validated local annotation; independent review pending. PR not created.

- Large scale intact glycopeptide identification by Mascot database search (Bollineni et al., Sci Rep 2018, PMID 29391424, PMC5795011, full text read via Europe PMC)
- SDRF: `annotations/PXD005931-standards.sdrf.tsv`
- Rows: 5; columns: 29
- SHA-256: `c4a26990b747761cd21614980532f5310f7840d1bee6fc20f801203eea1bec7d`
- Evidence manifest: `annotations/PXD005931-standards.evidence.json`
- Scope: Bovine standard glycoproteins (alpha-1-acid glycoprotein, fetuin) analysed at different NCE; templates ms-proteomics + vertebrates

## Validation

- parse_sdrf validate-sdrf -t ms-proteomics -t vertebrates: 'Everything seems to be fine'
- tools structure: OK
- tools check: CLEAN (0 hallucinated)
- RAW coverage: 5/5 standard RAW files, each once

## Limitations

- Standards' sample preparation (reduction/alkylation, supplier) is not described in the paper text read; organism part, developmental stage, strain and sex are not applicable/not available.
- Alpha-1-acid files with different NCE are labelled technical replicates 1-4 only to keep rows unique; they are distinct acquisition settings, not true replicates.
- The deposit contains no archives (.zip/.tar); only individual RAW files were claimed (29 RAW: 24 serum, 5 standards, each exactly once).
- Glyco_Fuc_HexNAc (Mascot custom modification on the residue code O = HexNAc, 'fucose addition on HexNAc') has no Unimod entry; written without AC.
- Reduction/alkylation reagents and enrichment process (TiO2) are described in the paper but not encoded (optional columns, ontology terms not verified).
