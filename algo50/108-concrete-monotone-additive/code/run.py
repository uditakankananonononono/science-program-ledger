import numpy as np, pandas as pd, hashlib, json, os, sys, warnings, itertools
from scipy.optimize import lsq_linear
from sklearn.ensemble import GradientBoostingRegressor, HistGradientBoostingRegressor
from sklearn.preprocessing import SplineTransformer
from sklearn.model_selection import GroupKFold
warnings.filterwarnings('ignore')
assert hashlib.sha256(open('concrete.csv','rb').read()).hexdigest()=='f656a971ce020d12a7d5e1d4aebd103aa28d99a164efca7125091a05380d3db2'
d=pd.read_csv('concrete.csv'); d.columns=['cement','slag','flyash','water','sp','coarse','fine','age','y']
mixkey=d[['cement','slag','flyash','water','sp','coarse','fine']].astype(str).agg('|'.join,axis=1); grp=pd.factorize(mixkey)[0]; y=d.y.values
RAW=['cement','slag','flyash','water','sp','coarse','fine','age']
def engineer(D):
    E=D[RAW].copy(); E['wc']=D.water/D.cement; E['wb']=D.water/(D.cement+D.slag+D.flyash); E['lage']=np.log(D.age); return E
X=engineer(d)
MON={'cement':1,'water':-1,'lage':1,'wc':-1,'wb':-1}; FREE=['slag','flyash','sp','coarse','fine']
class MAM:
    def __init__(s,K,lam,mon=MON,free=FREE): s.K=K;s.lam=lam;s.mon=mon;s.free=free
    def _basis(s,E,fit):
        cols=[]; 
        if fit: s.knots={};s.mu={};s.sd={};s.sp={}
        for f,sg in s.mon.items():
            z=sg*E[f].values.astype(float)
            if fit: s.knots[f]=np.unique(np.quantile(z,np.linspace(0,1,s.K+2)[1:-1])); s.mu[f]=0;s.sd[f]=z.std()+1e-9
            cols.append(z[:,None]/s.sd[f]); 
            for t in s.knots[f]: cols.append(np.maximum(0,z-t)[:,None]/s.sd[f])
        for f in s.free:
            z=E[f].values.astype(float)[:,None]
            if fit: s.sp[f]=SplineTransformer(n_knots=5,degree=3,knots='quantile',include_bias=False).fit(z)
            cols.append(s.sp[f].transform(z))
        return np.hstack(cols)
    def _nmon(s): return None
    def fit(s,E,yv):
        B=s._basis(E,True); s.bm=B.mean(0); Bc=B-s.bm; p=B.shape[1]
        # coefficient bound: monotone-feature columns are all nonneg (the linear col and ramps); free columns unbounded
        lb=np.full(p,-np.inf); i=0
        for f in s.mon:
            n=1+len(s.knots[f]); lb[i:i+n]=0; i+=n
        A=np.vstack([Bc,np.sqrt(s.lam*len(yv))*np.eye(p)]); b=np.concatenate([yv-yv.mean(),np.zeros(p)])
        s.coef=lsq_linear(A,b,bounds=(lb,np.inf),method='bvls' if p<400 else 'trf').x; s.b0=yv.mean(); return s
    def predict(s,E): return s.b0+(s._basis(E,False)-s.bm)@s.coef
class FreeOLS(MAM):
    def fit(s,E,yv):
        B=s._basis(E,True); s.bm=B.mean(0); Bc=B-s.bm; s.coef=np.linalg.lstsq(Bc,yv-yv.mean(),rcond=None)[0]; s.b0=yv.mean(); return s
