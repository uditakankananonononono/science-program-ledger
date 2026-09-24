import pandas as pd, numpy as np, json
from collections import Counter
rng=np.random.default_rng(7)
tissues=['Marrow','Lung','Heart','Spleen']
ann=pd.read_csv('results/local/annotations_FACS.csv')
ann=ann[ann['tissue'].isin(tissues)]
ann=ann[ann['cell_ontology_class'].notna() & (ann['cell_ontology_class']!='')]
# gene column pass -> common genes
genes=None
for t in tissues:
    g=pd.read_csv(f'results/local/{t}-counts.csv', usecols=[0]).iloc[:,0]
    g=pd.unique(g)
    genes=set(g) if genes is None else genes & set(g)
gc=sorted(genes); print('shared genes', len(gc), flush=True)
out={}
for t in tissues:
    a=ann[ann['tissue']==t].set_index('cell')
    hdr=pd.read_csv(f'results/local/{t}-counts.csv', nrows=0).columns.tolist()
    cells=[c for c in hdr[1:] if c in a.index]
    if len(cells)>3000:
        idx=np.sort(rng.choice(len(cells),3000,replace=False))
        cells=[cells[i] for i in idx]
    labs=a.loc[cells,'cell_ontology_class'].values
    keep={'Unnamed: 0'}|set(cells)
    dt={c: np.float32 for c in cells}
    chunks=[]
    for ch in pd.read_csv(f'results/local/{t}-counts.csv', index_col=0,
                          usecols=lambda c: c in keep, dtype=dt, chunksize=2000):
        chunks.append(ch)
    df=pd.concat(chunks)
    df=df[~df.index.duplicated()].reindex(gc).fillna(0)
    X=df[cells].values.T.astype(np.float32)
    del chunks, df
    np.save(f'results/local/{t}_X.npy', X)
    np.save(f'results/local/{t}_y.npy', labs)
    np.save(f'results/local/{t}_cells.npy', np.array(cells))
    out[t]=(None,labs,cells)
    del X
    print(t,'-> saved', flush=True)
np.save('results/local/genes.npy', np.array(gc))
import os
if os.path.exists('results/local/tabula_muris.npz'): os.remove('results/local/tabula_muris.npz')
ok={}
for t in tissues:
    for k,v in Counter(out[t][1]).items():
        if v>=30: ok.setdefault(k,[]).append(t)
classes=sorted([k for k,v in ok.items() if len(v)>=2])
json.dump(classes, open('results/class_list.json','w'), indent=1)
json.dump({'dev':['Marrow','Lung','Heart'],'frozen':['Spleen'],'seed':7,'cap':3000,
           'n_shared_genes':len(gc)}, open('results/split.json','w'), indent=1)
print('classes',len(classes),classes, flush=True)
for t in tissues:
    c=Counter(out[t][1]); print(t,{k:c[k] for k in classes if c.get(k)}, flush=True)
