import csv
from pathlib import Path

root = Path('results/denmark')
tech = dict(csv.reader((root / 'PXD024280_source_chromass_technical.tsv').open(newline=''), delimiter='\t'))
values = tech['comment[cleavage agent details]'].split('|')
assert values == ['NT=Lys-C;AC=MS:1001309', 'NT=Trypsin;AC=MS:1001251']
path = Path('annotations/PXD024280-chromass.sdrf.tsv')
with path.open(newline='') as f:
    rows = list(csv.reader(f, delimiter='\t'))
header = rows[0]
idx = header.index('comment[cleavage agent details]')
assert header.count('comment[cleavage agent details]') == 1
for row in rows[1:]:
    assert row[idx] == values[0]
    row.insert(idx + 1, values[1])
header.insert(idx + 1, 'comment[cleavage agent details]')
with path.open('w', newline='') as f:
    csv.writer(f, delimiter='\t', lineterminator='\n').writerows(rows)
