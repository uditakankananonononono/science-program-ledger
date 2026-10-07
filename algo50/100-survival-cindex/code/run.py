import numpy as np, pandas as pd, pyreadr, json, warnings
from lifelines import CoxPHFitter
from lifelines.utils import concordance_index
from sklearn.model_selection import StratifiedShuffleSplit
warnings.filterwarnings('ignore')
D='data/survival/data/'
pbc=list(pyreadr.read_r(D+'pbc.rda').values())[0]; lung=pyreadr.read_r(D+'cancer.rda')['lung']
def prep_pbc():
    d=pbc.dropna(subset=['age','edema','bili','albumin','protime','time','status']).copy()
    X=pd.DataFrame({'age':d.age,'edema':d.edema,'lbili':np.log(d.bili),'lalb':np.log(d.albumin),'lprot':np.log(d.protime)})
    X['T']=d.time.values.astype(float); X['E']=(d.status.values==2).astype(int); return X.reset_index(drop=True)
def prep_lung():
    d=lung.dropna(subset=['age','sex','ph.ecog','ph.karno','wt.loss','time','status']).copy()
    X=pd.DataFrame({'age':d.age,'sex':d.sex,'ecog':d['ph.ecog'],'karno':d['ph.karno'],'wtloss':d['wt.loss']})
    X['T']=d.time.values.astype(float); X['E']=(d.status.values==2).astype(int); return X.reset_index(drop=True)
PEN=0.1
def fitcox(df,entry=None):
    c=CoxPHFitter(penalizer=PEN,l1_ratio=0.0)
    if entry is None: c.fit(df,'T','E')
    else: c.fit(df,'T','E',entry_col='entry')
    return c
def sf(c,X,t): return c.predict_survival_function(X,times=[t]).values[0]
def scores(tr,te,h,tau):
    cov=[c for c in tr.columns if c not in('T','E')]
    B=fitcox(tr); sB=sf(B,te[cov],h)
    if tau is None: return -sB,-sB,False
    ea=tr.copy(); ea['E']=np.where(ea['T']>tau,0,ea['E']); ea['T']=np.minimum(ea['T'],tau)
    late=tr[tr['T']>tau].copy(); late['entry']=tau
    if late.E.sum()<10 or ea.E.sum()<10: return -sB,-sB,True
    try:
        Me=fitcox(ea); Ml=fitcox(late,entry=True)
        s=sf(Me,te[cov],tau)*sf(Ml,te[cov],h)/np.maximum(sf(Ml,te[cov],tau),1e-9); return -sB,-s,False
    except Exception: return -sB,-sB,True
def cidx(df,r): return concordance_index(df['T'],-r,df['E'])
def study(X,h,tau):
    # equivalence on split 1
    tr,te=next(StratifiedShuffleSplit(1,test_size=.3,random_state=1).split(X,X.E)); a,b,_=scores(X.iloc[tr],X.iloc[te],h,None); assert np.allclose(a,b)
    rows=[];fb=0
    for s in range(1,21):
        tr,te=next(StratifiedShuffleSplit(1,test_size=.3,random_state=s).split(X,X.E)); T=X.iloc[te]
        rb,rp,fell=scores(X.iloc[tr],T,h,tau); fb+=fell; rows.append((cidx(T,rb),cidx(T,rp)))
    R=np.array(rows); d=R[:,1]-R[:,0]; rs=np.random.RandomState(7); bs=[d[rs.randint(0,20,20)].mean() for _ in range(10000)]
    lo,hi=np.percentile(bs,[2.5,97.5]); v='WIN' if d.mean()>=.01 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
    return dict(n=len(X),events=int(X.E.sum()),c_base=float(R[:,0].mean()),c_pwc=float(R[:,1].mean()),diff=float(d.mean()),ci=[float(lo),float(hi)],wins=int((d>0).sum()),losses=int((d<0).sum()),fallbacks=int(fb),verdict=v)
out={'pbc':study(prep_pbc(),1461.0,1096.0)}; print(out,flush=True)
out['lung_secondary']=study(prep_lung(),365.0,180.0)
json.dump(out,open('results.json','w'),indent=1); print(json.dumps(out))
