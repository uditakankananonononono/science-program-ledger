import numpy as np, json
from sklearn.metrics import silhouette_score
rng=np.random.default_rng(79)
def sim(L,fst):
    pa=rng.uniform(0.1,0.5,L)
    a=(1-fst)/fst
    X=[]
    for pop in range(3):
        pi=rng.beta(a*pa,a*(1-pa))
        pi=np.clip(pi,0.001,0.999)
        X.append(rng.binomial(2,pi,size=(60,L)))
    X=np.concatenate(X)
    p=X.mean(axis=0)/2
    p=np.clip(p,0.01,0.99)
    Z=(X-2*p)/np.sqrt(2*p*(1-p))
    U,S,Vt=np.linalg.svd(Z,full_matrices=False)
    PC=U[:,:3]*S[:3]
    labels=np.repeat([0,1,2],60)
    sil=float(silhouette_score(PC[:,:2],labels))
    vr=float(S[0]**2/S[2]**2)
    return sil,vr
res={}
for fst in (0.01,0.05,0.15):
    for L in (200,1000,5000):
        sil,vr=sim(L,fst)
        res[f'f{fst}_L{L}']=dict(silhouette=sil,var_ratio=vr)
        print(fst,L,res[f'f{fst}_L{L}'],flush=True)
json.dump(res,open('results/results.json','w'),indent=1)
print('G1',res['f0.05_L5000']['silhouette']>=0.5)
print('G2',res['f0.01_L200']['silhouette']<0.3)
print('G3',res['f0.05_L200']['silhouette']<=res['f0.05_L1000']['silhouette']<=res['f0.05_L5000']['silhouette'])
print('G4',res['f0.15_L5000']['var_ratio']>2)
