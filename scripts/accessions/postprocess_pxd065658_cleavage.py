"""Restore Lys-C lost by the generic builder's single-value cleavage contract."""

import csv
from pathlib import Path


path = Path(__file__).resolve().parents[2] / "annotations/PXD065658.sdrf.tsv"
with path.open(newline="") as handle:
    rows = list(csv.reader(handle, delimiter="\t"))
header = rows[0]
assert header.count("comment[cleavage agent details]") == 1
index = header.index("comment[cleavage agent details]") + 1
assert all(row[index - 1] == "NT=Trypsin;AC=MS:1001251" for row in rows[1:])
for number, row in enumerate(rows):
    row.insert(index, "comment[cleavage agent details]" if number == 0 else "NT=Lys-C;AC=MS:1001309")
with path.open("w", newline="") as handle:
    csv.writer(handle, delimiter="\t", lineterminator="\n").writerows(rows)
print(f"added Lys-C cleavage column to {len(rows)-1} rows")
