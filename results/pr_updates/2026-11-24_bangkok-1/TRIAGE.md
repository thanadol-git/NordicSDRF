# bangkok-1 triage (20 Bangkok PXDs with fewest RAW files)

Sources: ProteomeCentral PROXI/XML records (PRIDE API and FTP unreachable from this session) and open papers read in the browser.

| # | PXD | RAW | Status |
|---|---|---|---|
| 1 | PXD021005 | 1 | blocked: only RAW is one BAF FILES.zip bundle; per-run names inside archive |
| 2 | PXD012793 | 1 | blocked: only RAW is raw.zip (Waters bundle); cell line unnamed; publication pending |
| 3 | PXD052291 | 4 | sandbox: 4/4 mapped; enzyme in supplement only; instrument PX/paper conflict |
| 4 | PXD062669 | 4 | annotated: 4/4; Sci Rep 2025 methods; review pending |
| 5 | PXD027317 | 6 | blocked: QE_0817_* names carry no FE group; key only in txt.zip / authors |
| 6 | PXD039718 | 6 | sandbox: 6/6 mapped; H/L suffix ambiguous (FE vs FCR) |
| 7 | PXD063183 | 6 | sandbox: 6/6 mapped; enzyme unstated (publication pending) |
| 8 | PXD064135 | 6 | annotated: 6/6; IJMS 2026 methods (QE Plus per paper); review pending |
| 9 | PXD017234 | 6 | annotated: 6/6 (.d.zip); Pharmaceuticals 2022 methods; review pending |
| 10 | PXD078923 | 7 | blocked: only mzXML deposited (no Agilent .d) |
| 11 | PXD016946 | 8 | sandbox: 8/8 mapped; enzyme unstated; two instruments listed |
| 12 | PXD048253 | 8 | blocked: FX1-8 strain/fraction key unknown; paper closed |
| 13 | PXD021066 | 8 | sandbox: 8/8 mapped; enzyme unstated (publication pending) |
| 14 | PXD052806 | 9 | blocked: L01/L02/L04 group codes not explained; paper has 2 groups |
| 15 | PXD052809 | 9 | blocked: L01/L02/L03 group codes not explained; L02 names repeat PXD052806 |
| 16 | PXD057572 | 9 | annotated: 9/9; Sci Rep 2025 methods; review pending |
| 17 | PXD037553 | 9 | sandbox: 9/9 mapped; enzyme unread (paper behind captcha) |
| 18 | PXD043954 | 11 | blocked: irregular M27 run set (M27_1.raw extra, two missing); paper not read |
| 19 | PXD026304 | 12 | blocked: le1/le2/le3 species key in paper (not read) |
| 20 | PXD073886 | 12 | blocked: Ag-OV / Ag-CCA meaning and enzyme only in metadata.csv (download-only) |

## Evidence notes

