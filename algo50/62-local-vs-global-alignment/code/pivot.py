import numpy as np, json
rng=np.random.default_rng(19)
# advance RNG past the run2 consumption is unnecessary; pivot uses fresh draws
def sw_trace(a,b):
    a=np.frombuffer(a.encode(),dtype=np.uint8); b=np.frombuffer(b.encode(),dtype=np.uint8)
    n,m=len(a),len(b)
    d=np.zeros((n+1,m+1),dtype=np.int64)
    ptr=np.zeros((n+1,m+1),dtype=np.int8)  # 1 diag,2 up,3 left
    best=0; bi=bj=0
    for s in range(2,n+m+1):
        i0=max(1,s-m); i1=min(n,s-1)
        ii=np.arange(i0,i1+1); jj=s-ii
        match=np.where(a[ii-1]==b[jj-1],2,-1)
        cand=np.stack([d[ii-1,jj-1]+match,d[ii-1,jj]-2,d[ii,jj-1]-2,np.zeros(len(ii),dtype=np.int64)])
        v=cand.max(axis=0); p=cand.argmax(axis=0)+1
        d[ii,jj]=v; ptr[ii,jj]=np.where(v>0,p,0)
        mx=v.max()
        if mx>best:
            best=int(mx); k=int(v.argmax()); bi,bj=int(ii[k]),int(jj[k])
    # traceback
    i,j=bi,bj
    while i>0 and j>0 and ptr[i,j]>0:
        p=ptr[i,j]
        if p==1: i-=1; j-=1
        elif p==2: i-=1
        else: j-=1
    return best,i,bi  # interval [i,bi) on query
def rnastr(n): return ''.join(rng.choice(list('ACGT'),n))
res={}
for ident in (0.8,1.0):
    cov=[]
    N=30
    for _ in range(N):
        F=1000
        dom=list(rnastr(60))
        mut=[c if rng.random()<ident else rng.choice([x for x in 'ACGT' if x!=c]) for c in dom]
        qa=rnastr(F)+''.join(dom)+rnastr(F)
        sa=rnastr(F)+''.join(mut)+rnastr(F)
        score,lo,hi=sw_trace(qa,sa)
        ov=max(0,min(hi,F+60)-max(lo,F))
        cov.append(ov/60)
    res[f'i{ident}']=dict(frac_cov_ge_50=float(np.mean(np.array(cov)>=0.5)),median_cov=float(np.median(cov)))
    print(ident,res[f'i{ident}'],flush=True)
res['nw_precision']=60/2060
json.dump(res,open('results/pivot_metrics.json','w'),indent=1)
print('P1',all(res[k]['frac_cov_ge_50']>=0.9 for k in ('i0.8','i1.0')))
print('P2 (informational) NW domain precision =',res['nw_precision'])
