import csv
from pathlib import Path

root = Path('results/denmark')
tech = dict(csv.reader((root / 'PXD074572_source_phospho_technical.tsv').open(newline=''), delimiter='\t'))
values = tech['comment[cleavage agent details]'].split('|')
assert values == ['NT=Lys-C;AC=MS:1001309', 'NT=Trypsin;AC=MS:1001251']
path = Path('annotations/PXD074572-phosphoproteome.sdrf.tsv')
with path.open(newline='') as f:
    rows = list(csv.reader(f, delimiter='\t'))
header = rows[0]
idx = header.index('comment[cleavage agent details]')
assert header.count('comment[cleavage agent details]') == 1
for row in rows[1:]:
    assert row[idx] == values[0]
    row.insert(idx + 1, values[1])
header.insert(idx + 1, 'comment[cleavage agent details]')
si = header.index('source name')
fi = header.index('comment[fraction identifier]')
ei = header.index('characteristics[phosphopeptide enrichment method]')
for row in rows[1:]:
    row[fi] = '1' if 'antibody' in row[ei] else '2'
    row[si] = row[si].rsplit('_', 1)[0]
with path.open('w', newline='') as f:
    csv.writer(f, delimiter='\t', lineterminator='\n').writerows(rows)
