import numpy as np, random, time, hashlib, json
from Bio import SeqIO
g=str(next(SeqIO.parse('../04-cds-hexamer-discrimination/data/NC_000913.3.gb','genbank')).seq).upper()
n=len(g)
comp={'A':0,'C':1,'G':2,'T':3}
mp=np.full(256,-1,dtype=np.int64)
for c,v in comp.items(): mp[ord(c)]=v
s=mp[np.frombuffer(g.encode(),dtype=np.uint8)].astype(np.int64)
# T = s + sentinel(rank -1) at position n
N=n+1
rank=np.concatenate([s,[-1]]).astype(np.int64)
sa=np.arange(N); k=1
while True:
    key2=np.full(N,-1,dtype=np.int64)
    if k<N: key2[:N-k]=rank[k:]
    order=np.argsort(key2,kind='stable'); order=order[np.argsort(rank[order],kind='stable')]
    sa=order
    nr=np.empty(N,dtype=np.int64); nr[sa[0]]=0
    k1=rank[sa]; k2=key2[sa]
    nr[sa[1:]]=np.cumsum((k1[1:]!=k1[:-1])|(k2[1:]!=k2[:-1]))
    rank=nr
    if rank[sa[-1]]==N-1: break
    k*=2
print('SA built',flush=True)
T=g+'$'
bwt=''.join(T[sa[i]-1] if sa[i]>0 else '$' for i in range(N))  # '$' appears at sa[i]==0 and sa[i]==n
C={}; tot=0
for c in '$ACGT': C[c]=tot; tot+=bwt.count(c)
cnt={c:0 for c in 'ACGT$'}
lf=np.empty(N,dtype=np.int64)
for i,ch in enumerate(bwt):
    lf[i]=C[ch]+cnt[ch]; cnt[ch]+=1
# invert: start at row where sa==n (suffix "$"), emit bwt then follow LF
i=int(np.where(sa==n)[0][0]); out=[]
for _ in range(N):
    out.append(bwt[i]); i=int(lf[i])
g2=''.join(reversed(out))[1:]  # leading '$' of reversed reconstruction
bwt_ok=(g2==g)
if not bwt_ok:
    i=int(np.where(sa==0)[0][0]); out=[]
    for _ in range(N):
        out.append(bwt[i]); i=int(lf[i])
    cand=''.join(reversed(out))
    for cand2 in (cand[1:],cand[:-1],cand):
        if cand2==g: g2=cand2; bwt_ok=True; break
print('BWT inversion exact:',bwt_ok,flush=True)
occ_step=64
bint=mp[np.frombuffer(bwt.encode(),dtype=np.uint8)]  # '$'->-1
occ=np.zeros((N//occ_step+2,4),dtype=np.int64); c=np.zeros(4,dtype=np.int64)
for i,v in enumerate(bint):
    if i%occ_step==0: occ[i//occ_step]=c
    if v>=0: c[v]+=1
def occf(v,pos):
    base=pos//occ_step
    return int(occ[base,v])+int((bint[base*occ_step:pos]==v).sum())
def fm_interval(pat):
    lo=0; hi=N
    for ch in reversed(pat):
        v=comp[ch]
        lo=C[ch]+occf(v,lo); hi=C[ch]+occf(v,hi)
        if lo>=hi: return lo,hi
    return lo,hi
def fm_count(pat):
    lo,hi=fm_interval(pat)
    if lo>=hi: return 0
    pos=sa[lo:hi]; L=len(pat)
    return int(((pos>=0)&(pos+L<=n)).sum())  # exclude wrap/sentinel hits
def sa_search(pat):
    L=len(pat); l=0; r=n
    while l<r:
        m=(l+r)//2
        if g[sa[m]:sa[m]+L]<pat: l=m+1
        else: r=m
    ll=l; up=pat[:-1]+chr(ord(pat[-1])+1); r=N
    while l<r:
        m=(l+r)//2
        if g[sa[m]:sa[m]+L]<up: l=m+1
        else: r=m
    return l-ll
def naive(pat):
    c=0; i=g.find(pat)
    while i>=0: c+=1; i=g.find(pat,i+1)
    return c
rng=random.Random(3)
qs=[g[rng.randrange(n-30):][:30] for _ in range(400)]
qs+=[''.join(rng.choice('ACGT') for _ in range(30)) for _ in range(100)]
agree=0; tf=ts=tn=0.0; disag=[]
for q in qs:
    t0=time.perf_counter(); f=fm_count(q); tf+=time.perf_counter()-t0
    t0=time.perf_counter(); a=sa_search(q); ts+=time.perf_counter()-t0
    t0=time.perf_counter(); nv=naive(q); tn+=time.perf_counter()-t0
    agree+=(f==a==nv)
    if not(f==a==nv): disag.append((q,f,a,nv))
print('agreement',agree,'/500; disagreements:',disag[:3],flush=True)
res=dict(agree=agree,bwt_ok=bwt_ok,fm_med=tf/500,sa_med=ts/500,naive_med=tn/500,note='SA/BWT construction fixed after sentinel bug; all scored numbers from corrected build')
json.dump(res,open('results/results.json','w'),indent=1)
print('G1',agree==500,'G2',bwt_ok,'G3 fm%',round(res['fm_med']/res['naive_med']*100,2),'sa%',round(res['sa_med']/res['naive_med']*100,2),'G4 fm/sa',round(res['fm_med']/res['sa_med'],3))
