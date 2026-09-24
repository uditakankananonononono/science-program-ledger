import numpy as np, json
rng=np.random.default_rng(19)
def nw(a,b):
    a=np.frombuffer(a.encode(),dtype=np.uint8); b=np.frombuffer(b.encode(),dtype=np.uint8)
    n,m=len(a),len(b)
    NEG=-10**9
    d=np.full((n+1,m+1),NEG)
    d[0,0]=0
    d[0,1:]=-2*np.arange(1,m+1); d[1:,0]=-2*np.arange(1,n+1)
    for s in range(2,n+m+1):
        i0=max(1,s-m); i1=min(n,s-1)
        ii=np.arange(i0,i1+1); jj=s-ii
        match=np.where(a[ii-1]==b[jj-1],2,-1)
        d[ii,jj]=np.maximum(np.maximum(d[ii-1,jj-1]+match,d[ii-1,jj]-2),d[ii,jj-1]-2)
    return int(d[n,m])
def sw(a,b):
    a=np.frombuffer(a.encode(),dtype=np.uint8); b=np.frombuffer(b.encode(),dtype=np.uint8)
    n,m=len(a),len(b)
    d=np.zeros((n+1,m+1),dtype=np.int64)
    best=0
    for s in range(2,n+m+1):
        i0=max(1,s-m); i1=min(n,s-1)
        ii=np.arange(i0,i1+1); jj=s-ii
        match=np.where(a[ii-1]==b[jj-1],2,-1)
        v=np.maximum(np.maximum(d[ii-1,jj-1]+match,d[ii-1,jj]-2),d[ii,jj-1]-2)
        v=np.maximum(v,0)
        d[ii,jj]=v
        if len(v) and v.max()>best: best=int(v.max())
    return best
def rnastr(n): return ''.join(rng.choice(list('ACGT'),n))
res={}
q='ACGT'*15
res['sanity']=(sw(q,q),nw(q,q))
assert res['sanity']==(120,120)
for F,N in ((0,120),(200,60),(1000,30)):
    for ident in (0.6,0.8,1.0):
        sws=[]; nws=[]; ok=True
        for _ in range(N):
            dom=list(rnastr(60))
            mut=[c if rng.random()<ident else rng.choice([x for x in 'ACGT' if x!=c]) for c in dom]
            qa=rnastr(F)+''.join(dom)+rnastr(F)
            sa=rnastr(F)+''.join(mut)+rnastr(F)
            s1=sw(qa,sa); s2=nw(qa,sa)
            if s1<s2: ok=False
            sws.append(s1); nws.append(s2)
        nulls=[]; nulln=[]
        for _ in range(N):
            qa=rnastr(60+2*F); sa=rnastr(60+2*F)
            nulls.append(sw(qa,sa)); nulln.append(nw(qa,sa))
        n95=float(np.percentile(nulls,95)); n95n=float(np.percentile(nulln,95))
        res[f'F{F}_i{ident}']=dict(sw_med=float(np.median(sws)),nw_med=float(np.median(nws)),
            sw_det=float(np.mean(np.array(sws)>n95)),nw_det=float(np.mean(np.array(nws)>n95n)),
            sw_ge_nw=ok,fpr_sw=float(np.mean(np.array(nulls)>n95)),N=N)
        print(F,ident,res[f'F{F}_i{ident}'],flush=True)
json.dump(res,open('results/results.json','w'),indent=1)
print('G1',all(res[k]['sw_ge_nw'] for k in res if k.startswith('F')))
print('G2',all(res[f'F{F}_i0.8']['sw_det']>=0.95 for F in (0,200,1000)))
print('G3',res['F1000_i0.8']['nw_det']<=0.30)
print('G4',all(0.03<=res[k]['fpr_sw']<=0.08 for k in res if k.startswith('F')))
