# PXD043021-swath

Status: validated annotation; independent review pending.

PRIDE title: "Escherichia coli displays a conserved membrane proteomic response to a range of alcohols". Aarhus University (lab PI Thomas Seviour); LC-MS at the Protein and Proteomics Centre, National University of Singapore. Paper: Biotechnol Biofuels Bioprod 2023, DOI 10.1186/s13068-023-02401-4, PMC10546733 (open access; Methods read).

- SDRF: `annotations/PXD043021-swath.sdrf.tsv`, 12 rows × 35 columns (12 SWATH runs, one per sample)
- SHA-256: `51f88b9e61fecf5b9227bbca00ad1595c2e1ec0e674f127372578278f3149ce6`
- Companion SDRFs from the same deposit: `PXD043021-ida` (3 IDA library injections of the pooled sample) and `PXD043021-mrmhr` (6 targeted MRM-HR runs)
- Evidence manifest: `annotations/PXD043021-swath.evidence.json`; working files in `sdrf-skills/scratchpad/PXD043021/`

## Templates
`ms-proteomics` v1.1.0 + `dia-acquisition` v1.1.0 (SWATH on a TripleTOF 6600). No organism template applies to bacteria (ms-proteomics only). The IDA and MRM-HR files use `ms-proteomics` alone.

## Design and file mapping (stated)
PRIDE protocol: 12 samples of E. coli grown without alcohol (07, 08, 09), with ethanol (05, 10, 11), butanol (01, 03, 04) or hexanol (02, 06, 12), three biological replicates each. File names `SWATH_2ul_<Control|Ethanol|Butanol|Hexanol>_<NN>.wiff` carry the sample number and condition and agree with that grouping. Alcohol at its MIC50 concentration in LB with 5 g/L glucose, cultures grown 18 h at 37 degC (paper Methods); total membrane fraction by ultracentrifugation. Factor: `factor value[treatment]`. `.wiff.scan` companions are not listed as runs.

## Technical values
TripleTOF 6600 (PRIDE record; paper). SWATH: 100 variable windows across 400-1200 m/z (paper; window table in a supplementary file not read, so isolation width is `not available`), rolling collision energy with 5 eV spread (not expressible as a number: `not available`); CID on the TripleTOF is instrument-determined. MMTS cysteine alkylation (Methylthio, UNIMOD:39, fixed) is taken from the ProteinPilot/Paragon library search parameters. Library search tolerances are not given; the SWATH extraction used 75 ppm: not an MS tolerance, so tolerances are `not available`.

## Validation
- `sdrf-tools build -t ms-proteomics -t dia-acquisition`: 12 rows × 35 columns.
- `parse_sdrf validate-sdrf … --use_ols_cache_only`: 0 errors; 4 warnings (alcohol names and the enrichment text not in NCIT/EFO/PRIDE).
- `check --offline`: CLEAN. `structure`: OK.
- `reconcile`: 1 BLOCKER `cleavage_agent_unsupported`: neither PRIDE nor the paper names the digestion enzyme (S-Trap micro-column digestion "according to the manufacturer's recommendations"). **Trypsin is an assumption** (S-Trap default; Paragon default); `cleavage agent details` cannot be `not available`. This is the first thing for a reviewer to attack.

## Limitations
- Strain is not stated for the proteomics samples (the paper uses E. coli BW25113 for growth inhibition and several deletion strains; the library search used the K-12 proteome); no strain column is written.
- Alcohol concentration (MIC50, differs per alcohol) is in the paper's Supplementary Fig. S1 and not recorded; treatment is the alcohol name only.
- Organism part / cell type `not applicable`; `material type` = cell.
