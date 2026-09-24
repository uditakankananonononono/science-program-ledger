import numpy as np, json, hashlib, sys, glob
sys.path.insert(0,'code')
from flows import cluster_flow, score
import scvelo as scv, scanpy as sc
p=glob.glob('results/local/data/DentateGyrus/*.h5ad')+glob.glob('results/local/data/**/*.h5ad', recursive=True)
p=[x for x in p if 'entate' in x or 'dentate' in x][0]
h=hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]
ad=sc.read_h5ad(p)
edges=json.load(open('results/canonical_edges_frozen.json'))
scv.pp.filter_and_normalize(ad, min_shared_counts=20)
Xl=ad.X.toarray() if hasattr(ad.X,'toarray') else np.asarray(ad.X)
hv=np.argsort(-Xl.var(0))[:2000]
ad=ad[:,sorted(hv)].copy(); del Xl
scv.pp.moments(ad, n_pcs=30, n_neighbors=30)
scv.tl.velocity(ad, mode='stochastic'); scv.tl.velocity_graph(ad)
T=ad.uns['velocity_graph'].toarray().astype(np.float32)
labels=ad.obs['clusters'].values
res=score(cluster_flow(T, labels), edges); res['sha256_16']=h; res['file']=p
json.dump(res, open('results/baseline_frozen.json','w'), indent=1)
np.save('results/local/velocity_frozen.npy', ad.layers['velocity'].astype(np.float32))
np.save('results/local/X_hvg_frozen.npy', (ad.X.toarray() if hasattr(ad.X,'toarray') else ad.X).astype(np.float32))
np.save('results/local/labels_frozen.npy', labels)
np.save('results/local/velocity_graph_T_frozen.npy', T)
print('baseline frozen:', res['recovered'],'/',res['total'],'wrong',res['wrong'], flush=True)
for k,v in res['detail'].items(): print(f"  {k}: net {v['net']:+.6f} {'OK' if v['recovered'] else 'MISS'}")
