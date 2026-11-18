import csv
from pathlib import Path
p=Path('annotations/PXD025523-human-biopsy.sdrf.tsv')
with p.open(newline='') as f: rows=list(csv.reader(f,delimiter='\t'))
h=rows[0];i=h.index('comment[cleavage agent details]')
assert h.count('comment[cleavage agent details]')==1
h.insert(i+1,'comment[cleavage agent details]')
for r in rows[1:]:
 assert r[i]=='NT=Lys-C;AC=MS:1001309'
 r.insert(i+1,'NT=Trypsin;AC=MS:1001251')
with p.open('w',newline='') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerows(rows)
