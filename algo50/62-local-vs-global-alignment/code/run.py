import numpy as np, json
rng=np.random.default_rng(19)
def nw(a,b):
    n,m=len(a),len(b)
    d=np.full((n+1,m+1),-10**9)
    d[0,:]=-2*np.arange(m+1); d[:,0]=-2*np.arange(n+1)
    for i in range(1,n+1):
        ai=a[i-1]
        for j in range(1,m+1):
            d[i,j]=max(d[i-1,j-1]+(2 if ai==b[j-1] else -1),d[i-1,j]-2,d[i,j-1]-2)
    return d[n,m]
def sw(a,b):
    n,m=len(a),len(b)
    d=np.zeros((n+1,m+1),dtype=int)
    best=0
    for i in range(1,n+1):
        ai=a[i-1]
        for j in range(1,m+1):
            v=max(d[i-1,j-1]+(2 if ai==b[j-1] else -1),d[i-1,j]-2,d[i,j-1]-2,0)
            d[i,j]=v
            if v>best: best=v
    return best
# vectorized speed: keep python loops but small n (1260 max) x 600 pairs x 9 cells too slow?
# 1260^2 = 1.6M ops per pair x 300 pairs x 3 cells(F=1000) too slow in pure python. Reduce: F=1000 cells get 80 pairs.
import time
def rnastr(n): return ''.join(rng.choice(list('ACGT'),n))
res={}
# sanity
q='ACGT'*15
res['sanity']=(sw(q,q),nw(q,q))
print('sanity',res['sanity'],flush=True)
for F in (0,200,1000):
    for ident in (0.6,0.8,1.0):
        N=60 if F>=1000 else 120
        sws=[]; nws=[]; ok=True
        for _ in range(N):
            dom=list(rnastr(60))
            mut=[c if rng.random()<ident else rng.choice([x for x in 'ACGT' if x!=c]) for c in dom]
            qa=rnastr(F)+''.join(dom)+rnastr(F)
            sa=rnastr(F)+''.join(mut)+rnastr(F)
            s1=sw(qa,sa); s2=nw(qa,sa)
            if s1<s2: ok=False
            sws.append(s1); nws.append(s2)
        # null
        nulls=[]; nulln=[]
        for _ in range(N):
            qa=rnastr(60+2*F); sa=rnastr(60+2*F)
            nulls.append(sw(qa,sa)); nulln.append(nw(qa,sa))
        n95=np.percentile(nulls,95); n95n=np.percentile(nulln,95)
        res[f'F{F}_i{ident}']=dict(sw_med=float(np.median(sws)),nw_med=float(np.median(nws)),
            sw_det=float(np.mean(np.array(sws)>n95)),nw_det=float(np.mean(np.array(nws)>n95n)),
            sw_ge_nw=ok,fpr_sw=float(np.mean(np.array(nulls)>n95)))
        print(F,ident,res[f'F{F}_i{ident}'],flush=True)
json.dump(res,open('results/results.json','w'),indent=1)
print('G1',res['sanity']==(120,120) and all(res[k]['sw_ge_nw'] for k in res if k.startswith('F')))
print('G2',all(res[f'F{F}_i0.8']['sw_det']>=0.95 for F in (0,200,1000)))
print('G3',res['F1000_i0.8']['nw_det']<=0.30)
print('G4',all(0.03<=res[k]['fpr_sw']<=0.08 for k in res if k.startswith('F')))