- PXD021005: rice flag leaf cytokinin x drought (Plants 2020 9(9), PMID 32867335). Only RAW = "BAF FILES.zip" (Bruker BAF bundle); also YEP zip, Pride_Leaf.zip. Instrument PX "ultraflex" (MALDI) but title says LC-MSMS. BLOCKED: per-run names inside archive.
- PXD012793: AgNP vs AgNO3 vs control, human carcinoma cell line, 48 h LC10; Synapt MS; publication pending. Only RAW = raw.zip (Waters .raw folders bundled); mgf x2 + mzid. BLOCKED: per-run names inside raw.zip; cell line unnamed in PX.
- PXD052291: SHED exosomes, apoptosis-induced (serum starvation 3 wk) vs normal; Sci Rep 2024 14:27921 (OA, read). RAW (4): Human-Apop-EX-LC-MS1.raw.raw, Human-Apop-Ex-LC-MS2.raw.raw, Human-Apop-Ex-LC-MS3.raw.raw, Human-DPSC-Ex-LC-MS.raw.raw (+2 xlsx results). Paper: "Orbitrap HF" + EASY-nLC1000, DDA top15, HCD NCE 28, MS1 375-1300 R120k, MS2 R15k; 2 ug exosomal protein. PX instrument: LTQ Orbitrap Elite (conflict w/ paper). Enzyme/mods only in Supplementary file (not read). "DPSC" in file name vs SHED in paper (normal exos). Mahidol Faculty of Science (Roytrakul-style lab?). -> SANDBOX candidate: enzyme unknown + instrument conflict; mapping clear (Apop x3, normal x1).
- PXD062669: C2C12 mouse myoblasts, Vdr siRNA vs negative-control siRNA (TGF-b1 context in paper; proteomics = Vdr KD vs control), RAW: Control_siRNA_1/2.raw, Vdr_siRNA_1/2.raw (+mzTab, fasta). Sci Rep 2025 15:41599 (OA, read): acetone precip, RapiGest, TCEP, IAA, Trypsin/Lys-C mix (Promega V5073) 37C o/n, 1.5 ug, Q Exactive HF + UltiMate 3000 RSLCnano, Proteome Discoverer, Mus musculus db. -> ANNOTATE.
- PXD027317: Korat (slow-growing) chicken duodenum, male, 10 wk, high-FE x3 vs low-FE x3; Poult Sci 2022 101:101824 (PMID 35395531). Q Exactive. RAW: QE_0817_18870/18872/18874/18877/18879/18881.raw (no group in names). MaxQuant txt.zip deposited (summary.txt inside zip would give experiment names). BLOCKED: run->FE group key only in txt.zip / authors.
- PXD039718: Korat chicken thigh muscle, 10 wk, high-FCR x3 vs low-FCR x3; Poult Sci 2023 102:102741 (PMID 37186966). Q Exactive HF. RAW: QE_0817_21929_TH76H, 21854_TH2L, 21880_TH75H, 21856_TH28L, 21862_TH13L, 21926_TH73H (H/L suffix = group, but H/L could be FE or FCR -> must confirm in paper). txt.zip (MaxQuant).
  PXD039718 paper (PMC10192536, read): 75 male Korat chickens, 10 wk; 3 highest FCR10 (3.33-3.36) = "low-FE", 3 lowest FCR10 (1.83-1.99) = "high-FE". Thigh muscle, freeze-dried; 8 M urea/AMBIC, DTT 5 mM, IAA 15 mM, trypsin 37C 24h; Q Exactive (paper) vs Q Exactive HF (PX), DDA HCD, 80-min gradient, Helsinki core. MaxQuant 1.6.5.0: trypsin 2 missed, Carbamidomethyl fixed, Ox M + Acetyl prot N-term var, 20/6 ppm, MS/MS 20 ppm. File suffix H/L ambiguous (high FE or high FCR?) -> SANDBOX.
