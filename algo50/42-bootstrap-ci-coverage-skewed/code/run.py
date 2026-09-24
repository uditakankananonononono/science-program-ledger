import numpy as np, json
from scipy.stats import t as tdist
rng=np.random.default_rng(1); true=np.exp(0.5); R=2000; B=999; out={}
for n in [15,100]:
    cT=cP=0; wT=[]; wP=[]
    for _ in range(R):
        x=rng.lognormal(0,1,n); m=x.mean(); h=tdist.ppf(0.975,n-1)*x.std(ddof=1)/np.sqrt(n)
        cT+=(m-h<=true<=m+h); wT.append(2*h)
        bm=x[rng.integers(0,n,(B,n))].mean(1); lo,hi=np.percentile(bm,[2.5,97.5])
        cP+=(lo<=true<=hi); wP.append(hi-lo)
    out[f'n={n}']={'T_cov':cT/R,'PCT_cov':cP/R,'T_width':float(np.mean(wT)),'PCT_width':float(np.mean(wP))}
json.dump(out,open('results/results.json','w'),indent=1); print(json.dumps(out,indent=1))
