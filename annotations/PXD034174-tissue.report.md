# PXD034174-tissue

Status: validated local annotation; independent review pending. PR not created.

- PXD034174 - Physiological constraints dictate toxin spatial heterogeneity in snake venom glands (Kazandjian et al., BMC Biol 2022)
- SDRF: `annotations/PXD034174-tissue.sdrf.tsv`
- Rows: 4; columns: 25
- SHA-256: `a72692fbea5216961162a7fba9f651c99cd9435caf657b422d82e2ddcda63178`
- Evidence manifest: `annotations/PXD034174-tissue.evidence.json`
- Scope: 4 tryptic on-section peptide samples of a N. nigricollis venom gland (quarters), TripleTOF 5600 DDA, ProteinPilot 4.5

## Validation

- parse_sdrf validate-sdrf -t ms-proteomics --use_ols_cache_only: clean
- tools structure: OK
- tools check: CLEAN (6/6 terms verified)
- Data files: 4/4 .wiff claimed once

## Limitations

- PXD034174 is split into three SDRFs because it holds three unrelated assays: tryptic LC-MS/MS of venom gland section quarters (-tissue), intact-venom LC-MS of spat vs milked venom (-venom), and MALDI mass spectrometry imaging (-msi).
- No organism template exists for snakes; only ms-proteomics is declared, with extra characteristics columns added.
- Each .wiff is claimed once; the companion .wiff.scan files are not listed as data files. imzML files (IMAGE DATA) are companions of the .ibd files; only .ibd (RAW category) are claimed.
- File names say Nmoss/Nmos/n-moss (Naja mossambica); the paper and PRIDE name the animal Naja nigricollis (Tanzanian origin), so Naja nigricollis is used. n-mel is mapped to Naja subfulva (paper: non-spitting cobra N. subfulva; PRIDE organism list) - the abbreviation itself is not decoded by any deposited file.
- Sex, age, developmental stage and strain are not reported and are not included.
- Quarter-to-gland-position (anterior/posterior) mapping is not deposited; quarter numbers follow file indices and are unverified. Biological replicate is 1 for all (pieces of one section, not replicates).
- Tolerances and dissociation not stated (not available); ProteinPilot .group/.xlsx outputs contain no readable modification list; variable modifications unknown beyond carbamidomethyl.
- Cell type is not available for tissue.
