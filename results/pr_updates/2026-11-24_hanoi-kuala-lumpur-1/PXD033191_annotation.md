## Add SDRF annotation for PXD033191

**Dataset**: [PXD033191](https://www.ebi.ac.uk/pride/archive/projects/PXD033191) — Drosophila melanogaster head + intestine, WT / lgl / lgl + melatonin, 0/6/12/18 h × 3; label-free, Orbitrap Fusion
**Organism**: Drosophila melanogaster
**Templates**: ms-proteomics v1.1.0, invertebrates v1.1.0
**Rows**: 72 | **Columns**: 30
**Factor values**: factor value[genotype], factor value[treatment], factor value[sampling time]
**Scope**: 72 of 72 RAW.

Promotes the sandbox draft (sandbox/PXD033191 PR) to `datasets/`; that sandbox PR can be closed once this is merged.

### Sources
- ProteomeCentral record and full file list
- Deposited MaxQuant `Head_summary.txt` (Trypsin; Carbamidomethyl C fixed; Oxidation M, Acetyl protein N-term variable)
- Wong KC et al. Arch Insect Biochem Physiol 2023 (closed; abstract only)

### Validation
- [x] `parse_sdrf validate-sdrf --use_ols_cache_only` (sdrf-pipelines main): passes, warnings only (free-text `untreated` treatment)
- [x] `.github/scripts/sdrf_review.py`: OK
- [x] Row coordinates unique; no ragged rows
- [ ] Independent adversarial review (not yet done)

### Open points for reviewers
Fly developmental stage / strain background not stated in the deposit (`not available`).

Annotation was agent-assisted (sdrf-skills workflow, NordicSDRF campaign, SEA / Kuala Lumpur–Hanoi batch); file names are taken from the deposited record, not invented.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_0123UuwVXEVXwAGTyNgTiwZe
