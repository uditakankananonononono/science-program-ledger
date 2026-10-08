#!/usr/bin/env python3
"""Unit 184 ASZED runner. Hash-bound to prereg.md via LOCK.json. Unit of analysis = dataset Subject_N ID."""
import sys, os, re, json, hashlib, zipfile, csv, collections, argparse, warnings
import numpy as np
from scipy.stats import rankdata
warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, "work")
ZIP = os.environ.get("ASZED_ZIP", "/tmp/aszed/aszed.zip")
ZIP_MD5 = "0e684f6c308c71ab59c7e3475c628691"
GROUPS_CSV = os.path.join(ROOT, "source-subject-groups.csv")
CH = ["Fp1","Fp2","F3","F4","C3","C4","P3","P4","O1","O2","F7","F8","T3","T4","T5","T6","Fz","Cz","Pz"]
BANDS = [("delta",1,4),("theta",4,8),("alpha",8,13),("beta",13,30),("gamma",30,40)]
SUBSET_INFO = {"subset_1":("1.1","arith0","CONTEK-KT2400"),"subset_2":("1.2","arith1","DISCOVERY-24E"),"subset_3":("1.2","arith0","DISCOVERY-24E")}
DEVICE_CODE = {"CONTEK-KT2400":0,"DISCOVERY-24E":1}
SPLIT_SEED = int(hashlib.sha256(b"unit184|aszed|split|v1").hexdigest()[:8],16)
MODEL_SEED = 184
TEST_FRAC = 0.30
WIN = 0.03
N_REP_DEV = 3
N_PERM = 60
N_BOOT = 2000
GRID = [(fs,c) for fs in ("BP","BPSP") for c in (0.01,0.1,1.0)]
BASELINES = ["B1_agesex","B2_bandmean","B3_RF"]

def sha(p):
    return hashlib.sha256(open(p,"rb").read()).hexdigest()

def check_lock():
    lk = os.path.join(ROOT,"LOCK.json")
    if not os.path.exists(lk): sys.exit("NO LOCK.json: outcome stages refused")
    L = json.load(open(lk))
    me = sha(os.path.abspath(__file__)); pr = sha(os.path.join(ROOT,"prereg.md"))
    if L["run_py_sha256"]!=me or L["prereg_sha256"]!=pr: sys.exit("HASH MISMATCH vs LOCK.json")
    txt = open(os.path.join(ROOT,"prereg.md")).read()
    if me not in txt: sys.exit("prereg.md does not embed run.py hash")
    if not os.path.exists(os.path.join(ROOT,"VERIFIED.txt")): sys.exit("VERIFIED.txt (main verification) missing")
    print("LOCK OK", me[:12], pr[:12])

# ---------------- data ----------------
def load_groups():
    rows = list(csv.DictReader(open(GROUPS_CSV)))
    return {int(r["source_subject_id"]): r for r in rows}

def list_edfs(z):
    out = collections.defaultdict(list)
    for n in z.namelist():
        m = re.match(r"ASZED/version_1\.1/node_1/(subset_\d)/subject_(\d+)/(.*\.edf)$", n)
        if m: out[int(m[2])].append((m[1], n))
    return out

def cmd_tab():
    G = load_groups(); z = zipfile.ZipFile(ZIP); E = list_edfs(z)
    assert set(E)==set(G) and len(G)==153
    print("label by exact subset membership"); c=collections.Counter()
    for i,fl in E.items(): c[(tuple(sorted({s for s,_ in fl})), G[i]["category"])]+=1
    for k,v in sorted(c.items()): print(" ",k,v)
    print("label by device"); c=collections.Counter()
    for i,fl in E.items():
        dev = {SUBSET_INFO[s][2] for s,_ in fl}; assert len(dev)==1
        c[(dev.pop(),G[i]["category"])]+=1
    for k,v in sorted(c.items()): print(" ",k,v)
    print("label by protocol"); c=collections.Counter()
    for i,fl in E.items():
        p = {SUBSET_INFO[s][0] for s,_ in fl}; assert len(p)==1
        c[(p.pop(),G[i]["category"])]+=1
    for k,v in sorted(c.items()): print(" ",k,v)
    print("label by arithmetic annotation (IDs in both subsets 2 and 3 counted as 'arith1+arith0')"); c=collections.Counter()
    for i,fl in E.items(): c[("+".join(sorted({SUBSET_INFO[s][1] for s,_ in fl})),G[i]["category"])]+=1
    for k,v in sorted(c.items()): print(" ",k,v)

