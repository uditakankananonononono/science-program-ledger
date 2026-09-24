import numpy as np, json
rng=np.random.default_rng(24)
G=2000
mu=np.exp(rng.normal(3,1.2,G))
gc=rng.uniform(0.3,0.7,G)
de=np.zeros(G,bool); dehi=np.zeros(G,bool)
hi=np.where(gc>0.6)[0]; lo=np.where((gc>=0.45)&(gc<=0.55))[0]
dehi[rng.choice(hi,50,replace=False)]=True
de[rng.choice(lo,50,replace=False)]=True
true_lfc=np.zeros(G); true_lfc[de|dehi]=1.0  # log2(2x)=1
bias=np.exp(3*(gc-0.5))
depth=2_000_000
lam=mu/mu.sum()*bias; lam/=lam.sum()
def simrep():
    m=depth*lam
    # negative binomial via gamma-poisson, dispersion 0.1
    g=rng.gamma(1/0.1,0.1*m)
    return rng.poisson(g)
def condition(de_mask):
    lam2=lam.copy(); lam2[de_mask]*=2; lam2/=lam2.sum()
    m=depth*lam2
    g=rng.gamma(1/0.1,0.1*m)
    return rng.poisson(g)
ctl=np.array([simrep() for _ in range(3)])
trt=np.array([condition(de|dehi) for _ in range(3)])
cpm=lambda x: x/x.sum()*1e6
lc=np.log2(cpm(ctl).mean(axis=0)+0.5); lt=np.log2(cpm(trt).mean(axis=0)+0.5)
raw=lt-lc
# conditional-median correction on control log-CPM (per-sample then average offset)
bins=np.digitize(gc,np.linspace(0.3,0.7,21))-1
off=np.zeros(G)
base=np.log2(cpm(ctl).mean(axis=0)+0.5)
gm=np.median(base)
for b in range(20):
    msk=bins==b
    off[msk]=np.median(base[msk])-gm
corr=raw - 0*off  # correction applies to both conditions equally: subtract offset from each condition
corr=(lc-off)-(lt-off)  # = raw! -> correction must be per-sample GC curve, not canceling...
# PROPER: estimate offset from AVERAGE of both conditions per gene? Standard: within-sample loess of M on GC.
# Use average of ctl+trt logCPM as offset estimate (DE genes are 5%, median robust)
avg=(lc+lt)/2
off2=np.zeros(G)
gm2=np.median(avg)
for b in range(20):
    msk=bins==b
    off2[msk]=np.median(avg[msk])-gm2
corr=raw # lfc itself is offset-free if bias identical across conditions!
# Note: bias b(GC) cancels in the LFC between conditions when identical in both. The bias shows in ABSOLUTE expression.
# Evaluate absolute-expression recovery: logCPM vs truth log mu
est_raw=lt; est_corr=lt-off2
truth=np.log2(mu/mu.sum()*1e6+0.5)
def gccor(x): return np.corrcoef(gc[nonde],x)[0,1]
nonde=~(de|dehi)
res={}
res['gc_corr_raw']=float(gccor(est_raw[nonde]))
res['gc_corr_corr']=float(gccor(est_corr[nonde]))
res['raw_minus_truth_corr']=float(np.corrcoef(est_raw[nonde],truth[nonde])[0,1])
res['corr_minus_truth_corr']=float(np.corrcoef(est_corr[nonde],truth[nonde])[0,1])
# DE recovery on LFC (bias cancels in LFC - G4 tests this)
res['lfc_neutral_med']=float(np.median(raw[de]))
res['lfc_hi_med']=float(np.median(raw[dehi]))
res['lfc_neutral_within']=float(np.mean(np.abs(raw[de]-1)<=0.3))
res['lfc_hi_within']=float(np.mean(np.abs(raw[dehi]-1)<=0.3))
# absolute recovery within tol: est vs truth offset by median difference
def within(est):
    d=est-truth; d-=np.median(d[nonde])
    return float(np.mean(np.abs(d[de])<=np.log2(2)*0.3/1)), float(np.mean(np.abs(d[dehi])<=np.log2(2)*0.3/1)), float(np.mean(np.abs(d[nonde])<=0.3))
res['abs_raw']=within(est_raw); res['abs_corr']=within(est_corr)
json.dump(res,open('results/pivot_metrics.json','w'),indent=1)
print(json.dumps(res,indent=1))
