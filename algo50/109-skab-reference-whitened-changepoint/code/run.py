import numpy as np, pandas as pd, hashlib, json, os, sys, glob, warnings, itertools
import ruptures as rpt
from ruptures.metrics import precision_recall
from scipy.signal import find_peaks
warnings.filterwarnings('ignore')
integ=pd.read_csv('file-integrity.csv'); FILES=[]
for _,r in integ.iterrows():
    assert hashlib.sha256(open(r.path,'rb').read()).hexdigest()==r.sha256,r.path; FILES.append(r.path)
assert len(FILES)==20 and integ.rows.sum()==22472
CH=['Accelerometer1RMS','Accelerometer2RMS','Current','Pressure','Temperature','Thermocouple','Voltage','Volume Flow RateRMS']; M=30; REF=200
def key(p): v,i=p.split('/')[1],int(p.split('/')[2][:-4]); return (v,i)
DEVF=[p for p in FILES if key(p)[0]=='valve1' and key(p)[1]<=7]; TESTF=[p for p in FILES if p not in DEVF]
def load(p):
    d=pd.read_csv(p,sep=';'); X=d[CH].values.astype(float); cp=np.where(d.changepoint.values==1)[0]
    mu=X[:REF].mean(0); sd=X[:REF].std(0); sd=np.maximum(sd,1e-6*np.median(X.std(0))+1e-12); return (X-mu)/sd,cp
def match(pred,true):
    pred=sorted(pred); true=list(true); used=set(); tp=0
    pairs=sorted((abs(p-t),i,j) for i,p in enumerate(pred) for j,t in enumerate(true) if abs(p-t)<=M)
    up=set();ut=set()
    for dist,i,j in pairs:
        if i in up or j in ut: continue
        up.add(i);ut.add(j);tp+=1
    return tp,len(pred)-tp,len(true)-tp
def f1(tp,fp,fn): return 2*tp/max(2*tp+fp+fn,1)
# equivalence vs ruptures
rs=np.random.RandomState(0)
for _ in range(200):
    n=1000
    t=sorted(rs.choice(np.arange(50,950,70),rs.randint(1,5),replace=False))  # spaced >2M apart
    p=[x+int(rs.choice([-60,-20,0,25,60])) for x in t if rs.rand()<0.7]+([int(rs.randint(60,940))] if rs.rand()<0.5 else [])
    p=sorted(set(p)); 
    if any(abs(a-b)<=2*M for a,b in zip(p[:-1],p[1:])) or any(abs(a-b)<=2*M for a,b in zip(t[:-1],t[1:])): continue
    tp,fp,fn=match(p,t); pr,rc=precision_recall(list(t)+[n],list(p)+[n],margin=M)
    if len(p)==0: continue
    assert abs(pr*len(p)-tp)<1e-9 and abs(rc*len(t)-tp)<1e-9,'equiv'
if os.environ.get('CHECK_A'): print('ok'); sys.exit()
def rwe(X,w,c):
    n=len(X); R=X[:REF]; S=np.cov(R.T)+0.1*np.trace(np.cov(R.T))/8*np.eye(8); L=np.linalg.cholesky(np.linalg.inv(S)); Z=X@L
    cs=np.vstack([np.zeros(8),np.cumsum(Z,0)]); s=np.full(n,0.0)
    for t in range(w,n-w+1): s[t]=(w/2)*np.sum(((cs[t+w]-cs[t])/w-(cs[t]-cs[t-w])/w)**2)
    ref=s[w:REF-w+1]; med=np.median(ref); med=max(med,np.percentile(ref,25),1e-12); th=c*med
    s2=s.copy(); s2[:REF]=0; pk,_=find_peaks(s2,height=th,distance=w); return list(pk)
