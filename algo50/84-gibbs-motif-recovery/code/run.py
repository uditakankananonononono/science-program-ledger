import numpy as np, json, time
rng=np.random.default_rng(87)
B='ACGT'; W=10; L=300; POS=L-W+1
def make(N,q,pref):
    seqs=[]; sites=[]
    for _ in range(N):
        a=rng.integers(0,4,L)
        if rng.random()<0.9:
            inst=np.where(rng.random(W)<q,pref,rng.integers(0,4,W))
            p=int(rng.integers(0,POS)); a[p:p+W]=inst; sites.append(p)
        else: sites.append(None)
        seqs.append(a)
    return seqs,sites
def gibbs(seqs,iters=300):
    N=len(seqs)
    pos=rng.integers(0,POS,N)
    cnt=np.full((W,4),0.5)
    for j in range(N):
        for k in range(W): cnt[k,seqs[j][pos[j]+k]]+=1
    lod_full=np.log(cnt/cnt.sum(axis=1,keepdims=True)/0.25)
    for it in range(iters):
        for i in rng.permutation(N):
            s=seqs[i]
            for k in range(W): cnt[k,s[pos[i]+k]]-=1
            lod=np.log(cnt/cnt.sum(axis=1,keepdims=True)/0.25)
            idx=np.arange(POS)[:,None]+np.arange(W)[None,:]
            sc=lod[np.arange(W)[None,:],s[idx]].sum(axis=1)
            sc-=sc.max(); pr=np.exp(sc); pr/=pr.sum()
            pos[i]=int(rng.choice(POS,p=pr))
            for k in range(W): cnt[k,s[pos[i]+k]]+=1
    return pos
res={}; t0=time.time()
for q in (0.5,0.65,0.8,0.95):
    pref=rng.integers(0,4,W)
    for N in (10,30):
        succ=[]
        for rep in range(20):
            seqs,sites=make(N,q,pref)
            est=gibbs(seqs)
            rec=np.mean([abs(e-t)<=5 for e,t in zip(est,sites) if t is not None])
            succ.append(rec>=0.6)
        res[f'q{q}_N{N}']=float(np.mean(succ))
        print(q,N,res[f'q{q}_N{N}'],f'{time.time()-t0:.0f}s',flush=True)
json.dump(res,open('results/results.json','w'),indent=1)
print('G1',res['q0.8_N30']>=0.8 and res['q0.95_N30']>=0.8)
print('G2',res['q0.5_N30']<=0.3)
print('G3',all(res[f'q{q}_N10']>=res[f'q{q}_N30']-0.2 for q in (0.5,0.65,0.8,0.95)))
print('G4',all(res[f'q{a}_N{N}']<=res[f'q{b}_N{N}']+1e-9 for a,b in zip((0.5,0.65,0.8),(0.65,0.8,0.95)) for N in (10,30)))
