# PXD005931-serum

Status: validated local annotation; independent review pending. PR not created.

- Large scale intact glycopeptide identification by Mascot database search (Bollineni et al., Sci Rep 2018, PMID 29391424, PMC5795011, full text read via Europe PMC)
- SDRF: `annotations/PXD005931-serum.sdrf.tsv`
- Rows: 24; columns: 31
- SHA-256: `a70c7eecbb6bae7425fb7b6f72099ced822ccf27c3a983830deca110e0363176`
- Evidence manifest: `annotations/PXD005931-serum.evidence.json`
- Scope: 24 Janus Serum Bank serum samples, sialylated glycopeptides (TiO2), Q Exactive DDA; templates ms-proteomics + human

## Validation

- parse_sdrf validate-sdrf -t ms-proteomics -t human: 'Everything seems to be fine'
- tools structure: OK
- tools check: CLEAN (0 hallucinated)
- RAW coverage: 24/24 serum RAW files, each once

## Limitations

- PRIDE text says serum from 'healthy individuals and prostate cancer patients' while the paper Methods describe all 24 donors as prostate cancer patients; the paper was followed (disease = prostate adenocarcinoma, per PRIDE disease field).
- Mapping of Janus numbers to the two clinical groups (localized vs high-risk/metastatic) is not deposited in files read (the 5 GB .rov Distiller file was not parsed); no factor value was added, and age/ancestry/individual are not available.
- Biological replicate set to 1 for all donors because no replicate structure is supported; RB_161102_JANUS39_TIO2.raw was acquired two days before the rest (161102 vs 161104) but is a serum sample with the same method.
- The deposit contains no archives (.zip/.tar); only individual RAW files were claimed (29 RAW: 24 serum, 5 standards, each exactly once).
- Glyco_Fuc_HexNAc (Mascot custom modification on the residue code O = HexNAc, 'fucose addition on HexNAc') has no Unimod entry; written without AC.
- Reduction/alkylation reagents and enrichment process (TiO2) are described in the paper but not encoded (optional columns, ontology terms not verified).
