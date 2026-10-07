import json, numpy as np, pandas as pd, hashlib, warnings
from epiweeks import Week
warnings.filterwarnings('ignore')
assert hashlib.sha256(open('data.json','rb').read()).hexdigest()=='3101cac5e7dae360f18489d9ddf39969d6e672de769a9c3365079f139f07e806'
e=pd.DataFrame(json.load(open('data.json'))['epidata'])[['epiweek','wili']]; e['ew']=e.epiweek.astype(int)
e['yr']=e.ew//100; e['wk']=e.ew%100
e['season']=np.where(e.wk>=40,e.yr,e.yr-1); e['pos']=np.where(e.wk>=40,e.wk-40,e.wk+13)  # approx week-of-season (wk 53 handled by +13)
e=e[(e.wk>=40)|(e.wk<=20)].sort_values('ew').reset_index(drop=True); e['y']=np.log(e.wili)
S={s:g.sort_values('pos').reset_index(drop=True) for s,g in e.groupby('season')}
H=(1,2,3,4)
def windows(seasons,W):
    X=[];P=[];D=[]
    for s in seasons:
        g=S[s]; y=g.y.values; p=g.pos.values
        for t in range(W-1,len(g)-4):
            if p[t]-p[t-W+1]!=W-1: continue
            X.append(y[t-W+1:t+1]); P.append(p[t]); D.append([y[t+h]-y[t] if t+h<len(g) and p[t+h]-p[t]==h else np.nan for h in H])
    return np.array(X),np.array(P),np.array(D)
def ara_fc(lib,W,k,lam,x,p):
    X,P,D=lib; d=np.sqrt(((X-x)**2).sum(1))+lam*np.abs(P-p); out=[]
    for j,h in enumerate(H):
        ok=~np.isnan(D[:,j]); idx=np.where(ok)[0][np.argsort(d[ok])[:k]]; w=1/(d[idx]+1e-3); out.append(x[-1]+(w*D[idx,j]).sum()/w.sum())
    return np.array(out)
# synthetic equivalence: library of one window -> persistence + its delta
Xs=np.array([[0.,1.,2.]]); Ps=np.array([5.]); Ds=np.array([[0.1,0.2,0.3,0.4]])
assert np.allclose(ara_fc((Xs,Ps,Ds),3,1,0.05,np.array([1.,1.5,2.5]),5),2.5+np.array([0.1,0.2,0.3,0.4]))
def ar_fit(seasons):
    M={}
    for j,h in enumerate(H):
        A=[];b=[]
        for s in seasons:
            g=S[s]; y=g.y.values; p=g.pos.values
            for t in range(2,len(g)-h):
                if p[t]-p[t-2]!=2 or p[t+h]-p[t]!=h: continue
                dm=np.zeros(36); dm[min(p[t],35)]=1; A.append(np.concatenate([[y[t],y[t-1],y[t-2]],dm])); b.append(y[t+h])
        M[h]=np.linalg.lstsq(np.array(A),np.array(b),rcond=1e-8)[0]
    return M
def origins(seasons,cut=None):
    o=[]
    for s in seasons:
        g=S[s]
        for t in range(6,len(g)-1):
            if cut and g.ew[t]>cut: continue
            o.append((s,t))
    return o
def evaluate(libseasons,testseasons,W,k,cut=None):
    lib=windows(libseasons,W); M=ar_fit(libseasons); rows=[]
    for s,t in origins(testseasons,cut):
        g=S[s]; y=g.y.values; p=g.pos.values
        if p[t]-p[t-W+1]!=W-1 or p[t]-p[t-2]!=2: continue
        fa=ara_fc(lib,W,k,0.05,y[t-W+1:t+1],p[t]); dm=np.zeros(36); dm[min(p[t],35)]=1; feat=np.concatenate([[y[t],y[t-1],y[t-2]],dm])
        for j,h in enumerate(H):
            if t+h>=len(g) or p[t+h]-p[t]!=h: continue
            if cut and g.ew[t+h]>cut: continue
            yt=y[t+h]; rows.append((s,t,h,abs(y[t]-yt),abs(feat@M[h]-yt),abs(fa[j]-yt)))
    return pd.DataFrame(rows,columns=['s','t','h','e0','e1','ea'])
val=evaluate(list(range(1997,2010)),list(range(2010,2015)),4,5)  # placeholder to warm
best=None
for W in (3,4,6):
    for k in (3,5,10):
        r=evaluate(list(range(1997,2010)),list(range(2010,2015)),W,k); m=r.ea.mean(); print('VAL',W,k,round(m,4),flush=True)
        if best is None or m<best[0]-1e-12: best=(m,W,k)
_,W,k=best; rv=evaluate(list(range(1997,2010)),list(range(2010,2015)),W,k)
head='B0' if rv.e0.mean()<=rv.e1.mean() else 'B1'; print('VAL baselines',rv.e0.mean(),rv.e1.mean(),'headline',head,'W,k',W,k,flush=True)
lib_s=list(range(1997,2015))
def block_ci(d,order,L=4,B=10000,seed=7):
    d=d[order]; n=len(d); rs=np.random.RandomState(seed); nb=int(np.ceil(n/L)); out=[]
    for _ in range(B):
        st=rs.randint(0,n-L+1,nb); out.append(np.concatenate([d[a:a+L] for a in st])[:n].mean())
    return np.percentile(out,[2.5,97.5])
def verdict(r):
    eb=r.e0 if head=='B0' else r.e1; d=(eb-r.ea).values; order=np.lexsort((r.h.values,r.t.values,r.s.values))
    lo,hi=block_ci(d,order); rel=d.mean()/eb.mean(); v='WIN' if rel>=.05 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
    return dict(n=int(len(r)),mae_base=float(eb.mean()),mae_ara=float(r.ea.mean()),mae_persist=float(r.e0.mean()),mae_ar=float(r.e1.mean()),rel=float(rel),diff=float(d.mean()),ci=[float(lo),float(hi)],verdict=v,
      by_h={int(h):dict(base=float((eb[r.h==h]).mean()),ara=float(r.ea[r.h==h].mean())) for h in H})
rt=evaluate(lib_s,list(range(2015,2020)),W,k,cut=202010); out=dict(chosen=dict(W=W,k=k,val_mae=best[0],head=head),test=verdict(rt))
r2=evaluate(lib_s,list(range(2022,2026)),W,k); out['secondary_2022_2025']=verdict(r2); out['secondary_2022_2025'].pop('verdict')
json.dump(out,open('results.json','w'),indent=1); print(json.dumps(out))
