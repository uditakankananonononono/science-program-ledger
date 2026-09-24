import numpy as np, json, warnings
from scipy.optimize import curve_fit
warnings.filterwarnings('ignore')
rng=np.random.default_rng(1); doses=np.logspace(-2,2,8); ld=np.log10(doses); R=1000; out={}
def f(x,b,t,lic,h): return b+(t-b)/(1+10**((x-lic)*h))
for h in [1,3]:
    eI=[]; eF=[]; fail=0
    X=np.repeat(ld,3)
    for _ in range(R):
        y=f(X,0,100,0,h)+rng.normal(0,8,X.size); m=y.reshape(8,3).mean(1)
        idx=np.nonzero((m[:-1]>=50)&(m[1:]<50))[0]
        if len(idx): i=idx[0]; eI.append(abs(ld[i]+(50-m[i])*(ld[i+1]-ld[i])/(m[i+1]-m[i])))
        else: eI.append(np.nan)
        try:
            p,_=curve_fit(f,X,y,p0=[0,100,0,1],maxfev=5000); eF.append(abs(p[2]))
        except Exception: fail+=1
    out[f'h={h}']={'INTERP_median_err':float(np.nanmedian(eI)),'FOURPL_median_err':float(np.median(eF)),'FOURPL_converged':1-fail/R,'INTERP_no_crossing':float(np.mean(np.isnan(eI)))}
json.dump(out,open('results/results.json','w'),indent=1); print(json.dumps(out,indent=1))
