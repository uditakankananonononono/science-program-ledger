import numpy as np, pandas as pd, json, warnings
from scipy.optimize import nnls
from scipy.stats import spearmanr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold
F=['benefitsReview','sideEffectsReview','commentsReview']
tr=pd.read_csv('data/drugLibTrain_raw.tsv',sep='\t',index_col=0).fillna('')
te=pd.read_csv('data/drugLibTest_raw.tsv',sep='\t',index_col=0).fillna('')
ytr=tr.rating.values.astype(float); yte=te.rating.values.astype(float)
kf=list(KFold(5,shuffle=True,random_state=0).split(tr))
def vec(): return TfidfVectorizer(ngram_range=(1,2),min_df=2,sublinear_tf=True)
def cvalpha(texts,y):
    best=None
    for a in (0.3,1,3,10):
        p=np.zeros(len(y))
        for i,j in kf:
            v=vec().fit(texts[i]); m=Ridge(alpha=a).fit(v.transform(texts[i]),y[i]); p[j]=m.predict(v.transform(texts[j]))
        r=np.sqrt(np.mean((p-y)**2))
        if best is None or r<best[0]: best=(r,a,p)
    return best
cat=lambda d:(d[F[0]]+' . '+d[F[1]]+' . '+d[F[2]]).values
rB,aB,pB=cvalpha(cat(tr),ytr)
# equivalence: ASL degenerate (one field=concat, no sparsity, trivial combiner) == B
r2,a2,_=cvalpha(cat(tr),ytr); assert (r2,a2)==(rB,aB)
vB=vec().fit(cat(tr)); mB=Ridge(alpha=aB).fit(vB.transform(cat(tr)),ytr); predB=mB.predict(vB.transform(cat(te)))
# ASL
oof=[];models=[]
for f in F:
    r,a,p=cvalpha(tr[f].values,ytr); oof.append(p)
    v=vec().fit(tr[f].values); Xt=v.transform(tr[f].values); m=Ridge(alpha=a).fit(Xt,ytr)
    keep=np.argsort(-np.abs(m.coef_))[:2000]
    m2=Ridge(alpha=a).fit(Xt[:,keep],ytr)
    models.append((v,keep,m2))
O=np.column_stack(oof); mu=O.mean(0); ym=ytr.mean()
w,_=nnls(O-mu,ytr-ym)
P=np.column_stack([m2.predict(v.transform(te[f].values)[:,keep]) for f,(v,keep,m2) in zip(F,models)])
predA=(P-mu)@w+ym
rs=np.random.RandomState(7); n=len(yte)
e=lambda p:(p-yte)**2
rm=lambda p:np.sqrt(np.mean(e(p)))
d=[]
for _ in range(10000):
    i=rs.randint(0,n,n); d.append(np.sqrt(e(predB)[i].mean())-np.sqrt(e(predA)[i].mean()))
lo,hi=np.percentile(d,[2.5,97.5]); diff=rm(predB)-rm(predA)
v='WIN' if diff>=.05 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
out=dict(rmse_base=rm(predB),rmse_asl=rm(predA),rmse_const=float(np.sqrt(np.mean((yte-ytr.mean())**2))),diff=diff,ci=[lo,hi],
 mae_base=float(np.mean(abs(predB-yte))),mae_asl=float(np.mean(abs(predA-yte))),sp_base=spearmanr(predB,yte)[0],sp_asl=spearmanr(predA,yte)[0],
 weights=list(w),alpha_base=aB,verdict=v)
json.dump(out,open('results.json','w'),indent=1,default=float); print(json.dumps(out,indent=1,default=float))
