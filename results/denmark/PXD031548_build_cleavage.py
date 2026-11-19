import csv
from pathlib import Path

root = Path('results/denmark')
tech = dict(csv.reader((root / 'PXD031548_source_technical.tsv').open(newline=''), delimiter='\t'))
values = tech['comment[cleavage agent details]'].split('|')
assert len(values) == 2 and values == ['NT=Lys-C;AC=MS:1001309', 'NT=Asp-N;AC=MS:1001304']
path = Path('annotations/PXD031548.sdrf.tsv')
with path.open(newline='') as f:
    rows = list(csv.reader(f, delimiter='\t'))
header = rows[0]
idx = header.index('comment[cleavage agent details]')
assert header.count('comment[cleavage agent details]') == 1
out = []
for i, row in enumerate(rows):
    if i:
        assert row[idx] == values[0]
        out.append(row[:idx+1] + [values[1]] + row[idx+1:])
    else:
        out.append(row[:idx+1] + ['comment[cleavage agent details]'] + row[idx+1:])
with path.open('w', newline='') as f:
    csv.writer(f, delimiter='\t', lineterminator='\n').writerows(out)
