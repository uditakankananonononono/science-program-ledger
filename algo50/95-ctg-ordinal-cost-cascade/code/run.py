import numpy as np, pandas as pd, json, warnings
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupKFold
from sklearn.metrics import f1_score, recall_score
warnings.filterwarnings('ignore')
F='LB AC FM UC ASTV MSTV ALTV MLTV DL DS DP Width Min Max Nmax Nzeros Mode Mean Median Variance Tendency'.split()
d=pd.read_excel('data/CTG.xls',sheet_name='Raw Data').dropna(subset=['NSP']).reset_index(drop=True)
X=d[F].values.astype(float); y=(d.NSP.values-1).astype(int); g=d.FileName.values
C=np.array([[0,1,2],[3,0,1],[10,4,0]],float)
cost=lambda yt,yp:C[yt,yp].mean()
assert cost(y,y)==0 and abs(cost(y,np.zeros_like(y))-sum(C[k,0]*(y==k).mean() for k in range(3)))<1e-12
u=np.array(sorted(set(g))); perm=np.random.RandomState(0).permutation(len(u)); te_g=set(u[perm[:int(.3*len(u))]])
te=np.array([x in te_g for x in g]); Xtr,ytr,gtr,Xte,yte,gte=X[~te],y[~te],g[~te],X[te],y[te],g[te]
print('train',len(ytr),np.bincount(ytr),'test',len(yte),np.bincount(yte),flush=True)
gkf=list(GroupKFold(5).split(Xtr,ytr,gtr))
bayes=lambda P:np.argmin(P@C,1)
def oof(make,proba=True):
    P=np.zeros((len(ytr),3))
    for a,b in gkf:
        m=make().fit(Xtr[a],ytr[a]); P[b]=m.predict_proba(Xtr[b])
    return P
mk_rf=lambda:RandomForestClassifier(500,random_state=0,n_jobs=2)
class LRs:
    def __init__(s,C):s.C=C
    def fit(s,a,b): s.sc=StandardScaler().fit(a); s.m=LogisticRegression(C=s.C,max_iter=1000).fit(s.sc.transform(a),b); return s
    def predict_proba(s,a): return s.m.predict_proba(s.sc.transform(a))
cv={}; Prf=oof(mk_rf); cv['B1']=cost(ytr,Prf.argmax(1)); cv['B2']=cost(ytr,bayes(Prf))
best_lr=None
for c in (.1,1,10):
    P=oof(lambda:LRs(c)); s=cost(ytr,bayes(P))
    if best_lr is None or s<best_lr[0]: best_lr=(s,c)
cv['B3']=best_lr[0]; print('baseline CV',cv,best_lr,flush=True); head=min(cv,key=cv.get)
# OCC
class OCC:
    def __init__(s,depth): s.dp=depth
    def fit(s,a,b):
        mk=lambda:HistGradientBoostingClassifier(max_depth=s.dp,learning_rate=.1,max_iter=200,random_state=0)
        s.m1=mk().fit(a,(b>=1).astype(int)); k=b>=1; s.m2=mk().fit(a[k],(b[k]==2).astype(int)); return s
    def pp(s,a): p1=s.m1.predict_proba(a)[:,1]; p2=s.m2.predict_proba(a)[:,1]; return p1,p1*p2
def occ_pred(p1,p12,t1,t2): return np.where(p12>=t2,2,np.where(p1>=t1,1,0))
grid=np.arange(.05,.951,.05); bestO=None
for dp in (3,None):
    P1=np.zeros(len(ytr));P12=np.zeros(len(ytr))
    for a,b in gkf:
        m=OCC(dp).fit(Xtr[a],ytr[a]); P1[b],P12[b]=m.pp(Xtr[b])
    for t1 in grid:
        for t2 in grid:
            s=cost(ytr,occ_pred(P1,P12,t1,t2))
            if bestO is None or s<bestO[0]-1e-12: bestO=(s,dp,t1,t2)
print('OCC CV',bestO,flush=True)
_,dp,t1,t2=bestO; m=OCC(dp).fit(Xtr,ytr); p1,p12=m.pp(Xte); pO=occ_pred(p1,p12,t1,t2)
if head=='B1': pB=mk_rf().fit(Xtr,ytr).predict(Xte)
elif head=='B2': pB=bayes(mk_rf().fit(Xtr,ytr).predict_proba(Xte))
else: pB=bayes(LRs(best_lr[1]).fit(Xtr,ytr).predict_proba(Xte))
rec=sorted(set(gte)); rs=np.random.RandomState(7); ds=[]
ix={r:np.where(gte==r)[0] for r in rec}
for _ in range(10000):
    idx=np.concatenate([ix[r] for r in rs.choice(rec,len(rec))]); ds.append(cost(yte[idx],pO[idx])-cost(yte[idx],pB[idx]))
lo,hi=np.percentile(ds,[2.5,97.5]); dd=cost(yte,pO)-cost(yte,pB)
v='WIN' if dd<=-.03 and hi<0 else ('NEGATIVE' if lo>0 else 'NULL')
out=dict(headline=head,cv=cv,occ_cv=list(map(lambda z:None if z is None else float(z),bestO)),cost_base=cost(yte,pB),cost_occ=cost(yte,pO),diff=dd,ci=[lo,hi],verdict=v,
 f1_base=f1_score(yte,pB,average='macro'),f1_occ=f1_score(yte,pO,average='macro'),recall_base=list(map(float,recall_score(yte,pB,average=None))),recall_occ=list(map(float,recall_score(yte,pO,average=None))),
 cost_allcosts={'B1':cost(yte,mk_rf().fit(Xtr,ytr).predict(Xte))})
json.dump(out,open('results.json','w'),indent=1,default=float); print(json.dumps(out,default=float))
