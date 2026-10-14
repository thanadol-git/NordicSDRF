# PXD029717-hplc

Status: validated local annotation; independent review pending. PR not created.

- Venoms for all occasions: sea anemone (Telmatactis stephensoni) milked venom proteomics (RP-HPLC fractions)
- SDRF: `annotations/PXD029717-hplc.sdrf.tsv`
- Rows: 35; columns: 31
- SHA-256: `e9fff38a8500cec93536cbca0303cf811653ee0ab086b33fa3e6534af70897ec`
- Evidence manifest: `annotations/PXD029717-hplc.evidence.json`
- Scope: 35 .wiff runs, RP-HPLC fractions of milked venom

## Validation

- parse_sdrf ms-proteomics + invertebrates: clean
- tools structure: OK
- tools check: CLEAN (11 verified)
- RAW coverage: 35/35 .wiff once

## Limitations

- Full text not accessible (not in Europe PMC open set); only PRIDE text, abstract and deposited ProteinPilot summaries were used.
- Only .wiff files claimed as runs; .wiff.scan companion files are not separate injections.
- Mass tolerances, dissociation method, reduction reagent and acquisition details not stated: not available/omitted.
- Deposit split in two SDRFs because the deposited ProteinPilot outputs show different Cys alkylation/modification sets (iodoethanol-derived Ethanolyl vs Carbamidomethyl).
- Sample identity relation between HPLC and in-gel workflows (same venom pool or not) and meaning of 'TD' in run names unknown; biological replicate 1 is a placeholder.
- RP-HPLC fraction numbers 25 and 30 are absent from the deposit; fraction identifiers follow file order, not original fraction numbers.
- No factor values: no comparison between samples is encoded.
- Animal is an invertebrate: invertebrates template declared; developmental stage, strain and material type are not available.
- Ethanolyl(C) is encoded as fixed Cys alkylation; the four variable modifications are a subset seen in the deposited PeptideSummary (other hits such as Ethanolyl(K), pyro-Glu exist), as search parameters were not deposited.
