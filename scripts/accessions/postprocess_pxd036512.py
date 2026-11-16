"""Add the second paper-supported digestion enzyme to a builder-generated SDRF.

The current builder emits one cleavage-agent column for this template.  The
specification permits repeated cleavage-agent columns, so add Trypsin after
Lys-C while preserving every other builder-generated cell.
"""

import csv
from pathlib import Path


root = Path(__file__).resolve().parents[2]
path = root / "annotations/PXD036512.sdrf.tsv"
with path.open(newline="") as handle:
    rows = list(csv.reader(handle, delimiter="\t"))
assert len(rows) == 65
header = rows[0]
assert header.count("comment[cleavage agent details]") == 1
index = header.index("comment[cleavage agent details]") + 1
for row in rows[1:]:
    assert len(row) == len(header)
    assert row[index - 1] == "NT=Lys-C;AC=MS:1001309"
for row in rows:
    row.insert(index, "comment[cleavage agent details]" if row is header else "NT=Trypsin;AC=MS:1001251")
with path.open("w", newline="") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerows(rows)
print("Added Trypsin cleavage column after Lys-C to 64 rows")
