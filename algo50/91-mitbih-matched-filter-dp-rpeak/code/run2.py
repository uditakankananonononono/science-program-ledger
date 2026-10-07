import numpy as np, json, warnings
from scipy.signal import butter, sosfiltfilt, find_peaks
from sklearn.cluster import KMeans
import run as R
warnings.filterwarnings('ignore')
FS=R.FS
def mfdp2(sig,lam,thr):
    sos=butter(2,[5,15],btype='band',fs=FS,output='sos'); f=sosfiltfilt(sos,sig)
    a=np.abs(f); c,_=find_peaks(a,distance=int(.2*FS)); c=c[(c>40)&(c<len(f)-40)]
    if len(c)<12: return c
    h=29; W=np.array([f[i-h:i+h+1]*np.sign(f[i]) for i in c])
    Wn=W-W.mean(1,keepdims=True); Wn/=np.linalg.norm(Wn,axis=1,keepdims=True)+1e-12
    top=np.argsort(-a[c])[:max(12,len(c)//5)]
    km=KMeans(3,random_state=0,n_init=10).fit(Wn[top]); T=km.cluster_centers_
    T=T-T.mean(1,keepdims=True); T/=np.linalg.norm(T,axis=1,keepdims=True)+1e-12
    sc=(Wn@T.T).max(1)-thr; n=len(c)
    best=sc.copy(); prev=-np.ones(n,int)
    for i in range(n):
        j=i-1
        while j>=0 and (c[i]-c[j])<=2*FS:
            rr=c[i]-c[j]
            if rr>=.2*FS:
                pj=prev[j]; pen=lam*abs(np.log(rr/(c[j]-c[pj]))) if pj>=0 else 0.0
                v=best[j]+sc[i]-pen
                if v>best[i]: best[i]=v; prev[i]=j
            j-=1
    i=int(np.argmax(best)); out=[]
    while i>=0: out.append(c[i]); i=prev[i]
    return np.array(out[::-1])
if __name__=='__main__':
    recs=open('data/RECORDS').read().split(); dev=recs[0::2]; test=recs[1::2]
    cache={r:R.load(r) for r in recs}; best=None
    for lam in (1,2,4):
        for thr in (.65,.75,.85):
            TP=FP=FN=0
            for r in dev:
                s,t=cache[r]; a,b,c=R.match(mfdp2(s,lam,thr),t); TP+=a;FP+=b;FN+=c
            f1=2*TP/(2*TP+FP+FN); print('dev',lam,thr,round(f1,4),flush=True)
            if best is None or f1>best[0]+1e-12: best=(f1,lam,thr)
    json.dump(dict(dev_f1=best[0],lam=best[1],thr=best[2]),open('dev_choice_v2.json','w'))
    lam,thr=best[1],best[2]; rows={}
    for r in test:
        s,t=cache[r]; rows[r]=dict(B=R.match(R.base(s),t),M=mfdp2(s,lam,thr) is None or R.match(mfdp2(s,lam,thr),t)); print(r,rows[r],flush=True)
    f1=lambda L:2*sum(x[0] for x in L)/max(1,2*sum(x[0] for x in L)+sum(x[1] for x in L)+sum(x[2] for x in L))
    Rr=list(rows); d=lambda idx:f1([rows[Rr[i]]['M'] for i in idx])-f1([rows[Rr[i]]['B'] for i in idx])
    diff=d(range(len(Rr))); rs=np.random.RandomState(7); bs=[d(rs.randint(0,len(Rr),len(Rr))) for _ in range(10000)]
    lo,hi=np.percentile(bs,[2.5,97.5]); v='WIN' if diff>=.01 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
    out=dict(role='SECOND-LOOK',lam=lam,thr=thr,f1_base=f1([rows[r]['B'] for r in Rr]),f1_mfdp2=f1([rows[r]['M'] for r in Rr]),diff=diff,ci=[lo,hi],verdict=v,per_record=rows)
    json.dump(out,open('results_v2.json','w'),indent=1,default=int); print(json.dumps({k:v for k,v in out.items() if k!='per_record'},default=float))
