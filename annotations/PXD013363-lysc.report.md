# PXD013363-lysc

Status: validated annotation; independent review pending.

PRIDE title: "Quantitative proteomic analysis of SUMOylation in renal cortical collecting duct cells after aldosterone stimulation". InterPrET Center, Department of Biomedicine, Aarhus University, Aarhus, Denmark (lab PI Robert A. Fenton). Paper: Wu Q, Aroankins TS, Cheng L, Fenton RA, J Proteome Res 2019, PMID 31502464, DOI 10.1021/acs.jproteome.9b00306 (closed access; Methods not read, annotation rests on the PRIDE protocols and the deposited Readme).

- SDRF: `annotations/PXD013363-lysc.sdrf.tsv`, 288 rows × 40 columns
- SHA-256: `690b64864441dc43a8957d9d299ee5e918c58d5a0274a3af61daf07f6424019f`
- Companion SDRF (Lys-C + Glu-C digest arm): `annotations/PXD013363-lysc-gluc.sdrf.tsv`
- Evidence manifest: `annotations/PXD013363-lysc.evidence.json`; working files in `sdrf-skills/scratchpad/PXD013363/`

## Templates
`ms-proteomics` v1.1.0 + `vertebrates` v1.1.0 (Mus musculus) + `cell-lines` v1.1.0 (mpkCCD). No `clinical-metadata`/`oncology-metadata` (no donors).

## Why two SDRFs
The deposit has two digestion arms that PRIDE says were searched in two parallel Proteome Discoverer nodes: Lys-C only (this file: KGG pull-down + 8 high-pH-style flow-through fractions) and Lys-C followed by Glu-C (companion file: KGG pull-down and flow-through, unfractionated).

## Design and file mapping (stated)
The deposit contains `Readme.docx` mapping every RAW file to SUMO isoform (SUMO1/SUMO2), biological replicate (A-D = 1-4), fraction (1-8 or N/A), sample type (flow-through or KGG pull-down) and enzyme. All 176 RAW files are covered and used here (144) or in the companion (32).
- Cells: mpkCCD expressing His-tagged SUMO1 or SUMO2 (T95K-style mutant); four biological replicates each (four passages).
- SILAC: per PRIDE protocol, aldosterone-treated cells were light and SILAC-heavy cells were the vehicle controls ("mpkCCD cells were treated with aldosterone while SILAC heavy labeled mpkCCD cells were used as vehicles"), equal protein pooled. Each RAW file therefore yields two rows: `SILAC light` = aldosterone source, `SILAC heavy` = vehicle source (`SUMO<n>_rep<r>_<treatment>_<KGG|FT>`). The same assignment holds for all four replicates per the text (no swap stated).
- Every RAW name exists twice (plain and `_<yymmddhhmmss>` suffix) with identical Readme annotation and different sizes: written as `technical replicate` 1 (plain) and 2 (timestamped). Whether these are repeat injections is inferred.
- Fractions 1-8 of the flow-through come from the Readme ("Fraction" column). KGG pull-downs are one file each (fraction 1).
- Factor: `factor value[treatment]` (aldosterone vs vehicle).

## Technical values
Q Exactive (PRIDE record); DDA. Lys-C. PRIDE data-processing protocol: fixed Carbamidomethyl C; variable Acetyl (protein N-term), Oxidation M, Phospho STY, GG on K and heavy GG on K (UNIMOD:799 Label:13C(6)+GG). No search parameter file deposited (`.pdResult` only, 3-5 GB each, not opened).

## Validation
- `sdrf-tools build -t ms-proteomics -t vertebrates -t cell-lines`: 288 rows × 40 columns.
- `parse_sdrf validate-sdrf … --use_ols_cache_only`: 0 errors; 3 warnings (`vehicle` not in NCIT/EFO; the diGly enrichment label not in PRIDE/EFO; `mpkCCD` not in CLO/BTO/EFO; Cellosaurus accession CVCL_R771 given).
- `check --offline`: CLEAN. `structure`: OK.
- `reconcile`: 1 MAJOR, `cleavage_agent_incomplete`: the record names Lys-C and Glu-C; expected for this arm, which is the Lys-C-only digest (the Glu-C arm is in the companion file).

## Limitations
- Tolerances, dissociation method and the fractionation method for the flow-through fractions are `not available` (not in the PRIDE text; paper not accessible). Q Exactive would imply HCD but it is not stated.
- Aldosterone dose/duration, passage and clone are not in the accessible text, so `sampling time` and passage are omitted; cell line is the generic Cellosaurus entry mpkCCD (CVCL_R771), not a specific clone.
- The His-SUMO1/SUMO2 expression is encoded only in the source name; no licensed column carries a genetic modification.
- The KGG pull-down was also His-tag purified; the flow-through rows are the KGG flow-through, so `enrichment process` is `not applicable` for them.
- Disease `not applicable` (cell line). Sex, strain not stated.