def rup(X,kind,a,b):
    n=len(X)
    if kind=='pelt-l2': al=rpt.Pelt(model='l2',min_size=20,jump=5).fit(X); r=al.predict(pen=a)
    elif kind=='pelt-rbf': al=rpt.Pelt(model='rbf',min_size=20,jump=5).fit(X); r=al.predict(pen=a)
    elif kind=='binseg': al=rpt.Binseg(model='l2',min_size=20,jump=5).fit(X); r=al.predict(pen=a)
    elif kind=='window': al=rpt.Window(width=a,model='l2',min_size=20,jump=5).fit(X); r=al.predict(pen=b)
    return [x for x in r[:-1] if x>=REF]
def sweep(files,methods):
    D={f:load(f) for f in files}; out={}
    for name,fn in methods.items():
        tot=[0,0,0]; per={}
        for f in files:
            X,cp=D[f]; r=match(fn(X),cp); per[f]=r
            for i in range(3): tot[i]+=r[i]
        out[name]=(f1(*tot),per)
    return out
meth={}
for pen in (10,30,100,300,1000): meth[('pelt-l2',pen,None)]=(lambda X,pen=pen:rup(X,'pelt-l2',pen,None)); meth[('binseg',pen,None)]=(lambda X,pen=pen:rup(X,'binseg',pen,None))
for pen in (1,3,10,30,100): meth[('pelt-rbf',pen,None)]=(lambda X,pen=pen:rup(X,'pelt-rbf',pen,None))
for wd,pen in itertools.product((20,40),(10,30,100,300)): meth[('window',wd,pen)]=(lambda X,wd=wd,pen=pen:rup(X,'window',wd,pen))
rw={('rwe',w,c):(lambda X,w=w,c=c:rwe(X,w,c)) for w in (10,20,30) for c in (5,10,20,40,80,160)}
dv=sweep(DEVF,{**meth,**rw}); hb=max(meth,key=lambda k:dv[k][0]); hr=max(rw,key=lambda k:(dv[k][0],k[1],k[2]))
print('DEV head',hb,dv[hb][0],'RWE',hr,dv[hr][0],flush=True)
tt=sweep(TESTF,{'base':meth[hb],'new':rw[hr],'oracleK':None} if False else {'base':meth[hb],'new':rw[hr]})
def pooled(per,files): 
    t=np.sum([per[f] for f in files],0); return f1(*t),t
fb,tb=pooled(tt['base'][1],TESTF); fn_,tn=pooled(tt['new'][1],TESTF)
rs=np.random.RandomState(7); ds=[]
for _ in range(10000):
    s=[TESTF[i] for i in rs.randint(0,len(TESTF),len(TESTF))]; ds.append(pooled(tt['new'][1],s)[0]-pooled(tt['base'][1],s)[0])
lo,hi=np.percentile(ds,[2.5,97.5]); diff=fn_-fb; v='WIN' if diff>=0.05 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
v1=[f for f in TESTF if key(f)[0]=='valve1']; v2=[f for f in TESTF if key(f)[0]=='valve2']
# oracle-K Binseg (descriptive)
tot=np.zeros(3)
for f in TESTF:
    X,cp=load(f); r=[x for x in rpt.Binseg(model='l2',min_size=20,jump=5).fit(X).predict(n_bkps=len(cp)+0)[:-1]]; tot+=np.array(match(r,cp))
res=dict(n_dev_files=len(DEVF),n_test_files=len(TESTF),n_test_events=int(sum(tb[0]+tb[2] for _ in [0])),base=[str(x) for x in hb],base_dev_f1=dv[hb][0],rwe=[str(x) for x in hr],rwe_dev_f1=dv[hr][0],edge=bool(hr[1] in (10,30) or hr[2] in (5,160)),test_f1_base=fb,test_f1_rwe=fn_,base_tp_fp_fn=[int(x) for x in tb],rwe_tp_fp_fn=[int(x) for x in tn],diff=float(diff),ci=[float(lo),float(hi)],valve1_f1={'base':pooled(tt['base'][1],v1)[0],'rwe':pooled(tt['new'][1],v1)[0]},valve2_f1={'base':pooled(tt['base'][1],v2)[0],'rwe':pooled(tt['new'][1],v2)[0]},oracleK_binseg_f1=f1(*tot),verdict=v)
json.dump(res,open('results.json','w'),indent=1); print(json.dumps(res))