def read_edf(b):
    ns = int(b[252:256]); nrec = int(b[236:244]); dur = float(b[244:252])
    off = 256
    def fld(w,i0): 
        return [b[i0+i*w:i0+(i+1)*w] for i in range(ns)]
    p = 256
    labels=[x.decode("latin1").strip() for x in fld(16,p)]; p+=16*ns
    p+=80*ns; p+=8*ns
    pmin=np.array([float(x) for x in fld(8,p)]); p+=8*ns
    pmax=np.array([float(x) for x in fld(8,p)]); p+=8*ns
    dmin=np.array([float(x) for x in fld(8,p)]); p+=8*ns
    dmax=np.array([float(x) for x in fld(8,p)]); p+=8*ns
    p+=80*ns
    nsamp=np.array([int(x) for x in fld(8,p)]); p+=8*ns
    hdr_len = 256*(ns+1)
    tot = nsamp.sum()
    nrec_eff = min(nrec,(len(b)-hdr_len)//(2*tot))
    d = np.frombuffer(b,dtype="<i2",count=nrec_eff*tot,offset=hdr_len).reshape(nrec_eff,tot)
    sig={}; c0=0
    for k in range(ns):
        if not labels[k].startswith("EDF Annotations"):
            x = d[:,c0:c0+nsamp[k]].reshape(-1).astype(np.float64)
            g = (pmax[k]-pmin[k])/(dmax[k]-dmin[k]); x = (x-dmin[k])*g+pmin[k]
            sig[labels[k]] = (x, nsamp[k]/dur)
        c0+=nsamp[k]
    return sig

def chname(l):
    l = re.sub(r"\[\d+\]","",l); l=re.sub(r"^EEG\s+","",l); l=re.sub(r"-LE$","",l)
    return l.strip()

PTP_REJECT_UV = 1e12  # amplitude rejection disabled (saturated IDs exist, e.g. subject_82); flatline rule only
def file_feats(sig):
    m = {chname(k):v for k,v in sig.items()}
    if not all(c in m for c in CH): return None
    fs = {m[c][1] for c in CH}
    if len(fs)!=1: return None
    fs = int(round(fs.pop()))
    L = min(len(m[c][0]) for c in CH)
    X = np.stack([m[c][0][:L] for c in CH]); X = X - X.mean(0,keepdims=True)  # common average reference over the 19 channels
    w = 2*fs; hop = fs
    if L < w: return None
    win = np.hanning(w); fr = np.fft.rfftfreq(w,1.0/fs); scale = 2.0/(fs*np.sum(win**2))
    acc=[]; nrej=0
    for s in range(0,L-w+1,hop):
        seg = X[:,s:s+w]; seg = seg-seg.mean(1,keepdims=True)
        if np.ptp(seg,axis=1).max()>PTP_REJECT_UV or seg.std(1).min()<0.05: nrej+=1; continue
        acc.append(np.abs(np.fft.rfft(seg*win,axis=1))**2*scale)
    if len(acc)<2: return None, nrej
    P = np.mean(acc,axis=0)
    tm = (fr>=1)&(fr<40)
    tot = P[:,tm].sum(1)
    bp = np.stack([P[:,(fr>=lo)&(fr<hi)].sum(1)/tot for _,lo,hi in BANDS],axis=1)  # ch x band
    p = P[:,tm]/tot[:,None]
    ent = -(p*np.log(p+1e-12)).sum(1)/np.log(tm.sum())
    am = (fr>=6)&(fr<=13); paf = fr[am][np.argmax(P[:,am],axis=1)]
    sp = np.stack([ent,paf,np.log(tot)],axis=1)
    return (np.log(bp+1e-12).reshape(-1), sp.reshape(-1), len(acc), nrej, fs)

def cmd_features():
    G = load_groups(); z = zipfile.ZipFile(ZIP); E = list_edfs(z)
    ids = sorted(E); BP=[];SP=[];dev=[];sub=[];age=[];sex=[];nfiles=[];nwin=[];nskip=[];nrejw=[];fsl=collections.Counter()
    for i in ids:
        tb=np.zeros(len(CH)*len(BANDS)); ts=np.zeros(len(CH)*3); W=0; nf=0; skip=0; rej=0
        for s,n in sorted(E[i],key=lambda t:t[1]):
            r = file_feats(read_edf(z.read(n)))
            if r is None: skip+=1; continue
            if len(r)==2: skip+=1; rej+=r[1]; continue
            b,sp,na,nr,fs = r; tb+=na*b; ts+=na*sp; W+=na; nf+=1; rej+=nr; fsl[fs]+=1
        assert W>0, i
        BP.append(tb/W); SP.append(ts/W); nwin.append(W); nfiles.append(nf); nskip.append(skip); nrejw.append(rej)
        dv={SUBSET_INFO[s][2] for s,_ in E[i]}.pop(); dev.append(DEVICE_CODE[dv])
        sub.append("+".join(sorted({s for s,_ in E[i]})))
        age.append(float(G[i]["age"])); sex.append(1.0 if G[i]["sex"]=="M" else 0.0)
        print(i,nf,skip,W,flush=True) if i%20==0 else None
    np.savez(os.path.join(WORK,"features.npz"),ids=np.array(ids),BP=np.array(BP),SP=np.array(SP),dev=np.array(dev),sub=np.array(sub),age=np.array(age),sex=np.array(sex),nfiles=np.array(nfiles),nwin=np.array(nwin),nskip=np.array(nskip),nrej=np.array(nrejw))
    print("fs counts used",dict(fsl),"files used",sum(nfiles),"skipped",sum(nskip),"rejected windows",sum(nrejw),"accepted windows",sum(nwin))

def load_all():
    F = np.load(os.path.join(WORK,"features.npz")); G = load_groups()
    ids = F["ids"]; y = np.array([1 if G[int(i)]["category"]=="Patient" else 0 for i in ids])
    return F, ids, y

def make_split(ids, dev, y):
    """House convention: sort IDs; DEV = even positions, TEST = odd positions (ID is the cluster; never split within an ID)."""
    order=np.argsort(ids); test=np.zeros(len(ids),bool); test[order[1::2]]=True
    return test

# ---------------- models ----------------
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold

def zdev(Xtr,dtr,Xte,dte):
    A=Xtr.copy(); B=Xte.copy()
    for d in (0,1):
        m=Xtr[dtr==d].mean(0); s=Xtr[dtr==d].std(0)+1e-8
        A[dtr==d]=(Xtr[dtr==d]-m)/s; B[dte==d]=(Xte[dte==d]-m)/s
    return A,B

def feats(F,name):
    BP=F["BP"]; SP=F["SP"]
    if name.startswith("G"):
        fs=name.split("_")[0][1:]
        return BP if fs=="BP" else np.hstack([BP,SP])
    if name=="B1_agesex": return np.stack([F["age"],F["sex"]],1)
    if name=="B2_bandmean": return BP.reshape(len(BP),len(CH),len(BANDS)).mean(1)
    if name=="B3_RF": return BP
    raise KeyError(name)

def fit_predict(name,X,dev,y,tr,te):
    Xtr,Xte=X[tr],X[te]
    if name=="B1_agesex":
        m=Xtr.mean(0);s=Xtr.std(0)+1e-8; Xtr=(Xtr-m)/s; Xte=(Xte-m)/s
    else:
        Xtr,Xte=zdev(Xtr,dev[tr],Xte,dev[te])
    if name=="B3_RF":
        mdl=RandomForestClassifier(n_estimators=300,min_samples_leaf=2,random_state=MODEL_SEED,n_jobs=1)
    else:
        C = float(name.split("_C")[1]) if name.startswith("G") else 1.0
        mdl=LogisticRegression(C=C,max_iter=5000)
    mdl.fit(Xtr,y[tr]); return mdl.predict_proba(Xte)[:,1]

def auc(y,s):
    if len(set(y))<2: return np.nan
    r=rankdata(s); n1=y.sum(); n0=len(y)-n1
    return (r[y==1].sum()-n1*(n1+1)/2)/(n1*n0)

def macro_auc(y,s,dev):
    return float(np.nanmean([auc(y[dev==d],s[dev==d]) for d in (0,1)]))

def fold_metric(folds):
    return float(np.nanmean([f[2] for f in folds]))

def model_names(): return [f"G{fs}_C{c}" for fs,c in GRID]+BASELINES

def cv_scores(name,X,dev,y,rep,perm_y=None):
    yy = y if perm_y is None else perm_y
    strata = dev*2+yy; oof=np.zeros(len(yy)); folds=[]
    skf=StratifiedKFold(5,shuffle=True,random_state=MODEL_SEED+rep)
    for k,(tr,te) in enumerate(skf.split(X,strata)):
        s=fit_predict(name,X,dev,yy,tr,te); oof[te]=s
        folds.append((k,te,macro_auc(yy[te],s,dev[te]),[auc(yy[te][dev[te]==d],s[dev[te]==d]) for d in (0,1)]))
    return oof,folds

def dev_part():
    F,ids,y=load_all(); dev=F["dev"]; test=make_split(ids,dev,y); d=~test
    return F,ids,y,dev,test,d

def sub(F,d):
    return {k:F[k][d] for k in ("BP","SP","age","sex")}

# ---------------- stages ----------------
def cmd_split():
    F,ids,y,dev,test,d=dev_part()
    print("DEV n",d.sum(),"TEST n",test.sum(),"rule: sorted IDs, even positions DEV, odd positions TEST")
    for nm,m in (("DEV",d),("TEST",test)):
        for dv in (0,1):
            for l in (0,1): print(nm,"device",dv,"label",l,int((m&(dev==dv)&(y==l)).sum()))
    print("DEV id sha256",hashlib.sha256(",".join(map(str,ids[d])).encode()).hexdigest())
    print("TEST id sha256",hashlib.sha256(",".join(map(str,ids[test])).encode()).hexdigest())

def hm_se(a,n1,n0):
    q1=a/(2-a);q2=2*a*a/(1+a)
    return float(np.sqrt((a*(1-a)+(n1-1)*(q1-a*a)+(n0-1)*(q2-a*a))/(n1*n0)))

def cmd_power():
    F,ids,y,dev,test,d=dev_part()
    print("label-free design facts: units=153 IDs; files/ID median",int(np.median(F["nfiles"])),"- files add no independent units; analysis rows = 1 per ID (cluster-collapsed)")
    cnt={dv:(int((test&(dev==dv)&(y==1)).sum()),int((test&(dev==dv)&(y==0)).sum())) for dv in (0,1)}
    print("TEST (patient,control) by device",cnt)
    for a in (0.60,0.65,0.70,0.75):
        se=np.sqrt(sum(hm_se(a,*cnt[dv])**2 for dv in (0,1)))/2
        print(f"macro within-device AUC {a}: HM SE {se:.3f}; 95% half-width {1.96*se:.3f}")
    se=np.mean([np.sqrt(sum(hm_se(a,*cnt[dv])**2 for dv in (0,1)))/2 for a in (0.55,0.65)])
    for r in (0.3,):
        sd=np.sqrt(2*se**2*(1-r)); print(f"paired diff SE (r={r}) ~{sd:.3f}; approx 80% power min detectable diff (one-sided .025) ~{(1.96+0.84)*sd:.3f}")

def run_all_models_perm(X_by,dev,y,nperm,seed):
    rng=np.random.default_rng(seed); res={n:[] for n in model_names()}
    for p in range(nperm):
        yp=y.copy()
        for dv in (0,1):
            idx=np.where(dev==dv)[0]; yp[idx]=rng.permutation(y[idx])
        for n in model_names():
            oof,fo=cv_scores(n,X_by[n],dev,y,0,perm_y=yp); res[n].append(fold_metric(fo))
    return res

def cmd_perm(stage_tag):
    F,ids,y,dev,test,d=dev_part()
    Fd=sub(F,d); X_by={n:feats(Fd,n) for n in model_names()}
    res=run_all_models_perm(X_by,dev[d],y[d],N_PERM,SPLIT_SEED%100000)
    ok=True; print("PERM gate (",N_PERM,"label permutations within device, DEV only, every grid member + baselines); pass iff |mean-0.5|<=0.03")
    for n,v in res.items():
        m=float(np.mean(v)); okm=abs(m-0.5)<=0.03; ok&=okm
        print(f"  {n:14s} mean {m:.4f} sd {np.std(v):.4f} min {min(v):.3f} max {max(v):.3f} {'PASS' if okm else 'FAIL'}")
    print("PERM GATE","PASS" if ok else "FAIL")
    # TEST-side smoke: DEV labels and TEST labels both shuffled within device; fit on shuffled DEV, score shuffled TEST. No real outcome used.
    rng=np.random.default_rng(SPLIT_SEED%100000+1); tres={n:[] for n in model_names()}
    tr=np.where(d)[0]; te=np.where(test)[0]
    for p in range(N_PERM):
        yp=y.copy()
        for msk in (d,test):
            for dv in (0,1):
                idx=np.where(msk&(dev==dv))[0]; yp[idx]=rng.permutation(y[idx])
        for n in model_names():
            sc=fit_predict(n,feats(F,n),dev,yp,tr,te); tres[n].append(macro_auc(yp[te],sc,dev[te]))
    print("TEST-side PERM smoke (both splits shuffled within device, 60 perms); pass iff |mean-0.5|<=0.04")
    for n,v in tres.items():
        m=float(np.mean(v)); okm=abs(m-0.5)<=0.04; ok&=okm
        print(f"  {n:14s} mean {m:.4f} sd {np.std(v):.4f} {'PASS' if okm else 'FAIL'}")
    print("PERM GATE (DEV+TEST smoke)","PASS" if ok else "FAIL")
    if stage_tag=="outcome": return ok

def cmd_dev():
    check_lock()
    F,ids,y,dev,test,d=dev_part(); Fd=sub(F,d); yd=y[d]; dd=dev[d]
    ok=cmd_perm("outcome")
    X_by={n:feats(Fd,n) for n in model_names()}; dev_m={}; folds0={}
    for n in model_names():
        ms=[]
        for rep in range(N_REP_DEV):
            oof,fo=cv_scores(n,X_by[n],dd,yd,rep); ms.append(fold_metric(fo))
            if rep==0: folds0[n]=fo; 
        dev_m[n]=float(np.mean(ms)); print(f"DEV {n:14s} macro within-device AUC per rep {np.round(ms,3)} mean {dev_m[n]:.4f}")
    print("per-fold checkpoints (rep 0): fold, n_test, AUC contek, AUC discovery, macro")
    for n in model_names():
        for k,te,m,pd in folds0[n]: print(f"  {n:14s} fold{k} n={len(te)} {np.round(pd,3)} macro {m:.3f}")
    grid_names=[f"G{fs}_C{c}" for fs,c in GRID]
    sel=max(grid_names,key=lambda n:dev_m[n]); bstar=max(BASELINES,key=lambda n:dev_m[n])
    print("SELECTED",sel,dev_m[sel],"STRONGEST BASELINE",bstar,dev_m[bstar])
    head = (dev_m[bstar]<1-2*WIN) and (dev_m[bstar]>=0.55)
    print("HEADROOM GATE","PASS" if head else "DROP", f"(baseline {dev_m[bstar]:.4f}; need 0.55<=b<{1-2*WIN:.2f})")
    # confound illustration + device-transfer sensitivity (DEV only)
    oof,_=cv_scores(sel,X_by[sel],dd,yd,0); print("pooled (device-confounded) OOF AUC selected",round(auc(yd,oof),4),"| device-only score AUC (device 0 -> patient)",round(auc(yd,1-dd.astype(float)),4))
    for a,b in ((0,1),(1,0)):
        tr=np.where(dd==a)[0]; te=np.where(dd==b)[0]
        Xs=X_by[sel]; ma,sa=Xs[tr].mean(0),Xs[tr].std(0)+1e-8; mb,sb=Xs[te].mean(0),Xs[te].std(0)+1e-8  # each device z-scored with its own rows (label-free)
        mdl=LogisticRegression(C=float(sel.split("_C")[1]),max_iter=5000).fit((Xs[tr]-ma)/sa,yd[tr]); s=mdl.predict_proba((Xs[te]-mb)/sb)[:,1]; print(f"S1 device transfer train device {a} -> test device {b}: AUC {auc(yd[te],s):.3f} (n_te {len(te)})")
    json.dump({"sel":sel,"bstar":bstar,"dev":dev_m,"headroom":bool(head),"perm_ok":bool(ok)},open(os.path.join(WORK,"dev_result.json"),"w"))
    print("TEST OPEN ALLOWED:", bool(head and ok))

def cmd_test():
    check_lock(); R=json.load(open(os.path.join(WORK,"dev_result.json")))
    assert R["headroom"] and R["perm_ok"], "gates not passed"
    F,ids,y,dev,test,d=dev_part(); sel,b=R["sel"],R["bstar"]
    Fd=sub(F,d); Ft=sub(F,test); yt=y[test]; dt=dev[test]; res={}
    for n in model_names():
        Xall=feats(F,n); tr=np.where(d)[0]; te=np.where(test)[0]
        res[n]=fit_predict(n,Xall,dev,y,tr,te)
    rng=np.random.default_rng(MODEL_SEED); strata=dt*2+yt
    def stat(ix,n): return macro_auc(yt[ix],res[n][ix],dt[ix])
    allix=np.arange(len(yt)); pt={n:stat(allix,n) for n in model_names()}
    bd=[];bc=[];bb=[]
    for _ in range(N_BOOT):
        ix=np.concatenate([rng.choice(np.where(strata==s)[0],(strata==s).sum()) for s in np.unique(strata)])
        c=stat(ix,sel); bb_=stat(ix,b); bc.append(c); bb.append(bb_); bd.append(c-bb_)
    lo=lambda v:float(np.nanpercentile(v,2.5)); hi=lambda v:float(np.nanpercentile(v,97.5))
    diff=pt[sel]-pt[b]
    print("TEST macro within-device AUC (all models):",{n:round(v,3) for n,v in pt.items()})
    print(f"selected {sel} {pt[sel]:.3f} CI [{lo(bc):.3f},{hi(bc):.3f}]; baseline {b} {pt[b]:.3f} CI [{lo(bb):.3f},{hi(bb):.3f}]")
    print(f"diff {diff:.3f} CI [{lo(bd):.3f},{hi(bd):.3f}] (ID-cluster bootstrap, stratified device x label, {N_BOOT} reps)")
    lab = "WIN" if (diff>=WIN and lo(bd)>0) else ("NEGATIVE" if hi(bd)<0 else "NULL")
    print("VERDICT:",lab,"(WIN: diff>=0.03 and CI lower>0; NEGATIVE: CI upper<0; else NULL; no re-banding)")
    for dv in (0,1): print(f"per-device TEST AUC selected device {dv}: {auc(yt[dt==dv],res[sel][dt==dv]):.3f}; baseline: {auc(yt[dt==dv],res[b][dt==dv]):.3f}")

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("stage"); a=ap.parse_args()
    os.makedirs(WORK,exist_ok=True)
    if a.stage in ("tab","features","split","power","perm_smoke"):
        import hashlib as _h
        h=_h.md5()
        if a.stage in ("tab","features"):
            with open(ZIP,"rb") as f:
                for blk in iter(lambda:f.read(1<<22),b""): h.update(blk)
            assert h.hexdigest()==ZIP_MD5,"archive md5 mismatch"; print("archive md5 OK",ZIP_MD5)
    {"tab":cmd_tab,"features":cmd_features,"split":cmd_split,"power":cmd_power,"perm_smoke":lambda:cmd_perm("smoke"),"dev":cmd_dev,"test":cmd_test}[a.stage]()
