# PXD008361-storage

Status: validated annotation; independent review pending.

- Title: Preservation methods and PBS washing affect the AML proteome
- Lab: Frode Selheim (PI) and Elise Aasebø (submitter), PROBE proteomics unit, Department of Biomedicine, University of Bergen, Bergen, Norway.
- Paper: Wangen R, Aasebø E, Trentani A, Døskeland SO, Bruserud Ø, Selheim F, Hernandez-Valladares M. "Preservation Method and Phosphate Buffered Saline Washing Affect the Acute Myeloid Leukemia Proteome." Int J Mol Sci 2018;19(1):296. doi:10.3390/ijms19010296, PMID 29351208, PMC5796241 (open access). I read the full text and the supplementary "Figures and Tables.pdf".
- Existing upstream annotation: none. `bigbio/sdrf-annotated-datasets` returned 404 for both `datasets/PXD008361` and `sandbox/PXD008361`.
- SDRF: `annotations/PXD008361-storage.sdrf.tsv`
- Rows: 24; columns: 38
- SHA-256: `164aa398a15afe45e174ec90823704d13f90c1488fc245a5f836fa979bfc343c`
- Evidence manifest: `annotations/PXD008361-storage.evidence.json`

## Why the deposit is split into two SDRFs

The deposit holds two separate experiments. They differ in instrument, sample type, design and search:

| SDRF | Experiment | Raw files | Instrument | Search archive |
|---|---|---|---|---|
| `PXD008361-storage` (this file) | Preservation method, THP-1 and MOLM-13 cell lines | 24 `RW_*` | Orbitrap Elite (CID, ion-trap MS2) | `MaxQuant-results_StorageConditions.txt.zip` |
| `PXD008361-pbs` | PBS wash of primary AML patient cells | 19 `PBS_*` | Q Exactive HF (HCD, Orbitrap MS2) | `MaxQuant-results_PBS.txt.zip` |

Every one of the 43 deposited raw files appears in exactly one of the two SDRFs.

## Templates

`ms-proteomics` v1.1.0, `human` v1.1.0 and `cell-lines` v1.1.0.

- `ms-proteomics`: label-free DDA LC-MS/MS.
- `human`: both cell lines are human (Cellosaurus OX 9606).
- `cell-lines`: every sample comes from the cultured AML cell lines THP-1 and MOLM-13.
- `dia-acquisition` does not apply. The method is a top-12 data-dependent CID method (`05b_TOP12CID_240K_..._CE35`).
- `oncology-metadata` and `clinical-metadata` were not used. These are cell lines in a technical method study, and there is no clinical data to record.

## Design and file mapping

Each cell line was split into three aliquots, one per preservation method. Each condition was run in triplicate (`-1`, `-2`, `-3`). For each cell line, a QC pool of all its samples was injected three times.

| Source name | Rows | Sample storage (factor) | Files |
|---|---|---|---|
| THP-1 sds 1–3 / MOLM-13 sds 1–3 | 6 | lysed in 4% SDS and stored at -80 °C | `RW_<line>_SDS-<n>.raw` |
| THP-1 dmso 1–3 / MOLM-13 dmso 1–3 | 6 | cryopreserved in medium with 20% FBS and 10% DMSO in liquid nitrogen | `RW_<line>_DMSO-<n>.raw` |
| THP-1 pellet 1–3 / MOLM-13 pellet 1–3 | 6 | dried cell pellet stored in liquid nitrogen | `RW_<line>_PELLET-<n>.raw` |
| THP-1 QC pool / MOLM-13 QC pool | 6 (3 + 3) | pooled | `RW_QC-<line>-1..3.raw` (technical replicates 1–3) |

- **How the mapping was established.** The deposited MaxQuant `summary.txt` assigns each raw file to an experiment with the same name: `THP1_DMSO-1` … `MOLM13_SDS-3`, `QC-THP1-1..3` and `QC-MOLM13-1..3`. The SDS, DMSO and PELLET tokens correspond to the three preservation protocols described in paper section 4.2 and in the PRIDE sample protocol. The QC composition comes from the PRIDE protocol ("a pool containing equal amounts of all the samples … analyzed three times") and from the Figure S2 caption ("QC samples are a pool of the replicates for each of the cell line samples").
- **Factor.** `factor value[sample storage]` mirrors `characteristics[sample storage]`. This is free text: the spec defines the term (PRIDE:0000730), but it is outside the three templates used here. The same column was used for the Bergen fresh-versus-frozen AML dataset `PXD003822-freshfrozen-lf` in this campaign. The cell line is a second, blocking variable and is recorded in `characteristics[cell line]`.
- **Cell-line metadata** comes from live Cellosaurus records:
  - THP-1 (CVCL_0006): male, 1Y, Japanese. Disease is childhood acute monocytic leukemia (NCIt C9163), written as `acute monocytic leukemia` (MONDO:0007896).
  - MOLM-13 (CVCL_2119): male, 20Y, Japanese. Disease is `adult acute monocytic leukemia` (NCIt C8263 → MONDO:0000875).
  - Both lines are derived from peripheral blood, written as `characteristics[sampling site]` = `blood` (UBERON:0000178).
  - The offline helper `sdrf-tools cellline lookup` reported THP-1's disease as "childhood acute megakaryoblastic leukemia". That is wrong; the live Cellosaurus record says acute monocytic leukemia, and that is what was used.
- **Row count.** 24 files × 1 row = 24 rows.

## Technical values

