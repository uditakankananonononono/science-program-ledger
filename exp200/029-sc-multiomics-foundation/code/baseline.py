import numpy as np, json
from sklearn.linear_model import Ridge
L='results/local'
Xtr=np.load(f'{L}/Xtr.npy'); Ytr=np.load(f'{L}/Ytr.npy')
Xte=np.load(f'{L}/Xte.npy'); Yte=np.load(f'{L}/Yte.npy')
Xfz=np.load(f'{L}/Xfz.npy'); Yfz=np.load(f'{L}/Yfz.npy')
m=Ridge(alpha=1.0).fit(Xtr, Ytr)
def score(X, Y):
    P=m.predict(X)
    rs=[float(np.corrcoef(P[:,i],Y[:,i])[0,1]) for i in range(Y.shape[1])]
    return {'per_protein_r':[round(r,4) for r in rs], 'mean_r':round(float(np.mean(rs)),4)}
res={'dev_test':score(Xte,Yte),'frozen':score(Xfz,Yfz)}
json.dump(res, open('results/ridge_scores.json','w'), indent=1)
print(json.dumps(res))
