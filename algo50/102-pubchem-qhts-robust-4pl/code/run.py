import pandas as pd, numpy as np, re, hashlib, json, warnings, os, sys
from scipy.optimize import curve_fit, least_squares
warnings.filterwarnings('ignore')
H={720691:'0a8f6226da0c193038f07a9efad07c6c949c47d23f21756c2e03a509527f5cec',720692:'ee72d53f56d7a504891024d2d5da395d88dedfc4f3ce6f36b42a99ad26cdd14b'}
for a,h in H.items(): assert hashlib.sha256(open(f'aid{a}.csv','rb').read()).hexdigest()==h
def f4(x,b,t,l,h): return b+(t-b)/(1+10**((l-x)*h))
def fit_B(x,y):
    lo,hi=x.min()-1,x.max()+1
    try:
        p,_=curve_fit(f4,x,y,p0=[y.min(),y.max(),np.median(x),1.0],maxfev=2000); return float(np.clip(p[2],lo,hi))
    except Exception: return hi
def fit_R(x,y,fs):
    lo,hi=x.min()-1,x.max()+1; best=None
    for q in (10,30,50,70,90):
        p0=[np.clip(y.min(),-150,150),np.clip(y.max(),-250,250),np.clip(np.percentile(x,q),lo,hi),1.0]
        try:
            r=least_squares(lambda p:f4(x,*p)-y,p0,bounds=([-150,-250,lo,0.3],[150,250,hi,4]),loss='soft_l1',f_scale=fs,max_nfev=300)
            if best is None or r.cost<best.cost: best=r
        except Exception: pass
    return float(best.x[2]) if best is not None else hi
# equivalence on synthetic
rs=np.random.RandomState(0); xs=np.linspace(-3,2,15)
for i in range(20):
    l=rs.uniform(-1,1); h=rs.uniform(1,2); y=f4(xs,0,-80,l,h)
    assert abs(fit_B(xs,y)-l)<0.05 and abs(fit_R(xs,y,10)-l)<0.05,'equiv'
if os.environ.get('CHECK'): print('checks passed'); sys.exit()
d=pd.read_csv('aid720692.csv',low_memory=False); d=d[pd.to_numeric(d.PUBCHEM_SID,errors='coerce').notna()].reset_index(drop=True)
comp=[]
for i,row in d.iterrows():
    cur=[]
    for r in (1,2,3):
        cols=[c for c in d.columns if c.startswith('Ratio-Activity at') and c.endswith(f'Replicate_{r}')]
        x=np.array([np.log10(float(re.search(r'at (.*) uM',c).group(1))) for c in cols]); y=pd.to_numeric(row[cols],errors='coerce').values.astype(float); ok=~np.isnan(y)
        if ok.sum()>=8 and np.abs(y[ok]).max()>=20:
            pub=pd.to_numeric(row.get(f'Ratio-Fit_LogAC50-Replicate_{r}'),errors='coerce'); cur.append((x[ok],y[ok],pub))
    if len(cur)>=2: comp.append((int(row.PUBCHEM_SID),cur))
comp.sort(key=lambda t:t[0]); dev=comp[0::2]; tst=comp[1::2]; print('compounds',len(comp),'dev',len(dev),'test',len(tst),flush=True)
def conc(vals): 
    return np.mean([abs(a-b) for i,a in enumerate(vals) for b in vals[i+1:]])
def score(cs,meth):
    return np.array([conc([meth(x,y) for x,y,_ in cur]) for _,cur in cs])
dres={fs:score(dev,lambda x,y:fit_R(x,y,fs)).mean() for fs in (5,10,20)}; dB=score(dev,fit_B).mean(); print('DEV',dB,dres,flush=True)
fs=min(dres,key=lambda k:(dres[k],-k))
sB=score(tst,fit_B); sR=score(tst,lambda x,y:fit_R(x,y,fs)); d_=sB-sR
rs=np.random.RandomState(7); bs=[d_[rs.randint(0,len(d_),len(d_))].mean() for _ in range(10000)]; lo,hi=np.percentile(bs,[2.5,97.5]); rel=d_.mean()/sB.mean()
eB=[];eR=[]
for _,cur in tst:
    for x,y,pub in cur:
        if not np.isnan(pub): eB.append(abs(fit_B(x,y)-6-pub)); eR.append(abs(fit_R(x,y,fs)-6-pub))
if len(eB)>=8: guard=bool(np.median(eR)<=np.median(eB)+0.1); gtxt=dict(n=len(eB),med_B=float(np.median(eB)),med_R=float(np.median(eR)))
else: guard=None; gtxt=dict(n=len(eB))
v='WIN' if (rel>=.10 and lo>0 and guard) else ('NEGATIVE' if hi<0 else 'NULL')
res=dict(n_compounds=len(comp),n_test=len(tst),dev_B=float(dB),dev_R={str(k):float(x) for k,x in dres.items()},fscale=fs,edge=fs in (5,20),test_B=float(sB.mean()),test_R=float(sR.mean()),diff=float(d_.mean()),rel=float(rel),ci=[float(lo),float(hi)],guard_ok=guard,guard=gtxt,verdict=v)
json.dump(res,open('results.json','w'),indent=1); print(json.dumps(res))
