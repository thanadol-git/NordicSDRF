# hanoi-kuala-lumpur-1 — evidence triage (session 2026-11-24)

This session could not reach any EBI host (PRIDE API/FTP, OLS, Europe PMC); the same
morning's GitHub Action reached PRIDE normally, so it was session egress, not an outage.
Evidence below comes from ProteomeCentral (dataset record + full file list) and PMC/NCBI only.
PMC supplementary downloads sit behind a proof-of-work bot check and were not fetched.
**No SDRF has been written yet.** Each Hanoi PXD below is multiplexed or needs a per-sample
supplementary table, so annotating from here would mean guessing the sample map.

| PXD | RAW | What it is | Blocker / what is needed |
|---|---:|---|---|
| PXD020510 | 51 | Human CSF, 45 patients (TBM 20, BM 10, encephalitis 10, non-CNS infection 5) + 6 pools `P01–P06`; label-free, Q Exactive HF; search: Deamidated NQ, Oxidation M variable, 10 ppm / 0.05 Da (CPFP). Paper PMC8128987 (open). Samples from HTD Ho Chi Minh City; lab head at OUCRU Hanoi. | Per-patient diagnosis for `HF0120_MSQ630_LVT_<id>.raw` is not in the article text; it should be in `mmc1.xlsx` (Supplementary Table S3) of PMC8128987. Also check the PRIDE sample protocol for alkylation (PX lists "iodoacetamide derivatized residue"). |
| PXD029710 | 7 | Human serum, nanodiamond + Triton X-114 fractionation at pH 3/7/11 × aqueous (A) / detergent (D) phase, plus `Control Sample.raw` (crude serum); LTQ Orbitrap Elite; MaxQuant `parameters.txt` deposited. Paper J Proteome Res 2022 21:67 (PMID 34928606). | Mods/enzyme/tolerances must come from the deposited MaxQuant `parameters.txt` (PRIDE FTP); serum donor info from the paper Methods (not in PMC). Phase letter (A/D) meaning to be confirmed from paper. |
| PXD035718 | 14 | Human BALF, small-cell lung cancer, 5 patients × tumor-bearing (T) / non-tumor (N) lung, label-free (10 RAW) + TMT fractions F1–F4; Q Exactive. Paper Proteomics Clin Appl 2023 17:e2300011 (not in PMC). | Label-free half is mappable from file names; TMT half needs the channel→sample map (`TMT_txt.rar` on PRIDE, or paper). Enzyme/mods need PRIDE protocol or `Label_free_txt.rar` parameters. |
| PXD047708 | 36 | Human aortic valve interstitial cells (hVIC), pro-calcifying medium ± niclosamide; `HVIC_Global_01–20` + `HVIC_Phospho_01–16`; Orbitrap Eclipse / LTQ Orbitrap Elite. Biochem Pharmacol 2024 230:116614. | Fractionated multiplexed design (global + phospho); channel map and fraction plan need the paper Methods / deposited search files. |
| PXD052208 | 36 | Arabidopsis thaliana leaf protoplasts, single-cell TMTpro (`SingleCellTMTpro_<n>`) vs bulk leaf `ARA_global_F<n>` fractions, ± ABA; Orbitrap Eclipse / Q Exactive. Paper doi:10.1186/s40543-024-00457-x (open access). | Single-cell TMTpro channel layout (carrier/blank/single-cell channels per run) must be read from the paper/supplement before any row is written. |

Kuala Lumpur (25 PXDs, incl. PXD034654 already in BigBio `sandbox/`) not yet triaged.
