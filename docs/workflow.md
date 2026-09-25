# Annotation workflow

How NordicSDRF uses a local GPU, Codex, and Claude. Campaign status and city
lists stay in the [README](../README.md).

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

## Workflow, per city

```bash
# 0. One-time setup (see sdrf-skills/README.md)
cd sdrf-skills && conda env create -f environment.yml && conda activate sdrf-skills

# 1. Tier 1 — local, free: dedup + pre-triage (from NordicSDRF root)
python scripts/check_existing_coverage.py lists/sweden/stockholm.txt \
  --against ../sdrf-annotated-datasets/datasets ../sdrf-skills/annotations \
  --out results/sweden/stockholm_new.txt

python scripts/local_triage.py results/sweden/stockholm_new.txt \
  --model qwen2.5:7b --out results/sweden/stockholm_triaged.tsv

# 2. Tier 2 — Codex: full screen against Nordic inclusion criteria
#    (run under Codex to keep this mechanical pass cheap)
$sdrf-metascreen target="results/sweden/stockholm_triaged.tsv" \
  criteria="criteria/nordic_screen.md" extract="criteria/nordic_screen.md" \
  output="results/sweden/stockholm_screen.tsv"

# 3. Today's 10 (or fewer) — skip corpus / done / blocked / already running
python scripts/daily_queue.py iceland            # writes results/queue/<date>_iceland.txt
#    then, in Claude Code (tier 3), annotate each queued PXD:
/sdrf-skills:sdrf-annotate PXD######
/sdrf-skills:sdrf-review annotations/PXD######.sdrf.tsv
$sdrf-adversarial-review annotations/PXD######.sdrf.tsv   # fresh-context gate, hash-bound receipt
#    optional overnight local draft of the first queued PXD, only if the GPU is free

# 4. Update the tracker (counts annotations/, results/, manifests; --corpus github
#    checks the live community repo; drop --no-pride to refresh PRIDE hit counts)
python scripts/update_status.py --no-pride --corpus github

# 5. Once validated + reviewed, contribute upstream
/sdrf-skills:sdrf-contribute PXD######
```

Repeat for `gothenburg.txt`, `lund.txt`, `uppsala.txt`, then the next country.

## Daily queue (aim: 10 PXDs / day)

Ten finished SDRFs a day is a **Claude** quota, not a local-GPU quota. The
laptop filters; Claude annotates. Iceland is the pilot — three confirmed PXDs,
none in the community corpus:

```bash
python scripts/daily_queue.py iceland                 # next 10 (here: the 3 remaining)
python scripts/daily_queue.py iceland --dry-run       # print only
python scripts/daily_queue.py --limit 10              # next country that still has a manifest
```

The script writes `results/queue/<YYYY-MM-DD>_<country>.txt` and prints the
`/sdrf-skills:sdrf-annotate` lines for today. It never starts a job. A PXD
already in flight (live JSONL or `claude -p`) is listed as `running` and kept
off the queue so you do not share the 8 GB GPU. If a city later has a
`results/<country>/<city>_screen.tsv`, only `include` rows are queued.

After the Claude pass, `python scripts/update_status.py --no-pride` so the
README charts pick up the new SDRFs.

## Local annotation (zero API tokens)

Claude Code can run the `sdrf-skills` plugin against a local Ollama model via
Ollama's Anthropic-compatible API. One-time setup:

```bash
curl -fsSL https://ollama.com/install.sh | sh          # needs sudo; installs + starts a systemd service on :11434
ollama pull qwen3.5:9b                                  # 6.6 GB; qwen3.5:4b (3.4 GB) fits fully in 8 GB VRAM
printf 'FROM qwen3.5:9b\nPARAMETER num_ctx 131072\n' > /tmp/Modelfile.128k
ollama create qwen3.5:9b-128k -f /tmp/Modelfile.128k                 # -f - (stdin) is not supported
```

The last line bakes a 128k-context variant. The service default is much
smaller, and 64k is not enough either: the first request alone is ~44k tokens
(Claude Code system prompt + tool schemas + the `sdrf-annotate` skill), so with
a 64k window Claude Code starts auto-compacting after the first tool call and
never gets going. Then:

```bash
scripts/annotate_local.sh PXD000542            # second arg or NORDIC_LOCAL_MODEL overrides the model
```

