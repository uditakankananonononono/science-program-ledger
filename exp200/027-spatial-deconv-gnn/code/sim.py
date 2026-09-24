import numpy as np, json
BASE='/home/sandbox/ledger/exp200/022-cross-tissue-embedding/results/local'
OUT='results/local'
KEEP=['B cell','T cell','dendritic cell','endothelial cell','leukocyte','macrophage','monocyte',
      'natural killer cell','stromal cell','type II pneumocyte']
rng_split=np.random.default_rng(3)
X=np.load(f'{BASE}/Lung_X.npy', mmap_mode='r')
y=np.load(f'{BASE}/Lung_y.npy', allow_pickle=True)
keep_mask=np.isin(y, KEEP)
idx_all=np.where(keep_mask)[0]
y_k=y[keep_mask]
# stratified 50/50 split: halfA (signature+DEV), halfB (FROZEN)
halfA, halfB = [], []
for t in KEEP:
    ti=idx_all[y_k==t]; rng_split.shuffle(ti)
    h=len(ti)//2; halfA+=ti[:h].tolist(); halfB+=ti[h:].tolist()
halfA=np.array(sorted(halfA)); halfB=np.array(sorted(halfB))
print('halfA', len(halfA), 'halfB', len(halfB))
# signature + HVG on halfA only (log1p normalized per cell to 1e4)
Xa=np.asarray(X[halfA], dtype=np.float32)
lib=Xa.sum(1, keepdims=True); lib[lib==0]=1
Xa_log=np.log1p(Xa/lib*1e4)
genes=np.load(f'{BASE}/genes.npy', allow_pickle=True)
hv=Xa_log.var(0).argsort()[::-1][:2000]; hv=np.sort(hv)
ya=y[halfA]
sig=np.stack([Xa_log[ya==t][:,hv].mean(0) for t in KEEP]).astype(np.float32)  # 10 x 2000
np.save(f'{OUT}/hvg.npy', hv); np.save(f'{OUT}/sig.npy', sig)
json.dump({'halfA': halfA.tolist(), 'halfB': halfB.tolist(), 'keep_types': KEEP,
           'seed_split':3}, open(f'{OUT}/split.json','w'))
print('sig', sig.shape, 'hvg', hv[:5])
