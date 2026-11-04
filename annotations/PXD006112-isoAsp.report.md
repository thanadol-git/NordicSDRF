# PXD006112-isoAsp

Status: validated annotation; independent review pending. PARTIAL: the temperature method (the factor) could not be established for 18 of the 42 runs (six 12-peptide-mix triplets); they carry `not available`.

- Dataset: "Improved reversed phase chromatography of hydrophilic peptides from spatial and temporal changes in column temperature" (PXD006112), Department of Proteomics, Novo Nordisk Foundation Center for Protein Research, University of Copenhagen, Denmark (PI Michael Lund Nielsen; submitter Clifford Young).
- Paper: Young C, Podtelejnikov AV, Nielsen ML. J Proteome Res 2017;16(6):2307-2317, PMID 28387123, doi:10.1021/acs.jproteome.6b01055. The full text was **not accessible** (ACS paywall, no PMC copy, repository records metadata-only). Methods come from the PRIDE protocol fields and the abstract.
- Not previously annotated: `datasets/PXD006112` and `sandbox/PXD006112` both return 404 in bigbio/sdrf-annotated-datasets.
- SDRF: `annotations/PXD006112-isoAsp.sdrf.tsv`, 42 rows x 28 columns.
- SHA-256: `eb3c56aaa694df994ddcfd734af0530df908785d3a98b0f570086072d02e1ef3`
- Evidence manifest: `annotations/PXD006112-isoAsp.evidence.json`
- Companion SDRFs: `annotations/PXD006112-BSA.sdrf.tsv` and `annotations/PXD006112-HeLa.sdrf.tsv`. See the BSA report for why the deposit is split.

## Templates

`ms-proteomics` v1.1.0 only. The samples are synthetic peptides from Thermo Scientific (purity >97%), so no organism, cell-line or clinical layer applies. DDA, so no DIA layer.

## Design and file mapping

- Study design: twelve synthetic peptides were chosen because their aspartic and isoaspartic acid forms co-elute or elute close together. About 208 pg of each peptide was loaded; the RAW headers say "2.5 ng Thermo IsoAsp 12mix" for the mixture and "0.83 ng ... Peptide 11/12" for single peptides. Runs used a 40 min method with dynamic exclusion 0 and were analysed in triplicate under column-temperature methods. Peptide 11 (Asp form, `D_Peptide11`) and peptide 12 (isoAsp form, `IsoD_Peptide12`) were also run alone under two methods.
- Source = sample x run triplet:
  - `IsoAsp 12-peptide mix, runs 08-10`, for each of the 10 mixture triplets. These are named by run numbers because the method is disputed for six of them.
  - `synthetic peptide 11 (aspartic acid form), temperature method 25 25 5C`, and the equivalents for the single peptides.
  - `characteristics[biological replicate]` = 1. `comment[technical replicate]` = 1-3 within each source. Fraction 1 throughout.
- Factor: `factor value[elution conditions]` mirrors `comment[elution conditions]` (OBI:0302905, free text).
- How the mapping was established: the RAW-header sample comment (HTTP range read of all 42 RAW files) was compared with the deposited `Readme.pdf` pictogram table. Both sources group the same runs into the same triplets. They agree on the method for 24 runs and **conflict for 18 runs**: the same six methods are assigned to the six triplets in a different order.

| 12mix triplet | RAW header method | Readme pictogram | Written |
|---|---|---|---|
| 01, 02, 05 | 25 25 25 | 25 25 25 | 25 25 25 |
| 08, 09, 10 | DTF DTF | zone 1 cold, 25, 25 | not available |
| 11, 12, 14 | 0 25 25 | zone 1 50 °C, 25, 25 | not available |
| 16, 18, 20 | 0-50 25 25 | 25, zone 2 cold, 25 | not available |
| 21, 22, 24 | 25 5 25 | 25, zone 2 50 °C, 25 | not available |
| 27, 29, 30 | 25 25 5C | 25, 25, zone 3 cold | 25 25 5C |
| 31, 33, 34 | 25 25 50 | 25, 25, zone 3 50 °C | 25 25 50 |
| 36, 38, 39 | 25 50 25 | zone 1 cold then 50 °C, 25, 25 | not available |
| 41, 42, 45 | 50 25 25 | DTF DTF | not available |
| 46, 47, 50 | 25 5 5D | 25, zone 2 and 3 cold | 25 5 5D |

