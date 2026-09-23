# NordicSDRF

Annotate every Nordic-affiliated PRIDE proteomics dataset with a validated
[SDRF](https://github.com/bigbio/proteomics-metadata-standard) file, worked
country by country and city by city, starting with Sweden.

This repo is a **campaign tracker**, not an annotation engine. The actual
annotation work is done by [`sdrf-skills`](https://github.com/bigbio/sdrf-skills)
(the skill pack you've used before — `sdrf-metascreen`, `sdrf-annotate`,
`sdrf-validate`, `sdrf-fix`, `sdrf-review`, `sdrf-adversarial-review`, ...).
NordicSDRF holds the city manifests, the screening/annotation outputs, and the
progress tracker; finished SDRFs eventually get contributed upstream to
[`sdrf-annotated-datasets`](https://github.com/bigbio/sdrf-annotated-datasets)
via `sdrf-contribute`.

## Why hybrid (local GPU + Codex + Claude)

Full expert annotation is token-expensive and most of that cost is wasted on
datasets that turn out to be irrelevant or unannotatable. Three tiers, cheapest
first:

| Tier | Runs on | Job | Why here |
|---|---|---|---|
| **1. Local** | Your NVIDIA RTX PRO 2000 GPU (Ollama), free | Dedup against the existing corpus; local LLM pre-triage of PRIDE's structured fields (organism, instrument, keywords, protocol text) into rough include / exclude / uncertain; flag likely-multiplexed studies with no visible channel→sample map | Zero token cost, runs on the whole list at once, cuts what reaches tier 2/3 |
| **2. Codex** | Cheaper reasoning | `sdrf-metascreen` full screen (PRIDE + paper) on what survives tier 1; `sdrf-fix` mechanical repairs; `sdrf-validate` iteration loops | Mostly mechanical evidence-lookup and rule-following — doesn't need frontier judgment |
| **3. Claude** | Reserved, highest reasoning cost | `sdrf-annotate` on `include` rows; `sdrf-review`; the fresh-context `sdrf-adversarial-review` gate | This is where the annotator brief's hard traps live (Dimethyl vs Carbamidomethyl swaps, OLS smart-mode wrong hits, cell-line identity research, channel-map fabrication risk) — errors here are silent and costly, so don't cut corners on model quality |

Tier 1 never writes an SDRF and never makes a final include/exclude call — it
only reorders/filters the queue so tiers 2–3 spend tokens on datasets likely
to be worth it. A local false negative just means tier 2 re-screens something
tier 1 under-rated; nothing is silently dropped without a rerunnable trail.

## Repository layout

```
NordicSDRF/
├── config.yml                  # single source of truth: countries → cities → counts/status
├── sweden/
│   ├── stockholm.txt           # one PXD per line — your source lists
│   ├── gothenburg.txt
│   ├── lund.txt
│   └── uppsala.txt
├── results/                   # sdrf-metascreen output, resumable TSV + .log per city
│   └── sweden/
│       └── <city>_screen.tsv
├── annotations/                # sdrf-annotate output — same shape as sdrf-skills/annotations
│   ├── <PXD>.sdrf.tsv
│   ├── <PXD>.report.md
│   ├── BLOCKED.md              # screened `include` but not annotatable, and why
│   └── DUPLICATES.md           # overlapping depositions found (checksum-verified)
├── status/
│   └── sweden.md               # per-city progress table (generated/updated as you go)
├── criteria/
│   └── nordic_screen.md        # inclusion rules + extract fields for sdrf-metascreen
└── scripts/
    ├── check_existing_coverage.py   # tier 1: dedup against sdrf-annotated-datasets + BLOCKED/DUPLICATES
    └── local_triage.py              # tier 1: local Ollama pre-screen of a city manifest
```

`sdrf-skills` is used as an external dependency, not vendored — either a
sibling checkout (`../sdrf-skills`, already present on this machine, and the
default recorded in `config.yml`) or a git submodule if you want the repo
self-contained and pinned to a version.

`config.yml` is the single manifest: which sibling tools to use, the
tier-1/2/3 pipeline assignment, and per-country/per-city PXD counts and
progress counters. Update its counters as cities move through the pipeline;
`status/*.md` can stay as a human-readable render of the same numbers.

## Current status

| City | PXDs listed | Screened | Annotated | Blocked |
|---|---:|---:|---:|---:|
| Stockholm | 165 | 0 | 0 | 0 |
| Lund | 163 | 0 | 0 | 0 |
| Gothenburg | 135 | 0 | 0 | 0 |
| Uppsala | 75 | 0 | 0 | 0 |
| **Total** | **538** | 0 | 0 | 0 |

No duplicates found within or across the four city lists. One anomaly to
resolve before screening: `sweden/stockholm.txt` line 1 is `PRD000423`,
an old pre-`PXD` ProteomeXchange accession — resolve it to its current `PXD`
id (ProteomeXchange redirect or PRIDE search) before it hits `sdrf-metascreen`,
which expects `PXD`/`MSV` accessions.

Norway, Denmark, Finland, and Iceland are not yet scoped (`status: not_started`
in `config.yml`) — add a `<country>/<city>.txt` manifest the same way and a
matching block under `countries:` in `config.yml` when you have those lists.

## Workflow, per city

```bash
# 0. One-time setup (see sdrf-skills/README.md)
cd sdrf-skills && conda env create -f environment.yml && conda activate sdrf-skills

# 1. Tier 1 — local, free: dedup + pre-triage (from NordicSDRF root)
python scripts/check_existing_coverage.py sweden/stockholm.txt \
  --against ../sdrf-annotated-datasets/datasets ../sdrf-skills/annotations \
  --out results/sweden/stockholm_new.txt

python scripts/local_triage.py results/sweden/stockholm_new.txt \
  --model qwen2.5:7b --out results/sweden/stockholm_triaged.tsv

# 2. Tier 2 — Codex: full screen against Nordic inclusion criteria
#    (run under Codex to keep this mechanical pass cheap)
$sdrf-metascreen target="results/sweden/stockholm_triaged.tsv" \
  criteria="criteria/nordic_screen.md" extract="criteria/nordic_screen.md" \
  output="results/sweden/stockholm_screen.tsv"

# 3. Tier 3 — Claude: annotate only the `include` rows, one at a time
/sdrf-skills:sdrf-annotate PXD######
/sdrf-skills:sdrf-review annotations/PXD######.sdrf.tsv
$sdrf-adversarial-review annotations/PXD######.sdrf.tsv   # fresh-context gate, hash-bound receipt

# 4. Update the tracker
#    append/refresh the PXD's row in status/sweden.md

# 5. Once validated + reviewed, contribute upstream
/sdrf-skills:sdrf-contribute PXD######
```

Repeat for `gothenburg.txt`, `lund.txt`, `uppsala.txt`, then the next country.

### Concurrency

If annotating several `PXD`s at once, follow `sdrf-skills/annotations/ANNOTATOR_BRIEF.md`'s
private-scratch-directory rule per accession — concurrent agents sharing a
scratch dir have silently corrupted each other's runs before (wrong dataset's
cached files, wrong paper fetched). Never share `$CLAUDE_SCRATCH` across two
in-flight `PXD`s.

### Review gate

Nothing counts as "done" without a passing `sdrf-adversarial-review` receipt —
enforced by `python -m tools review-gate gate` in `sdrf-skills`, keyed to the
SDRF's SHA-256 so any edit re-opens the gate.

## Next steps

1. Resolve `PRD000423` in the Stockholm list.
2. Write `criteria/nordic_screen.md` (Swedish institution/city affiliation,
   MS-based proteomics scope, any exclusions you want — e.g. non-human only).
3. Write `scripts/check_existing_coverage.py` and `scripts/local_triage.py`
   (tier 1 automation described above).
4. Run Stockholm end-to-end first as a pilot to tune `dig_passes` and the
   local triage model choice before scaling to the other three cities.
