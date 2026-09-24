"""P13-07 stage 2: train per cohort, test on every cohort (N x N), AUC + 200-resample bootstrap CI."""
import numpy as np, json, sys, warnings; warnings.filterwarnings("ignore")
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from scipy.stats import rankdata
kind,tl=sys.argv[1],sys.argv[2]; rng=np.random.default_rng(0)
P=np.load("results/prep.npz"); info=json.load(open("results/prep_info.json")); cids=info["info"]["cohorts"]
def auc(y,p):
    r=rankdata(p); n1=y.sum(); n0=len(y)-n1; return (r[y==1].sum()-n1*(n1+1)/2)/(n1*n0)
def auc_ci(y,p,B=200):
    a=auc(y,p); bs=[]
    for _ in range(B):
        i=rng.integers(0,len(y),len(y)); yy=y[i]
        if 0<yy.sum()<len(yy): bs.append(auc(yy,p[i]))
    return float(a),float(np.quantile(bs,.025)),float(np.quantile(bs,.975))
def fit(X,y):
    if kind=="lr":
        s=StandardScaler().fit(X); m=LogisticRegression(C=0.1,max_iter=300).fit(s.transform(X),y); return lambda Z:m.predict_proba(s.transform(Z))[:,1]
    m=HistGradientBoostingClassifier(max_iter=150,random_state=0).fit(X,y); return lambda Z:m.predict_proba(Z)[:,1]
res=[]
for c in cids:
    y=P[f"{tl}_{c}"]; idx=np.where(y>=0)[0]; rng.shuffle(idx); h=len(idx)//2; tr,te=idx[:h],idx[h:]
    pr=fit(P[f"F_{c}"][tr],y[tr])
    for d in cids:
        for el in ["L1","L2"]:
            if d==c and el!=tl: continue
            if d==c: Xt,yt=P[f"F_{c}"][te],y[te]
            else:
                yd=P[f"{el}_{d}"]; m=yd>=0; Xt,yt=P[f"F_{d}"][m],yd[m]
            if 0<yt.sum()<len(yt):
                a,l,u=auc_ci(yt,pr(Xt)); res.append(dict(model=kind,train=c,train_label=tl,test=d,test_label=el,auc=a,lo=l,hi=u))
json.dump(res,open(f"results/tr_{kind}_{tl}.json","w"),indent=1); print(kind,tl,len(res))