- **Instrument**: `Orbitrap Elite` (MS:1001910). The raw headers of `RW_THP1_SDS-1.raw` and `RW_QC-MOLM13-1.raw` (first 3 MB, HTTP range read) give "Orbitrap Elite MS", tune `Elite_nano`, and acquisition folder `2017-03-30_OrbitrapElite_Freezing-effect`. Paper section 4.4 agrees. PRIDE lists both an LTQ Orbitrap Elite and a Q Exactive for the project; the Q Exactive (HF) belongs to the PBS arm.
- **Acquisition**: DDA (PRIDE:0000627). MS1 is `FTMS + p norm o(300.0-2000.0)`, so `comment[ms1 scan range]` = 300m/z-2000m/z. MS2 is `ITMS + c … Dep Wideband MS/MS`, CID, normalized collision energy 35.0, top 12. This gives:
  - `comment[dissociation method]` = collision-induced dissociation (MS:1000133)
  - `comment[collision energy]` = 35 NCE
  - `comment[ms2 mass analyzer]` = linear ion trap (MS:1000291)
- **Fragment mass tolerance**: 0.6 Da, the MaxQuant `MS/MS tol. (ITMS)` in the deposited `parameters.txt`. MS2 was acquired in the ion trap.
- **Precursor mass tolerance**: omitted. MaxQuant 1.5.5.1 `parameters.txt` does not report it, and no `mqpar.xml` was deposited.
- **Cleavage agent**: Trypsin (MS:1001251). `summary.txt` gives Enzyme = Trypsin, mode Specific, for every raw file. The PRIDE data-processing text and the paper also name trypsin.
- **Modifications**, from the deposited search:
  - Fixed: Carbamidomethyl (C), UNIMOD:4, from `parameters.txt`.
  - Variable: Oxidation (M), UNIMOD:35, and Acetyl (Protein N-term), UNIMOD:1, from `summary.txt`.
  - These match the paper.
- **Label**: label free sample. MaxQuant multiplicity is 1, and both PRIDE and the paper describe LFQ.

## Validation

All commands were run from the sdrf-skills checkout, one at a time.

- `timeout 900 .venv/bin/parse_sdrf validate-sdrf -s /home/thanadol/Documents/GitHub/NordicSDRF/annotations/PXD008361-storage.sdrf.tsv -t ms-proteomics -t human -t cell-lines --use_ols_cache_only`
  - Result: "Everything seems to be fine. Well done." There were 0 errors and 0 warnings on the first validation of the final file. Peak RSS was about 1.9 GB.
- `.venv/bin/python -m tools structure <sdrf>`: Structure OK.
- `.venv/bin/python -m tools check <sdrf>`: CLEAN. 14 of 14 terms were verified, with no UNIMOD swaps and no label mismatches.
- `.venv/bin/python -m tools reconcile <sdrf> --record scratchpad/PXD008361/pride.json --accession PXD008361`. The first run flagged `run_names_name_a_cell_line` because `organism part` was set to `blood`. I moved `blood` to `characteristics[sampling site]`, set `organism part` to `not applicable`, and rebuilt. The final run reports three findings, all reviewed and kept:
  - BLOCKER `disease_on_control_runs`. This is a false positive: the `DMSO` token in `RW_*_DMSO-*` names a preservation method, not a vehicle control. Every sample is an AML cell line, so the disease holds on every row.
  - BLOCKER `cleavage_agent_unsupported`. Trypsin is stated in the deposited `summary.txt` and in the PRIDE data-processing text ("Trypsin was set as protease"), so the value was kept.
  - MAJOR `instrument_contradicted`. The protocol's mention of "Q Exactive HF" refers to the PBS arm. The raw headers of this arm say Orbitrap Elite.

## Limitations

- **Biological replicates (inferred).** The triplicates `-1/-2/-3` are encoded as `characteristics[biological replicate]` 1–3. The paper calls them "triplicates of each preservation method" and uses paired t-tests. Whether they are independent cultures or repeated splits of one culture is not stated.
- **QC pools.** Each QC pool is encoded as one pooled source per cell line with technical replicates 1–3. Its `biological replicate` and `sample storage` are both `pooled`. Whether the three QC injections came from one mix or from three separate mixes is not stated.
- **`organism part`** is `not applicable` because the material is cultured cell lines. The anatomical origin (peripheral blood) is recorded in `sampling site`, from Cellosaurus.
- **Age, sex and ancestry** describe the cell-line donors and come from Cellosaurus, not from the paper.
- **Culture medium.** The paper describes an in-house RPMI-based medium with adjusted metabolites, and no single NCIT medium term fits it. Passage number, authentication and biorepository are also not stated. These columns are omitted.
- **Storage temperature.** Only the SDS lysate's -80 °C is stated. The liquid-nitrogen temperature is not given numerically, so `characteristics[sample storage temperature]` is omitted and the conditions are written in `sample storage` text.
- **Reagents.** Reduction and alkylation reagents for FASP are not named, so those columns are omitted. Carbamidomethyl is still searched as fixed.
- **Precursor mass tolerance** is not available, because MaxQuant 1.5 `parameters.txt` does not report it.
- **Instrument settings** were read from 2 of the 24 raw headers. The other files are assumed to be identical: they share the acquisition folder, the MaxQuant search and the ITMS tolerance.
- **Custom column.** `characteristics[sample storage]` / `factor value[sample storage]` is free text outside the declared templates. The validator accepted it without warnings.
