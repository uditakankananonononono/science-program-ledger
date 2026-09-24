import numpy as np, json
from scipy.stats import norm
rng=np.random.default_rng(1); m=1000; k=100; R=500
def bh(p,q=0.05):
    o=np.argsort(p); s=p[o]; ok=np.nonzero(s<=q*np.arange(1,m+1)/m)[0]
    r=np.zeros(m,bool)
    if len(ok): r[o[:ok[-1]+1]]=True
    return r
out={}
for rho in [0.0,0.5]:
    acc={x:[[],[]] for x in ['UNC','BONF','BH']}
    for _ in range(R):
        z=np.sqrt(rho)*rng.standard_normal()+np.sqrt(1-rho)*rng.standard_normal(m)
        z[:k]+=3.0; p=norm.sf(z); truth=np.arange(m)<k
        for name,rej in [('UNC',p<0.05),('BONF',p<0.05/m),('BH',bh(p))]:
            acc[name][0].append((rej&~truth).sum()/max(1,rej.sum())); acc[name][1].append((rej&truth).sum()/k)
    out[f'rho={rho}']={n:{'FDR':float(np.mean(a[0])),'power':float(np.mean(a[1]))} for n,a in acc.items()}
json.dump(out,open('results/results.json','w'),indent=1); print(json.dumps(out,indent=1))
