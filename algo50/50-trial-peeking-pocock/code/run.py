import numpy as np, json
from scipy.stats import norm
rng=np.random.default_rng(1); R=5000; K=10; b=20; out={}
for name,d in [('null',0.0),('alt',0.3)]:
    a=rng.standard_normal((R,K*b)); c=rng.standard_normal((R,K*b))+d
    ns=np.arange(1,K+1)*b
    diff=np.stack([c[:,:n].mean(1)-a[:,:n].mean(1) for n in ns],1)
    p=2*norm.sf(np.abs(diff/np.sqrt(2/ns)))
    naive=(p<0.05).any(1); poc=(p<0.0106).any(1); fixed=p[:,-1]<0.05
    first=np.where(poc,np.argmax(p<0.0106,1),K-1); 
    out[name]={'FIXED':float(fixed.mean()),'NAIVE':float(naive.mean()),'POCOCK':float(poc.mean()),'POCOCK_mean_n_per_arm':float(((first+1)*b).mean())}
json.dump(out,open('results/results.json','w'),indent=1); print(json.dumps(out,indent=1))
