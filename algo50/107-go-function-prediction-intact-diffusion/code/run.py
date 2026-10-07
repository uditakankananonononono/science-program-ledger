import gzip, hashlib, numpy as np, scipy.sparse as sp, json, os, sys, collections
from scipy.stats import rankdata
H={'intact.tsv.gz':'7e9f6bba8ea0511e510b71a383817dc22b32469e799bb3457c769e331d442a85','gaf.gz':'a0afba19dfb1f8fa996bc1bdcd61fd0c9bd4cf0d2bf2509d09ac86993c0e70a2','go-basic.obo':'b08d45b268b8c24ccb2513dbbbc7d4df9f6521c099b413f79eb31e06e0fa3bcc'}
for f,h in H.items(): assert hashlib.sha256(open(f,'rb').read()).hexdigest()==h,f
CUT='2022'; EXP={'EXP','IDA','IPI','IMP','IGI','IEP','HTP','HDA','HMP','HGI','HEP'}
par={};cur=None;obs=set()
for l in open('go-basic.obo'):
    l=l.strip()
    if l=='[Term]': cur=None
    elif l.startswith('['): cur=None
    elif l.startswith('id: GO:'): cur=l[4:]; par.setdefault(cur,set())
    elif cur and l.startswith('is_obsolete: true'): obs.add(cur)
    elif cur and l.startswith('is_a: '): par[cur].add(l.split()[1])
    elif cur and l.startswith('relationship: part_of '): par[cur].add(l.split()[2])
for o in obs: par.pop(o,None)
sys.setrecursionlimit(10000); anc={}
def ancs(t):
    if t in anc: return anc[t]
    s={t}
    for p in par.get(t,()):
        if p in par: s|=ancs(p)
    anc[t]=s; return s
tr_ann=collections.defaultdict(set); te_ann=collections.defaultdict(set)
for l in gzip.open('gaf.gz','rt'):
    if l[0]=='!': continue
    f=l.rstrip('\n').split('\t')
    if 'NOT' in f[3] or f[6]=='ND' or f[4] not in par: continue
    if f[13][:4]<CUT: tr_ann[f[1]]|=ancs(f[4])
    elif f[6] in EXP: te_ann[f[1]]|=ancs(f[4])
E={}
for i,l in enumerate(gzip.open('intact.tsv.gz','rt')):
    if i==0: continue
    f=l.rstrip('\n').split('\t'); a,b=f[0],f[1]
    if not(a.startswith('uniprotkb:') and b.startswith('uniprotkb:')): continue
    a=a[10:].split('-')[0]; b=b[10:].split('-')[0]
    if a==b or f[9]>='2022': continue
    k=tuple(sorted((a,b))); E[k]=min(E.get(k,'9'),f[9])
E={k:v for k,v in E.items() if v<'2022/01/01'}
deg=collections.Counter(x for k in E for x in k)
prots=sorted(p for p in deg if p in tr_ann and len(tr_ann[p])>0); pi={p:i for i,p in enumerate(prots)}; n=len(prots)
edges=[k for k in E if k[0] in pi and k[1] in pi]
def A_of(edges):
    r=[pi[a] for a,b in edges]+[pi[b] for a,b in edges]; c=[pi[b] for a,b in edges]+[pi[a] for a,b in edges]; return sp.csr_matrix((np.ones(len(r),np.float32),(r,c)),shape=(n,n))
def b1(A,Y):
    k=np.asarray(A.sum(1)).ravel(); R=sp.diags(np.where(k>0,1/np.maximum(k,1),0).astype(np.float32))@A; return R@Y
def b2(A,Y):
    k=np.asarray(A.sum(1)).ravel(); R=(sp.diags(np.where(k>0,1/np.maximum(k,1),0).astype(np.float32))@A).tocsr(); R2=(R@R).tolil(); R2.setdiag(0); return R2.tocsr()@Y
def dcd(A,Y,a,w2,b):
    k=np.asarray(A.sum(1)).ravel(); d=np.where(k>0,k**-a,0).astype(np.float32); An=(sp.diags(d)@A@sp.diags(d)).tocsr()
    S=An@Y
    if w2: A2=(An@An).tolil(); A2.setdiag(0); S=S+w2*(A2.tocsr()@Y)
    return S/((k+1)**b)[:,None]
