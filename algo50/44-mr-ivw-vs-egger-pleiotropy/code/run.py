import numpy as np, json
rng=np.random.default_rng(1); J=30; R=1000; b=0.3; out={}
for sc in ['NONE','DIR']:
    ivw=[]; eg=[]
    for _ in range(R):
        bx=rng.uniform(0.05,0.2,J); a=np.zeros(J) if sc=='NONE' else rng.uniform(0,0.04,J)
        bxh=bx+rng.normal(0,0.01,J); byh=b*bx+a+rng.normal(0,0.02,J)
        s=np.sign(bxh); bxh*=s; byh*=s
        ivw.append((bxh*byh).sum()/(bxh**2).sum())
        X=np.c_[np.ones(J),bxh]; eg.append(np.linalg.lstsq(X,byh,rcond=None)[0][1])
    ivw=np.array(ivw); eg=np.array(eg)
    out[sc]={'IVW_bias':float(ivw.mean()-b),'IVW_sd':float(ivw.std()),'EGGER_bias':float(eg.mean()-b),'EGGER_sd':float(eg.std())}
json.dump(out,open('results/results.json','w'),indent=1); print(json.dumps(out,indent=1))
