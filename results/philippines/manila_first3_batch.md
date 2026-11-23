# Manila first 3 PXD batch

Selected on 2026-11-23: all three `confirmed` Philippines hits in
`lists/philippines/manila.txt` / `manila_candidates.tsv`. None are in the
community corpus (`manila_in_corpus.txt` is empty) and none are annotated or
blocked locally yet. This is the whole Manila manifest.

Queue file: [../../results/queue/2026-11-23_manila-1.txt](../../results/queue/2026-11-23_manila-1.txt).
Ordered cohort: [manila_first3_batch.tsv](manila_first3_batch.tsv).

| Order | Accession | Title |
|---:|---|---|
| 1 | PXD027710 | Filipino NSCLC proteome (initial insights) |
| 2 | PXD050598 | Aberrant protein expression in NSCLC |
| 3 | PXD071583 | Hexosamine pathway / cytoskeletal remodeling |

Annotate in Claude Code (tier 3):

```text
/sdrf-skills:sdrf-annotate PXD027710
/sdrf-skills:sdrf-annotate PXD050598
/sdrf-skills:sdrf-annotate PXD071583
```

Optional local draft of the first PXD if the GPU is free:

```bash
NORDIC_BATCH=1 scripts/annotate_local.sh PXD027710
```