# equivalence (i): all-free, tiny lam, MAM(lsq_linear, no lower bound) vs lstsq
rs=np.random.RandomState(0); sub=X.iloc[:300]; ys=y[:300]
m_free=MAM(4,1e-12,mon={},free=['cement','water','lage','wc','slag']).fit(sub,ys); m_ols=FreeOLS(4,0,mon={},free=['cement','water','lage','wc','slag']).fit(sub,ys)
assert np.abs(m_free.predict(sub)-m_ols.predict(sub)).max()<0.02,'equiv_ols'
if os.environ.get('CHECK_A'): print('A ok'); sys.exit()
ug=np.unique(grp); perm=np.random.RandomState(41).permutation(len(ug)); devg=set(ug[perm[:len(ug)//2]]); isdev=np.array([g in devg for g in grp])
di=np.where(isdev)[0]; ti=np.where(~isdev)[0]
# equivalence (ii): monotonicity of MAM fit on DEV
mm=MAM(4,0.1).fit(X.iloc[di],y[di]); med=X.iloc[ti].median()
def sweep(f,vals):
    G=pd.DataFrame([med.values]*len(vals),columns=X.columns); G[f]=vals
    if f=='age': G['lage']=np.log(vals)
    if f in('cement','water'): G['wc']=G.water/G.cement; G['wb']=G.water/(G.cement+G.slag+G.flyash)
    return mm.predict(G)
for f,sg in (('age',1),('cement',1),('water',-1)):
    vals=np.linspace(X[f].quantile(.02),X[f].quantile(.98),50) if f!='age' else np.linspace(3,365,50); p=sweep(f,vals)
    # raw cement/water also shift wc, wb (monotone in the same direction); check sign
    assert (sg*np.diff(p)).min()>-1e-6,('mono',f)
if os.environ.get('CHECK'): print('checks passed'); sys.exit()
def cv(make,cols):
    r=[]
    for tr,te in GroupKFold(5).split(di,groups=grp[di]):
        a=di[tr];b=di[te]; m=make().fit(X.iloc[a][cols] if cols else X.iloc[a],y[a]); r.append(((m.predict(X.iloc[b][cols] if cols else X.iloc[b])-y[b])**2).mean()*len(b))
    return np.sqrt(sum(r)/len(di))
cst=[1 if c=='cement' else -1 if c=='water' else 1 if c=='age' else 0 for c in RAW]
class W:
    def __init__(s,m): s.m=m
    def fit(s,E,yv): s.m.fit(E[RAW].values,yv); return s
    def predict(s,E): return s.m.predict(E[RAW].values)
tune={}
for name,mk in (('GBR',lambda ne,lr,md: W(GradientBoostingRegressor(n_estimators=ne,learning_rate=lr,max_depth=md,subsample=0.8,random_state=0))),):
    for ne,lr,md in itertools.product((200,400),(0.05,0.1),(2,3,4)): tune[(name,ne,lr,md)]=cv(lambda: mk(ne,lr,md),None)
for name,mono in (('HGB',None),('HGBM',cst)):
    for it,lr,ml in itertools.product((200,400),(0.05,0.1),(8,16)):
        tune[(name,it,lr,ml)]=cv(lambda: W(HistGradientBoostingRegressor(max_iter=it,learning_rate=lr,max_leaf_nodes=ml,random_state=0,monotonic_cst=mono)),None)
bestb={n:min((k for k in tune if k[0]==n),key=lambda k:tune[k]) for n in ('GBR','HGB','HGBM')}; print('DEV base',{n:(bestb[n],tune[bestb[n]]) for n in bestb},flush=True)
head=min(bestb,key=lambda n:tune[bestb[n]])
mt={(K,lam):cv(lambda: MAM(K,lam),None) for K in (4,8) for lam in (0.01,0.1,1,10)}; Kb,lb=min(mt,key=lambda k:(mt[k],k)); print('DEV MAM',mt,(Kb,lb),flush=True)
def build(n,k):
    if n=='GBR': return W(GradientBoostingRegressor(n_estimators=k[1],learning_rate=k[2],max_depth=k[3],subsample=0.8,random_state=0))
    return W(HistGradientBoostingRegressor(max_iter=k[1],learning_rate=k[2],max_leaf_nodes=k[3],random_state=0,monotonic_cst=None if n=='HGB' else cst))
pred={n:build(n,bestb[n]).fit(X.iloc[di],y[di]).predict(X.iloc[ti]) for n in bestb}; pred['MAM']=MAM(Kb,lb).fit(X.iloc[di],y[di]).predict(X.iloc[ti])
yt=y[ti]; rmse={n:float(np.sqrt(((p-yt)**2).mean())) for n,p in pred.items()}; mae={n:float(np.abs(p-yt).mean()) for n,p in pred.items()}; r2={n:float(1-((p-yt)**2).sum()/((yt-yt.mean())**2).sum()) for n,p in pred.items()}
gt=grp[ti]; ugt=np.unique(gt); ix={g:np.where(gt==g)[0] for g in ugt}; rs=np.random.RandomState(7); ds=[]
for _ in range(10000):
    s=np.concatenate([ix[g] for g in ugt[rs.randint(0,len(ugt),len(ugt))]]); ds.append(np.sqrt(((pred[head][s]-yt[s])**2).mean())-np.sqrt(((pred['MAM'][s]-yt[s])**2).mean()))
lo,hi=np.percentile(ds,[2.5,97.5]); diff=rmse[head]-rmse['MAM']; rel=diff/rmse[head]; v='WIN' if rel>=.05 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
res=dict(n_dev=len(di),n_test=len(ti),head=head,dev_base={n:[list(bestb[n]),tune[bestb[n]]] for n in bestb},dev_mam={str(k):v_ for k,v_ in mt.items()},mam_params=[Kb,lb],edge=bool(Kb in (4,8) or lb in (0.01,10)),test_rmse=rmse,test_mae=mae,test_r2=r2,diff=float(diff),rel=float(rel),ci=[float(lo),float(hi)],verdict=v)
json.dump(res,open('results.json','w'),indent=1); print(json.dumps(res))
