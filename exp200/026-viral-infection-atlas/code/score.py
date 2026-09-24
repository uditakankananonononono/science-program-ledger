import numpy as np, pandas as pd, json, glob, urllib.request
from scipy.sparse import load_npz, vstack
from sklearn.decomposition import NMF
from sklearn.metrics import roc_auc_score
chunks=sorted(glob.glob('results/local/chunks/chunk_*.npz'), key=lambda p:int(p.split('_')[-1].split('.')[0]))
X=vstack([load_npz(p) for p in chunks]).tocsr()
genes=np.load('results/local/genes.npy', allow_pickle=True)
obs=pd.read_csv('results/local/sel.csv')
gidx={str(g).upper():i for i,g in enumerate(genes)}
# Hallmark ISG sets from Enrichr GMT
url='https://maayanlab.cloud/Enrichr/geneSetLibrary?mode=text&libraryName=MSigDB_Hallmark_2020'
txt=urllib.request.urlopen(url, timeout=60).read().decode()
isg=set()
for line in txt.splitlines():
    f=line.split('\t')
    if f[0] in ('Interferon Alpha Response','Interferon Gamma Response'):
        isg|={g.upper() for g in f[2:] if g}
isg_present=sorted(isg & set(gidx))
print('ISG genes in set', len(isg), 'present', len(isg_present), flush=True)
def colmean(idx):
    return np.asarray(X[:, idx].mean(1)).ravel()
isg_cols=[gidx[g] for g in isg_present]
base_score=colmean(isg_cols)
def auroc_by_ct(score, mask, cts=None, dis=None):
    mask=np.asarray(mask)
    out={}
    if cts is None: cts=obs['cell_type'].values
    if dis is None: dis=obs['disease'].values
    for ct in sorted(set(cts[mask])):
        m=mask & (cts==ct)
        y=(dis[m]!='normal').astype(int)
        if y.sum()<20 or (1-y).sum()<20: continue
        out[ct]=float(roc_auc_score(y, np.asarray(score)[m]))
    return out
dev=obs['disease'].isin(['COVID-19','normal']).values
frz=obs['disease'].isin(['influenza','normal']).values
base_dev=auroc_by_ct(base_score, dev)
base_frz=auroc_by_ct(base_score, frz)
print('baseline dev', {k:round(v,3) for k,v in base_dev.items()}, flush=True)
print('baseline frz', {k:round(v,3) for k,v in base_frz.items()}, flush=True)
# topic: NMF on dev, HVG-3000
Xd=X[dev]
v=np.asarray(Xd.power(2).mean(0))-np.asarray(Xd.mean(0))**2
hv=np.argsort(-v.ravel())[:3000]
nmf=NMF(n_components=10, init='nndsvda', random_state=7, max_iter=300)
W=nmf.fit_transform(Xd[:, hv])
H=nmf.components_
dev_obs=obs[dev].reset_index(drop=True)
best=None
for k in range(10):
    a=auroc_by_ct(W[:,k], np.ones(len(dev_obs), bool), dev_obs['cell_type'].values, dev_obs['disease'].values)
    m=np.mean(list(a.values()))
    if best is None or m>best[1]: best=(k,m,a)
k=best[0]
top50=[hv[i] for i in np.argsort(-H[k])[:50]]
prog_genes=sorted({str(genes[i]).upper() for i in top50})
topic_score=colmean(top50)
topic_dev=auroc_by_ct(topic_score, dev)
topic_frz=auroc_by_ct(topic_score, frz)
print('topic dev', {k2:round(v,3) for k2,v in topic_dev.items()}, flush=True)
print('topic frz', {k2:round(v,3) for k2,v in topic_frz.items()}, flush=True)
mb=lambda d: float(np.mean(list(d.values())))
res={'isg_set_size':len(isg),'isg_present':len(isg_present),
     'baseline':{'dev':base_dev,'frozen':base_frz,'dev_mean':mb(base_dev),'frozen_mean':mb(base_frz)},
     'topic':{'dev':topic_dev,'frozen':topic_frz,'dev_mean':mb(topic_dev),'frozen_mean':mb(topic_frz),
              'nmf_component':int(k),'top50_genes':prog_genes}}
json.dump(res, open('results/scores.json','w'), indent=1)
print('MEANS dev base', round(mb(base_dev),4), 'topic', round(mb(topic_dev),4),
      '| frz base', round(mb(base_frz),4), 'topic', round(mb(topic_frz),4))
