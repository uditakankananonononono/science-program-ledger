"""BatchSentinel: phase-aligned z / Isolation Forest / dense autoencoder ensemble on IndPenSim (locked protocol)."""
import numpy as np, pandas as pd, json, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0,'tool'); from load import load
from sklearn.ensemble import IsolationForest
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
FEAT="Fg RPM Fs Fa Fb Fc Fh Fw pressure Fremoved DO2 V Wt pH T Q CO2outgas Fpaa Foil OUR O2 CER NH3_shots".split()
d=load(); d=d.sort_values(["Batch_ID","Time"])
rng=np.random.default_rng(0); split={}
for lo in (1,31,61):
    ids=rng.permutation(np.arange(lo,lo+30)); split.update({int(i):"train" for i in ids[:15]}); split.update({int(i):"cal" for i in ids[15:20]}); split.update({int(i):"test" for i in ids[20:]})
for i in range(91,101): split[i]="fault"
B={b:g.reset_index(drop=True) for b,g in d.groupby("Batch_ID")}
tr=[b for b,s in split.items() if s=="train"]
# (a) phase-aligned z
bins=np.arange(0,400,2.0)
T=pd.concat([B[b] for b in tr]); T["bin"]=np.digitize(T.Time,bins)
mu=T.groupby("bin")[FEAT].mean(); sd=T.groupby("bin")[FEAT].std().clip(lower=1e-6)
gsd=T[FEAT].std().clip(lower=1e-6); sd=sd.clip(lower=0.01*gsd,axis=1)
Pm=T.groupby("bin")["P"].mean(); Ps=T.groupby("bin")["P"].std().clip(lower=1e-6)
def zmat(g):
    bi=np.clip(np.digitize(g.Time,bins),mu.index.min(),mu.index.max()); m=mu.reindex(bi).ffill().bfill().values; s=sd.reindex(bi).ffill().bfill().values
    return (g[FEAT].values-m)/s, bi
def win(g,z):
    W=5; Z=np.nan_to_num(z,nan=0.0,posinf=50,neginf=-50).clip(-50,50); out=[]
    for i in range(len(Z)):
        w=Z[max(0,i-W+1):i+1]; out.append(np.r_[w.mean(0),w[-1]-w[0],w.std(0)])
    return np.array(out)
Zs={b:zmat(B[b])[0] for b in B}; Wf={b:win(B[b],Zs[b]) for b in B}
Xtr=np.vstack([Wf[b] for b in tr]); sc=StandardScaler().fit(Xtr); Xs=sc.transform(Xtr)
iso=IsolationForest(n_estimators=200,random_state=0).fit(Xs)
sub=rng.choice(len(Xs),min(20000,len(Xs)),replace=False)
ae=MLPRegressor(hidden_layer_sizes=(32,8,32),max_iter=60,random_state=0).fit(Xs[sub],Xs[sub])
def raw_scores(b):
    z=np.nan_to_num(Zs[b],nan=0.0).clip(-50,50); X=sc.transform(Wf[b])
    return {"z":np.sqrt((z**2).mean(1)),"iso":-iso.score_samples(X),"ae":((ae.predict(X)-X)**2).mean(1)}
S={b:raw_scores(b) for b in B}
cal=[b for b,s in split.items() if s=="cal"]
ref={k:np.sort(np.concatenate([S[b][k] for b in cal])) for k in ["z","iso","ae"]}
def ens(b): return np.max([np.searchsorted(ref[k],S[b][k])/len(ref[k]) for k in ref],axis=0)
def events(sc_,th,k=3):
    a=sc_>th; ev=[]; run=0
    for i,x in enumerate(a):
        run=run+1 if x else 0
        if run==k: ev.append(i)
    return ev
def rate(th,ids,key): return np.mean([len(events(ens(b) if key=="ens" else S[b][key],th)) for b in ids])
res={"split":split}
for key in ["ens","z","iso","ae"]:
    grid=np.unique(np.concatenate([np.linspace(0.9,1.0001,200)] if key=="ens" else [np.quantile(ref[key],np.linspace(0.9,1,200)),[ref[key][-1]*1.5,ref[key][-1]*3]]))
    th=next((t for t in grid if rate(t,cal,key)<=0.5),grid[-1])
    sc_f=lambda b:ens(b) if key=="ens" else S[b][key]
    test=[b for b,s in split.items() if s=="test"]
    fa_nom=[len(events(sc_f(b),th)) for b in test]
    per=[]
    for b in range(91,101):
        g=B[b]; fw=np.where(g.Fault_ref.values!=0)[0]; on,off=fw[0],fw[-1]; ev=events(sc_f(b),th)
        pre=[e for e in ev if e<on]; hit=[e for e in ev if on<=e<=off]
        bi=np.clip(np.digitize(g.Time,bins),Pm.index.min(),Pm.index.max()); pz=np.abs(g.P.values-Pm.reindex(bi).ffill().bfill().values)/Ps.reindex(bi).ffill().bfill().values
        man=None; run=0
        for i in range(on,len(g)):
            run=run+1 if pz[i]>3 else 0
            if run==3: man=i-2; break
        tman=g.Time.iloc[man] if man is not None else g.Time.iloc[-1]; dur=g.Time.iloc[-1]-g.Time.iloc[0]
        ta=g.Time.iloc[hit[0]] if hit else None
        per.append(dict(batch=b,onset_h=float(g.Time.iloc[on]),window_end_h=float(g.Time.iloc[off]),detected=bool(hit),first_alarm_h=None if ta is None else float(ta),
            delay_h=None if ta is None else float(ta-g.Time.iloc[on]),manifest_h=float(tman),manifest_observed=man is not None,
            lead_frac=None if ta is None else float((tman-ta)/dur),pre_onset_alarms=len(pre)))
    det=np.mean([p["detected"] for p in per]); fa=(sum(fa_nom)+sum(p["pre_onset_alarms"] for p in per))/(len(test)+10)
    leads=[p["lead_frac"] for p in per if p["lead_frac"] is not None]
    res[key]=dict(threshold=float(th),cal_fa_per_batch=float(rate(th,cal,key)),test_nominal_fa_per_batch=float(np.mean(fa_nom)),fa_per_batch_all=float(fa),
        detection_rate=float(det),median_lead_frac=float(np.median(leads)) if leads else None,per_batch=per)
e=res["ens"]; res["G1"]=dict(detection=e["detection_rate"],fa_per_batch=e["fa_per_batch_all"],pass_=e["detection_rate"]>=0.9 and e["fa_per_batch_all"]<=1)
res["G2"]=dict(median_lead_frac=e["median_lead_frac"],pass_=(e["median_lead_frac"] or -1)>=0.2)
json.dump(res,open("results/results.json","w"),indent=1)
for k in ["ens","z","iso","ae"]: print(k,{x:res[k][x] for x in ["threshold","cal_fa_per_batch","test_nominal_fa_per_batch","fa_per_batch_all","detection_rate","median_lead_frac"]})
print(res["G1"],res["G2"])
for p in res["ens"]["per_batch"]: print(p)
