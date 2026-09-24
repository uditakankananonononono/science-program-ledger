import json, time
import numpy as np
from Bio import SeqIO
val={'A':0,'C':1,'G':2,'T':3}
g=np.array([val[c] for c in ''.join(str(r.seq) for r in SeqIO.parse('data/NC_000913.3.gb','gb')).upper()],dtype=np.int8)
G=len(g)
rng=np.random.default_rng(1)
# variant sites: 2000 het + 1000 homalt, spacing >=50
pos=[]; 
while len(pos)<3000:
    cand=rng.integers(300,G-300)
    if all(abs(cand-p)>=50 for p in pos[-4000:]) if len(pos)>4000 else True:
        if not pos or min(abs(cand-p) for p in pos)>=50: pos.append(cand)
pos=np.array(sorted(pos)); 
ref=g[pos]
alt=np.array([rng.choice([b for b in range(4) if b!=r]) for r in ref])
gtype=np.array([1]*2000+[2]*1000)  # 1=het 2=homalt
order=np.argsort(pos); pos=pos[order]; ref=ref[order]; alt=alt[order]; gtype=gtype[order]
# non-variant sites: every 16th position, excluding variant neighborhoods
nv=np.arange(300,G-300,16)
mask=np.ones(len(nv),bool)
import bisect
for p in pos:
    i=np.searchsorted(nv,p)
    for j in (i-1,i,i+1):
        if 0<=j<len(nv) and abs(nv[j]-p)<50: mask[j]=False
nv=nv[mask][:297000]
sites=np.concatenate([pos,nv]); s_ref=np.concatenate([ref,g[nv]])
s_alt=np.concatenate([alt,np.full(len(nv),-1)])
s_gt=np.concatenate([gtype,np.zeros(len(nv),int)])
order=np.argsort(sites); sites=sites[order]; s_ref=s_ref[order]; s_alt=s_alt[order]; s_gt=s_gt[order]
np.savez('data/sites.npz',sites=sites,s_ref=s_ref,s_alt=s_alt,s_gt=s_gt)
print('sites',len(sites))
def pileup(cov):
    nreads=int(G*cov/300)
    counts=np.zeros((len(sites),2),dtype=np.int64)  # n, alt
    produced=0; CH=50000
    while produced<nreads:
        m=min(CH,nreads-produced)
        rng=np.random.default_rng(1000+produced)
        starts=rng.integers(0,G-300,m)
        lo=np.searchsorted(sites,starts)
        hi=np.searchsorted(sites,starts+300)
        for k in range(m):
            a,b=lo[k],hi[k]
            if a==b: continue
            idx=np.arange(a,b)
            sp=sites[idx]; rpos=sp-starts[k]
            rb=s_ref[idx]; ab=s_alt[idx]; gt=s_gt[idx]
            base=rb.copy()
            hetmask=gt==1
            draw=rng.random(hetmask.sum())<0.5
            base[hetmask]=np.where(draw,ab[hetmask],rb[hetmask])
            base[gt==2]=ab[gt==2]
            err=rng.random(len(idx))<0.01
            if err.any():
                choices=rng.integers(0,3,err.sum())
                cur=base[err]
                # map to a random different base
                base[err]=np.where(choices<cur,choices,choices+1)
            np.add.at(counts,(idx,0),1)
            np.add.at(counts,(idx[base==ab if False else (base==ab)&(ab>=0)],1),1)
        produced+=m
    return counts
def calls(counts):
    n=counts[:,0]; a=counts[:,1]; r=n-a
    frac=np.divide(a,n,out=np.zeros_like(a,dtype=float),where=n>0)
    ft=np.zeros(len(n),int)
    ft[(a>=4)&(frac>=0.2)&(frac<=0.8)]=1
    ft[(a>=4)&(frac>0.8)]=2
    e=0.01
    with np.errstate(divide='ignore'):
        ll0=r*np.log(1-e/3)+a*np.log(e/3)
        ll1=n*np.log(0.5)
        ll2=r*np.log(e/3)+a*np.log(1-e/3)
    ll0[n==0]=ll1[n==0]=ll2[n==0]=0
    lp0,lp1,lp2=np.log(0.9985),np.log(0.001),np.log(0.0005)
    L=np.stack([ll0+lp0,ll1+lp1,ll2+lp2])
    mx=L.max(0)
    P=np.exp(L-mx); P/=P.sum(0)
    bb=np.zeros(len(n),int)
    best=P.argmax(0)
    bb[(best==1)&(P[1]>0.9)]=1
    bb[(best==2)&(P[2]>0.9)]=2
    return ft,bb
def metrics(call,gt,name):
    het=gt==1; ha=gt==2; nv=gt==0
    out={}
    for lbl,m in (('het',1),('homalt',2)):
        pred=call==m; true=gt==m
        tp=(pred&true).sum()
        out[lbl+'_recall']=float(tp/max(1,true.sum()))
        out[lbl+'_prec']=float(tp/max(1,pred.sum()))
        p=out[lbl+'_prec']; r=out[lbl+'_recall']
        out[lbl+'_f1']=2*p*r/max(1e-9,p+r)
    out['fp_nonvar']=int(((call>0)&nv).sum())
    out['fp_rate']=float(((call>0)&nv).sum()/max(1,nv.sum()))
    return out
res={}
for cov in (30,8):
    t0=time.time()
    c=pileup(cov)
    np.save(f'results/pileup_{cov}x.npy',c)
    ft,bb=calls(c)
    res[f'{cov}x']={'FT':metrics(ft,s_gt,'FT'),'BB':metrics(bb,s_gt,'BB'),'elapsed':round(time.time()-t0,1)}
    print(cov,res[f'{cov}x'],flush=True)
json.dump(res,open('results/results.json','w'),indent=1)
r=res['30x']
print('G1',r['BB']['het_f1']>=r['FT']['het_f1']+0.02)
print('G2',r['BB']['fp_nonvar']<=r['FT']['fp_nonvar'])
r8=res['8x']
print('G3',r8['BB']['het_recall']>=r8['FT']['het_recall']+0.05 and r8['BB']['het_prec']>=0.9)
print('G4',r['BB']['homalt_recall']>=0.95)