- PXD063183: LX-2 + TGF-b1 10 ng/mL +/- 7-octenoic acid; RAW TGF_01..03, 7-OCT_01..03; Q Exactive HF; publication pending. Enzyme not stated -> SANDBOX (same lab as 052806 uses trypsin+TCEP/IAA, PD 2.4 — do not transfer).
- PXD052806: LX-2 TGF-b1 +/- beta-citronellol; Biomolecules 2024 14:800 (read): acetone, RapiGest, TCEP 1 mM, IAA 5 mM, trypsin 1:40 37C 6h; "HF-X" + EASY-nLC1000 (PX: Q Exactive HF), DDA top15 HCD 29, PD 2.4. RAW L01_01-03, L02_01-03, L04_01-03 = 3 groups but paper describes only TGF vs b-CIT+TGF; L-code->group unknown -> BLOCKED (needs authors / xlsx).
- PXD052809: LX-2 TGF-b1 +/- 1-phenyl-2-pentanol; IJMS 2024 25:8995. RAW L01_04-06, L02_01-03, L03_01-03 (L02 files share names with PXD052806 -> shared group across deposits?). Same L-code->group gap -> BLOCKED. Note: L02_01-03 appear in both 052806 and 052809 (same runs reused?) — flag for authors.
- PXD064135: RAW 264.7, miR-146a mimic vs negative control mimic (40 nM, RNAiMAX 24h) then LPS 100 ng/mL 24h; IJMS 2026 27:6514 (read). 8 M urea/Tris, EasyPep Mini kit (Thermo A40006; Trypsin/Lys-C mix, red/alk in kit), EASY-nLC1000 + Q Exactive Plus (paper) vs PX Q Exactive HF; MSFragger 2.2/FragPipe 12.1, 10 ppm; Carbamidomethyl fixed, Ox M + Acetyl prot N-term var. Paper says 5 bio reps/group; 3+3 RAW deposited (mimicNC_1-3, MiR146a_1-3). -> ANNOTATE (QE Plus per paper; enzyme from kit -> Trypsin + Lys-C).
- PXD017234: B16-F10 mouse melanoma, control vs Lingzhi octapeptide PVRSSNCA 50 ug/mL 48h; Pharmaceuticals 2022 15:684 (read). RAW (Bruker .d zipped, 1 run each): lysate_control_BE3_01_25860/25862/25864.d.zip, lysate_treatment_BE4_01_25866/25868/25870.d.zip. HEPES/Triton/DTT lysis, acetone, RapiGest, DTT 5 mM 72C, IAA 20 mM, trypsin 37C 3h; impact II + UltiMate 3000; Mascot: trypsin 3 missed, 1.0 Da / 0.5 Da, CAM fixed, Ox M + Acetyl prot N-term var. -> ANNOTATE.
- PXD078923: L. johnsonii KD1 cell-free supernatant; 6545XT Q-TOF; pub pending. Only mzXML (PKD1-3, PMRS1-3, Blank01) deposited, no Agilent .d -> BLOCKED (vendor-RAW rule); also MRS medium control (PMRS) + blank.
- PXD048253: P. aeruginosa PA14 WT vs trmA mutant; J Mol Biol 2025 437:169020 (Elsevier, closed). Q Exactive. RAW FX1..FX8 + one PD msf "1261_JC_Fractions_2" -> FX = fractions? strain/fraction key unknown -> BLOCKED.
- PXD021066: P. aeruginosa PAO1 envelope proteins, pMfs1 / pMfs2 overexpression vs empty vector p; pub pending. LTQ Orbitrap Velos. RAW (8): PAO1_pMfs1_Rep1-3, PAO1_pMfs2_Rep1-3, PAO1_p_Rep1-2 (p_Rep3 has msf only, no raw). Enzyme unstated -> SANDBOX (all 8 mapped).
- PXD057572: differentiated SH-SY5Y, DMSO control vs ECa 233 vs MDS+ASS mixture; Sci Rep 2025 15:29348 (read). RAW Control_N1-3, EC2_N1-3, MDS_ASS_N1-3 (paper: 3 bio x 3 tech, only 9 RAW deposited -> 1 per bio rep). EasyPep Mini kit (trypsin/Lys-C mix 37C 3h; kit red/alk reagents unnamed), RSLCnano + Orbitrap Exploris 480. Search mods not read -> check validator.
- PXD037553: HepG2, control vs caffeine 100 uM vs trigonelline 100 uM, 24 h; Biomed Pharmacother 2023 158:114124 (ScienceDirect captcha, not in PMC -> not read). LTQ Orbitrap XL. RAW Control_1_1-3, CAF_1_1, CAF_1-2, CAF_1-3, TRI_1_1-3. MaxQuant txt (proteinGroups/peptides/msms) + combined.zip deposited (parameters not read). Enzyme unread -> SANDBOX.
- PXD043954: Brevibacillus sp. SPR20 WT vs ARTP mutant M27; IJMS 2023 24:12016 (not read). QE HF. RAW (11): WT1_01/02, WT2_01/02, WT3_01/02, M27_1, M27_1_01/02, M27_2_02, M27_3_01 -> irregular M27 set (M27_1 extra, M27_2_01 & M27_3_02 missing). Enzyme unread -> SANDBOX/partial (needs authors for M27_1.raw).
- PXD026304: Leishmania species-specific proteomics; ACS Omega 2022 7:12580 (not read). QE HF. RAW le1_01-04, le2_01/03/04/05, le3_01-04 (le1/2/3 = species/isolates? which ones unknown; le2_02 missing). BLOCKED: le-code -> species key in paper.
- PXD073886: O. viverrini (Khon Kaen, listed under Thailand manifest) — media / adult worm / "Ag-OV" / "Ag-CCA" x3 each, Bruker compact (.d.zip, 12 runs); pub pending. Sample meaning of Ag-OV / Ag-CCA (urine of Ov-infected / CCA patients? antigen pull-down?) and enzyme only in metadata.csv (download-only) -> BLOCKED.

