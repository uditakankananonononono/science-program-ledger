# Unit 193 result - PTB-XL label-shift-weighted conformal vs split/Mondrian conformal
Prereg algo50/193-PREREG.md sha256 f5ef32df80d4c1a731094f78103f29ba32c49fe26b5c3f7e1602e75951651a57. Fold 10 opened once. Files from PhysioNet S3 mirror (physionet-open.s3.amazonaws.com, v1.0.3); the prereg did not name a mirror.

VERDICT: LOSS (candidate coverage gap larger than the DEV-fixed primary baseline B2)

## TEST (fold 10) verbatim output
```
records 15983 {1: 1614, 2: 1588, 3: 1617, 4: 1560, 5: 1586, 6: 1555, 7: 1621, 8: 1622, 9: 1600, 10: 1620}
TEST natural acc 0.6951 n tr/ca/te 9520 3243 1620
B1 {'cov': 0.7450595818979721, 'gap': 0.15494041810202797, 'sel_risk': 0.35319677195298826, 'singleton': 0.3547184464164141, 'setsize': 1.8749070651358146}
B2 {'cov': 0.8877111035124966, 'gap': 0.01228889648750342, 'sel_risk': 0.18239244881900496, 'singleton': 0.18985057014833617, 'setsize': 2.5692369926256275}
C {'cov': 0.8444539778740535, 'gap': 0.055546022125946504, 'sel_risk': 0.2371996952833899, 'singleton': 0.18698479605475712, 'setsize': 2.4513100301359625}
oracleW {'cov': 0.8691536538761301, 'gap': 0.03084634612386994, 'sel_risk': 0.17188986215520796, 'singleton': 0.13994014871344132, 'setsize': 2.675658745612133}
wh [1.618, 2.941, 1.886, 0.459, 1.412]
gap reduction rel -3.520 cond1 False | cond2 sel risk C 0.2372 vs B2+.005 0.1874 False | cond3 CI of (B2 gap - C gap) [-0.0934,0.0025] n_boot 2000 False | cond4 singleton C 0.1870 vs 0.9*B2 0.1709 True
VERDICT LOSS
```

## DEV (fold 9) verbatim numbers
```
G0 acc 0.728125 baseline B2 G1 red 0.8114076418246532
B1 {'cov': 0.7640952197402151, 'gap': 0.13590478025978492, 'sel_risk': 0.33445998092938894, 'singleton': 0.3431337122625828, 'setsize': 1.8625784932157796}
B2 {'cov': 0.8801466498344308, 'gap': 0.019853350165569217, 'sel_risk': 0.1711426538148323, 'singleton': 0.20914668858392357, 'setsize': 2.48334718457743}
C {'cov': 0.8962558098745944, 'gap': 0.003744190125405611, 'sel_risk': 0.18878486138500308, 'singleton': 0.14774275707399182, 'setsize': 2.6440205012008944}
oracleW {'cov': 0.8962558098745944, 'gap': 0.003744190125405611, 'sel_risk': 0.1857974386346437, 'singleton': 0.15011830152135947, 'setsize': 2.6215648268815426}
wh [1.598, 5.2, 1.711, 0.239, 1.996]
```

Notes: DEV predicted conditions 2 and 4 would fail; on TEST condition 2 failed and 4 passed, and condition 1 and 3 failed because the BBSE weight estimate was worse on fold 10 (HYP weight 2.94 vs 5.2 on DEV; oracle weights also gave gap 0.031, above B2 0.012). The candidate won clearly vs B1 on both folds but not vs the stronger Mondrian baseline fixed by DEV. Incremental method (weighted conformal exists in literature). Code hashes: dev193.py b3384f30, test193.py 03790d06; full code of both scripts follows; feature cache kept local.

## feat.py
```python
import numpy as np, pandas as pd, wfdb, os, sys
from scipy.stats import skew, kurtosis
from scipy.signal import welch
BANDS=[(0.5,4),(4,10),(10,20),(20,40)]
def feats(path):
    sig,_=wfdb.rdsamp(path); sig=np.nan_to_num(sig)
    f,P=welch(sig,fs=100,nperseg=256,axis=0)
    out=[]
    for l in range(12):
        x=sig[:,l]
        out+=[x.mean(),x.std(),x.min(),x.max(),skew(x),kurtosis(x)]
        for lo,hi in BANDS:
            m=(f>=lo)&(f<hi); out.append(np.log10(P[m,l].sum()+1e-12))
    return out
if __name__=='__main__':
    d=pd.read_csv('single.csv',index_col=0); d=d[d.strat_fold<=int(sys.argv[1])]
    cache='feat_cache.pkl'; C=pd.read_pickle(cache) if os.path.exists(cache) else {}
    for i,p in d.filename_lr.items():
        if i in C: continue
        b='data/'+p
        if os.path.exists(b+'.dat') and os.path.exists(b+'.hea'):
            try: C[i]=feats(b)
            except Exception as e: pass
    pd.to_pickle(C,cache); print(len(C),'of',len(d))
```

