# PXD000746-itraq

Status: validated annotation; independent review pending.

PRIDE title: "Proteomics of Fuchs Endothelial Corneal Dystrophy support that the extracellular matrix of Descemet's membrane is Disordered". Department of Molecular Biology and Genetics, Aarhus University, Aarhus, Denmark (lab PI Jan J. Enghild; submitter Ebbe T. Poulsen). Paper: Poulsen ET et al., J Proteome Res 2014, PMID 24846694, DOI 10.1021/pr500252r, PMC4227554.

- SDRF: `annotations/PXD000746-itraq.sdrf.tsv`, 600 rows × 34 columns (40 source-channel-replicate rows × 15 SCX fractions)
- SHA-256: `35a32a32d7996fc7f32ecf280bf7c2c8f0b8e8522b9216e0733afa758f78aef9`
- Companion SDRF (XIC label-free arm): `annotations/PXD000746-xic.sdrf.tsv`
- Evidence manifest: `annotations/PXD000746-itraq.evidence.json`; working files in `sdrf-skills/scratchpad/PXD000746/`

## Templates
`ms-proteomics` v1.1.0 + `human` v1.1.0 (DDA, TripleTOF 5600, iTRAQ 4plex, SCX fractionation).

## Channel map (stated, from paper Figure 1)
Five 4plex sets, SCX1–SCX5; 114 = pooled reference "Mix" in every set (5 µg of every patient and control):

| set | 114 | 115 | 116 | 117 |
|---|---|---|---|---|
| SCX1 | Mix | P1 | P2 | C1 |
| SCX2 | Mix | P3 | P4 | C2 |
| SCX3 | Mix | P5 | P6 | C3 |
| SCX4 | Mix | P7 | P8 | C4 |
| SCX5 | Mix | P9 | P10 | Mix |

P = late-onset FECD patient (P1–P5 female, P6–P10 male), C = secondary bullous keratopathy control (all female). The figure is an image in the paper (`pr-2014-00252r_0001.jpg`, from Europe PMC supplementaryFiles of PMC4227554, verified to be this paper). In SCX5, channel 117 carries a second Mix (as drawn). The two Mix channels in SCX5 are separate sources (`Mix_SCX5_114`, `Mix_SCX5_117`).

## File mapping
- Each SCX set was fractionated into 15 fractions; fraction n of set k is `…SCX<k>-<n>.wiff`. All 150 `2013-*` .wiff files are used (10 groups × 15 fractions: 5 sets × 2 series).
- "Two iTRAQ experiments were performed on each 4plex set either with iTRAQ collision energy adjustment enabled or disabled." Series A = files named `…-ETP-FuchsiTRAQ-SCX<k>-<n>` (March 12–17), series B = `…-ETP-Fuchs-iTRAQmethod-SCX<k>-<n>` (March 17–April 4). They are written as `comment[technical replicate]` 1 and 2. **Which series is CE-adjusted is not stated**, so the replicate numbering is arbitrary and no collision energy column is written. `2013-03-17-ETP-FuchsiTRAQ-SCX5-12.wiff` (dated March 17, named FuchsiTRAQ) is series A fraction 12 of SCX5 (the series A SCX5 run is missing fraction 12 otherwise).
- 600 rows = 40 (source × channel × series) × 15 fractions.

## Technical values
- TripleTOF 5600 (MS:1000932), paper + PRIDE; .wiff headers not read. DDA, 50 MS/MS per cycle for iTRAQ. Fractionation: SCX (PRIDE:0000561).
- Mascot 2.3.02 (PRIDE data processing protocol): Carbamidomethyl (C) fixed, proline hydroxylation variable (Oxidation UNIMOD:35 on P), methionine-containing peptides discarded (so no Met oxidation), 10 ppm / 0.2 Da, "iTRAQ 4plex protocol selected as quantitation method". iTRAQ4plex (UNIMOD:214) on K and peptide N-term as Fixed is **inferred** from that Mascot quantitation protocol; no search parameter file is deposited.
- CID from instrument type (see XIC report). Trypsin; samples also CNBr-cleaved before digestion (single-valued column).

## Validation
- `sdrf-tools build -t ms-proteomics -t human`: 600 rows × 34 columns.
- `parse_sdrf validate-sdrf … --use_ols_cache_only`: 0 errors. `check --offline`: CLEAN. `structure`: OK. `reconcile`: every value agrees with the record.
- First validation failed: `characteristics[age] = pooled` is rejected by the validator pattern although TERMS.tsv lists pooled; the Mix rows use `not available`. One fix round.

## Limitations
- Age `not available` (only group averages published). Mix rows: sex `not applicable`, disease `not applicable`, `pooled sample = pooled`, biological replicate `pooled`.
- Individuals P1–P10 / C1–C4 are assumed identical to those in the XIC arm (Figure 1 shows one set of 14 samples feeding both arms).
- Controls are bullous keratopathy tissue, not healthy.
