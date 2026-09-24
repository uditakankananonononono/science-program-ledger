import numpy as np, json
from collections import defaultdict
rng=np.random.default_rng(86); K=31; RL=75
def rand_seq(n): return rng.integers(0,4,n)
trans=[]; iso_pairs=[]; unique_frac=[]
ti=0
for g in range(190):
    if g<10:
        shared=rand_seq(400)
        L1=int(rng.integers(800,1500)); L2=int(rng.integers(800,1500))
        t1=np.concatenate([rand_seq(L1-400),shared]); t2=np.concatenate([shared,rand_seq(L2-400)])
        trans += [t1,t2]; iso_pairs.append((ti,ti+1))
        for t in (t1,t2):
            km=set(tuple(t[i:i+K]) for i in range(len(t)-K+1))
            unique_frac.append(None)  # filled later
        ti+=2
    else:
        trans.append(rand_seq(int(rng.integers(800,1500)))); ti+=1
T=len(trans)
# unique k-mer fraction per transcript
kmer_map=defaultdict(set)
for i,t in enumerate(trans):
    for j in range(len(t)-K+1): kmer_map[tuple(t[j:j+K])].add(i)
uf=[]
for i,t in enumerate(trans):
    km=[tuple(t[j:j+K]) for j in range(len(t)-K+1)]
    uf.append(np.mean([len(kmer_map[k])==1 for k in km]))
abund=rng.geometric(0.15,T).astype(float); abund/=abund.sum()
lens=np.array([len(t) for t in trans])
w=abund*lens; w/=w.sum()
def run_depth(nreads,seed):
    r=np.random.default_rng(seed)
    tids=r.choice(T,size=nreads,p=w)
    classes=defaultdict(lambda:[0,None])
    for tid in tids:
        t=trans[tid]
        st=int(r.integers(0,len(t)-RL+1)); read=t[st:st+RL].copy()
        err=r.random(RL)<0.01; read[err]=r.integers(0,4,err.sum())
        ks=[tuple(read[o:o+K]) for o in (0,(RL-K)//2,RL-K)]
        ec=None
        for k in ks:
            s=kmer_map.get(k,set())
            ec=set(s) if ec is None else (ec & s)
            if not ec: break
        if not ec: continue
        key=tuple(sorted(ec)); classes[key][0]+=1
    keys=list(classes); cnt=np.array([classes[k][0] for k in keys],float)
    mem=[np.array(k) for k in keys]
    theta=np.full(T,1.0/T)
    for it in range(100):
        new=np.zeros(T)
        for c,m in zip(cnt,mem):
            p=theta[m]*lens[m]; p/=p.sum(); new[m]+=c*p
        theta=new/new.sum()
    exp_reads=abund*nreads
    est=theta/ theta.sum()
    rho=float(__import__('scipy.stats',fromlist=['spearmanr']).spearmanr(est,abund).statistic)
    mask=exp_reads>=50
    l2=np.abs(np.log2((est[mask]+1e-12)/(abund[mask]+1e-12)))
    med=float(np.median(l2))
    iso_err=[]
    for a,b in iso_pairs:
        for i in (a,b):
            if uf[i]>=0.3 and exp_reads[i]>=20:
                iso_err.append(float(abs(np.log2((est[i]+1e-12)/(abund[i]+1e-12)))))
    return rho,med,iso_err
res={}
for depth,seed in ((50000,861),(200000,862),(800000,863)):
    rho,med,ie=run_depth(depth,seed)
    res[str(depth)]={'rho':rho,'med_log2err':med,'iso_err':ie}
    print(depth,rho,med,ie,flush=True)
json.dump(res,open('results/results.json','w'),indent=1)
r=res['200000']
print('G1',r['rho']>=0.95)
print('G2',r['med_log2err']<=0.5)
print('G3',all(e<=1.0 for e in r['iso_err']) if r['iso_err'] else 'no isoforms with uf>=0.3')
print('G4',res['50000']['med_log2err']>=res['200000']['med_log2err']>=res['800000']['med_log2err'])
