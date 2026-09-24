import numpy as np, json
rng=np.random.default_rng(1); R=2000; r=0.1; t=np.arange(30); X=np.c_[np.ones(30),t]; out={}
for c0 in [2,50]:
    L=[]; P=[]
    for _ in range(R):
        C=rng.poisson(c0*np.exp(r*t)); L.append(np.polyfit(t,np.log(C+1),1)[0])
        w=np.array([np.log(max(C.mean(),0.5)) - r*14.5*0, 0.0])
        w=np.linalg.lstsq(X,np.log(C+0.5),rcond=None)[0]
        for _ in range(50):
            mu=np.exp(X@w); w+=np.linalg.solve(X.T@(X*mu[:,None]),X.T@(C-mu))
        P.append(w[1])
    L=np.array(L); P=np.array(P)
    out[f'c0={c0}']={'LOGLIN_bias':float(L.mean()-r),'LOGLIN_rmse':float(np.sqrt(((L-r)**2).mean())),'POISGLM_bias':float(P.mean()-r),'POISGLM_rmse':float(np.sqrt(((P-r)**2).mean()))}
json.dump(out,open('results/results.json','w'),indent=1); print(json.dumps(out,indent=1))