# equivalence
T=sp.csr_matrix(np.array([[0,1,0,0,0],[1,0,1,0,0],[0,1,0,1,0],[0,0,1,0,1],[0,0,0,1,0]],np.float32)); Yt=np.array([[1],[0],[0],[0],[0]],np.float32)
assert np.allclose(b1(T,Yt).ravel(),[0,0.5,0,0,0]),'b1'
assert np.allclose(b2(T,Yt).ravel(),[0,0,0.25,0,0]),'b2'
dd=1/np.array([1,2,2,2,1.]); One=(np.diag(dd)@T.toarray()@np.diag(dd))@Yt
assert np.allclose(dcd(T,Yt,1.0,0,0).ravel(),One.ravel()),'dcd'
if os.environ.get('CHECK'): print('checks passed'); sys.exit()
terms=sorted({t for p in prots for t in tr_ann[p]}); 
cnt=collections.Counter(t for p in prots for t in tr_ann[p]); tc=collections.Counter(t for p in prots for t in (te_ann.get(p,set())-tr_ann[p]))
sel=[t for t in terms if 10<=cnt[t]<=300 and tc[t]>=5]; ti={t:i for i,t in enumerate(sel)}
print('prots',n,'edges',len(edges),'terms',len(sel),flush=True)
def mats(ts):
    r=[];c=[];r2=[];c2=[]
    idx={t:i for i,t in enumerate(ts)}
    for p in prots:
        for t in tr_ann[p]:
            if t in idx: r.append(pi[p]); c.append(idx[t])
        for t in te_ann.get(p,set())-tr_ann[p]:
            if t in idx: r2.append(pi[p]); c2.append(idx[t])
    Y=np.zeros((n,len(ts)),np.float32); Y[r,c]=1; Z=np.zeros((n,len(ts)),np.float32); Z[r2,c2]=1; return Y,Z
def auc(sc,y):
    r=rankdata(sc); n1=y.sum(); n0=len(y)-n1; return (r[y==1].sum()-n1*(n1+1)/2)/(n1*n0)
def macro(S,Y,Z):
    out=[]
    for j in range(S.shape[1]):
        el=Y[:,j]==0; y=Z[el,j]
        out.append(auc(S[el,j],y) if 0<y.sum()<len(y) else np.nan)
    return np.array(out)
A=A_of(edges); dev_t=sel[0::2]; test_t=sel[1::2]
Yd,Zd=mats(dev_t); dv={'B1':np.nanmean(macro(b1(A,Yd),Yd,Zd)),'B2':np.nanmean(macro(b2(A,Yd),Yd,Zd))}; head='B1' if dv['B1']>=dv['B2'] else 'B2'; print('DEV base',dv,flush=True)
best=None;dd_={}
for a in (0.5,0.75,1.0):
    for w2 in (0,0.5,1):
        for b in (0,0.5,1):
            m=np.nanmean(macro(dcd(A,Yd,a,w2,b),Yd,Zd)); dd_[f'{a},{w2},{b}']=float(m)
            if best is None or m>best[0]+1e-12: best=(m,a,w2,b)
print('DEV best',best,flush=True)
Yt_,Zt=mats(test_t); sb=b1(A,Yt_) if head=='B1' else b2(A,Yt_); mb=macro(sb,Yt_,Zt); md=macro(dcd(A,Yt_,*best[1:]),Yt_,Zt)
ok=~np.isnan(mb)&~np.isnan(md); d=(md-mb)[ok]; rs=np.random.RandomState(7); bs=[d[rs.randint(0,len(d),len(d))].mean() for _ in range(10000)]
lo,hi=np.percentile(bs,[2.5,97.5]); diff=float(d.mean()); v='WIN' if diff>=0.02 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
res=dict(n_prots=n,n_edges=len(edges),n_terms=len(sel),n_test_terms=int(ok.sum()),dev_baselines={k:float(x) for k,x in dv.items()},head=head,dev_best=dict(auc=float(best[0]),a=best[1],w2=best[2],b=best[3]),edge=bool(best[1] in (0.5,1.0) or best[2] in (0,1) or best[3] in (0,1)),test_macro_base=float(mb[ok].mean()),test_macro_dcd=float(md[ok].mean()),diff=diff,ci=[float(lo),float(hi)],frac_dcd_better=float((d>0).mean()),median_pos=float(np.median(Zt.sum(0))),verdict=v)
json.dump(res,open('results.json','w'),indent=1); print(json.dumps(res))
