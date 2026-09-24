import numpy as np, json
from scipy.spatial import cKDTree
SECS=['m09','m10','m11','m12','m13','m14','m15s1','m15s2','m16s1','m16s2','m16s3']
TUMOR={'m09':'m09','m10':'m10','m11':'m11','m12':'m12','m13':'m13','m14':'m14',
       'm15s1':'m15','m15s2':'m15','m16s1':'m16','m16s2':'m16','m16s3':'m16'}
sec={}
for s in SECS:
    d=np.load(f'results/local/{s}.npz')
    zc=(d['chol']-d['chol'].mean())/d['chol'].std()
    zd=(d['cd8']-d['cd8'].mean())/d['cd8'].std()
    C=np.stack([d['row'],d['col']],1).astype(np.float64)
    _,idx=cKDTree(C).query(C,7)
    wzd=zd[idx[:,1:]].mean(1)  # row-standardized W @ z_d
    ib=float((zc*wzd).mean())  # bivariate Moran's I (standardized inputs)
    sec[s]=round(ib,4)
tum={}
for t in ['m09','m10','m11','m12','m13','m14','m15','m16']:
    tum[t]=round(float(np.median([sec[s] for s in SECS if TUMOR[s]==t])),4)
order=sorted(tum, key=lambda t:-tum[t])
ranks={t:i+1 for i,t in enumerate(order)}
res={'per_section':sec,'per_tumor':tum,'ranks':ranks,
     'G2_P1_perfect_sep': bool(ranks['m15']<=2 and ranks['m16']<=2)}
json.dump(res, open('results/p1_scores.json','w'), indent=1)
print(json.dumps(res, indent=1))
