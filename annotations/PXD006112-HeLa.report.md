# PXD006112-HeLa

Status: validated annotation; independent review pending.

- Dataset: "Improved reversed phase chromatography of hydrophilic peptides from spatial and temporal changes in column temperature" (PXD006112), Department of Proteomics, Novo Nordisk Foundation Center for Protein Research, University of Copenhagen, Denmark (PI Michael Lund Nielsen; submitter Clifford Young).
- Paper: Young C, Podtelejnikov AV, Nielsen ML. J Proteome Res 2017;16(6):2307-2317, PMID 28387123, doi:10.1021/acs.jproteome.6b01055. The full text was **not accessible** (ACS paywall, no PMC copy). Methods come from the PRIDE protocol fields and the abstract.
- Not previously annotated: `datasets/PXD006112` and `sandbox/PXD006112` both return 404 in bigbio/sdrf-annotated-datasets.
- SDRF: `annotations/PXD006112-HeLa.sdrf.tsv`, 12 rows x 41 columns.
- SHA-256: `a1afe2034cca6f59d2b3dbd7e3ab7e17ef573a5a389947be2ee4744c3f2d67a1`
- Evidence manifest: `annotations/PXD006112-HeLa.evidence.json`
- Companion SDRFs: `annotations/PXD006112-BSA.sdrf.tsv` and `annotations/PXD006112-isoAsp.sdrf.tsv`. The deposit splits by sample, gradient, MS settings and search; see the BSA report for the reasons.

## Templates

`ms-proteomics` v1.1.0 + `human` v1.1.0 + `cell-lines` v1.1.0. The sample is the Thermo Pierce HeLa protein digest standard, a human cell line. DDA, so no DIA layer. The validator was run against the union of the three templates.

## Design and file mapping

- Study design: 500 ng of HeLa digest was run with a 140 min method under six column-temperature methods, each in duplicate. The protocol says "All temperature methods were conducted in duplicate".
- Source = digest x temperature method, e.g. `HeLa digest, temperature method 0-50 25 25`, giving 6 sources x 2 injections. `characteristics[biological replicate]` = 1 (one commercial digest). `comment[technical replicate]` = 1-2 within each source. Fraction 1 throughout.
- Factor: `factor value[elution conditions]` mirrors `comment[elution conditions]` (OBI:0302905, free text), describing each run's temperature method.
- How the mapping was established: three independent sources agree for all 12 runs.
  - The RAW-header sample comment, e.g. `500 ng Pierce HeLa DTF 0-50 25 25 Long140min`.
  - The Readme pictogram table.
  - The MaxQuant experiment names in `summary.txt` (`PierceHeLa_01+02`, `03+04`, ... `11+12`), which pair the same runs.

| Source (method) | Runs |
|---|---|
| 25 25 25 | 01, 02 |
| DTF DTF (zone 1 and 2 cold then 50 °C, zone 3 50 °C) | 03, 04 |
| 0-50 25 25 (precolumn 0 °C at loading, then 50 °C) | 05, 06 |
| 0 25 25 | 07, 08 |
| 25 DTF DTF (zone 2 cold then 50 °C, zone 3 50 °C) | 09, 10 |
| 25 25 50 | 11, 12 |

- Cell line values come from Cellosaurus CVCL_0030 (`sdrf-tools cellline lookup HeLa` plus the Cellosaurus API):
  - organism `Homo sapiens`; organism part `uterine cervix` (UBERON:0000002); cell type `epithelial cell`.
  - disease `cervical adenocarcinoma`: NCIt C27677 has no MONDO cross-reference, so it was matched by label to MONDO:0005153.
  - sex `female`; age `30Y6M`; ancestry category `African American` (HANCESTRO:0568, from Cellosaurus "Population: African American").
  - material type `cell line`.

## Technical values (all rows)

- Instrument `NT=Q Exactive Plus;AC=MS:1002634`, from the RAW headers ("Q Exactive Plus - Orbitrap MS") and the protocol. PRIDE's structured field says Q Exactive.
- DDA top-12 (`PRIDE:0000627`). HCD (`MS:1000422`) with `25 NCE`: the HeLa method is described as "similarly configured", with no change to NCE stated. MS2 in the orbitrap at 17,500 resolution. Label free.
- Cleavage agent `NT=Trypsin;AC=MS:1001251`. MaxQuant was set to Trypsin/P specific, and about 99% of peptide C-termini in the first 12,715 rows of the deposited `evidence.txt` are K or R. Thermo's product page could not be fetched (403), so the vendor's digestion protocol (trypsin alone or a trypsin/Lys-C mix) is unconfirmed.
- Modifications from the MaxQuant `summary.txt` and `parameters.txt` (1.5.1.2): Carbamidomethyl C fixed, Acetyl protein N-term variable, Oxidation M variable.
- Tolerances `4.5 ppm` (main search) and `20 ppm` (MS/MS), from the protocol ("majority of search settings from the BSA analysis were also employed").
- No MS1 scan range is given: the protocol does not restate it for HeLa.

## Validation

- `parse_sdrf validate-sdrf -s PXD006112-HeLa.sdrf.tsv -t ms-proteomics -t human -t cell-lines --use_ols_cache_only`: exit 0, "Everything seems to be fine. Well done." (0 errors, 0 warnings).
- `sdrf-tools check` (online): exit 0, 15/15 terms verified, CLEAN.
- `sdrf-tools structure`: OK.
- `sdrf-tools reconcile`: "every annotated value agrees with the deposit record".

## Limitations

- **Paper not read** (paywalled). The deposit and the PRIDE protocol text are the evidence.
- **Temperature zones.** Zone 1 is the precolumn (from the abstract: "increasing the precolumn temperature to 50 °C after the 500 ng sample was loaded at a low temperature"). Zones 2 and 3 are not physically located in the accessible evidence. The cold value of "DTF" zones is not stated and is written as "cold".
- **Donor characteristics.** Age, sex, ancestry and disease are Cellosaurus facts about the HeLa line, not measurements of this lot.
- **Not available.** `passage number`, `culture medium`, `sample storage temperature` and `individual` are `not available`: this is a commercial digest standard and the lot is not stated.
- **Stray header string.** The RAW headers also carry a `50 fmol BSA` string in a separate field. The protocol does not describe BSA in HeLa runs, so it is not annotated.
