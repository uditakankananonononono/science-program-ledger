import numpy as np, json
from scipy.optimize import nnls
OUT='results/local'
sig=np.load(f'{OUT}/sig.npy')  # 10 x 2000, log1p space
res={}
for which in ['dev','frozen']:
    S=np.load(f'{OUT}/spots_{which}.npy')  # 2000 x 2000 log1p
    P=np.load(f'{OUT}/props_{which}.npy')  # 2000 x 10
    pred=np.zeros((len(S),10), np.float32)
    for i in range(len(S)):
        w,_=nnls(sig.T, S[i])
        s=w.sum()
        pred[i]= w/s if s>0 else np.full(10, 0.1)
    rs=[]
    for t in range(10):
        a,b=pred[:,t], P[:,t]
        if a.std()>1e-8 and b.std()>1e-8:
            rs.append(float(np.corrcoef(a,b)[0,1]))
        else:
            rs.append(float('nan'))
    res[which]={'per_type_r': [round(r,4) for r in rs], 'mean_r': round(float(np.nanmean(rs)),4)}
    np.save(f'{OUT}/nnls_pred_{which}.npy', pred)
json.dump(res, open('results/nnls_scores.json','w'), indent=1)
print(json.dumps(res))
