import json,numpy as np
d=json.load(open('data/set.json')); F=np.array([x['fam'] for x in d]); n=len(F)
W=np.zeros((n,n),np.float32)
for i in range(n):
    r=np.load(f'results/sw_rows/{i}.npy'); W[i,i:]=r; W[i:,i]=r
s=np.diag(W).copy(); Wn=W/np.minimum.outer(s,s); np.fill_diagonal(Wn,-np.inf)
tw=np.load('results/bestid.npy')<40
sw_acc=(F[Wn.argmax(1)]==F).mean(); sw_tw=(F[Wn.argmax(1)]==F)[tw].mean()
K=[1,2,3,5,10,20,30,50,100,200]; out={'sw_acc':float(sw_acc),'sw_tw':float(sw_tw),'k':K,'methods':{}}
for m in ['K3','MH3','RA-C4','RA-SP']:
    M=np.load(f'results/sim_{m}.npy').astype(np.float64); np.fill_diagonal(M,-np.inf)
    rng=np.random.default_rng(0); M=M+rng.uniform(0,1e-9,M.shape)  # deterministic tie-break
    order=np.argsort(-M,1); r={'acc':[],'acc_tw':[],'recall':[]}
    for k in K:
        cand=order[:,:k]; best=cand[np.arange(n),np.take_along_axis(Wn,cand,1).argmax(1)]
        c=F[best]==F; hit=(F[cand]==F[:,None]).any(1)
        r['acc'].append(float(c.mean())); r['acc_tw'].append(float(c[tw].mean())); r['recall'].append(float(hit.mean()))
    out['methods'][m]=r
json.dump(out,open('results/cascade.json','w'),indent=1)
print('SW',round(sw_acc,4),'tw',round(sw_tw,4))
for m,r in out['methods'].items():
    print(m); [print(f'  k={k:3d} acc={a:.3f} tw={t:.3f} recall={c:.3f}') for k,a,t,c in zip(K,r['acc'],r['acc_tw'],r['recall'])]
