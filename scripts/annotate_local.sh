#!/usr/bin/env bash
# Run /sdrf-skills:sdrf-annotate for one PXD with Claude Code pointed at a
# local Ollama model — zero API tokens.
#
#   scripts/annotate_local.sh PXD000542 [ollama-model]        # interactive
#   NORDIC_BATCH=1 scripts/annotate_local.sh PXD000542         # headless (used by the Slurm job)
#
# Env knobs: NORDIC_LOCAL_MODEL, OLLAMA_HOST, NORDIC_MAX_TURNS (batch, default 120),
#            NORDIC_CTX (context tokens the model was created with, default 131072).
# The first request alone is ~44k tokens (Claude Code system prompt + tool schemas +
# the sdrf-annotate skill), so a 64k window auto-compacts after the first tool call.
set -euo pipefail

PXD="${1:?usage: $0 PXD###### [model]}"
MODEL="${2:-${NORDIC_LOCAL_MODEL:-qwen3.5:9b-128k}}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$(cd "$REPO_ROOT/../sdrf-skills" && pwd)"
OUT_DIR="$REPO_ROOT/annotations"
LOG_DIR="$REPO_ROOT/results/logs"
CORPUS_DIR="$(cd "$REPO_ROOT/../sdrf-annotated-datasets/datasets" && pwd)"
OLLAMA_URL="${OLLAMA_HOST:-http://localhost:11434}"
case "$OLLAMA_URL" in http://*|https://*) ;; *) OLLAMA_URL="http://$OLLAMA_URL" ;; esac

if ! curl -fs "$OLLAMA_URL/api/tags" >/dev/null 2>&1; then
  echo "Ollama is not reachable at $OLLAMA_URL — start it first (see README 'Local annotation')." >&2
  exit 1
fi
if ! curl -fs "$OLLAMA_URL/api/tags" | grep -q "\"name\":\"$MODEL\""; then
  echo "Model $MODEL not pulled — run: ollama pull $MODEL" >&2
  exit 1
fi

# The skill checks the community repo with `gh api`, which is not installed here;
# point it at the local sibling checkout instead and keep outputs in this repo.
PROMPT="/sdrf-skills:sdrf-annotate $PXD

Environment notes for this run:
- \`gh\` is not installed. For Step 0.5 list $CORPUS_DIR/$PXD/ instead (no directory = new annotation).
- Use scratchpad/$PXD/ under $SKILLS_DIR for temp files.
- Write the final $PXD.sdrf.tsv and $PXD.report.md to $OUT_DIR/ (not to sdrf-skills/annotations/).
- Validate with $SKILLS_DIR/.venv/bin/parse_sdrf before presenting the result."

if [[ "${NORDIC_BATCH:-0}" == "1" ]]; then
  PROMPT="$PROMPT
- This is a non-interactive batch run: nobody can answer questions. Do not wait for
  confirmation at any step; make the template choice yourself and record the reasoning
  in the report. If information is missing, write \`not available\` and say so in the report.
- If the dataset cannot be annotated, write $OUT_DIR/$PXD.BLOCKED.md explaining why and stop."
fi

mkdir -p "$OUT_DIR" "$LOG_DIR" "$SKILLS_DIR/scratchpad/$PXD"
cd "$SKILLS_DIR"
# .venv here is a conda env (no activate script); putting its bin first is enough
# for parse_sdrf, python -m tools, and the MCP server's interpreter.
export PATH="$SKILLS_DIR/.venv/bin:$PATH"

export ANTHROPIC_BASE_URL="$OLLAMA_URL"
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_API_KEY=""
export ANTHROPIC_MODEL="$MODEL"
export ANTHROPIC_DEFAULT_SONNET_MODEL="$MODEL"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="$MODEL"
export ANTHROPIC_DEFAULT_OPUS_MODEL="$MODEL"
# Claude Code assumes 200k for models it does not know; tell it the real window so
# auto-compaction triggers before Ollama truncates.
export CLAUDE_CODE_MAX_CONTEXT_TOKENS="${NORDIC_CTX:-131072}"
export CLAUDE_SCRATCH="$SKILLS_DIR/scratchpad/$PXD"
# Claude Code's stream timeouts are tuned for Anthropic's API. A 9B model with
# half its layers on the CPU needs minutes to prefill a 60k+ prompt and ~10 tok/s
# to write a full SDRF, which otherwise ends the run with
# "API Error: The response stopped arriving" (PXD001817, turn 42).
export CLAUDE_STREAM_FIRST_BYTE_TIMEOUT_MS="${NORDIC_FIRST_BYTE_MS:-1200000}"   # 20 min for prefill
export CLAUDE_STREAM_IDLE_TIMEOUT_MS="${NORDIC_IDLE_MS:-600000}"                # 10 min between chunks
export API_TIMEOUT_MS="${NORDIC_API_TIMEOUT_MS:-3600000}"                      # 60 min per request
export CLAUDE_CODE_MAX_OUTPUT_TOKENS="${NORDIC_MAX_OUTPUT:-32000}"             # room for thinking + a whole SDRF

# The plugin's Stop hook (tools/review_gate.py) blocks the session until every
# unreviewed SDRF in the sdrf-skills git tree has been adversarially reviewed —
# including unrelated untracked files there. Run the gate as an explicit step
# instead (see README), so a local model cannot burn hours self-reviewing.
COMMON_ARGS=(--plugin-dir . --model "$MODEL" --settings '{"disableAllHooks": true}')

echo "Annotating $PXD with $MODEL via $OLLAMA_URL (outputs -> $OUT_DIR)"
if [[ "${NORDIC_BATCH:-0}" == "1" ]]; then
  LOG="$LOG_DIR/$PXD.$(date +%Y%m%d-%H%M%S).jsonl"
  echo "Batch mode: max ${NORDIC_MAX_TURNS:-120} turns, trace -> $LOG"
  claude -p "${COMMON_ARGS[@]}" \
    --mcp-config .mcp.json \
    --permission-mode bypassPermissions \
    --max-turns "${NORDIC_MAX_TURNS:-120}" \
    --output-format stream-json --verbose \
    -- "$PROMPT" > "$LOG" || status=$?
  # One-line verdict so a Slurm .out (or your terminal) shows the outcome without opening the trace.
  python3 - "$LOG" "$PXD" "$OUT_DIR" <<'EOF'
import json, sys, pathlib
log, pxd, out = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
calls = 0; end = None
for line in open(log):
    try: d = json.loads(line)
    except json.JSONDecodeError: continue
    if d.get("type") == "assistant":
        calls += sum(1 for b in d["message"].get("content", []) if b.get("type") == "tool_use")
    elif d.get("type") == "result":
        end = f"{d.get('subtype')} after {d.get('num_turns')} turns, {round((d.get('duration_ms') or 0)/60000)} min"
sdrf = out / f"{pxd}.sdrf.tsv"; blocked = out / f"{pxd}.BLOCKED.md"
produced = "SDRF written" if sdrf.exists() else "BLOCKED" if blocked.exists() else "no output file"
print(f"{pxd}: {end or 'no result event (killed or max turns?)'}; {calls} tool calls; {produced}")
EOF
  exit "${status:-0}"
else
  exec claude "${COMMON_ARGS[@]}" -- "$PROMPT"
fi
