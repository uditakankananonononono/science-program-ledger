import json,gzip,numpy as np,pickle
d=json.load(gzip.open('data/disprot.json.gz','rt'))['data']
AA="ACDEFGHIKLMNPQRSTVWY"; out=[]
for e in d:
    s=e['sequence']
    if not s or len(s)>3000 or set(s)-set(AA): continue
    y=np.zeros(len(s),np.int8)
    for r in (e.get('disprot_consensus') or {}).get('Structural state',[]):
        if r['type']=='D': y[r['start']-1:r['end']]=1
    out.append(dict(acc=e['acc'],seq=s,y=y,tax=e.get('ncbi_taxon_id'),u50=e.get('uniref50') or e['acc']))
rng=np.random.default_rng(7); cl=sorted(set(x['u50'] for x in out)); rng.shuffle(cl)
nt=int(0.7*len(cl)); tr=set(cl[:nt]); tune=set(cl[:int(0.2*nt)])
for x in out: x['split']='tune' if x['u50'] in tune else ('train' if x['u50'] in tr else 'test')
pickle.dump(out,open('data/set.pkl','wb'))
from collections import Counter
print(len(out),Counter(x['split'] for x in out),'disorder frac',np.mean(np.concatenate([x['y'] for x in out])))
