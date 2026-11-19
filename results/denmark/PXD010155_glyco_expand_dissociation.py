import csv
from pathlib import Path
p=Path("annotations/PXD010155-glyco.sdrf.tsv")
with p.open(newline="") as f:
    rows=list(csv.reader(f, delimiter="\t"))
h=rows[0]
i=h.index("comment[dissociation method]")
assert h.count("comment[dissociation method]")==1
h.insert(i+1, "comment[dissociation method]")
for r in rows[1:]:
    assert r[i]=="NT=beam-type collision-induced dissociation;AC=MS:1000422"
    r.insert(i+1, "NT=electron transfer dissociation;AC=MS:1000598")
with p.open("w", newline="") as f:
    csv.writer(f, delimiter="\t", lineterminator="\n").writerows(rows)
