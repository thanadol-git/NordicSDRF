# PXD035945-kidney

Status: validated local annotation; independent review pending. PR not created.

- Type IV collagen gel bands from kidneys of P4ha2+/+ and P4ha2-/- mice - prolyl 4-hydroxylation, University of Turku (Matrix Biol 2024).
- SDRF: `annotations/PXD035945-kidney.sdrf.tsv`
- Rows: 18; columns: 32
- SHA-256: `b218fb63b6bc7da202c127a6834849d8c84963f476c1b1c38fca6f7ed58c8529`
- Evidence manifest: `annotations/PXD035945-kidney.evidence.json`
- Scope: 18 RAW files = 9 mice x 2 technical replicates, one SDS-PAGE lane per mouse; Q Exactive HF.

## Validation

- `parse_sdrf validate-sdrf --use_ols_cache_only`: passed (free-text enrichment/ontology warnings only).
- `sdrf-tools build`: RAW coverage exact, each deposited RAW file claimed once.

## Limitations

- The in-gel digestion used a Trypsin/Lys-C mix; recorded as Trypsin (reconciler flags it).
- Reconciler 'organism_part_from_cultured_material' is a false positive from the shared record (MEF part); this file is mouse kidney tissue.
- Galactosyl (UNIMOD:907) / Glucosylgalactosyl (UNIMOD:393) map the Mascot 'galactosyl(K)' and 'glukosylgalactosyl(K)' names; the exact Unimod entries were matched by name only.
- Age, sex and strain of mice not stated in the deposit: not available.
