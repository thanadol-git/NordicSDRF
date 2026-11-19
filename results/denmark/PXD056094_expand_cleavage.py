import csv
from pathlib import Path
for tag in ('HF','HFX'):
 path = Path(f'annotations/PXD056094_{tag}.sdrf.tsv')
 with path.open(newline='') as f: rows=list(csv.reader(f,delimiter='\t'))
 h=rows[0];i=h.index('comment[cleavage agent details]')
 assert h.count('comment[cleavage agent details]')==1
 assert all(r[i]=='NT=Lys-C;AC=MS:1001309' for r in rows[1:])
 rows[0].insert(i+1,'comment[cleavage agent details]')
 for r in rows[1:]:r.insert(i+1,'NT=Trypsin;AC=MS:1001251')
 with path.open('w',newline='') as f:csv.writer(f,delimiter='\t',lineterminator='\n').writerows(rows)
