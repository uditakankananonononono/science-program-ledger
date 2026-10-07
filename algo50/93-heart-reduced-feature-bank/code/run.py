import numpy as np, pandas as pd, json, warnings
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
warnings.filterwarnings('ignore')
cols='age sex cp trestbps chol fbs restecg thalach exang oldpeak slope ca thal num'.split(); F=cols[:-1]
def ld(s):
    d=pd.read_csv(f'data/processed.{s}.data',header=None,names=cols,na_values='?').astype(float)
    d.loc[d.chol==0,'chol']=np.nan; d.loc[d.trestbps==0,'trestbps']=np.nan; return d
tr=ld('cleveland'); sites={s:ld(s) for s in ('hungarian','switzerland','va')}
Xtr=tr[F].values; ytr=(tr.num.values>0).astype(int)
class LR:
    def fit(s,a,b): s.sc=StandardScaler().fit(a); s.m=LogisticRegression(C=1,max_iter=1000).fit(s.sc.transform(a),b); return s
    def p(s,a): return s.m.predict_proba(s.sc.transform(a))[:,1]
def B1(a,b,c):
    med=np.nanmedian(a,0); a2=np.where(np.isnan(a),med,a); c2=np.where(np.isnan(c),med,c)
    return RandomForestClassifier(300,random_state=0).fit(a2,b).predict_proba(c2)[:,1]
def B2(a,b,c):
    im=IterativeImputer(max_iter=10,random_state=0).fit(a); return LR().fit(im.transform(a),b).p(im.transform(c))
cvs={}
for n,f in (('B1',B1),('B2',B2)):
    p=np.zeros(len(ytr))
    for a,b in StratifiedKFold(5,shuffle=True,random_state=0).split(Xtr,ytr): p[b]=f(Xtr[a],ytr[a],Xtr[b])
    cvs[n]=roc_auc_score(ytr,p)
print('CV',cvs,flush=True); head=max(cvs,key=cvs.get); fb={'B1':B1,'B2':B2}[head]
cache={}
def rfb_one(x):
    O=tuple(np.where(~np.isnan(x))[0])
    if len(O)<3: return ytr.mean()
    if O not in cache:
        k=~np.isnan(Xtr[:,list(O)]).any(1)
        if k.sum()<60 or len(set(ytr[k]))<2: cache[O]=None
        else:
            a=Xtr[k][:,list(O)]; b=ytr[k]
            cache[O]=(LR().fit(a,b),RandomForestClassifier(200,max_depth=4,random_state=0).fit(a,b))
    m=cache[O]
    if m is None: return ytr.mean()
    z=x[list(O)][None]; return 0.5*m[0].p(z)[0]+0.5*m[1].predict_proba(z)[0,1]
# equivalence on Cleveland rows with complete features
full=~np.isnan(Xtr).any(1); a=Xtr[full]; b=ytr[full]; m1=LR().fit(a,b); m2=RandomForestClassifier(200,max_depth=4,random_state=0).fit(a,b)
ref=0.5*m1.p(a[:20])+0.5*m2.predict_proba(a[:20])[:,1]
got=np.array([rfb_one(r) for r in a[:20]]); assert np.allclose(ref,got)
Xs=np.vstack([s[F].values for s in sites.values()]); ys=np.concatenate([(s.num.values>0).astype(int) for s in sites.values()]); sid=np.concatenate([[n]*len(s) for n,s in sites.items()])
pB=fb(Xtr,ytr,Xs); pR=np.array([rfb_one(r) for r in Xs])
rs=np.random.RandomState(7); ds=[]
for _ in range(10000):
    i=rs.randint(0,len(ys),len(ys))
    if len(set(ys[i]))<2: continue
    ds.append(roc_auc_score(ys[i],pR[i])-roc_auc_score(ys[i],pB[i]))
lo,hi=np.percentile(ds,[2.5,97.5]); d=roc_auc_score(ys,pR)-roc_auc_score(ys,pB)
v='WIN' if d>=.02 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
per={s:dict(n=int((sid==s).sum()),pos=int(ys[sid==s].sum()),auc_base=float(roc_auc_score(ys[sid==s],pB[sid==s])),auc_rfb=float(roc_auc_score(ys[sid==s],pR[sid==s]))) for s in sites}
out=dict(cv=cvs,headline=head,auc_base=roc_auc_score(ys,pB),auc_rfb=roc_auc_score(ys,pR),diff=d,ci=[lo,hi],verdict=v,per_site=per,n_patterns=len(cache))
json.dump(out,open('results.json','w'),indent=1,default=float); print(json.dumps(out,default=float))
