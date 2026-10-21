# PXD050151 (proteome)

Status: validated annotation; independent review pending. PR not created.

- Dermokine (DMKN) knockout N/TERT-1 keratinocytes, 2D culture, DIA on Orbitrap Exploris 480, Spectronaut; Lyngby/DTU (NordicSDRF). This file covers the global proteome runs; the other half of the deposit is `PXD050151-phospho.sdrf.tsv`.
- SDRF: `annotations/PXD050151-proteome.sdrf.tsv`; rows 18; columns 36; SHA-256 `d49ec287e27d0c672dc5ba8705505450229f77a22c7fedaffb1e30c37bb5cfae`
- Evidence manifest: `annotations/PXD050151-proteome.evidence.json`
- Design: 3 genotypes (WT, DMKN beta/gamma KO, DMKN alpha/beta KO) x 2 treatments (untreated vs recombinant dermokine-beta "supplemented"/rescue) x 3 biological replicates = 18 runs, one RAW per row, label free. Run-to-condition map taken from deposited `ConditionSetup_v1.txt`. Factors: genotype, treatment.
- Why two SDRFs: proteome (EvoSep One, 2022-12-15) and phosphoproteome (Easy-nLC 1200, 140 min, 2022-11-27) differ in LC, enrichment and search modifications (Carbamidomethyl, Oxidation, Acetyl N-term).
- Templates: ms-proteomics v1.1.0, human, cell-lines. Template dia-acquisition not used (see below).

## Validation

- parse_sdrf validate-sdrf -t ms-proteomics -t human -t cell-lines --use_ols_cache_only: no errors, warnings only (free-text values not found in the ontology lists: treatment values, N/TERT-1 cell line).
- tools structure: OK. tools check --offline: CLEAN (0 hallucinated). tools reconcile: 1 MAJOR, cleavage_agent_incomplete (Lys-C not declared); the column is single-valued, so only Trypsin was recorded.
- Validator quirk: with dia-acquisition added, the documented form `NT=Data-independent acquisition;AC=PRIDE:0000450` is rejected ("Invalid value ... must be one of the allowed values") although the template lists it; the plain label `Data-independent acquisition` passes. I kept the NT/AC form and dropped the dia-acquisition template (its window columns have no deposited values anyway). A reviewer may prefer the opposite.
- RAW coverage: 18 of 18 proteome RAW files, each once (36 RAW in the deposit in total).

## Limitations

- Age not stated; Cellosaurus accession for N/TERT-1 not verified (not in the local DB), so `not available`; Cellosaurus name omitted.
- Mapping of DMKN_BG_KO (labelled DTU) to beta/gamma KO and DMKN_AB_KO (labelled CS) to alpha/beta KO is inferred from the paper's naming. Whether the WT "supplemented" arm received the same recombinant dermokine-beta is inferred from the condition label.
- PRIDE disease 'Wounds and injuries' not used; cultured keratinocytes from normal foreskin recorded as `normal`.
- Modifications are from the PRIDE processing prose; the Spectronaut .sne archives (7.8 and 11.8 GB) were not opened. Tolerances and dissociation method are `not available`; RAW headers not read. Lys-C pre-digestion (before trypsin) not representable.
- characteristics[genotype] and [treatment] are not columns of the selected templates; used as additional columns and mirrored in factor values.
- The 3D organotypic culture proteomics in the paper is not part of this PRIDE project (PARTIAL submission).
- Culture medium, passage number, storage temperature not recorded (medium details are in the paper, not mapped to NCIT terms).
