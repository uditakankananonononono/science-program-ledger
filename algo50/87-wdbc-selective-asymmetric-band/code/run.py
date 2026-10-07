import numpy as np, json, sys
from scipy.stats import beta
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
rows=[l.strip().split(',') for l in open('data/wdbc.data')]
y=np.array([1 if r[1]=='M' else 0 for r in rows]); X=np.array([[float(v) for v in r[2:]] for r in rows])
def split(r):
    rs=np.random.RandomState(r); tr=[];ca=[];te=[]
    for c in (0,1):
        idx=rs.permutation(np.where(y==c)[0]); n=len(idx); a=int(.6*n); b=int(.8*n)
        tr+=list(idx[:a]);ca+=list(idx[a:b]);te+=list(idx[b:])
    return map(np.array,(tr,ca,te))
def cp(k,n,conf=.9):
    return 1.0 if n==0 else (1.0 if k==n else beta.ppf(conf,k+1,n-k))
def ok(s,yy,lo,hi,d):
    ab=s<=lo; am=s>=hi
    nb=ab.sum(); nm=am.sum()
    miss=((yy==1)&ab).sum(); fa=((yy==0)&am).sum()
    return cp(miss,nb)<=d and cp(fa,nm)<=d, (nb+nm)/len(s)
def fit_rcab(s,yy,d):
    q=np.unique(np.concatenate([[0],s,[1]])); best=(-1,0.0,1.0)
    los=q[q<=.5]; his=q[q>=.5]
    for lo in los:
        for hi in his:
            if lo>=hi: continue
            g,c=ok(s,yy,lo,hi,d)
            if g and c>best[0]: best=(c,lo,hi)
    return best[1],best[2]
def fit_chow(s,yy,d):
    best=(-1,0.0,1.0)
    for tau in np.unique(np.maximum(s,1-s)):
        if tau<.5: continue
        g,c=ok(s,yy,1-tau,tau,d)
        if g and c>best[0]: best=(c,1-tau,tau)
    return best[1],best[2]
def evalte(s,yy,lo,hi):
    ab=s<=lo; am=s>=hi; acc=ab|am; nb=ab.sum()
    return acc.mean(), (((yy==1)&ab).sum()/nb if nb else 0.0)
out={}
for d in (0.10,0.20):
    D=[];C0=[];C1=[];viol=[0,0];miss=[[],[]]
    for r in range(100):
        tr,ca,te=split(r); sc=StandardScaler().fit(X[tr])
        m=LogisticRegression(C=1.0,max_iter=2000).fit(sc.transform(X[tr]),y[tr])
        s=lambda i:m.predict_proba(sc.transform(X[i]))[:,1]
        sc_,st=s(ca),s(te)
        lo0,hi0=fit_chow(sc_,y[ca],d)
        # equivalence: RCAB restricted to symmetric must equal chow
        sym=[(c,1-t,t) for t in np.unique(np.maximum(sc_,1-sc_)) if t>=.5 for g,c in [ok(sc_,y[ca],1-t,t,d)] if g]
        if sym: assert abs(max(sym)[0]-ok(sc_,y[ca],lo0,hi0,d)[1])<1e-12
        lo1,hi1=fit_rcab(sc_,y[ca],d)
        c0,m0=evalte(st,y[te],lo0,hi0); c1,m1=evalte(st,y[te],lo1,hi1)
        D.append(c1-c0);C0.append(c0);C1.append(c1); miss[0].append(m0); miss[1].append(m1)
        viol[0]+=m0>d; viol[1]+=m1>d
    D=np.array(D); rs=np.random.RandomState(7)
    bs=[D[rs.randint(0,100,100)].mean() for _ in range(10000)]
    lo,hi=np.percentile(bs,[2.5,97.5]); v1=viol[1]/100
    verdict='WIN' if (D.mean()>=.02 and lo>0 and v1<=.15) else ('NEGATIVE' if hi<0 else 'NULL')
    out[str(d)]=dict(cov_chow=float(np.mean(C0)),cov_rcab=float(np.mean(C1)),mean_diff=D.mean(),ci=[lo,hi],pos=int((D>0).sum()),neg=int((D<0).sum()),zero=int((D==0).sum()),
      viol_chow=viol[0]/100,viol_rcab=v1,mean_miss_chow=float(np.mean(miss[0])),mean_miss_rcab=float(np.mean(miss[1])),verdict=verdict)
json.dump(out,open('results_v2.json','w'),indent=1); print(json.dumps(out,indent=1))
