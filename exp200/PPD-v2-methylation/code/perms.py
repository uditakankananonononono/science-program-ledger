import json,sys,numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
a,b=int(sys.argv[1]),int(sys.argv[2])
rng=np.random.default_rng(20260924)
Z=np.load('/tmp/ppdv2_beta.npz',allow_pickle=True); B=Z['beta']
meta=json.load(open('/tmp/ppdv2_meta.json')); y=np.array(meta['ppd']); batch=np.array(meta['batch'])
M=np.log2(np.clip(B,1e-4,1-1e-4)/np.clip(1-B,1e-4,1-1e-4))
def welch_t(X,y):
    X1=X[:,y==1];X0=X[:,y==0]
    return np.abs((X1.mean(1)-X0.mean(1))/np.sqrt(X1.var(1,ddof=1)/X1.shape[1]+X0.var(1,ddof=1)/X0.shape[1]+1e-12))
def fit_predict(Xtr,ytr,Xte,seed=0):
    idx=np.argsort(welch_t(Xtr,ytr))[-200:]
    sc=StandardScaler().fit(Xtr[idx].T)
    clf=LogisticRegression(penalty='elasticnet',solver='saga',l1_ratio=0.5,C=1.0,tol=1e-2,max_iter=1000,random_state=seed)
    clf.fit(sc.transform(Xtr[idx].T),ytr); return clf.predict_proba(sc.transform(Xte[idx].T))[:,1]
def cv_auc(X,y,groups,seed=0):
    preds=np.zeros(len(y))
    for tr,te in GroupKFold(5).split(X.T,y,groups): preds[te]=fit_predict(X[:,tr],y[tr],X[:,te],seed)
    return roc_auc_score(y,preds)
out={}
if a==0:
    out['obs']=cv_auc(M,y,batch)
for i in range(a,b):
    out[f'perm_{i}']=cv_auc(M,rng.permutation(y),batch,i)
json.dump(out,open(f'/tmp/perms_{a}_{b}.json','w'))
print('done',a,b)
