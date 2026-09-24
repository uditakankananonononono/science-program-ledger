import numpy as np, json
from scipy.stats import norm
from scipy.optimize import curve_fit
rng=np.random.default_rng(1)
NSNP=200; D=5000; LAM=50000.0
pos=np.arange(NSNP)*D
maf=rng.uniform(0.1,0.4,NSNP)
thr=norm.ppf(1-maf)
def sample(N):
    X=np.zeros((N,NSNP)); X[:,0]=rng.normal(size=N)
    for i in range(1,NSNP):
        a=np.exp(-(pos[i]-pos[i-1])/LAM)
        X[:,i]=a*X[:,i-1]+np.sqrt(1-a*a)*rng.normal(size=N)
    return (X>thr).astype(np.int8)
def ld(H):
    N=H.shape[0]
    r2s=[];dps=[];ds=[]
    for i in range(NSNP):
        for j in range(i+1,NSNP):
            a=H[:,i]; b=H[:,j]
            pa=a.mean(); pb=b.mean(); pab=(a&b).mean()
            D_=pab-pa*pb
            den=pa*(1-pa)*pb*(1-pb)
            if den<=0: continue
            r2=D_*D_/den
            if D_>=0: dmax=min(pa*(1-pb),(1-pa)*pb)
            else: dmax=min(pa*pb,(1-pa)*(1-pb))
            dp=abs(D_)/dmax if dmax>0 else 0
            r2s.append(r2); dps.append(dp); ds.append(pos[j]-pos[i])
    return np.array(ds),np.array(r2s),np.array(dps)
def fitlam(ds,r2s):
    f=lambda d,l: np.exp(-d/l)
    (l,),_=curve_fit(f,ds,r2s,p0=[50000],bounds=([1000],[5e5]))
    return l
out={}
for N in (500,100):
    H=sample(N)
    ds,r2s,dps=ld(H)
    lam=fitlam(ds,r2s)
    near=r2s[ds<10000].mean(); far=r2s[(ds>=90000)&(ds<100000)].mean()
    farDp=dps[(ds>=90000)&(ds<100000)].mean()
    out[str(N)]=dict(lam=float(lam),r2_near=float(near),r2_far=float(far),Dp_far=float(farDp))
    print(N,out[str(N)],flush=True)
json.dump(out,open('results/results.json','w'),indent=1)
a=out['500']
print('G1',abs(a['lam']/50000-1)<=0.30)
print('G2',a['r2_near']>=3*a['r2_far'])
print('G3',a['Dp_far']>=2*a['r2_far'])
print('G4',abs(out['100']['lam']/50000-1)<=0.60)
