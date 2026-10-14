# PXD007894-serum

Status: validated local annotation; independent review pending. PR not created.

- SDRF: `annotations/PXD007894-serum.sdrf.tsv`
- Rows: 33; columns: 39
- SHA-256: `0b9734ffadc64d228cf66a3bee79ab185d426746cb117a3c8c6602323bfad635`
- Evidence manifest: `annotations/PXD007894-serum.evidence.json`

## Validation

- parse_sdrf ms-proteomics + human: see build log (clean)
- tools structure: OK

## Limitations

- The full text of the associated paper (PMID 30112540, Analyst 2018) is not open access and was not read; no claim cites it. Sample information comes from the PRIDE record, file names, Mascot .dat headers and RAW headers only.
- The deposit was split into two SDRFs because the deposited Mascot searches differ: -peptides (75 files, no fixed/oxidation mods, fragment tolerance 0.02 Da) and -serum (33 files, Carbamidomethyl fixed, Oxidation variable, fragment tolerance 0.05 Da). The grouping follows the .dat headers, not a paper description.
- comment[label] is the generic 'Dimethyl Labeling' (PRIDE:0000513) with one row per RAW file: which light/medium/heavy channels are present in each run is not recorded in a deposited mapping and was not inferred. tools check flags this as a wrong-ontology term only because the checker expects MS; the template column is PRIDE-backed.
- S1-S3 / R1-R3 suffixes are treated as technical (analytical) replicate injections of one source with biological replicate 1; this follows the PRIDE abstract statement of three analytical replicates but not a deposited mapping.
- Age, sex, ancestry, individual and disease are not available (commercial/pooled serum origin is not described). PRIDE lists organism part 'Blood cell' in addition to serum; no run could be linked to it.
- Instrument Q Exactive (MS:1001911) confirmed from RAW headers (Method of Q Exactive) and the protocol.
- Only dimethyl labeling modifications Dimethyl (light, UNIMOD:36, +28.0313), Dimethyl:2H(4) (medium, UNIMOD:199, +32.0564) and Dimethyl:2H(4)13C(2) (heavy, UNIMOD:510, +36.0757) were matched by exact delta mass in the Mascot .dat headers; all as K and any N-term variable.
- TTT_180522_M_* runs were split into PXD007894-ttt.sdrf.tsv after review.
