import csv,json
from pathlib import Path
p=Path('scratchpad/PXD025523')
j=json.loads((p/'files.json').read_text())
raw=sorted(x['fileName'] for x in j if x['fileName'].lower().endswith('.raw'))
human=[f for f in raw if '_ARCV_fr' in f]
assert len(raw)==58 and len(human)==46 and len(set(human))==46
assert [int(f.rsplit('_fr',1)[1].split('.',1)[0]) for f in human]==list(range(1,47))
(p/'human_raw_selected.json').write_text(json.dumps(human,indent=2)+'\n')
channels=[('Ctrl1','TMT126','normal',1),('Ctrl2','TMT127N','normal',2),('Ctrl3','TMT127C','normal',3),('ARVC1','TMT128N','arrhythmogenic right ventricular cardiomyopathy',1),('ARVC2','TMT128C','arrhythmogenic right ventricular cardiomyopathy',2),('ARVC3','TMT129N','arrhythmogenic right ventricular cardiomyopathy',3),('ARVC4','TMT129C','arrhythmogenic right ventricular cardiomyopathy',4),('ARVC5','TMT131C','arrhythmogenic right ventricular cardiomyopathy',5)]
head=['source name','files','label','technical replicate','characteristics[organism]','characteristics[organism part]','characteristics[cell type]','characteristics[biological replicate]','characteristics[disease]','characteristics[age]','characteristics[sex]','characteristics[ancestry category]','characteristics[individual]','factor value[disease]']
with (p/'human_samples.tsv').open('w',newline='') as out:
 w=csv.writer(out,delimiter='\t',lineterminator='\n');w.writerow(head)
 for name,label,disease,rep in channels:
  w.writerow([name,','.join(human),label,'1','Homo sapiens','heart','not applicable',str(rep),disease,'not available','not available','not available',name,disease])
tech=[('comment[sdrf version]','v1.1.0'),('comment[sdrf annotation tool]','manual curation'),('comment[proteomics data acquisition method]','NT=Data-dependent acquisition;AC=PRIDE:0000627'),('comment[instrument]','NT=Orbitrap Exploris 480;AC=MS:1003028'),('comment[cleavage agent details]','NT=Lys-C;AC=MS:1001309|NT=Trypsin;AC=MS:1001251'),('comment[dissociation method]','NT=beam-type collision-induced dissociation;AC=MS:1000422'),('comment[collision energy]','30 NCE'),('comment[precursor mass tolerance]','not available'),('comment[fragment mass tolerance]','not available')]
with (p/'human_technical.tsv').open('w',newline='') as out:
 w=csv.writer(out,delimiter='\t',lineterminator='\n');w.writerow(['column','value']);w.writerows(tech)
