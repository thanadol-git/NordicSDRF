"""Add the paper-supported second digestion enzyme to the Tg SDRF."""

import csv
from pathlib import Path

root = Path(__file__).resolve().parents[2]
path = root / "annotations/PXD035230-tg.sdrf.tsv"
with path.open(newline="") as handle:
    rows = list(csv.reader(handle, delimiter="\t"))
assert len(rows) == 13
header = rows[0]
assert header.count("comment[cleavage agent details]") == 1
index = header.index("comment[cleavage agent details]") + 1
assert all(row[index - 1] == "NT=Lys-C;AC=MS:1001309" for row in rows[1:])
for row in rows:
    row.insert(index, "comment[cleavage agent details]" if row is header else "NT=Trypsin;AC=MS:1001251")
with path.open("w", newline="") as handle:
    csv.writer(handle, delimiter="\t", lineterminator="\n").writerows(rows)
