import json, time, os
import numpy as np
from Bio import SeqIO
K=21; L=300; MASK=(1<<(2*K))-1; NB=16; CH=30000
val={'A':0,'C':1,'G':2,'T':3}
def genome_of(acc): return ''.join(str(r.seq) for r in SeqIO.parse(f'data/{acc}.gb','gb')).upper()
gc=np.array([val[c] for c in genome_of('NC_000913.3')],dtype=np.int64)
gcb=np.array([val[c] for c in genome_of('NC_000964.3')],dtype=np.int64)
G=len(gc)
def gen_reads(seed, gcodes, nreads):
    rng=np.random.default_rng(seed)
    starts=rng.integers(0,len(gcodes)-L,nreads)
    reads=gcodes[starts[:,None]+np.arange(L)].copy()
    mut=rng.random(reads.shape)<0.01
    reads[mut]=rng.integers(0,4,mut.sum())
    return reads
def codes_of(reads):
    n=reads.shape[0]
    codes=np.zeros((n,L-K+1),dtype=np.int64)
    f=np.zeros(n,dtype=np.int64); r=np.zeros(n,dtype=np.int64)
    for i in range(L):
        v=reads[:,i]
        f=((f<<2)|v)&MASK
        r=(r>>2)|((3-v)<<(2*(K-1)))
        if i>=K-1: codes[:,i-K+1]=np.minimum(f,r)
    return codes.ravel()
def spectrum(nreads, tag, contam=0.0):
    # one pass: bucket all codes to disk
    files=[open(f'/tmp/bk_{tag}_{b}.raw','wb') for b in range(NB)]
    nc=int(nreads*contam)
    produced=0
    while produced<nreads:
        m=min(CH,nreads-produced)
        if produced<nc:
            m1=min(m,nc-produced)
            r1=gen_reads(1000+produced,gcb,m1)
            r2=gen_reads(1+produced+m1,gc,m-m1) if m>m1 else None
            reads=np.vstack([r1,r2]) if r2 is not None else r1
        else:
            reads=gen_reads(1+produced,gc,m)
        c=codes_of(reads)
        bk=(c>>38)
        order=np.argsort(bk,kind='stable')
        c=c[order]; bk=bk[order]
        bounds=np.searchsorted(bk,np.arange(NB+1))
        for b in range(NB):
            c[bounds[b]:bounds[b+1]].tofile(files[b])
        produced+=m
    for f in files: f.close()
    hist=np.zeros(201,dtype=np.int64)
    for b in range(NB):
        arr=np.fromfile(f'/tmp/bk_{tag}_{b}.raw',dtype=np.int64)
        _,counts=np.unique(arr,return_counts=True)
        hist+=np.bincount(np.minimum(counts,200),minlength=201)
        os.remove(f'/tmp/bk_{tag}_{b}.raw')
    return hist
def estimate(hist):
    peak=int(np.argmax(hist[2:])+2)
    cut=3
    for m in range(2,peak):
        if hist[m]<hist[m-1] and m+1<=peak and hist[m]<hist[m+1]:
            cut=m; break
    mults=np.arange(len(hist)); sel=mults>=cut
    tot=(hist[sel]*mults[sel]).sum()
    mean_mult=(hist[sel]*mults[sel]**2).sum()/tot
    return tot/mean_mult, mean_mult, int(cut), int(peak)
out={}
for name,cov,contam in (('clean30x',30,0.0),('contam30x',30,0.01),('clean5x',5,0.0)):
    nreads=int(G*cov/L)
    t0=time.time()
    hist=spectrum(nreads,name,contam)
    size,cmult,cut,peak=estimate(hist)
    out[name]=dict(size=float(size),cov=float(cmult),cutoff=cut,peak=peak,elapsed=round(time.time()-t0,1))
    print(name,out[name],flush=True)
    np.save(f'results/hist_{name}.npy',hist)
json.dump(out,open('results/results.json','w'),indent=1)
print('G1',abs(out['clean30x']['size']/G-1)<=0.10,'G2',abs(out['clean30x']['cov']/30-1)<=0.10,
      'G3',abs(out['contam30x']['size']/out['clean30x']['size']-1)<0.05,'G4',abs(out['clean5x']['size']/G-1)<=0.20,flush=True)
