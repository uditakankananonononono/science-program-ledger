import numpy as np, json
from numpy.lib.stride_tricks import sliding_window_view as swv
K,W=15,10
def read(p):
    s=''.join(l.strip() for l in open(p) if not l.startswith('>')).upper()
    return np.frombuffer(s.encode(),dtype=np.uint8)
LUT=np.full(256,255,np.uint8)
for i,c in enumerate('ACGT'): LUT[ord(c)]=i
def kmers(a):
    x=LUT[a].astype(np.uint64); n=len(x)-K+1; v=np.zeros(n,np.uint64)
    for i in range(K): v=(v<<np.uint64(2))|x[i:i+n]
    return v,x
def sm(v):
    with np.errstate(over='ignore'):
        z=v+np.uint64(0x9E3779B97F4A7C15)
        z=(z^(z>>np.uint64(30)))*np.uint64(0xBF58476D1CE4E5B9)
        z=(z^(z>>np.uint64(27)))*np.uint64(0x94D049BB133111EB)
        return z^(z>>np.uint64(31))
def lowc(v,x):
    n=len(v); lc=np.zeros(n,bool)
    # homopolymer >=5: positions where 5 equal consecutive bases lie inside kmer
    eq=np.zeros(len(x),bool); 
    run=(x[:-4]==x[1:-3])&(x[1:-3]==x[2:-2])&(x[2:-2]==x[3:-1])&(x[3:-1]==x[4:]) # run start flags, len=len(x)-4
    cs=np.concatenate([[0],np.cumsum(run)])
    # kmer i covers run starts i..i+K-5
    lc|=(cs[np.arange(n)+K-4]-cs[np.arange(n)])>0
    # distinct 2-mers <=4
    d=np.zeros((n,16),bool)
    for j in range(K-1):
        di=(x[j:j+n].astype(np.int64)*4+x[j+1:j+1+n].astype(np.int64))
        d[np.arange(n),di]=True
    lc|=d.sum(1)<=4
    return lc
def rank(arm,v,x,gate=True):
    if arm=='lex': return v
    r=sm(v)>>np.uint64(1)
    if arm=='echo' and gate: r=r+(lowc(v,x).astype(np.uint64)<<np.uint64(63))
    return r
def sel(r):
    win=swv(r,W); return np.arange(len(win))+win.argmin(1)
def dens(r): return len(np.unique(sel(r)))/len(r)
def mutate(a,seed):
    rs=np.random.RandomState(seed); b=a.copy(); m=rs.rand(len(a))<0.05
    alts=np.frombuffer(b'ACGT',np.uint8)
    for i in np.where(m)[0]:
        c=[z for z in alts if z!=b[i]]; b[i]=c[rs.randint(3)]
    return b
out={}
for name in ('NC_001422.1','NC_001416.1','NC_000913.3'):
    a=read(f'data/{name}.fa'); v,x=kmers(a)
    assert (rank('echo',v,x,gate=False)==rank('rand',v,x)).all()
    res={}
    base={arm:rank(arm,v,x) for arm in ('rand','lex','echo')}
    selo={arm:np.unique(sel(base[arm])) for arm in base}
    cons={arm:[] for arm in base}
    for sd in range(10):
        b=mutate(a,sd); vm,xm=kmers(b)
        for arm in base:
            sm_=np.unique(sel(rank(arm,vm,xm))); cons[arm].append(np.isin(selo[arm],sm_).mean())
    for arm in base: res[arm]=dict(density=len(selo[arm])/len(v),conservation=float(np.mean(cons[arm])),cons_min=float(min(cons[arm])),cons_max=float(max(cons[arm])))
    B=res['rand'];E=res['echo']
    dg=E['density']<=B['density']*.97; cg=E['conservation']>=B['conservation']+.01
    bad=E['density']>B['density']*1.03 or E['conservation']<B['conservation']-.01
    res['verdict']='WIN' if (dg or cg) and not bad else ('NEGATIVE' if bad else 'NULL')
    res['n_kmers']=int(len(v)); out[name]=res; print(name,json.dumps(res),flush=True)
out['project_verdict']='WIN' if all(out[n]['verdict']=='WIN' for n in out) else ('NEGATIVE' if any(out[n]['verdict']=='NEGATIVE' for n in out) else 'NULL')
json.dump(out,open('results.json','w'),indent=1); print(out['project_verdict'])
