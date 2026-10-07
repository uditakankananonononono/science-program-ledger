import numpy as np, pandas as pd, json, warnings
from scipy.optimize import nnls
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold
warnings.filterwarnings('ignore')
F=['benefitsReview','sideEffectsReview','commentsReview']
d=pd.concat([pd.read_csv(f'data/drugLib{s}_raw.tsv',sep='\t',index_col=0) for s in ('Train','Test')]).fillna('').reset_index(drop=True)
y=d.rating.values.astype(float); cat=(d[F[0]]+' . '+d[F[1]]+' . '+d[F[2]]).values
vec=lambda:TfidfVectorizer(ngram_range=(1,2),min_df=2,sublinear_tf=True)
def cvfit(T,yy):
    kf=list(KFold(3,shuffle=True,random_state=0).split(T)); best=None
    # cache vectorizer per fold
    V=[]
    for i,j in kf:
        v=vec().fit(T[i]); V.append((v.transform(T[i]),v.transform(T[j]),i,j))
    for a in (0.3,1,3,10):
        p=np.zeros(len(yy))
        for Xi,Xj,i,j in V: p[j]=Ridge(alpha=a).fit(Xi,yy[i]).predict(Xj)
        r=np.sqrt(np.mean((p-yy)**2))
        if best is None or r<best[0]: best=(r,a,p)
    return best
def sparse_fit(v,Xt,yy,a,keep_n=2000):
    m=Ridge(alpha=a).fit(Xt,yy); keep=np.argsort(-np.abs(m.coef_))[:keep_n]; return keep,Ridge(alpha=a).fit(Xt[:,keep],yy)
def run(tr,te,fraction=1.0):
    ytr=y[tr]; yte=y[te]
    if fraction<1: tr=tr[:int(fraction*len(tr))]; ytr=y[tr]
    r=lambda p:float(np.sqrt(np.mean((p-yte)**2)))
    out={}
    # B
    _,a,_=cvfit(cat[tr],ytr); v=vec().fit(cat[tr]); out['B']=r(Ridge(alpha=a).fit(v.transform(cat[tr]),ytr).predict(v.transform(cat[te])))
    # A2
    Xt=v.transform(cat[tr]); keep,m2=sparse_fit(v,Xt,ytr,a); out['A2']=r(m2.predict(v.transform(cat[te])[:,keep]))
    # per-field
    oof=[];sp=[];ns=[]
    for f in F:
        T=d[f].values; rr,af,p=cvfit(T[tr],ytr); oof.append(p); vf=vec().fit(T[tr]); Xf=vf.transform(T[tr])
        keep,mf=sparse_fit(vf,Xf,ytr,af); mfull=Ridge(alpha=af).fit(Xf,ytr)
        sp.append(mf.predict(vf.transform(T[te])[:,keep])); ns.append(mfull.predict(vf.transform(T[te])))
    O=np.column_stack(oof); mu=O.mean(0); ym=ytr.mean(); w,_=nnls(O-mu,ytr-ym)
    out['ASL']=r((np.column_stack(sp)-mu)@w+ym); out['A1']=r((np.column_stack(ns)-mu)@w+ym)
    return out
res={}
for s in range(101,111):
    rs=np.random.RandomState(s); p=rs.permutation(len(y)); n=int(.75*len(y)); res[s]=run(p[:n],p[n:]); print(s,{k:round(v,4) for k,v in res[s].items()},flush=True)
R=pd.DataFrame(res).T; dB=(R.B-R.ASL).values; rs=np.random.RandomState(7); bs=[dB[rs.randint(0,10,10)].mean() for _ in range(10000)]
lo,hi=np.percentile(bs,[2.5,97.5]); wins=int((dB>0).sum())
v='ROBUST' if dB.mean()>=.05 and lo>0 and wins>=8 else ('NOT ROBUST' if hi<.05 or wins<6 else 'MIXED')
out=dict(mean_rmse=R.mean().to_dict(),diff_B_minus_ASL=float(dB.mean()),ci=[float(lo),float(hi)],wins=wins,verdict=v,
 abl={'B-A1':float((R.B-R.A1).mean()),'B-A2':float((R.B-R.A2).mean()),'A1-ASL':float((R.A1-R.ASL).mean())})
rs0=np.random.RandomState(101); p=rs0.permutation(len(y)); n=int(.75*len(y)); out['boundary']={str(f):run(p[:n],p[n:],f) for f in (0.1,0.25,0.5)}
json.dump(out,open('results_robust.json','w'),indent=1,default=float); print(json.dumps(out,default=float))
