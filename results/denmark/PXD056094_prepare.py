import csv
import json
from pathlib import Path
p = Path('scratchpad/PXD056094')
files = sorted(x['fileName'] for x in json.loads((p/'files.json').read_text()) if x['fileName'].lower().endswith('.raw'))
assert len(files) == 28 and len(set(files)) == 28
hf = [f for f in files if f.startswith(('AE1045_', 'AE1060_'))]
hfx = [f for f in files if f not in hf]
assert len(hf) == 3 and len(hfx) == 25
head = ['source name','files','label','technical replicate','characteristics[organism]','characteristics[organism part]','characteristics[cell type]','characteristics[biological replicate]','characteristics[disease]']
for tag, selected, instrument in [('hf',hf,'NT=Q Exactive HF;AC=MS:1002523'),('hfx',hfx,'NT=Q Exactive HF-X;AC=MS:1002877')]:
 (p/f'{tag}_raw_selected.json').write_text(json.dumps(selected,indent=2)+'\n')
 with (p/f'{tag}_samples.tsv').open('w',newline='') as out:
  w=csv.writer(out,delimiter='\t',lineterminator='\n');w.writerow(head)
  for f in selected:
   stem=f.rsplit('.',1)[0]
   w.writerow([stem,f,'label free sample','1','not applicable','not applicable','not applicable','1','not applicable'])
 tech=[
 ('comment[sdrf version]','v1.1.0'),
 ('comment[sdrf annotation tool]','manual curation'),
 ('comment[proteomics data acquisition method]','NT=Data-dependent acquisition;AC=PRIDE:0000627'),
 ('comment[instrument]',instrument),
 ('comment[cleavage agent details]','NT=Lys-C;AC=MS:1001309|NT=Trypsin;AC=MS:1001251'),
 ('comment[dissociation method]','NT=beam-type collision-induced dissociation;AC=MS:1000422'),
 ('comment[precursor mass tolerance]','4.5 ppm'),
 ('comment[fragment mass tolerance]','20 ppm'),
 ('comment[modification parameters]','NT=Carbamidomethyl;AC=UNIMOD:4;TA=C;MT=Fixed|NT=Oxidation;AC=UNIMOD:35;TA=M;MT=Variable|NT=Deamidated;AC=UNIMOD:7;TA=N,Q;MT=Variable|NT=Gln->pyro-Glu;AC=UNIMOD:28;TA=Q;PP=Peptide N-term;MT=Variable|NT=Glu->pyro-Glu;AC=UNIMOD:27;TA=E;PP=Peptide N-term;MT=Variable'),
 ]
 if tag == 'hf':
  tech[-1] = (tech[-1][0], tech[-1][1] + '|NT=Oxidation;AC=UNIMOD:35;TA=P;MT=Variable')
 with (p/f'{tag}_technical.tsv').open('w',newline='') as out:
  w=csv.writer(out,delimiter='\t',lineterminator='\n');w.writerow(['column','value']);w.writerows(tech)
