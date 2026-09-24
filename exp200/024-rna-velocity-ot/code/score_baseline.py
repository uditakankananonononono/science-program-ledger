import numpy as np, json, hashlib, sys
import scvelo as scv, scanpy as sc
sys.path.insert(0,'code')
from flows import cluster_flow, score
p='results/local/data/Pancreas/endocrinogenesis_day15.h5ad'
h=hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]
print('sha256_16', h, flush=True)
ad=sc.read_h5ad(p)
edges=json.load(open('results/canonical_edges.json'))
scv.pp.filter_and_normalize(ad, min_shared_counts=20)
import numpy as _np
Xl=ad.X.toarray() if hasattr(ad.X,'toarray') else _np.asarray(ad.X)
hv=_np.argsort(-Xl.var(0))[:2000]
ad=ad[:,sorted(hv)].copy()
del Xl
scv.pp.moments(ad, n_pcs=30, n_neighbors=30)
scv.tl.velocity(ad, mode='stochastic')
scv.tl.velocity_graph(ad)
T=ad.uns['velocity_graph'].toarray().astype(np.float32)  # rows=source, cols=target (pi_ij=cos(x_j-x_i, v_i), scvelo docs)
labels=ad.obs['clusters'].values
F=cluster_flow(T, labels)
res=score(F, edges)
res['sha256_16']=h
json.dump(res, open('results/baseline_dev.json','w'), indent=1)
np.save('results/local/velocity.npy', ad.layers['velocity'].astype(np.float32))
np.save('results/local/X_hvg.npy', ad.X.toarray().astype(np.float32) if hasattr(ad.X,'toarray') else ad.X.astype(np.float32))
np.save('results/local/hvg_genes.npy', ad.var_names.values)
np.save('results/local/labels.npy', labels)
print('baseline dev:', res['recovered'],'/',res['total'],'wrong',res['wrong'])
print(json.dumps(res['detail'], indent=1))
