"""Restore sequential trypsin digestion after the builder's single-cleavage contract."""

import csv
from pathlib import Path


path = Path(__file__).resolve().parents[2] / "annotations/PXD017475-secretome.sdrf.tsv"
with path.open(newline="") as handle:
    rows = list(csv.reader(handle, delimiter="\t"))
assert len(rows) == 10
header = rows[0]
assert header.count("comment[cleavage agent details]") == 1
index = header.index("comment[cleavage agent details]") + 1
assert all(row[index - 1] == "NT=Lys-C;AC=MS:1001309" for row in rows[1:])
for number, row in enumerate(rows):
    row.insert(index, "comment[cleavage agent details]" if number == 0 else "NT=Trypsin;AC=MS:1001251")
with path.open("w", newline="") as handle:
    csv.writer(handle, delimiter="\t", lineterminator="\n").writerows(rows)
print("PXD017475 secretome: restored sequential trypsin to nine rows")
