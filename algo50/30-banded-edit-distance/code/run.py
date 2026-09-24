import random, time, json
rng=random.Random(1)
def edit(a,b,k=None):
    n,m=len(a),len(b)
    INF=float('inf')
    prev=list(range(m+1))
    for i in range(1,n+1):
        lo=1 if k is None else max(1,i-k)
        hi=m if k is None else min(m,i+k)
        cur=[INF]*(m+1)
        if k is None or i-k<=0: cur[0]=i
        ai=a[i-1]
        for j in range(lo,hi+1):
            cur[j]=min(prev[j]+1,cur[j-1]+1,prev[j-1]+(ai!=b[j-1]))
        # check band edges for early exit? keep simple
        prev=cur
    return prev[m]
def band_adaptive(a,b,k0=8,kmax=4096):
    # double band until result stable (k doubles, distance unchanged) or kmax
    k=k0; prev=None
    while k<=kmax:
        d=edit(a,b,k)
        if prev is not None and d==prev: return d,k
        if k>=max(len(a),len(b)): return d,k
        prev=d; k*=2
    return prev,kmax
def mut(a,d):
    b=list(a)
    n=int(len(a)*d)
    for _ in range(n):
        op=rng.random()
        p=rng.randrange(len(b))
        if op<0.7: b[p]=rng.choice('ACGT')
        elif op<0.85 and len(b)>10: del b[p]
        else: b.insert(p,rng.choice('ACGT'))
    return ''.join(b)
out={}
# mutated pairs at divergences
for d in (0.05,0.10,0.20,0.30):
    match=0; matchA=0; tF=tA=0.0; N=60
    for _ in range(N):
        a=''.join(rng.choice('ACGT') for _ in range(400))
        b=mut(a,d)
        t0=time.perf_counter(); df=edit(a,b); tF+=time.perf_counter()-t0
        # oracle band
        k=int(d*400*1.5)+2
        t0=time.perf_counter(); db=edit(a,b,k); tB=time.perf_counter()-t0
        t0=time.perf_counter(); da,kk=band_adaptive(a,b); tA+=time.perf_counter()-t0
        match+=db==df; matchA+=da==df
    out[f'd{d}']=dict(oracle_match=match/N,banda_match=matchA/N,time_ratio=tA/tF)
    print(d,out[f'd{d}'],flush=True)
# random pairs (large distance)
matchA=0; wrong_silent=0; N=60; tF=tA=0
for _ in range(N):
    a=''.join(rng.choice('ACGT') for _ in range(400))
    b=''.join(rng.choice('ACGT') for _ in range(400))
    t0=time.perf_counter(); df=edit(a,b); tF+=time.perf_counter()-t0
    t0=time.perf_counter(); da,kk=band_adaptive(a,b); tA+=time.perf_counter()-t0
    matchA+=da==df
    if da!=df and kk<4096: wrong_silent+=1
out['random']=dict(banda_match=matchA/N,wrong_silent=wrong_silent,time_ratio=tA/tF)
print('random',out['random'],flush=True)
json.dump(out,open('results/results.json','w'),indent=1)
print('G1',all(out[f'd{d}']['banda_match']>=0.99 for d in (0.05,0.10,0.20)))
print('G2',out['d0.05']['time_ratio']<=0.30)
print('G3',out['random']['wrong_silent']==0 and out['random']['banda_match']>=0.95)
print('G4',out['d0.3']['oracle_match']>=0.95)
