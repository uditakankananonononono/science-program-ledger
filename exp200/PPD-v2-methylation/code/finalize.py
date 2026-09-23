import json,numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
rng=np.random.default_rng(7)
Z=np.load('/tmp/ppdv2_beta.npz',allow_pickle=True); B=Z['beta']; probes=Z['probes']
meta=json.load(open('/tmp/ppdv2_meta.json')); y=np.array(meta['ppd']); batch=np.array(meta['batch'])
base_probes=set(json.load(open('/tmp/ppdv2_baseline_probes.json')))
M=np.log2(np.clip(B,1e-4,1-1e-4)/np.clip(1-B,1e-4,1-1e-4))
def welch_t(X,y):
    X1=X[:,y==1];X0=X[:,y==0]
    return np.abs((X1.mean(1)-X0.mean(1))/np.sqrt(X1.var(1,ddof=1)/X1.shape[1]+X0.var(1,ddof=1)/X0.shape[1]+1e-12))
def fit_predict(Xtr,ytr,Xte,seed=0):
    idx=np.argsort(welch_t(Xtr,ytr))[-200:]
    sc=StandardScaler().fit(Xtr[idx].T)
    clf=LogisticRegression(penalty='elasticnet',solver='saga',l1_ratio=0.5,C=1.0,tol=1e-2,max_iter=1000,random_state=seed)
    clf.fit(sc.transform(Xtr[idx].T),ytr); return clf.predict_proba(sc.transform(Xte[idx].T))[:,1],probes[np.argsort(welch_t(Xtr,ytr))[-200:]].tolist()
p1=json.load(open('/tmp/perms_0_100.json'));p2=json.load(open('/tmp/perms_100_200.json'))
obs=p1.pop('obs'); nulls=np.array(list(p1.values())+list(p2.values()))
tr=batch!='5'; te=batch=='5'
p5,top=fit_predict(M[:,tr],y[tr],M[:,te])
g2=roc_auc_score(y[te],p5)
boot=[]
for _ in range(2000):
    b=rng.integers(0,int(te.sum()),int(te.sum()))
    if len(set(y[te][b]))>1: boot.append(roc_auc_score(y[te][b],p5[b]))
bp=[i for i,p in enumerate(probes) if p in base_probes]
mu=M[bp][:,tr].mean(1,keepdims=True); sd=M[bp][:,tr].std(1,keepdims=True)+1e-9
s_tr=((M[bp][:,tr]-mu)/sd).mean(0); s_te=((M[bp][:,te]-mu)/sd).mean(0)
sgn=-1 if roc_auc_score(y[tr],s_tr)<0.5 else 1
g2c=roc_auc_score(y[te],sgn*s_te)
res={'g1_cv_auroc':float(obs),'perm_max':float(nulls.max()),'perm_n':200,
 'pass_g1':bool(obs>=0.70 and obs>nulls.max()),
 'g2_batch5_auroc':float(g2),'g2_boot_ci':[float(np.percentile(boot,2.5)),float(np.percentile(boot,97.5))],
 'pass_g2':bool(g2>=0.65 and np.percentile(boot,2.5)>0.5),
 'g2c_baseline_auroc':float(g2c),'panel_minus_baseline':float(g2-g2c),
 'n_baseline_probes':len(bp),'batch5_counts':[int(y[te].sum()),int(te.sum())],
 'top200_probes_train':top}
json.dump(res,open('results/run1.json','w'),indent=1)
print(json.dumps({k:v for k,v in res.items() if k!='top200_probes_train'},indent=1))