## dev193.py
```python
import numpy as np, pandas as pd, json
from scipy.optimize import nnls
from sklearn.ensemble import HistGradientBoostingClassifier
d=pd.read_csv('single.csv',index_col=0); F=pd.read_pickle('feat_cache.pkl')
d=d[d.index.isin(F.keys())&(d.strat_fold<=9)].copy()
X=np.array([F[i] for i in d.index]); y=d.y.values; fold=d.strat_fold.values
cls=np.array(sorted(set(y))); yi=np.searchsorted(cls,y); K=len(cls)
PI=dict(NORM=.15,MI=.30,STTC=.25,CD=.20,HYP=.10); pis=np.array([PI[c] for c in cls])
tr=fold<=6; ca=(fold>=7)&(fold<=8); dv=fold==9
clf=HistGradientBoostingClassifier(max_iter=200,learning_rate=0.1,max_depth=4,l2_regularization=1.0,random_state=193).fit(X[tr],yi[tr])
P=clf.predict_proba(X); assert list(clf.classes_)==list(range(K))
S=1-P   # S[i,k] score if class k
acc=(P[dv].argmax(1)==yi[dv]).mean(); print('G0 DEV natural acc %.4f'%acc, 'n tr/ca/dv',tr.sum(),ca.sum(),dv.sum())
def qlevel(s,a=0.10):
    n=len(s); k=int(np.ceil((n+1)*(1-a))); return np.inf if k>n else np.sort(s)[k-1]
sc=S[ca,:][np.arange(ca.sum()),yi[ca]]; yc=yi[ca]
qB1=qlevel(sc); qB2=np.array([qlevel(sc[yc==k]) for k in range(K)])
picacal=np.bincount(yc,minlength=K)/len(yc)
def wq(w_rec,sc):
    o=np.argsort(sc); cw=np.cumsum(w_rec[o]); tot=w_rec.sum()+w_rec.max()
    ok=np.where(cw/tot>=0.90)[0]; return sc[o][ok[0]] if len(ok) else np.inf
def shiftw(yv): 
    nat=np.bincount(yv,minlength=K)/len(yv); return (pis/nat)[yv]
def bbse(Pf,wrec):
    pred=Pf.argmax(1); mu=np.bincount(pred,weights=wrec,minlength=K)/wrec.sum()
    Cj=np.zeros((K,K)); pc=P[ca].argmax(1)
    for a,b in zip(pc,yc): Cj[a,b]+=1
    Cj/=len(yc); v,_=nnls(Cj,mu); pit=v*picacal; pit/=pit.sum(); return pit/picacal
def evalset(idx):
    yv=yi[idx]; Pf=P[idx]; w=shiftw(yv); out={}
    wh=bbse(Pf,w); wrec=wh[yc]; qC=wq(wrec,sc)
    wo=pis/picacal; qO=wq(wo[yc],sc)
    for name,qs in [('B1',np.full(K,qB1)),('B2',qB2),('C',np.full(K,qC)),('oracleW',np.full(K,qO))]:
        sets=(1-Pf)<=qs[None,:]
        cov=(w*sets[np.arange(len(yv)),yv]).sum()/w.sum()
        sing=sets.sum(1)==1; wsing=w[sing].sum()/w.sum()
        err=(w[sing]*(~sets[sing,:][np.arange(sing.sum()),yv[sing]])).sum()/max(w[sing].sum(),1e-12)
        out[name]=dict(cov=float(cov),gap=float(abs(cov-0.9)),sel_risk=float(err),singleton=float(wsing),setsize=float((w*sets.sum(1)).sum()/w.sum()))
    out['wh']=wh.round(3).tolist(); return out
r=evalset(np.where(dv)[0])
for k,v in r.items(): print(k,v)
bb='B1' if r['B1']['gap']<=r['B2']['gap'] else 'B2'
red=(r[bb]['gap']-r['C']['gap'])/r[bb]['gap'] if r[bb]['gap']>0 else float('nan')
print('primary baseline',bb,'candidate gap reduction %.3f'%red,'G0',acc>=0.6,'G1',red>=0.25)
json.dump(dict(res=r,acc=float(acc),baseline=bb,red=float(red),n=dict(tr=int(tr.sum()),ca=int(ca.sum()),dv=int(dv.sum()))),open('dev193_result.json','w'))
```

