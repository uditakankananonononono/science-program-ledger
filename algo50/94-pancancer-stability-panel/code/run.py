import numpy as np, pandas as pd, json, warnings
from sklearn.feature_selection import f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import f1_score
warnings.filterwarnings('ignore')
D='data/TCGA-PANCAN-HiSeq-801x20531/'
X=np.log2(pd.read_csv(D+'data.csv',index_col=0).values.astype(np.float32)+1); lab=pd.read_csv(D+'labels.csv',index_col=0).Class.values
cls=sorted(set(lab)); y=np.array([cls.index(c) for c in lab])
def l1fit(A,b,C):
    sc=StandardScaler().fit(A); m=LogisticRegression(penalty='l1',solver='liblinear',C=C).fit(sc.transform(A),b); return m.coef_
def prefilter(A,b): F=np.nan_to_num(f_classif(A,b)[0]); return np.argsort(-F)[:500],F
def sel_b1(A,b):
    idx,_=prefilter(A,b); Z=A[:,idx]
    for C in np.geomspace(1e-3,1,30):
        w=l1fit(Z,b,C)
        if (np.abs(w).max(0)>0).sum()>=10: return idx[np.argsort(-np.abs(w).max(0))[:10]],C
    return idx[np.argsort(-np.abs(w).max(0))[:10]],C
def sel_b2(A,b): _,F=prefilter(A,b); return np.argsort(-F)[:10]
def sel_ssp(A,b,seed=0,nsub=50,C=0.05):
    idx,F=prefilter(A,b); Z=A[:,idx]; cnt=np.zeros(len(idx)); rs=np.random.RandomState(seed)
    sss=StratifiedShuffleSplit(n_splits=nsub,train_size=.5,random_state=seed)
    for s,_ in sss.split(Z,b): cnt+=(np.abs(l1fit(Z[s],b[s],C)).max(0)>0)
    o=np.lexsort((-F[idx],-cnt)); return idx[o[:10]]
def fitpred(A,b,T,genes):
    sc=StandardScaler().fit(A[:,genes]); m=LogisticRegression(C=1,max_iter=2000).fit(sc.transform(A[:,genes]),b); return m.predict(sc.transform(T[:,genes]))
res=[]
for seed in range(1,21):
    tr,te=next(StratifiedShuffleSplit(1,test_size=.3,random_state=seed).split(X,y)); A,b,T,u=X[tr],y[tr],X[te],y[te]
    g1,C1=sel_b1(A,b); g2=sel_b2(A,b); g3=sel_ssp(A,b,seed)
    if seed==1:
        idx,_=prefilter(A,b); w=l1fit(A[:,idx],b,C1); assert set(idx[np.argsort(-np.abs(w).max(0))[:10]])==set(g1)
        sw=sel_ssp.__defaults__  # sanity: defaults present
    r=[]
    for g in (g1,g2,g3):
        p=fitpred(A,b,T,g); r+= [float((p==u).mean()),float(f1_score(u,p,average='macro'))]
    res.append(r); print(seed,[round(x,4) for x in r],flush=True)
R=np.array(res); out={}
rs=np.random.RandomState(7)
for name,j in (('SSP-B1',0),('SSP-B2',2)):
    d=R[:,4]-R[:,j]; bs=[d[rs.randint(0,20,20)].mean() for _ in range(10000)]; lo,hi=np.percentile(bs,[2.5,97.5])
    out[name]=dict(diff=float(d.mean()),ci=[float(lo),float(hi)],wins=int((d>0).sum()),losses=int((d<0).sum()))
win=all(out[k]['diff']>=.01 and out[k]['ci'][0]>0 for k in out); neg=any(out[k]['ci'][1]<0 for k in out)
out.update(acc_b1=float(R[:,0].mean()),acc_b2=float(R[:,2].mean()),acc_ssp=float(R[:,4].mean()),f1_b1=float(R[:,1].mean()),f1_b2=float(R[:,3].mean()),f1_ssp=float(R[:,5].mean()),verdict='WIN' if win else ('NEGATIVE' if neg else 'NULL'))
json.dump(out,open('results.json','w'),indent=1); print(json.dumps(out))
