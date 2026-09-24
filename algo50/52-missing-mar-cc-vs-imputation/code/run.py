import numpy as np, json
rng=np.random.default_rng(1); n=500; R=2000
res={k:[[],[]] for k in ['CC','MEANIMP','REGIMP','IPW']}; miss=[]
for _ in range(R):
    x=rng.standard_normal(n); y=1+0.8*x+rng.normal(0,0.6,n)
    m=rng.random(n)<1/(1+np.exp(-(-0.5+1.5*x))); o=~m; miss.append(m.mean())
    yc=y[o]; res['CC'][0].append(yc.mean()); res['CC'][1].append(yc.std(ddof=1))
    ym=y.copy(); ym[m]=yc.mean(); res['MEANIMP'][0].append(ym.mean()); res['MEANIMP'][1].append(ym.std(ddof=1))
    B=np.polyfit(x[o],yc,1); yr=y.copy(); yr[m]=np.polyval(B,x[m]); res['REGIMP'][0].append(yr.mean()); res['REGIMP'][1].append(yr.std(ddof=1))
    X=np.c_[np.ones(n),x]; w=np.zeros(2); t=o.astype(float)
    for _ in range(25):
        p=1/(1+np.exp(-X@w)); H=X.T@(X*(p*(1-p))[:,None]); w+=np.linalg.solve(H,X.T@(t-p))
    p=1/(1+np.exp(-X@w)); wt=1/p[o]; mu=(wt*yc).sum()/wt.sum()
    res['IPW'][0].append(mu); res['IPW'][1].append(np.sqrt((wt*(yc-mu)**2).sum()/wt.sum()))
out={'missing_frac':float(np.mean(miss))}
for k,(a,s) in res.items(): out[k]={'mean_bias':float(np.mean(a)-1),'mean_SD':float(np.mean(s))}
json.dump(out,open('results/results.json','w'),indent=1); print(json.dumps(out,indent=1))
