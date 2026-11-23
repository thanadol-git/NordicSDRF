# Penang first 3 PXD batch

Selected on 2026-11-23: all three `confirmed` Penang hits in
`lists/malaysia/penang.txt` / `penang_candidates.tsv`.

- **PXD018338** is already in the community corpus — listed for completeness, **not** re-annotated in this batch.
- **PXD010171** and **PXD077525** are new (not in corpus, no local SDRF).

Queue file: [../../results/queue/2026-11-23_penang-1.txt](../../results/queue/2026-11-23_penang-1.txt).
Ordered cohort: [penang_first3_batch.tsv](penang_first3_batch.tsv).

| Order | Accession | In corpus | Title |
|---:|---|---|---|
| 1 | PXD010171 | no | Entamoeba histolytica membrane proteins |
| 2 | PXD018338 | yes | Malaysian pigmented rice SWATH (skip annotate) |
| 3 | PXD077525 | no | Ixotrophy predator / nutrient availability |

Annotate (medium agents / sdrf-annotate):

```text
/sdrf-skills:sdrf-annotate PXD010171
/sdrf-skills:sdrf-annotate PXD077525
```