The script points `ANTHROPIC_BASE_URL` at the running Ollama service, loads
the plugin from `../sdrf-skills`, and asks the skill to write into
`annotations/` here. Measured on the RTX PRO 2000 (8 GB): the 9B model at 64k
context loads as 8.5 GB, 72% GPU / 28% CPU, ~10 tok/s generation; at 128k the
KV cache is larger, so expect more CPU offload and a slower rate. If that is
too slow, `qwen3.5:4b` at 128k is the fallback. Expect a local 4–9B
model to be far weaker than tier 3 on the annotator brief's traps — treat its
output as a draft and keep the `sdrf-adversarial-review` gate mandatory.

**Stream timeouts are raised.** Claude Code's defaults assume Anthropic's
latency; the first full attempt on PXD001817 died at turn 42 (68 min, context
67k) with `API Error: The response stopped arriving` while the model was
writing the SDRF. The launcher therefore sets
`CLAUDE_STREAM_FIRST_BYTE_TIMEOUT_MS=1200000` (prefill of a 60k+ prompt with
CPU offload), `CLAUDE_STREAM_IDLE_TIMEOUT_MS=600000`, `API_TIMEOUT_MS=3600000`
and `CLAUDE_CODE_MAX_OUTPUT_TOKENS=32000`; override with `NORDIC_FIRST_BYTE_MS`,
`NORDIC_IDLE_MS`, `NORDIC_API_TIMEOUT_MS`, `NORDIC_MAX_OUTPUT`.

**Plugin hooks are disabled in these runs.** The `sdrf-skills` `Stop` hook
(`tools/review_gate.py stop-hook`) refuses to end a session while *any* SDRF in
the `sdrf-skills` git tree lacks a review receipt — including unrelated
untracked files there — and tells the model to spawn reviewer subagents. With a
local model that turned a 2-turn test into a 15-minute self-review of four
unrelated files. Run the gate yourself as an explicit step instead:

```bash
cd ../sdrf-skills && .venv/bin/python -m tools review-gate gate --cwd ../NordicSDRF
```

## Batch runs with Slurm

This machine has a single-node Slurm (`ClusterName=dell`, partition `cpu`, no
GPU resource declared) whose daemons are not running by default. Start them,
then submit one array task per manifest line, throttled to one at a time
because the 8 GB GPU fits one model instance:

```bash
sudo systemctl start slurmctld slurmd
sbatch --array=1-$(wc -l < lists/sweden/uppsala.txt)%1 scripts/annotate_slurm.sbatch lists/sweden/uppsala.txt
squeue -u "$USER"; tail -f results/logs/slurm-*_1.out
```

Each task runs `scripts/annotate_local.sh` in headless mode
(`NORDIC_BATCH=1`: `claude -p`, permissions bypassed, `--max-turns 120`, full
`stream-json` trace in `results/logs/<PXD>.<ts>.jsonl`), skips PXDs that already
have an `annotations/<PXD>.sdrf.tsv` or `.BLOCKED.md`, and reuses the running
Ollama service. On a real cluster the same script starts a private `ollama
serve` on a job-local port when none is reachable; uncomment `--gres=gpu:1`
there, and check the compute nodes can reach PRIDE/Europe PMC/OLS (many block
outbound traffic). To declare the GPU to the local Slurm, add
`GresTypes=gpu`, `Gres=gpu:1` on the `NodeName` line in `/etc/slurm/slurm.conf`
and `Name=gpu File=/dev/nvidia0` in `/etc/slurm/gres.conf`.

## Checking status locally

Everything is on disk; nothing needs a token. Three levels: is a run alive,
what is that run doing, and where is the campaign.

Needs `python3` with PyYAML for the tracker (`mambaforge` or
`../sdrf-skills/.venv/bin/python`). Traces are gitignored under
`results/logs/`.

**1. Is a run alive?**

```bash
pgrep -af "claude -p"                        # headless Claude Code process(es)
curl -s localhost:11434/api/ps | python3 -m json.tool   # model in Ollama, VRAM/CPU split, expires_at
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv   # GPU busy = model is generating
squeue -u "$USER"                            # Slurm array: PD = waiting, R = running
```

Ollama unloads the model 5 min after the last request, so an empty `api/ps`
while `claude -p` still exists means Claude Code is between requests (a tool
call), not that the run is dead.

**2. What is the run doing?** Every headless run writes a `stream-json` trace
to `results/logs/<PXD>.<timestamp>.jsonl`. Summarise a live or finished trace
with `scripts/trace_summary.py` (needs only the stdlib):