## test193.py
```python
import numpy as np, pandas as pd, json
from scipy.optimize import nnls
from sklearn.ensemble import HistGradientBoostingClassifier
d=pd.read_csv('single.csv',index_col=0); F=pd.read_pickle('feat_cache.pkl')
d=d[d.index.isin(F.keys())].copy(); print('records',len(d), d.strat_fold.value_counts().sort_index().to_dict())
X=np.array([F[i] for i in d.index]); y=d.y.values; fold=d.strat_fold.values; pid=d.patient_id.values
cls=np.array(sorted(set(y))); yi=np.searchsorted(cls,y); K=len(cls)
PI=dict(NORM=.15,MI=.30,STTC=.25,CD=.20,HYP=.10); pis=np.array([PI[c] for c in cls])
tr=fold<=6; ca=(fold>=7)&(fold<=8); te=fold==10
clf=HistGradientBoostingClassifier(max_iter=200,learning_rate=0.1,max_depth=4,l2_regularization=1.0,random_state=193).fit(X[tr],yi[tr])
P=clf.predict_proba(X)
print('TEST natural acc %.4f'%((P[te].argmax(1)==yi[te]).mean()),'n tr/ca/te',tr.sum(),ca.sum(),te.sum())
S=1-P
def qlevel(s,a=0.10):
    n=len(s); k=int(np.ceil((n+1)*(1-a))); return np.inf if k>n else np.sort(s)[k-1]
sc=S[ca,:][np.arange(ca.sum()),yi[ca]]; yc=yi[ca]
qB1=qlevel(sc); qB2=np.array([qlevel(sc[yc==k]) for k in range(K)])
picacal=np.bincount(yc,minlength=K)/len(yc)
def wq(w_rec,sc):
    o=np.argsort(sc); cw=np.cumsum(w_rec[o]); tot=w_rec.sum()+w_rec.max()
    ok=np.where(cw/tot>=0.90)[0]; return sc[o][ok[0]] if len(ok) else np.inf
Cj=np.zeros((K,K)); pc=P[ca].argmax(1)
for a,b in zip(pc,yc): Cj[a,b]+=1
Cj/=len(yc)
def metrics(Pf,yv):
    nat=np.bincount(yv,minlength=K)/len(yv)
    if (nat==0).any(): return None
    w=(pis/nat)[yv]
    mu=np.bincount(Pf.argmax(1),weights=w,minlength=K)/w.sum()
    v,_=nnls(Cj,mu); pit=v*picacal; pit/=pit.sum(); wh=pit/picacal
    qC=wq(wh[yc],sc); qO=wq((pis/picacal)[yc],sc)
    out={}
    for name,qs in [('B1',np.full(K,qB1)),('B2',qB2),('C',np.full(K,qC)),('oracleW',np.full(K,qO))]:
        sets=(1-Pf)<=qs[None,:]; n=len(yv)
        cov=(w*sets[np.arange(n),yv]).sum()/w.sum(); sing=sets.sum(1)==1
        err=(w[sing]*(~sets[sing,:][np.arange(sing.sum()),yv[sing]])).sum()/max(w[sing].sum(),1e-12)
        out[name]=dict(cov=float(cov),gap=float(abs(cov-0.9)),sel_risk=float(err),singleton=float(w[sing].sum()/w.sum()),setsize=float((w*sets.sum(1)).sum()/w.sum()))
    out['wh']=wh.round(3).tolist(); return out
it=np.where(te)[0]; r=metrics(P[it],yi[it])
for k,v in r.items(): print(k,v)
bb='B2'  # fixed by DEV
c1=(r[bb]['gap']-r['C']['gap'])/r[bb]['gap']
cond1=c1>=0.25; cond2=r['C']['sel_risk']<=r[bb]['sel_risk']+0.005; cond4=r['C']['singleton']>=0.9*r[bb]['singleton']
# paired patient-cluster bootstrap
rng=np.random.default_rng(193); pats=pd.Series(it).groupby(pid[it]).apply(list); pl=list(pats.values); npat=len(pl)
red=[]
for b in range(2000):
    ch=rng.integers(0,npat,npat); idx=np.concatenate([pl[i] for i in ch]); m=metrics(P[idx],yi[idx])
    if m is not None: red.append(m[bb]['gap']-m['C']['gap'])
lo,hi=np.percentile(red,[2.5,97.5]); cond3=lo>0
print('gap reduction rel %.3f cond1 %s | cond2 sel risk C %.4f vs B2+.005 %.4f %s | cond3 CI of (B2 gap - C gap) [%.4f,%.4f] n_boot %d %s | cond4 singleton C %.4f vs 0.9*B2 %.4f %s'%(c1,cond1,r['C']['sel_risk'],r[bb]['sel_risk']+0.005,cond2,lo,hi,len(red),cond3,r['C']['singleton'],0.9*r[bb]['singleton'],cond4))
verdict='WIN' if (cond1 and cond2 and cond3 and cond4) else ('LOSS' if r['C']['gap']>r[bb]['gap'] else 'NULL')
print('VERDICT',verdict)
json.dump(dict(res=r,conds=dict(c1=bool(cond1),c2=bool(cond2),c3=bool(cond3),c4=bool(cond4)),ci=[float(lo),float(hi)],verdict=verdict,rel=float(c1)),open('test193_result.json','w'))
```
