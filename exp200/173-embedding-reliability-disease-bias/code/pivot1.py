import pandas as pd, numpy as np, json
rng=np.random.default_rng(0)
D=pd.read_csv('results/variants_scored.csv'); P=D[D.y==1].dropna(subset=['plddt']).copy(); B=D[D.y==0].dropna(subset=['plddt'])
P['lo']=P.plddt<70; P['hit']=P.am_class=='LPath'
def gap(d): return d[~d.lo].hit.mean()-d[d.lo].hit.mean()
def boot(d):
    G={g:x for g,x in d.groupby('gene')}; gs=list(G); bs=[]
    for i in range(1000):
        s=pd.concat([G[g] for g in rng.choice(gs,len(gs))])
        if s.lo.any() and (~s.lo).any(): bs.append(gap(s))
    return [float(np.percentile(bs,2.5)),float(np.percentile(bs,97.5))]
res={'n_PLP':int(len(P)),'sens_hi_plddt':float(P[~P.lo].hit.mean()),'sens_lo_plddt':float(P[P.lo].hit.mean()),'gap':float(gap(P)),'gap_ci':boot(P)}
for t in ['low','high']:
    d=P[P.tier==t]; res[t]={'n':int(len(d)),'n_lo':int(d.lo.sum()),'gap':float(gap(d)),'gap_ci':boot(d)}
for lo,hi in [(0,50),(50,70),(70,90),(90,101)]:
    p=P[(P.plddt>=lo)&(P.plddt<hi)]; b=B[(B.plddt>=lo)&(B.plddt<hi)]
    res[f'band_{lo}_{hi}']={'n_PLP':int(len(p)),'sens':float(p.hit.mean()) if len(p) else None,'n_BLB':int(len(b)),'spec':float((b.am_class=='LBen').mean()) if len(b) else None}
print(json.dumps(res,indent=1)); json.dump(res,open('results/pivot1.json','w'),indent=1)