| Single peptide | Runs | Method (header = Readme) |
|---|---|---|
| peptide 11 (Asp) | 06, 07, 08 | 25 25 5C |
| peptide 11 (Asp) | 01, 02, 05 | 25 5 5D |
| peptide 12 (isoAsp) | 06, 09, 10 | 25 25 5C |
| peptide 12 (isoAsp) | 01, 03, 04 | 25 5 5D |

- Neither source could be shown to be wrong without the paper. The RAW-header comment is typed into the acquisition sequence; the Readme was drawn for the 2017 deposit. Writing either set would risk a wrong specific value for 18 runs, so they are `not available`. Both candidate methods are listed above.
- Original acquisition names in the headers equal the deposited names, apart from `QE6+` -> `QE6` and a timestamp suffix on Peptide11_06 and Peptide11_08.

## Technical values (all rows)

- Instrument `NT=Q Exactive Plus;AC=MS:1002634` (RAW headers). DDA (`PRIDE:0000627`). HCD (`MS:1000422`) with `25 NCE`; MS2 in the orbitrap; "mass spectra were acquired in a similar manner as the BSA samples, but dynamic exclusion was set to zero". Label free.
- `comment[cleavage agent details]` = `not applicable`: the synthetic peptides were not digested.
- `comment[modification parameters]` and both tolerances = `not applicable`: no database search was done. Retention times and peak areas came from Xcalibur 3.0.63 (Genesis peak detection), and no search output was deposited for these runs.
- `characteristics[organism]`, `organism part`, `cell type` and `disease` = `not applicable`. `material type` = `synthetic`; `synthetic peptide` = `synthetic`.

## Validation

- `parse_sdrf validate-sdrf -s PXD006112-isoAsp.sdrf.tsv -t ms-proteomics --use_ols_cache_only`: exit 0, "Everything seems to be fine. Well done." (0 errors, 0 warnings).
- `sdrf-tools check` (online): exit 0, 5/5 terms verified, CLEAN.
- `sdrf-tools structure`: OK.
- `sdrf-tools reconcile`: exit 1, with two findings, both on `comment[cleavage agent details]`: BLOCKER `cleavage_agent_contradicted` and MAJOR `cleavage_agent_incomplete`, "the record's digest names Trypsin". **Rejected with counter-evidence.** The record's trypsin refers to the BSA and HeLa tryptic digests in the same project. The IsoAsp samples are "twelve synthetic peptides ... purchased from Thermo Scientific" (sample processing protocol) and were dissolved in water, not digested. `not applicable` is correct for this sub-experiment.

## Limitations

- **PARTIAL.** The temperature method is `not available` for 18 of 42 runs (12mix triplets 08-10, 11-14, 16-20, 21-24, 36-39, 41-45) because the RAW headers and the Readme conflict. The paper's run table would resolve it.
- **Peptide identities unknown.** The sequences of the twelve synthetic peptides, and of peptides 11 and 12, are not available (paper paywalled). Peptide 11 = aspartic acid form and peptide 12 = isoaspartic acid form are inferred from the file names (`D_Peptide11`, `IsoD_Peptide12`).
- **Temperature zones.** Zone 1 is the precolumn (abstract/protocol). Zones 2 and 3 are not physically located in accessible evidence, though the protocol mentions "methods involving cooling the middle of the analytical column". The cold value of "DTF" zones is not stated. The suffixes `5C` and `5D` are kept verbatim; their meaning is undocumented.
- **Stray header string.** Every RAW header also carries a `50 fmol BSA` string in a separate field. The protocol describes no BSA in the IsoAsp runs, so it is not annotated.
