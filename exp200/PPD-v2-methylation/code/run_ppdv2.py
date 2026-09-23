import json, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
rng=np.random.default_rng(20260924)
Z=np.load('/tmp/ppdv2_beta.npz',allow_pickle=True); B=Z['beta']; probes=Z['probes']
meta=json.load(open('/tmp/ppdv2_meta.json')); y=np.array(meta['ppd']); batch=np.array(meta['batch'])
base_probes=set(json.load(open('/tmp/ppdv2_baseline_probes.json')))
M=np.log2(np.clip(B,1e-4,1-1e-4)/np.clip(1-B,1e-4,1-1e-4))  # M-values
def welch_t(X,y):
    X1=X[:,y==1]; X0=X[:,y==0]
    m1,m0=X1.mean(1),X0.mean(1); v1,v0=X1.var(1,ddof=1),X0.var(1,ddof=1)
    return np.abs((m1-m0)/np.sqrt(v1/X1.shape[1]+v0/X0.shape[1]+1e-12))
def fit_predict(Xtr,ytr,Xte,seed=0):
    t=welch_t(Xtr,ytr); idx=np.argsort(t)[-200:]
    sc=StandardScaler().fit(Xtr[idx].T)
    clf=LogisticRegression(penalty='elasticnet',solver='saga',l1_ratio=0.5,C=1.0,tol=1e-2,max_iter=2000,random_state=seed)
    clf.fit(sc.transform(Xtr[idx].T),ytr)
    return clf.predict_proba(sc.transform(Xte[idx].T))[:,1]
def cv_auc(X,y,groups,seed=0):
    gkf=GroupKFold(5); preds=np.zeros(len(y))
    for tr,te in gkf.split(X.T,y,groups):
        preds[te]=fit_predict(X[:,tr],y[tr],X[:,te],seed)
    return roc_auc_score(y,preds),preds
obs,preds=cv_auc(M,y,batch)
nulls=[]
for i in range(200):
    yp=rng.permutation(y)
    a,_=cv_auc(M,yp,batch,i)
    nulls.append(a)
nulls=np.array(nulls)
# G2 held-out batch 5
tr=batch!='5'; te=batch=='5'
p5=fit_predict(M[:,tr],y[tr],M[:,te])
g2=roc_auc_score(y[te],p5)
boot=[roc_auc_score(y[te][b],p5[b]) for b in (rng.integers(0,te.sum(),te.sum()) for _ in range(2000)) if len(set(y[te][b]))>1]
# G2c baseline: mean z(M) of HP1BP3/TTC9B probes, sign oriented on train
bp=[i for i,p in enumerate(probes) if p in base_probes]
tr_z=(M[bp][:,tr]-M[bp][:,tr].mean(1,keepdims=True))/ (M[bp][:,tr].std(1,keepdims=True)+1e-9)
te_z=(M[bp][:,te]-M[bp][:,tr].mean(1,keepdims=True))/ (M[bp][:,tr].std(1,keepdims=True)+1e-9)
s_tr=tr_z.mean(0); 
if roc_auc_score(y[tr],s_tr)<0.5: sgn=-1
else: sgn=1
s_te=sgn*te_z.mean(0)
g2c=roc_auc_score(y[te],s_te)
# panel genes for mechanism check
t=welch_t(M[:,tr],y[tr]); top=np.argsort(t)[-200:]
res={'g1_cv_auroc':float(obs),'perm_max':float(nulls.max()),'perm_n':200,'pass_g1':bool(obs>=0.70 and obs>nulls.max()),
     'g2_batch5_auroc':float(g2),'g2_boot_ci':[float(np.percentile(boot,2.5)),float(np.percentile(boot,97.5))],
     'g2c_baseline_auroc':float(g2c),'panel_minus_baseline':float(g2-g2c),
     'n_baseline_probes':len(bp),'batch5_counts':[int(y[te].sum()),int(te.sum())],
     'top200_probes_train':probes[top].tolist()}
json.dump(res,open('results/run1.json','w'),indent=1)
print(json.dumps({k:v for k,v in res.items() if k!='top200_probes_train'},indent=1))
