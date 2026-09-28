#!/usr/bin/env bash
# Opens ONE update PR to bigbio/sdrf-annotated-datasets. The PR replaces 19 merged
# Lund SDRFs with the versions that passed independent adversarial review.
#
# Run it from the NordicSDRF repo root:
#   bash results/pr_updates/2026-09-28_lund_postreview/open_update_pr.sh [FORK_DIR]
# FORK_DIR is your local clone of thanadol-git/sdrf-annotated-datasets.
# Default: ~/Github/sdrf-annotated-datasets. The script clones it if it is missing.
set -euo pipefail

NORDIC="$(pwd)"
PKG="$NORDIC/results/pr_updates/2026-09-28_lund_postreview"
FORK_DIR="${1:-$HOME/Github/sdrf-annotated-datasets}"
BRANCH="update/lund-postreview-2026-09-28"

[ -f "$PKG/manifest.sha256" ] || { echo "run from the NordicSDRF repo root"; exit 1; }

# 1. The files must be exactly the reviewed versions (reviews are bound to these hashes).
( cd "$NORDIC/annotations" && sha256sum -c "$PKG/manifest.sha256" )

# 2. Get a fresh branch from upstream main.
if [ ! -d "$FORK_DIR/.git" ]; then
  gh repo clone thanadol-git/sdrf-annotated-datasets "$FORK_DIR" -- --depth 1
fi
cd "$FORK_DIR"
git remote get-url upstream >/dev/null 2>&1 || git remote add upstream https://github.com/bigbio/sdrf-annotated-datasets.git
# Sync your fork's main first so the push only uploads the new commit.
gh repo sync thanadol-git/sdrf-annotated-datasets --branch main >/dev/null 2>&1 || true
if [ "$(git rev-parse --is-shallow-repository)" = "true" ]; then
  git fetch --depth 1 upstream main
else
  git fetch upstream main
fi
git diff --quiet && git diff --cached --quiet || { echo "$FORK_DIR has uncommitted changes — commit or stash them first"; exit 1; }
git checkout -B "$BRANCH" upstream/main

# 3. Copy the reviewed files into place.
while read -r _ f; do
  acc="${f%%.*}"; acc="${acc%%-*}"
  [ -d "datasets/$acc" ] || { echo "datasets/$acc missing on upstream main — abort"; exit 1; }
  cp "$NORDIC/annotations/$f" "datasets/$acc/$f"
  git add "datasets/$acc/$f"
done < "$PKG/manifest.sha256"

# 4. Guard: only modifications of existing files, nothing added or deleted.
git diff --cached --name-status
if git diff --cached --name-status | grep -qv '^M'; then
  echo "unexpected add/delete/rename — abort"; exit 1
fi

# 5. Validate the way CI does.
if command -v parse_sdrf >/dev/null; then
  for f in $(git diff --cached --name-only); do
    echo "== $f"; parse_sdrf validate-sdrf --sdrf_file "$f" --use_ols_cache_only | tail -1
  done
fi

# 6. Commit, push and open the PR (DRYRUN=1 stops here).
[ "${DRYRUN:-0}" = "1" ] && { echo "DRYRUN: stopping before commit"; exit 0; }
git commit -m "Post-review corrections for 19 Lund SDRFs (PXD021241 … PXD032369)"
git push -u origin "$BRANCH"
gh pr create --repo bigbio/sdrf-annotated-datasets --base main \
  --head "thanadol-git:$BRANCH" \
  --title "Post-review corrections for 19 Lund SDRFs" \
  --body-file "$PKG/PR_BODY.md"
