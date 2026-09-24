import numpy as np, json
rng=np.random.default_rng(9)
L=100
def theory_norun(L,k,p):
    # DP: probability of NO run of k successes; states 0..k-1 current run length
    f=np.zeros(k); f[0]=1.0
    for _ in range(L):
        nf=np.zeros(k)
        for j in range(k):
            nf[0]+=f[j]*(1-p)
            if j+1<k: nf[j+1]+=f[j]*p
        f=nf
    return f.sum()
res={}
for e in (0.01,0.02,0.05,0.10,0.15,0.20):
    for k in (11,15,18,21,25):
        errs=rng.random((20000,L))<e
        # hit if any error-free window length k: compute via run lengths
        ok=np.zeros(20000,bool)
        run=np.zeros(20000,dtype=int)
        for i in range(L):
            run=np.where(~errs[:,i],run+1,0)
            ok|=run>=k
        sim=ok.mean()
        th=1-theory_norun(L,k,1-e)
        se=np.sqrt(sim*(1-sim)/20000)
        res[f'e{e}_k{k}']=dict(sim=float(sim),theory=float(th),within=abs(sim-th)<=2*se)
within=sum(v['within'] for v in res.values())
# multi-seed contrast, e sweep, simulated
multi={}
for e in (0.01,0.02,0.05,0.10,0.15,0.20):
    errs=rng.random((20000,L))<e
    def hit(k):
        ok=np.zeros(20000,bool); run=np.zeros(20000,dtype=int)
        for i in range(L):
            run=np.where(~errs[:,i],run+1,0); ok|=run>=k
        return ok
    h15=hit(15); h11a=hit(11)
    # second independent 11-seed: reshuffle error pattern (new draw, independent)
    errs2=rng.random((20000,L))<e
    ok=np.zeros(20000,bool); run=np.zeros(20000,dtype=int)
    for i in range(L):
        run=np.where(~errs2[:,i],run+1,0); ok|=run>=11
    multi[e]=dict(single15=float(h15.mean()),two11=float((h11a|ok).mean()))
res['_within_count']=within
res['_multi']=multi
json.dump(res,open('results/results.json','w'),indent=1)
print('within 2SE cells:',within,'/30')
print('G1',within>=24)
print('G2',res['e0.05_k11']['sim']>=0.99,res['e0.05_k25']['sim']<=0.60,res['e0.05_k11']['sim'],res['e0.05_k25']['sim'])
print('G3',all(multi[e]['two11']>=multi[e]['single15'] for e in multi))
print({e:multi[e] for e in multi})
