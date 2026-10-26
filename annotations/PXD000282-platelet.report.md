# PXD000282-platelet

Status: validated annotation; independent review pending.

- Dataset: "EPAC1 knockout mouse effects in platelets and plasma" (PXD000282), Proteomics Unit, Department of Biomedicine, University of Bergen, Norway (PI Frode Selheim; submitter Eystein Oveland).
- Paper: Nygaard G et al. "Epac1-deficient mice have bleeding phenotype and thrombocytes with decreased GPIbβ expression", Sci Rep 2017;7:8725, PMID 28821815, PMC5562764, doi:10.1038/s41598-017-08975-y (open access; full text and Supplementary Dataset 1 read).
- Not previously annotated: `datasets/PXD000282` and `sandbox/PXD000282` both 404 in bigbio/sdrf-annotated-datasets.
- SDRF: `annotations/PXD000282-platelet.sdrf.tsv`, 48 rows x 34 columns.
- SHA-256: `6454d5fdb82235e19aabbe383030c2acfee314e69b4fe819892601e2043558f3`
- Evidence manifest: `annotations/PXD000282-platelet.evidence.json`
- Companion SDRF: `annotations/PXD000282-plasma.sdrf.tsv` (plasma sub-experiment; see that report for why the deposit is split).

## Templates

`ms-proteomics` v1.1.0 (LC-MS/MS, DDA) + `vertebrates` v1.1.0 (Mus musculus). Platelets are primary cells isolated from blood, not a cell line, so `cell-lines` does not apply.

## Design and file mapping

- Gel-filtered platelets from Epac1-/- and wild-type C57BL/6JBomTac mice. 10 µg of platelet protein per genotype was run on a 10% SDS-PAGE gel, sliced into bands and digested in-gel with trypsin. Each band was run once, label-free (90 min gradient).
- Two sources, `WT_platelets` and `Epac1KO_platelets`, each with `characteristics[biological replicate]` = 1. Each source has 24 rows: `P_WT_1..24.raw` and `P_KO_1..24.raw` are fractions 1-24, ordered by the number in the deposited file name. Total 48 rows = 48 RAW files, each claimed once.
- Mapping source: deposited file names (`P_WT_n` / `P_KO_n`). The deposited Scaffold PRIDE XMLs give the same two-group split: Ac_29636 "Wild-type mice in EPAC label-free proteomics", source folder "Mouse platelets wild type", MaxQuant experiment E1; Ac_29637 "EPAC knockout mice ...", folder "Mouse platelets EPAC KO", experiment E2. Supplementary Table S4 agrees: E1 GPIbβ intensity 7048600 = Table 2 WT, E2 919540 = Table 2 Epac1-/-.
- Factor: `factor value[genotype]` = `Epac1-/-` / `wild type`, mirroring `characteristics[genotype]`.

## Technical values (all rows)

- Instrument `NT=Orbitrap Velos Pro;AC=MS:1003096` (RAW headers, all 48 read; Scaffold XML "Orbitrap Velos Pro"). PRIDE's "LTQ Orbitrap" was overridden.
- DDA (`PRIDE:0000627`), CID (`MS:1000133`) at 35% NCE, MS2 in the linear ion trap (`MS:1000083`), MS1 300-2000 m/z.
- Trypsin (`MS:1001251`). Fractionation `NT=SDS PAGE;AC=PRIDE:0000568`, a descendant of PRIDE:0000550 in live OLS.
- Precursor tolerance 6 ppm (MaxQuant main search; first search 20 ppm), from Supplementary S5. Fragment tolerance `not available`: S5 says only "MaxQuant's default settings".
- Modifications from Supplementary S5: Carbamidomethyl C fixed (UNIMOD:4); Oxidation M (UNIMOD:35) and Acetyl protein N-term (UNIMOD:1) variable. No mqpar.xml or summary.txt was deposited, so these could not be read from search files.

## Validation

- `sdrf-tools build ... -t ms-proteomics -t vertebrates`: wrote 48 rows x 34 columns.
- `sdrf-tools reconcile ... --record project.json --accession PXD000282`: "every annotated value agrees with the deposit record" (exit 0).
- `timeout 900 parse_sdrf validate-sdrf -s PXD000282-platelet.sdrf.tsv -t ms-proteomics -t vertebrates --use_ols_cache_only`: exit 0, 0 errors, 1 warning: `C57BL/6JBomTac` in `characteristics[strain or breed]` is not found in NCBITaxon. No such term exists in live OLS, and the column is free text in TERMS.tsv, so it is kept.
- `sdrf-tools structure`: OK. `sdrf-tools check --offline`: CLEAN.
- One validation round. Independent adversarial review not run (by instruction).

## Limitations

- **Genotype per file rests on the deposited names only.** The RAW headers show that all 48 platelet runs were acquired in one folder, `20120625_Platelets_KO`. The files deposited as `P_WT_n` were acquired as `P_KO_n` (n = 1-24), and those deposited as `P_KO_n` were acquired as `P_KO_1nn` (101-124; `P_KO_3` was `P_KO_103ny`). The submitter's renaming at deposition is taken as the genotype statement. It is consistent with the 24 + 24 split and the two Scaffold experiments, but the PRIDE XML spectra carry no per-file reference, so it could not be checked independently.
- **24 files vs 23 bands.** The paper and S5 say the gel was cut into 23 bands, and S4 shows 23 slices per MaxQuant experiment (201-223, 301-323). The Scaffold source file is "P_KO_1 and 45 more", i.e. 46 runs analysed. So 48 runs were deposited and one per genotype was apparently not analysed; which one is not recoverable. All 24 are annotated as fractions 1-24.
- Fraction order = file number (inferred; gel-band position per file is not stated). The MaxQuant slice numbers (2xx/3xx) do not match the file numbers (1-24/101-124), so fraction mapping cannot be cross-checked.
- Pooling: not stated whether each genotype's lane came from one mouse or pooled platelets; `characteristics[pooled sample]` is omitted and biological replicate = 1.
- `characteristics[sex]`, `characteristics[developmental stage]`: `not available` (not stated).
- `characteristics[organism part]` = `blood`, `characteristics[cell type]` = `platelet` (CL:0000233). PRIDE also lists BTO "blood platelet".
- `characteristics[disease]` = `normal` for both genotypes, following the paper's statement that Epac1-/- mice are healthy under standard housing.
- `characteristics[genotype]` is an extra free-text column outside the vertebrates template.
- Fragment tolerance not filled. The MaxQuant 1.3 ion-trap default (0.5 Da) is not stated in any source, so it is left as `not available` rather than inferred.
- Reduction/alkylation reagents for the in-gel digest are not stated in the paper (the protocol is cited as ref. 25 only), so those columns are omitted.
