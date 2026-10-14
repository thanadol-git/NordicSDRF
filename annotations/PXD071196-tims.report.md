# PXD071196-tims

Status: validated local annotation; independent review pending. PR not created.

- TCR T cells targeting IgA- and IgG-expressing multiple myeloma (PXD071196)
- SDRF: `annotations/PXD071196-tims.sdrf.tsv`
- Rows: 2; columns: 39
- SHA-256: `be2072951a61fac740dd05ae383f1394796075dcb555d9fbe0c2c23a07ad8dc5`
- Evidence manifest: `annotations/PXD071196-tims.evidence.json`
- Scope: 2 timsTOF Pro DDA-PASEF runs (.d.zip), Ig immunopeptidome

## Validation

- parse_sdrf validate-sdrf (ms-proteomics, human, immunopeptidomics) --use_ols_cache_only: no errors
- tools structure: OK
- tools check: CLEAN, 0 hallucinated terms
- RAW coverage exact: every file in raw.json claimed once

## Limitations

- Full text of the associated paper (doi 10.1182/blood.2025031897) was not available (not open access, no preprint found); no claim cites the paper. All values come from the PRIDE record, RAW headers and deposited .pin files.
- The deposit is split into three SDRFs (PXD071196-hf, -qe, -tims) because RAW headers show Q Exactive HF (2023), Q Exactive (2021) and timsTOF Pro (.d.zip) acquisitions with different methods.
- Modifications were inferred from mass shifts in the deposited FragPipe .pin files (+15.9949 on M, +119.0041 on C, +42.0106 N-term, pyro-Glu features); no fragger.params was deposited, so fixed/variable status, tolerances and enzyme rest on the stated 'default Nonspecific-HLA workflow'. Tolerances = not available; cleavage = not applicable (non-specific).
- Run-to-sample mapping is not deposited; sources are named from file names only. Biological replicate numbers are ordinal, not from a mapping.
- HLA-A*02:01 typing is as stated in the protocol for all three cell lines; other HLA alleles are unknown. Antibody enrichment = not applicable (Strep-Tactin beads on tagged HLA, per protocol).
- Fractionation method not stated; the two EBVA2 files (20% and 30% ACN, 5 mM NH4OH) are treated as fractions 1 and 2 of one sample (ordinal numbering) - an interpretation of the file names.
- Organism part and cell type set to not available (PRIDE lists 'B cell, Cell culture' at project level only).
- Cell line identity not assigned for IGHA1_A2 / IGHG1_A2 (likely transduced 721.221 or similar, but no mapping), so cell-lines template omitted. Dissociation and collision energy not available (ion mobility-dependent 20-59 eV in protocol, no dissociation type stated). Deposited .d.zip archives were not unpacked; acquisition details come from the protocol text only.
