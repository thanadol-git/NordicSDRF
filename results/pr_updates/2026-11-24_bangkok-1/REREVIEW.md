# bangkok-1 re-review (2026-11-25), sandbox + blocked PXDs

Validator: `parse_sdrf validate-sdrf --use_ols_cache_only` with `sdrf-pipelines[ontology]` installed (earlier runs this session were structural only).

| PXD | Was | Now | Finding |
|---|---|---|---|
| PXD063183 | sandbox | sandbox, validates | Published: Sci Rep 2025;15:45609, doi:10.1038/s41598-025-29722-8. Trypsin 1:40, TCEP, IAA; paper says HF-X vs PX Q Exactive HF. PR #4321. |
| PXD021066 | sandbox | sandbox, validates | Published: Front Microbiol 2020;11:592153, PMC7835679. In-gel trypsin, LTQ-Orbitrap Velos, SEQUEST/PD 1.2. PR #4322. |
| PXD043954 | blocked | draft annotation | IJMS 2023 PMC10419081: 3 bio x 2 tech = 12 runs; trypsin, QE HF, CAM fixed, Ox M var, 20 ppm / 0.05 Da. 10/11 RAW mapped, `M27_1.raw` excluded. File names from TRIAGE shorthand: verify vs PRIDE. See annotations/PXD043954.report.md. |
| PXD052291 | sandbox | sandbox | Control = normal SHED (DPSC is only the file name). Enzyme in supplementary .docx, not downloadable here. PR #4323. |
| PXD039718 | sandbox | sandbox | Paper uses low-FE/high-FE, never H/L or bird IDs; suffix still ambiguous. PR #4324. |
| PXD016946 | sandbox | sandbox | Still unpublished. PR #4325. |
| PXD037553 | sandbox | sandbox | OA paper, full text unreachable here. PR #4326. |
| PXD012793 | blocked | blocked | Linked paper: Samutrtai P et al., Anal Sci 2020 (paywalled); still raw.zip only, cell line unnamed. |
| PXD073886 | blocked | blocked | Abstract: metacercariae + adult worms vs urine from Ov-infected and CCA patients (Ag-OV / Ag-CCA likely urine groups); "media" and enzyme still unknown. |
| PXD026304 | blocked | blocked | Species: L. orientalis, L. martiniquensis, L. donovani; le1-3 order unknown (full text unreachable). |
| PXD048253 | blocked | blocked | J Mol Biol 2025, PMID 40055058, closed, no preprint. |
| PXD052806 / PXD052809 | blocked | blocked | IJMS 2024 (052809) gives only 1-PHE+TGF vs TGF; L-code key and shared L02 runs need authors. |
| PXD021005, PXD027317, PXD078923 | blocked | blocked | No new public evidence. |
