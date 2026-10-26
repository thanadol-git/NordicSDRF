# PXD000282-plasma

Status: validated annotation; independent review pending.

- Dataset: "EPAC1 knockout mouse effects in platelets and plasma" (PXD000282), Proteomics Unit, Department of Biomedicine, University of Bergen, Norway (PI Frode Selheim; submitter Eystein Oveland).
- Paper: Nygaard G et al. "Epac1-deficient mice have bleeding phenotype and thrombocytes with decreased GPIbβ expression", Sci Rep 2017;7:8725, PMID 28821815, PMC5562764, doi:10.1038/s41598-017-08975-y (open access; full text and Supplementary Dataset 1 `41598_2017_8975_MOESM1_ESM.xls` read).
- Not previously annotated: `datasets/PXD000282` and `sandbox/PXD000282` both 404 in bigbio/sdrf-annotated-datasets.
- SDRF: `annotations/PXD000282-plasma.sdrf.tsv`, 23 rows x 35 columns.
- SHA-256: `2798d7c85f1ddccc15b784251a530c5ac0600a96cfdd3be0b27a6d98795e2573`
- Evidence manifest: `annotations/PXD000282-plasma.evidence.json`
- Companion SDRF: `annotations/PXD000282-platelet.sdrf.tsv` (same deposit, platelet sub-experiment).

## Why two SDRFs

The deposit holds two experiments that differ in sample, sample preparation, LC setup and search: plasma (in-solution digest, 180 min gradient on a 50 cm column, Progenesis LC-MS + SearchGUI/OMSSA/PeptideShaker, 0 missed cleavages, 10 ppm / 0.7 Da) and platelet lysate (SDS-PAGE, 23 bands in-gel, 90 min gradient on a 15 cm column, MaxQuant 1.3.05/Andromeda, Acetyl protein N-term, 6 ppm). The run-level search settings cannot be expressed in one file, so the deposit is split by search/design. This file covers the 23 plasma RAW files.

## Templates

`ms-proteomics` v1.1.0 (LC-MS/MS, DDA) + `vertebrates` v1.1.0 (Mus musculus). No DIA, cell-line, single-cell or clinical layer applies. The validator was run against the union.

## Design and file mapping

- Plasma from Epac1-/- (Rapgef3 knockout) and wild-type C57BL/6JBomTac mice. Each mouse gave a crude plasma sample and an albumin-depleted sample (Qproteome Murine Albumin Depletion Kit). Each was run once, label-free.
- Source = one mouse x one preparation, e.g. `Epac1KO_mouse3_plasma_crude`, `WT_mouse8_plasma_albumin-depleted`. `characteristics[biological replicate]` = the mouse number from the file name, so a mouse's crude and depleted rows share it. The exception is `12a_CTR_Crude.raw`: it is its own source, `WT_mouse12a_plasma_crude`, with biological replicate 14. That integer is unused elsewhere and is not a mouse ID from the deposit. `characteristics[depletion]` = `no depletion` (Crude) / `depletion` (Depl).
- Wild type: 10 rows. Mice 8, 9, 10 and 13 have crude + depleted runs. Mouse 12 has a depleted run (`12_CTR_Depl.raw`). Mouse 12a has a crude run (`12a_CTR_Crude.raw`). Epac1-/-: mice 1-6 crude + depleted, mouse 7 depleted only = 13 rows. Total 23 rows = 23 RAW files, each claimed once. Fraction 1 and technical replicate 1 throughout.
- Mapping source: the deposited RAW file names (`<mouse>_<KO|CTR>_<Crude|Depl>.raw`), cross-checked against the original acquisition paths in the RAW headers (`C:\Xcalibur\Data\FrodeS\20120621_EPAC_FSEO\<same name>`, all 23 read) and against the sample columns of Supplementary Table S1 (KO1, KO2and7, KO3-KO6, CTR8, CTR9, CTR10, CTR12, CTR13).
- Factor: `factor value[genotype]` = `Epac1-/-` / `wild type`, mirroring `characteristics[genotype]`.

## Technical values (all rows)

- Instrument `NT=Orbitrap Velos Pro;AC=MS:1003096`: RAW headers say "Orbitrap Velos Pro", matching Methods "LTQ-Orbitrap Velos Pro". PRIDE's structured field (LTQ Orbitrap, MS:1000449) is too generic and was overridden.
- DDA (`PRIDE:0000627`), CID (`MS:1000133`) at 35% NCE, MS2 in the linear ion trap (`MS:1000083`), MS1 scan range 300-2000 m/z (PRIDE sample protocol / paper Methods).
- Trypsin (`MS:1001251`); DTT (`PRIDE:0000608`) and iodoacetamide (`PRIDE:0000599`) from the supplementary in-solution trypsination protocol (S5).
- Precursor 10 ppm, fragment 0.7 Da: Methods text, and the deposited PeptideShaker PRIDE XMLs (Ac_29638 depleted, Ac_29639 crude) give "Peptide mass tolerance setting 10.0", "Fragment mass tolerance setting 0.7", "Allowed missed cleavages 0".
- Modifications: Carbamidomethyl C fixed (UNIMOD:4), Oxidation M variable (UNIMOD:35), from the PRIDE data-processing protocol and Supplementary S5.

