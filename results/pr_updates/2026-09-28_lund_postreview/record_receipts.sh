#!/usr/bin/env bash
# Records the independent-review receipts in your NordicSDRF .git state (one per reviewed SDRF).
# Usage, from the NordicSDRF repo root:  SDRF_SKILLS=/path/to/sdrf-skills bash results/pr_updates/2026-09-28_lund_postreview/record_receipts.sh
set -euo pipefail
: "${SDRF_SKILLS:?set SDRF_SKILLS to your sdrf-skills checkout}"
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD021241.sdrf.tsv --report results/reviews/PXD021241.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD021245.sdrf.tsv --report results/reviews/PXD021245.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD021394.sdrf.tsv --report results/reviews/PXD021394.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD023075.sdrf.tsv --report results/reviews/PXD023075.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD023244.sdrf.tsv --report results/reviews/PXD023244.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD023708-dda.sdrf.tsv --report results/reviews/PXD023708-dda.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD023708-dia.sdrf.tsv --report results/reviews/PXD023708-dia.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD023708.sdrf.tsv --report results/reviews/PXD023708.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD024286.sdrf.tsv --report results/reviews/PXD024286.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD024448.sdrf.tsv --report results/reviews/PXD024448.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD024508.sdrf.tsv --report results/reviews/PXD024508.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD026371.sdrf.tsv --report results/reviews/PXD026371.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD026661.sdrf.tsv --report results/reviews/PXD026661.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD026690.sdrf.tsv --report results/reviews/PXD026690.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD027173.sdrf.tsv --report results/reviews/PXD027173.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD027259.sdrf.tsv --report results/reviews/PXD027259.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD029028-dda-library.sdrf.tsv --report results/reviews/PXD029028-dda-library.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD029028.sdrf.tsv --report results/reviews/PXD029028.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD029135.sdrf.tsv --report results/reviews/PXD029135.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD029625.sdrf.tsv --report results/reviews/PXD029625.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD029805-dda.sdrf.tsv --report results/reviews/PXD029805-dda.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD029805-dia.sdrf.tsv --report results/reviews/PXD029805-dia.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD029805.sdrf.tsv --report results/reviews/PXD029805.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD029821-dda.sdrf.tsv --report results/reviews/PXD029821-dda.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD029821-dia.sdrf.tsv --report results/reviews/PXD029821-dia.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD029821.sdrf.tsv --report results/reviews/PXD029821.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD030043.sdrf.tsv --report results/reviews/PXD030043.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD031202.sdrf.tsv --report results/reviews/PXD031202.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD031693.sdrf.tsv --report results/reviews/PXD031693.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD032213.sdrf.tsv --report results/reviews/PXD032213.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD032266.sdrf.tsv --report results/reviews/PXD032266.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD032285.sdrf.tsv --report results/reviews/PXD032285.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" approve annotations/PXD032369.sdrf.tsv --report results/reviews/PXD032369.sdrf.tsv.review.json --reviewer independent-hook-agent --cwd .
python3 "$SDRF_SKILLS/tools/review_gate.py" status --cwd .
