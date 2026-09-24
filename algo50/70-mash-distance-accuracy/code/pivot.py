import numpy as np, json
rng=np.random.default_rng(47)
B='ACGT'
anc=''.join(rng.choice(list(B),50000))
def descendant(p):
    out=[]
    for c in anc:
        if rng.random()<p: out.append(rng.choice([x for x in B if x!=c]))
        else: out.append(c)
    return ''.join(out)
def kmers(s,k):
    return {hash(s[i:i+k]) for i in range(len(s)-k+1)}
res={}
for k in (11,15,21,31):
    for p in (0.01,0.05,0.10,0.15,0.20,0.30,0.40):
        ests=[]
        for _ in range(20):
            d=descendant(p)
            A=kmers(anc,k); D=kmers(d,k)
            J=len(A&D)/len(A|D)
            ests.append(-np.log(2*J/(1+J))/k)
        fin=[e for e in ests if np.isfinite(e)]
        res[f'k{k}_p{p}']=dict(med=float(np.median(fin)) if fin else None,
            err=(float(np.median(fin)-p) if fin else None),
            frac_inf=1-len(fin)/len(ests), E=50000*(1-p)**k)
    print(k,flush=True)
json.dump(res,open('results/pivot_metrics.json','w'),indent=1)
hi=[v for v in res.values() if v['E']>=1000]
lo=[v for v in res.values() if v['E']<=50]
P1=all(v['err'] is not None and abs(v['err'])<=0.02 for v in hi)
P2=all(v['frac_inf']>=0.5 for v in lo)
print('P1',P1,[(round(v['E']),round(v['err'],4)) for v in hi])
print('P2',P2,[(round(v['E']),v['frac_inf']) for v in lo])
for k in (11,15,21,31):
    meds=[res[f'k{k}_p{p}']['med'] if res[f'k{k}_p{p}']['med'] is not None else float('inf') for p in (0.01,0.05,0.10,0.15,0.20,0.30,0.40)]
    print('mono k',k,all(a<=b for a,b in zip(meds,meds[1:])))
