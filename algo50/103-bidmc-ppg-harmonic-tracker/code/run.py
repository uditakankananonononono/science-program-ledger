import numpy as np, pandas as pd, hashlib, json, sys
from scipy.signal import butter, sosfiltfilt, sosfilt
FS=125
rows=[l.rstrip('\n').split('\t') for l in open('files.tsv')]
for f,u,h,b in rows:
    assert hashlib.sha256(open('data/'+f,'rb').read()).hexdigest()==h, f
GRID=np.arange(40,201)
W=8*FS; HOP=2*FS
def bp(x,lo,hi): return sosfiltfilt(butter(2,[lo,hi],btype='band',fs=FS,output='sos'),x)
def elgendi(x):
    y=bp(x,0.5,8); y=np.clip(y,0,None)**2
    w1=int(round(.111*FS)); w2=int(round(.667*FS))
    k=lambda w: np.convolve(y,np.ones(w)/w,'same')
    mp,mb=k(w1),k(w2); thr=mb+0.02*y.mean(); m=mp>thr
    peaks=[];i=0;n=len(y)
    while i<n:
        if m[i]:
            j=i
            while j<n and m[j]: j+=1
            if j-i>=w1: peaks.append(i+int(np.argmax(y[i:j])))
            i=j
        else: i+=1
    return np.array(peaks)
def hr_elgendi(win,prev):
    p=elgendi(win)
    if len(p)<2: return prev
    return 60.0/np.median(np.diff(p)/FS)
def spec(win,hi):
    x=bp(win,0.7,hi); x=(x-x.mean())*np.hanning(len(x)); N=1<<15
    P=np.abs(np.fft.rfft(x,N))**2; fr=np.fft.rfftfreq(N,1/FS)*60
    return fr,P
def hr_fft(win):
    fr,P=spec(win,3.5); return GRID[np.argmax(np.interp(GRID,fr,P))]
def score(win):
    fr,P=spec(win,8.0); eps=1e-8*P.max(); S=np.zeros(len(GRID))
    for m in (1,2,3): S+=np.log(np.interp(GRID*m,fr,P)+eps)/m
    return (S-S.mean())/(S.std()+1e-12)
D=np.abs(GRID[:,None]-GRID[None,:]).astype(float)
def track(Ss,lam):
    d=None;out=[]
    for S in Ss:
        d=S if d is None else S+np.max(d[None,:]-lam*D,axis=1)
        d=d-d.max(); out.append(GRID[np.argmax(d)])
    return np.array(out,float)
def load(r):
    sg=pd.read_csv(f'data/bidmc_{r:02d}_Signals.csv'); sg.columns=[c.strip() for c in sg.columns]
    nm=pd.read_csv(f'data/bidmc_{r:02d}_Numerics.csv'); nm.columns=[c.strip() for c in nm.columns]
    return sg['PLETH'].values.astype(float), nm['HR'].values.astype(float)
def windows(x,hr):
    out=[]
    for s in range(0,len(x)-W+1,HOP):
        t0=s//FS; ref=np.nanmean(hr[t0:t0+8]) if np.any(~np.isnan(hr[t0:t0+8])) else np.nan
        out.append((s,ref))
    return out
# equivalence check: synthetic 72-bpm pulse train
t=np.arange(W)/FS; syn=np.sin(2*np.pi*1.2*t)+0.3*np.sin(2*np.pi*2.4*t)+0.05*np.random.RandomState(0).randn(W)
assert abs(hr_elgendi(syn,75)-72)<2 and abs(hr_fft(syn)-72)<2 and abs(GRID[np.argmax(score(syn))]-72)<2, 'equivalence'
cache={}
def est(r,lams):
    x,hr=load(r); ws=windows(x,hr); Ss=[score(x[s:s+W]) for s,_ in ws]
    b1=[];prev=75.0
    for s,_ in ws: prev=hr_elgendi(x[s:s+W],prev); b1.append(prev)
    b2=[hr_fft(x[s:s+W]) for s,_ in ws]; ref=np.array([a for _,a in ws])
    return dict(ref=ref,b1=np.array(b1),b2=np.array(b2),h={l:track(Ss,l) for l in lams})
LAMS=(0.02,0.05,0.1,0.2,0.5)
def mae(a,ref): ok=~np.isnan(ref); return np.abs(a[ok]-ref[ok]).mean()
dev={r:est(r,LAMS) for r in range(1,19)}
dm={k:np.mean([mae(dev[r][k],dev[r]['ref']) for r in dev]) for k in ('b1','b2')}
dl={l:np.mean([mae(dev[r]['h'][l],dev[r]['ref']) for r in dev]) for l in LAMS}
head='b1' if dm['b1']<=dm['b2'] else 'b2'; lam=min(LAMS,key=lambda l:(dl[l],-l))
print('DEV',dm,dl,'head',head,'lam',lam,flush=True)
te={r:est(r,[lam]) for r in range(19,54)}
pb=np.array([mae(te[r][head],te[r]['ref']) for r in te]); ph=np.array([mae(te[r]['h'][lam],te[r]['ref']) for r in te])
d=pb-ph; rs=np.random.RandomState(7); bs=[d[rs.randint(0,len(d),len(d))].mean() for _ in range(10000)]
lo,hi=np.percentile(bs,[2.5,97.5]); rel=d.mean()/pb.mean()
v='WIN' if rel>=.10 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
allref=np.concatenate([te[r]['ref'] for r in te]); ok=~np.isnan(allref)
ae=lambda k: np.abs(np.concatenate([te[r][k] if k!='h' else te[r]['h'][lam] for r in te])[ok]-allref[ok])
res=dict(dev_mae_baselines=dm,dev_mae_lambda={str(k):v for k,v in dl.items()},headline=head,lam=lam,lam_at_edge=lam in (0.02,0.5),
 test=dict(n_records=len(te),mae_base=pb.mean(),mae_htv=ph.mean(),rel=rel,diff=d.mean(),ci=[lo,hi],verdict=v,records_htv_better=int((d>0).sum()),
  other_baseline_mae=float(np.mean([mae(te[r]['b2' if head=='b1' else 'b1'],te[r]['ref']) for r in te])),
  window_mae={k:float(ae(k).mean()) for k in (head,'h')},window_med={k:float(np.median(ae(k))) for k in (head,'h')},frac_gt5={k:float((ae(k)>5).mean()) for k in (head,'h')}))
json.dump(res,open('results.json','w'),indent=1,default=float); print(json.dumps(res,default=float))