```bash
python scripts/trace_summary.py results/logs/*.jsonl          # one line per trace
python scripts/trace_summary.py -v results/logs/PXD001817.20260923-204007.jsonl   # + every tool call
watch -n 30 'python scripts/trace_summary.py results/logs/*.jsonl'                # refresh every 30 s
```

```text
PXD001817.20260923-202912.jsonl: FINISHED error_during_execution after 4 turns, 10 min; 1 tool calls; context 32k; 14 compactions; last tool: Bash(...)
PXD001817.20260923-204007.jsonl: FINISHED success after 42 turns, 68 min — API Error: The response stopped arriving. ...; 37 tool calls; context 67k; 0 compactions; last tool: Read(.../TERMS.tsv)
PXD001817.20260923-220741.jsonl: RUNNING (last write 0 min ago); 2 tool calls; context 44k; 0 compactions; last tool: Bash(...)
```

How to read a line:

| Field | Meaning |
|---|---|
| `RUNNING` / `FINISHED <subtype>` | Live vs done. `success` is Claude Code exiting cleanly — still a failure if the text starts with `API Error` or there is no file in `annotations/` |
| `error_during_execution` | Process died (killed, hook, crash) |
| *N* tool calls | Real progress meter. A full annotation is roughly 30–50: PRIDE metadata → paper → OLS lookups → write SDRF → `parse_sdrf` |
| `context Nk` | Prompt size; this is what drives per-turn time on the 8 GB GPU |
| *N* compactions | `> 0` means the context window is too small (the 64k variant — see above) |
| `looks stalled` | No write to the JSONL for 15 min |
| `last tool` | What the model just did |

Raw stream, if you want it: `tail -f results/logs/<PXD>.*.jsonl | cut -c1-200`.

Outputs on disk, independent of the trace:

```bash
ls -la annotations/                          # <PXD>.sdrf.tsv + .report.md = done; <PXD>.BLOCKED.md = gave up
ls ../sdrf-skills/scratchpad/<PXD>/          # cached PRIDE/PMC files the model pulled
tail -3 results/logs/slurm-*_*.out           # each Slurm task ends with a verdict line:
                                             #   "PXD001817: success after 42 turns, 68 min; 37 tool calls; SDRF written"
```

**3. Where is the campaign?** The tracker never calls out. It counts files
here and writes `config.yml`, the [Current status](../README.md#current-status)
block in the README, and `status/<country>.md`:

```bash
python scripts/update_status.py --no-pride --dry-run              # print the numbers, change nothing
python scripts/update_status.py --no-pride                        # refresh from local files only (offline)
python scripts/update_status.py --no-pride --country iceland      # one country
python scripts/update_status.py --no-pride --corpus github        # + live check against bigbio/sdrf-annotated-datasets
cat status/sweden.md                                              # generated per-country page + chart
cat status/iceland.md
```

| File | What it tells you |
|---|---|
| `status/<country>.md` | Same chart as in the README, one country |
| `config.yml` → city `annotated` / `blocked` / `in_corpus` | Machine counters the tables are built from |
| `annotations/<PXD>.sdrf.tsv` | That PXD is counted as annotated |
| `annotations/<PXD>.BLOCKED.md` | Counted as blocked |
| `results/<country>/<city>_screen.tsv` | Counted as screened (data rows) |
| `results/<country>/<city>_in_corpus.txt` | Manifest PXDs already in the community corpus |
| `results/<country>/<city>_candidates.tsv` | Evidence from `build_manifest.py` (keep / reject) |

Slurm tasks run the offline form automatically after each PXD, so the tables
lag a batch by at most one task. Use `--dry-run` while a job is writing.
Drop `--no-pride` only when you want to re-query PRIDE hit counts (slow,
needs the network).

## Concurrency

If annotating several `PXD`s at once, follow `sdrf-skills/annotations/ANNOTATOR_BRIEF.md`'s
private-scratch-directory rule per accession — concurrent agents sharing a
scratch dir have silently corrupted each other's runs before (wrong dataset's
cached files, wrong paper fetched). Never share `$CLAUDE_SCRATCH` across two
in-flight `PXD`s.

## Review gate

Nothing counts as "done" without a passing `sdrf-adversarial-review` receipt —
enforced by `python -m tools review-gate gate` in `sdrf-skills`, keyed to the
SDRF's SHA-256 so any edit re-opens the gate.
