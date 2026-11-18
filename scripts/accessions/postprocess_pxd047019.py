"""Restore the second wet-lab cleavage stage in a repeated SDRF column."""

import csv
from pathlib import Path

path = Path(__file__).resolve().parents[2] / "annotations/PXD047019.sdrf.tsv"
with path.open(newline="") as handle:
    rows = list(csv.reader(handle, delimiter="\t"))
header = rows[0]
assert header.count("comment[cleavage agent details]") == 1
index = header.index("comment[cleavage agent details]") + 1
assert len(rows) == 91
assert all(row[index - 1] == "NT=Lys-C;AC=MS:1001309" for row in rows[1:])
for number, row in enumerate(rows):
    row.insert(index, "comment[cleavage agent details]" if number == 0 else "NT=Asp-N;AC=MS:1001304")
with path.open("w", newline="") as handle:
    csv.writer(handle, delimiter="\t", lineterminator="\n").writerows(rows)
print("PXD047019: restored Asp-N in 90 rows")
