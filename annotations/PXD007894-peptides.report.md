# PXD007894-peptides

Status: validated local annotation; independent review pending. PR not created.

- Absolute quantitation of proteins by two-point quantitation using dimethylated proteotypic peptides
- SDRF: `annotations/PXD007894-peptides.sdrf.tsv`
- Rows: 75; columns: 37
- SHA-256: `8f0d46cff6417f22405c6c001116a48a421e6a77dadc3d1f8c29d4fae6cb2640`
- Evidence manifest: `annotations/PXD007894-peptides.evidence.json`
- Scope: 75 RAW files, synthetic peptide dilution series (file names NNNamol/fmol/pmolS1-3). Inferred as peptide-only (no serum) from file names and the abstract; organism Homo sapiens refers to the peptide sequences. Cleavage not applicable (no digestion step for synthetic peptides described for these runs).

## Validation

- parse_sdrf validate-sdrf (ms-proteomics + human, --use_ols_cache_only): Everything seems to be fine.
- tools structure: OK.
- tools check: 12 terms verified, 0 hallucinated, 1 wrong-ontology flag (PRIDE label, explained in limitations).
- RAW coverage: 75 of 75 files in this SDRF; with PXD007894-serum all 126 deposited RAW files exactly once.

## Limitations

- The full text of the associated paper (PMID 30112540, Analyst 2018) is not open access and was not read; no claim cites it. Sample information comes from the PRIDE record, file names, Mascot .dat headers and RAW headers only.
- The deposit was split into two SDRFs because the deposited Mascot searches differ: -peptides (75 files, no fixed/oxidation mods, fragment tolerance 0.02 Da) and -serum (51 files, Carbamidomethyl fixed, Oxidation variable, fragment tolerance 0.05 Da). The grouping follows the .dat headers, not a paper description.
- comment[label] is the generic 'Dimethyl Labeling' (PRIDE:0000513) with one row per RAW file: which light/medium/heavy channels are present in each run is not recorded in a deposited mapping and was not inferred. tools check flags this as a wrong-ontology term only because the checker expects MS; the template column is PRIDE-backed.
- Meaning of file-name tokens (amount such as 100amol, S1-S3, Serum-0.5/1/2, 10fmol-100fmol, R1-R3, TTT_180522_M_01..10) is not documented in the deposit; they are kept verbatim in source names. No factor value columns were added because the quantity, what it refers to (light, heavy or both) and units for serum volume are undecoded.
- S1-S3 / R1-R3 suffixes are treated as technical (analytical) replicate injections of one source with biological replicate 1; this follows the PRIDE abstract statement of three analytical replicates but not a deposited mapping.
- Acquisition method is PRM for all files because every RAW instrument method name contains PRM (e.g. TTT-HCD-60min-PRM-Dimethylation-Simplex.meth; TTT_180522_M files use __60min_Top10_15s-Dimeth-PRM.meth, a Top10 plus PRM method). HCD with NCE 28 is stated in the PRIDE protocol. A separate DDA acquisition is also described in the protocol and may apply to some runs; it cannot be assigned to files.
- Age, sex, ancestry, individual and disease are not available (commercial/pooled serum origin is not described). PRIDE lists organism part 'Blood cell' in addition to serum; no run could be linked to it.
- Instrument Q Exactive (MS:1001911) confirmed from RAW headers (Method of Q Exactive) and the protocol.
- Only dimethyl labeling modifications Dimethyl (light, UNIMOD:36, +28.0313), Dimethyl:2H(4) (medium, UNIMOD:199, +32.0564) and Dimethyl:2H(4)13C(2) (heavy, UNIMOD:510, +36.0757) were matched by exact delta mass in the Mascot .dat headers; all as K and any N-term variable.
