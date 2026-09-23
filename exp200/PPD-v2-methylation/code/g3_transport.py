import json,gzip,numpy as np
from sklearn.metrics import roc_auc_score
P=json.load(open('results/panel_full.json'))
want={P['probes'][i]:(P['coef'][i],P['mean'][i],P['scale'][i]) for i in range(len(P['probes'])) if abs(P['coef'][i])>1e-6}
b2g=json.load(open('/tmp/gse201287_map.json'))
gsm=[];dis=[]
with gzip.open('data/GSE201287_series_matrix.txt.gz','rt',errors='replace') as f:
    for line in f:
        if line.startswith('!Sample_geo_accession'): gsm=[x.strip().strip('"') for x in line.split('\t')[1:]]
        elif 'disease state' in line: dis=[x.strip().strip('"').split(':')[1].strip() for x in line.split('\t')[1:]]
ylabel={g:(1 if d=='Major depressive disorder' else 0) for g,d in zip(gsm,dis)}
rows={}; cols=None
with gzip.open('data/GSE201287_matrix_norm.txt.gz','rt',errors='replace') as f:
    for line in f:
        if line.startswith('TargetID'):
            hdr=line.rstrip('\n').split('\t')
            cols=[(j,h.split('.')[0]) for j,h in enumerate(hdr) if h.endswith('.AVG_Beta')]
            continue
        if cols is None or line.startswith('['): continue
        pid=line.split('\t',1)[0]
        if pid in want:
            parts=line.rstrip('\n').split('\t')
            rows[pid]=parts
gsms=[b2g[b] for _,b in cols if b in b2g]
y=np.array([ylabel[g] for g in gsms])
sc=np.zeros(len(gsms)); used=0
for pid,(c,m,s) in want.items():
    if pid not in rows: continue
    raw=[rows[pid][j] for j,b in cols if b in b2g]
    if any(x in ('','NA') for x in raw): continue
    v=np.array([float(x) for x in raw])
    b=np.clip(v,1e-4,1-1e-4); mv=np.log2(b/(1-b))
    sc+=c*(mv-m)/s; used+=1
auc=roc_auc_score(y,sc)
rng=np.random.default_rng(3)
boot=[]
for _ in range(2000):
    bi=rng.integers(0,len(y),len(y))
    if len(set(y[bi]))>1: boot.append(roc_auc_score(y[bi],sc[bi]))
out={'cohort':'GSE201287 MDD blood 450K (GenomeStudio AVG_Beta, control-normalized)','n':int(len(y)),'n_mdd':int(y.sum()),
 'probes_used':used,'transport_auroc':float(auc),'boot_ci':[float(np.percentile(boot,2.5)),float(np.percentile(boot,97.5))]}
json.dump(out,open('results/g3_transport.json','w'),indent=1)
print(json.dumps(out,indent=1))
