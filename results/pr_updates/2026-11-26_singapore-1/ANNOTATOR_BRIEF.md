# singapore-1 annotator brief (one PXD per agent)

You annotate ONE Singapore PRIDE dataset with an SDRF for the NordicSDRF campaign.

## Read first
- `/home/claude/thanadol-git/sdrf-skills/annotations/ANNOTATOR_BRIEF.md` (hard rules and traps; its paths to
  `/home/sachsenb/...` and conda do not apply here).
- `/home/claude/thanadol-git/sdrf-skills/skills/sdrf-annotate/SKILL.md` (workflow).
- Spec: `/home/claude/thanadol-git/sdrf-skills/spec/sdrf-proteomics/TERMS.tsv` and
  `/home/claude/thanadol-git/sdrf-skills/spec/sdrf-proteomics/sdrf-templates/` (resolve templates with
  `spec/scripts/resolve_templates.py` if useful).
- Examples of finished work in this campaign: `/home/claude/nordicsdrf/annotations/PXD046383.sdrf.tsv`
  (+ `.report.md`), `PXD034530.*`, `PXD022257.BLOCKED.md`.

## Network (important)
- The shell has NO internet (proxy 403). Do not try curl/pip for data.
- File lists and PX metadata: the cloud browser (`mcp__remote-browser__browser_navigate`) on
  `https://proteomecentral.proteomexchange.org/api/proxi/v0.1/datasets/<PXD>?resultType=full`.
  PRIDE's own API (`www.ebi.ac.uk/pride/ws/archive/v3/...`) was down today; try it once, don't rely on it.
- The cloud browser is SHARED by up to 5 agents. Use the page content returned by the navigate call itself
  (or a snapshot taken immediately after), and ALWAYS check that the returned Page URL and JSON contain
  YOUR accession before using it. If it shows another PXD, navigate again. Long pages: use
  `browser_snapshot` with `offset` to read on, re-checking the Page URL each time.
- Papers, Europe PMC, PMC, OLS (`https://www.ebi.ac.uk/ols4/api/search?q=...&ontology=...`): WebFetch
  first (ask it to return text verbatim), cloud browser if WebFetch fails.
- Save every fetched payload you rely on as a file under your private scratch dir
  `/home/claude/singapore1/scratch/<PXD>/` (write the exact file names list there too). Never read another
  PXD's scratch dir.

## Deliverables (only these files; touch nothing else, no git commands)
In `/home/claude/nordicsdrf/annotations/`:
1. If annotatable: `<PXD>.sdrf.tsv` (one row per raw data file × label channel; every deposited raw run
   that has a sample) and `<PXD>.report.md` (format like PXD046383.report.md: Study, Scope/evidence/decisions
   incl. deposited-vs-annotated reconciliation, values left not available/not applicable and why,
   stated vs INFERRED, conflicts; end with a "Review status" section saying "pending").
2. If not annotatable: `<PXD>.BLOCKED.md` in the PXD022257.BLOCKED.md style (why, evidence checked,
   what would unblock). Do NOT edit the shared `annotations/BLOCKED.md`.

Precedence: raw-file headers / deposited search outputs > paper Methods > PX record fields. Never fabricate
file names, sample mappings or ontology accessions; verify every accession (OLS/UNIMOD/Cellosaurus/NCBITaxon)
live. `comment[sdrf annotation tool]` = `manual curation` is acceptable as in prior files, or follow the skill.

## Status classes (pick exactly one)
- `annotated`: every run mapped from STATED evidence; validates.
- `sandbox`: SDRF written and validates, but something material is INFERRED or unresolved (e.g. group
  codes inferred, enzyme unstated, instrument conflict). Explain the open point in the report.
- `blocked`: no defensible SDRF (e.g. channel map absent, no raw files, run→sample key unknown).
- `duplicate`: byte-identical data in another PXD (write a BLOCKED.md saying so).

## Validate
```
parse_sdrf validate-sdrf --sdrf_file /home/claude/nordicsdrf/annotations/<PXD>.sdrf.tsv --use_ols_cache_only
```
(add `--template <name>` for each declared template). Fix every ERROR. Factor value columns go last.

## Final reply (exactly this, nothing else)
Line 1: `<PXD>\t<status>\t<short note, <=110 chars, same style as results/queue/2026-11-25_bangkok-3.txt>`
Line 2: rows × cols, templates, validation result.
Line 3-6: the judgement calls a reviewer should attack hardest, and the paper/DOI/PMCID used.

## Lessons from bangkok-3 (apply them)
- The BigBio CI gate validates EVERY declared template against the WHOLE file
  (`python3 /home/claude/sdrf-annotated-datasets/.github/scripts/sdrf_review.py <file>` must print [OK]).
  Never declare a template on only some rows; split into several `<PXD>-<part>.sdrf.tsv` files instead.
- (source name, biological replicate, technical replicate, fraction) must be unique within a file
  (e.g. DDA + SWATH runs of one sample: technical replicate 1/2, or separate files).
- Primary cells cannot share a file that declares cell-lines (it forbids reserved words in cell line).
- A label/channel→condition map that is only guessed means BLOCKED or clearly flagged sandbox, never annotated.
- Verify the PX record's linked paper actually cites the PXD (two bangkok-3 records linked the wrong paper).
- Our cached raw counts were wrong 3 times: always re-derive the file list yourself.
- `annotated` requires every run mapped from STATED evidence; otherwise `sandbox`.

## Update (2026-11-26 13:10): PRIDE FTP is readable in the cloud browser
`https://ftp.pride.ebi.ac.uk/pride/data/archive/<YYYY>/<MM>/<PXD>/` opens in the cloud browser (WebFetch is blocked
by robots, the shell has no network). Use it for the directory listing, small text files (sample metadata,
README, checksum.txt, *_Proteins.txt / summary.txt headers). Do not open multi-GB binaries. Deposited
sample-metadata files can hold the channel map (PXD062330 did).