## Validation

- `sdrf-tools build ... -t ms-proteomics -t vertebrates`: wrote 23 rows x 35 columns.
- `sdrf-tools reconcile ... --record project.json --accession PXD000282`: "every annotated value agrees with the deposit record" (exit 0).
- `timeout 900 parse_sdrf validate-sdrf -s PXD000282-plasma.sdrf.tsv -t ms-proteomics -t vertebrates --use_ols_cache_only`: exit 0, 0 errors, 1 warning: `C57BL/6JBomTac` in `characteristics[strain or breed]` is not found in NCBITaxon. Live OLS has no NCBITaxon or other term for this substrain, and TERMS.tsv defines the column as free text, so the paper's strain name is kept.
- `sdrf-tools structure`: OK. `sdrf-tools check --offline`: CLEAN (0 hallucinated, 0 UNIMOD swaps).
- Round 1 (SHA-256 255272b9...a3386): 0 errors, 1 warning (strain). Independent review returned FAIL with one blocker: `12a_CTR_Crude.raw` had been merged into mouse 12.
- Round 2 (this file): `samples.tsv` row for `12a_CTR_Crude.raw` changed to source `WT_mouse12a_plasma_crude`, biological replicate 14 (was `WT_mouse12_plasma_crude`, 12). Rebuilt with `sdrf-tools build` (23 rows x 35 columns). reconcile: agrees (exit 0). structure OK. check --offline CLEAN. `timeout 900 parse_sdrf validate-sdrf -s PXD000282-plasma.sdrf.tsv -t ms-proteomics -t vertebrates --use_ols_cache_only`: exit 0, 0 errors, same single strain warning.
- Re-review pending; no approve/commit/PR.

## Limitations

- `12a_CTR_Crude.raw` is mouse 12a, coded as its own source (`WT_mouse12a_plasma_crude`, biological replicate 14). The deposit does not say whether 12a is a separate animal from mouse 12 (`12_CTR_Depl.raw`). The RAW header has only the same file name, and Table S1 has one CTR12 column. Treating it as a separate animal is inferred from the Figure 4 legend (WT n = 6). With only 5 WT IDs in the file names (8, 9, 10, 12, 13), 12/12a is the only way to reach six animals. Biological replicate 14 is an arbitrary distinct integer.
- Mouse 7 (Epac1-/-) has only a depleted run, with no `7_KO_Crude.raw` deposited. Supplementary Table S1 has a combined column "KO2and7", so the submitters may have merged mice 2 and 7 in quantification. The SDRF keeps them as separate sources, as the file names do.
- Figure 4 legend: WT n = 6, Epac1-/- n = 7 for plasma. Table S1 has 5 WT columns (CTR8, CTR9, CTR10, CTR12, CTR13) and 6 KO columns (KO1, KO2and7, KO3-KO6). Six WT animals are reached only if CTR12 covers both 12 and 12a; seven KO only if KO2and7 covers two. In the S2 ANOVA sheets, "Mouse1-6: Epac1 KO" and "Mouse7-11: WT" are column positions, not animal IDs.
- `characteristics[sex]` and `characteristics[developmental stage]`: `not available`. Neither sex nor age of the blood-donor mice is stated (the 8-10 weeks in the paper refers only to pregnant mice for embryonic livers).
- `characteristics[disease]` = `normal` for both genotypes. The paper states "Epac1-/- and Epac2-/- mice are healthy and apparently indistinguishable from WT mice under standard housing". The knockout's bleeding phenotype is a measured outcome, not a diagnosis.
- `characteristics[genotype]` is an extra column outside the vertebrates template. Values are free text (`Epac1-/-` as written in the paper; gene Rapgef3).
- Strain: the paper says knockouts were backcrossed to C57BL/6JBomTac for at least ten generations, and WT were littermates or commercial C57BL/6JBomTac (Taconic). Which WT mice were littermates is not stated.
- Reduction/alkylation reagents come from the supplementary "Trypsination of protein samples in solution" protocol. It is not labelled per sample type; it is assigned to plasma because plasma was the in-solution digest (platelets were digested in-gel).
- Fragment tolerance unit: the sources give "0.7" with no unit; Da is inferred, since OMSSA fragment tolerance is in Da and the MS2 was ion-trap.
- The PRIDE-generated mzTab lists `MOD:01090` (iodoacetamide-derivatized N-terminus) and `MOD:01047` (hydroxylated lysine) as variable mods. This is a mass-based conversion artefact (+57.021 / +15.995 Da) and was not used.
- Albumin-depleted samples were acetone precipitated after depletion; no column for this.
