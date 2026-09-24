import numpy as np, json
rng=np.random.default_rng(1); n=200; R=1000; true=np.log(2)/0.1
def km_median(t,e):
    o=np.argsort(t,kind='stable'); t=t[o]; e=e[o]; S=1.0; atrisk=len(t)
    for ti,ei in zip(t,e):
        if ei: S*=1-1/atrisk
        atrisk-=1
        if S<=0.5: return ti
    return np.nan
out={}
for cmax in [30,10]:
    r={'KM':[],'DROP':[],'ASDEATH':[]}; cens=[]
    for _ in range(R):
        T=rng.exponential(10,n); C=rng.uniform(0,cmax,n); t=np.minimum(T,C); e=T<=C
        cens.append(1-e.mean()); r['KM'].append(km_median(t,e)); r['DROP'].append(np.median(t[e])); r['ASDEATH'].append(np.median(t))
    d={'censoring_frac':float(np.mean(cens))}
    for k,v in r.items():
        v=np.array(v); ok=~np.isnan(v); d[k]={'rel_bias':float(np.nanmean(v)/true-1),'reached_frac':float(ok.mean())}
    out[f'Cmax={cmax}']=d
json.dump(out,open('results/results.json','w'),indent=1); print(json.dumps(out,indent=1))
