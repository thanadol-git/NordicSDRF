#!/usr/bin/env bash
# Slurm array job: one task per line of a PXD manifest, each running the local
# (zero-token) annotation in headless mode. Submit from the NordicSDRF root:
#
#   sbatch --array=1-$(wc -l < lists/sweden/uppsala.txt)%1 scripts/annotate_slurm.sbatch lists/sweden/uppsala.txt
#
# `%1` runs one task at a time — the 8 GB laptop GPU fits one model instance.
# On a multi-GPU cluster raise the throttle and uncomment --gres below.
#
#SBATCH --job-name=nordic-sdrf
#SBATCH --partition=cpu
#SBATCH --cpus-per-task=8
#SBATCH --mem=24G
#SBATCH --time=06:00:00
#SBATCH --output=results/logs/slurm-%A_%a.out
##SBATCH --gres=gpu:1          # enable once gpu is declared in slurm.conf / gres.conf
set -euo pipefail

MANIFEST="${1:?usage: sbatch --array=1-N scripts/annotate_slurm.sbatch <manifest.txt>}"
REPO_ROOT="${SLURM_SUBMIT_DIR:-$(pwd)}"
cd "$REPO_ROOT"
mkdir -p results/logs

PXD="$(sed -n "${SLURM_ARRAY_TASK_ID:?run as an array job}p" "$MANIFEST" | tr -d '[:space:]')"
[[ "$PXD" =~ ^PXD[0-9]{6}$ ]] || { echo "line $SLURM_ARRAY_TASK_ID of $MANIFEST is not a PXD: '$PXD' — skipping"; exit 0; }
if [[ -e "annotations/$PXD.sdrf.tsv" || -e "annotations/$PXD.BLOCKED.md" ]]; then
  echo "$PXD already has an output in annotations/ — skipping (delete it to rerun)"; exit 0
fi

export PATH="$HOME/.local/bin:$PATH"           # claude
MODEL="${NORDIC_LOCAL_MODEL:-qwen3.5:9b-128k}"

# Use an already-running Ollama (the systemd service on this laptop) if there is
# one; otherwise start a private instance for this job — the cluster case, where
# the job owns the GPU and nothing is listening yet.
OLLAMA_URL="${OLLAMA_HOST:-http://localhost:11434}"
if ! curl -fs "$OLLAMA_URL/api/tags" >/dev/null 2>&1; then
  PORT=$((20000 + SLURM_JOB_ID % 20000))
  export OLLAMA_HOST="127.0.0.1:$PORT"
  export OLLAMA_MODELS="${OLLAMA_MODELS:-$HOME/.ollama/models}"
  export OLLAMA_KV_CACHE_TYPE=q8_0 OLLAMA_FLASH_ATTENTION=1
  ollama serve > "results/logs/ollama-${SLURM_JOB_ID}.log" 2>&1 &
  OLLAMA_PID=$!
  trap 'kill $OLLAMA_PID 2>/dev/null || true' EXIT
  for _ in $(seq 1 60); do curl -fs "http://$OLLAMA_HOST/api/tags" >/dev/null 2>&1 && break; sleep 2; done
  OLLAMA_URL="http://$OLLAMA_HOST"
  curl -fs "$OLLAMA_URL/api/tags" | grep -q "\"name\":\"$MODEL\"" || ollama pull "$MODEL"
fi

echo "[$(date -Is)] task $SLURM_ARRAY_TASK_ID -> $PXD on $(hostname) via $OLLAMA_URL"
nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv,noheader 2>/dev/null || echo "no nvidia-smi on this node"

start=$SECONDS
NORDIC_BATCH=1 OLLAMA_HOST="$OLLAMA_URL" scripts/annotate_local.sh "$PXD" "$MODEL" || status=$?
echo "[$(date -Is)] $PXD finished with exit ${status:-0} after $(( (SECONDS - start) / 60 )) min"
ls -la "annotations/$PXD".* 2>/dev/null || echo "no output written for $PXD"

# Refresh config.yml / README / status/ from what is now on disk. Offline mode is
# instant; the lock keeps concurrent array tasks from writing the same files at once.
PY=../sdrf-skills/.venv/bin/python; [[ -x $PY ]] || PY=python3     # needs PyYAML
flock -w 120 results/.status.lock \
  "$PY" scripts/update_status.py --no-pride || echo "tracker update failed (non-fatal)"
