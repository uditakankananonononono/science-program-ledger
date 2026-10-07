import numpy as np, json, wfdb, sys, warnings
import neurokit2 as nk
from scipy.signal import butter, sosfiltfilt, find_peaks
warnings.filterwarnings('ignore')
FS=360; BEATS=set('NLRBAaJSVrFejnE/fQ')
recs=open('data/RECORDS').read().split() if __import__('os').path.exists('data/RECORDS') else None
def load(r):
    rec=wfdb.rdrecord(f'data/{r}',channels=[0]); ann=wfdb.rdann(f'data/{r}','atr')
    t=np.array([s for s,c in zip(ann.sample,ann.symbol) if c in BEATS]); return rec.p_signal[:,0],t[t>=5*FS]
def match(det,truth,tol=int(.15*FS)):
    det=np.sort(det); used=np.zeros(len(det),bool); tp=0
    for t in truth:
        j=np.searchsorted(det,t); best=None
        for k in (j-1,j):
            if 0<=k<len(det) and not used[k] and abs(det[k]-t)<=tol and (best is None or abs(det[k]-t)<abs(det[best]-t)): best=k
        if best is not None: used[best]=True; tp+=1
    return tp,len(det)-tp,len(truth)-tp
def base(sig):
    try: return nk.ecg_peaks(sig,sampling_rate=FS,method='pantompkins1985')[1]['ECG_R_Peaks']
    except Exception: return np.array([],int)
def mfdp(sig,lam,thr):
    sos=butter(2,[5,15],btype='band',fs=FS,output='sos'); f=sosfiltfilt(sos,sig)
    a=np.abs(f); c,_=find_peaks(a,distance=int(.2*FS)); c=c[(c>40)&(c<len(f)-40)]
    if len(c)<5: return c
    h=29; W=np.array([f[i-h:i+h+1]*np.sign(f[i]) for i in c])
    top=c[np.argsort(-a[c])[:max(5,len(c)//5)]]
    tmpl=np.median(np.array([f[i-h:i+h+1]*np.sign(f[i]) for i in top]),axis=0)
    tn=(tmpl-tmpl.mean()); tn/=np.linalg.norm(tn)+1e-12
    Wn=W-W.mean(1,keepdims=True); Wn/=np.linalg.norm(Wn,axis=1,keepdims=True)+1e-12
    sc=Wn@tn-thr
    n=len(c)
    if n<3: return c
    NEG=-1e18; best=np.array(sc,float).copy(); prev=-np.ones(n,int)
    for i in range(n):
        j=i-1
        while j>=0 and (c[i]-c[j])<=2*FS:
            rr=c[i]-c[j]
            if rr>=.2*FS:
                pj=prev[j]; pen=0.0
                if pj>=0: pen=lam*abs(np.log(rr/(c[j]-c[pj])))
                v=best[j]+sc[i]-pen
                if v>best[i]: best[i]=v; prev[i]=j
            j-=1
    i=int(np.argmax(best)); out=[]
    while i>=0: out.append(c[i]); i=prev[i]
    return np.array(out[::-1])
if __name__=='__main__':
    recs=open('data/RECORDS').read().split(); dev=recs[0::2]; test=recs[1::2]
    cache={r:load(r) for r in recs}
    # equivalence
    s,t=cache[dev[0]]; assert match(t,t)==(len(t),0,0)
    # tune on dev
    best=None
    for lam in (0,.25,.5,1):
        for thr in (.2,.35,.5,.65):
            TP=FP=FN=0
            for r in dev:
                s,t=cache[r]; a,b,c=match(mfdp(s,lam,thr),t); TP+=a;FP+=b;FN+=c
            f1=2*TP/(2*TP+FP+FN); print('dev',lam,thr,round(f1,4),flush=True)
            if best is None or f1>best[0]+1e-12: best=(f1,lam,thr)
    json.dump(dict(dev_f1=best[0],lam=best[1],thr=best[2]),open('dev_choice.json','w'))
    lam,thr=best[1],best[2]; rows={}
    for r in test:
        s,t=cache[r]; rows[r]=dict(B=match(base(s),t),M=match(mfdp(s,lam,thr),t)); print(r,rows[r],flush=True)
    f1=lambda L:2*sum(x[0] for x in L)/max(1,2*sum(x[0] for x in L)+sum(x[1] for x in L)+sum(x[2] for x in L))
    R=list(rows); d=lambda idx:f1([rows[R[i]]['M'] for i in idx])-f1([rows[R[i]]['B'] for i in idx])
    diff=d(range(len(R))); rs=np.random.RandomState(7); bs=[d(rs.randint(0,len(R),len(R))) for _ in range(10000)]
    lo,hi=np.percentile(bs,[2.5,97.5]); v='WIN' if diff>=.01 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
    out=dict(lam=lam,thr=thr,f1_base=f1([rows[r]['B'] for r in R]),f1_mfdp=f1([rows[r]['M'] for r in R]),diff=diff,ci=[lo,hi],verdict=v,per_record=rows)
    json.dump(out,open('results.json','w'),indent=1,default=int); print(json.dumps({k:v for k,v in out.items() if k!='per_record'},default=float))
