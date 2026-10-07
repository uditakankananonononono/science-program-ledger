import gzip, hashlib, numpy as np, scipy.sparse as sp, json, os, sys
from scipy.stats import hypergeom, nchypergeom_fisher, fisher_exact
assert hashlib.sha256(open('HUMAN-uniprot.gaf.gz','rb').read()).hexdigest()=='a0afba19dfb1f8fa996bc1bdcd61fd0c9bd4cf0d2bf2509d09ac86993c0e70a2'
assert hashlib.sha256(open('go-basic.obo','rb').read()).hexdigest()=='b08d45b268b8c24ccb2513dbbbc7d4df9f6521c099b413f79eb31e06e0fa3bcc'
par={};cur=None;obs=set()
for l in open('go-basic.obo'):
    l=l.strip()
    if l=='[Term]': cur=None; blk=True
    elif l.startswith('['): cur=None
    elif l.startswith('id: GO:'): cur=l[4:]; par.setdefault(cur,set())
    elif cur and l.startswith('is_obsolete: true'): obs.add(cur)
    elif cur and l.startswith('is_a: '): par[cur].add(l.split()[1])
    elif cur and l.startswith('relationship: part_of '): par[cur].add(l.split()[2])
for o in obs: par.pop(o,None)
anc={}
def ancs(t):
    if t in anc: return anc[t]
    s={t}
    for p in par.get(t,()):
        if p in par: s|=ancs(p)
    anc[t]=s; return s
sys.setrecursionlimit(10000)
ann={}
for l in gzip.open('HUMAN-uniprot.gaf.gz','rt'):
    if l[0]=='!': continue
    f=l.rstrip('\n').split('\t')
    if 'NOT' in f[3] or f[6]=='ND' or f[4] not in par: continue
    ann.setdefault(f[1],set()).add(f[4])
genes=sorted(ann); gi={g:i for i,g in enumerate(genes)}
terms=sorted({t for g in genes for a in ann[g] for t in ancs(a)}); ti={t:i for i,t in enumerate(terms)}
r=[];c=[]
for g in genes:
    for t in {x for a in ann[g] for x in ancs(a)}: r.append(gi[g]); c.append(ti[t])
M=sp.csr_matrix((np.ones(len(r),dtype=np.int8),(r,c)),shape=(len(genes),len(terms))); Mc=M.tocsc()
K=np.asarray(M.sum(0)).ravel(); N=len(genes); nann=np.asarray(M.sum(1)).ravel().astype(float)
test=np.where((K>=10)&(K<=500))[0]; print('N',N,'terms',len(terms),'testable',len(test),flush=True)
sumw=np.asarray(M.T@nann).ravel()
def odds_of(gam):
    win=sumw/np.maximum(K,1); wout=(nann.sum()-sumw)/np.maximum(N-K,1); return (win/wout)**gam
def pvals(k,Kt,n,odds=None):
    if odds is None: return hypergeom.sf(k-1,N,Kt,n)
    return nchypergeom_fisher.sf(k-1,N,Kt,n,odds)
def bh(p,m):
    o=np.argsort(p); q=np.empty(len(p)); ps=p[o]*m/np.arange(1,len(p)+1); ps=np.minimum.accumulate(ps[::-1])[::-1]; q[o]=np.minimum(ps,1); return q
def called(L,gam):
    k=np.asarray(M[L][:,test].sum(0)).ravel(); ok=k>=1; n=len(L)
    res={}
    for name in ('F','A'):
        p=np.ones(len(test))
        if ok.any():
            p[ok]=pvals(k[ok],K[test][ok],n,None if name=='F' else odds_of(gam)[test][ok])
        q=bh(p,len(test)) if True else None
        res[name]=set(test[q<0.05])
    return res
# BH uses all testable terms: p=1 for k=0; bh over len(test) values handled above
# equivalence
rs=np.random.RandomState(1)
for _ in range(50):
    Nn=rs.randint(200,500);Kk=rs.randint(10,100);n=rs.randint(20,100);k=rs.randint(max(0,n+Kk-Nn),min(n,Kk)+1)
    p1=hypergeom.sf(k-1,Nn,Kk,n); p2=fisher_exact([[k,Kk-k],[n-k,Nn-Kk-n+k]],alternative='greater')[1]; p3=nchypergeom_fisher.sf(k-1,Nn,Kk,n,1.0)
    assert abs(p1-p2)<1e-9 and abs(p3-p1)<1e-7,'equiv'
if os.environ.get('CHECK'): print('checks passed'); sys.exit()
# related sets
desc={}
for t in terms:
    for a in ancs(t): desc.setdefault(a,set()).add(t)
members={}
def mem(t): 
    if t not in members: members[t]=set(Mc[:,ti[t]].indices)
    return members[t]
def related(t):
    R={ti[x] for x in ancs(t)|desc.get(t,set()) if x in ti}; R.add(ti[t]); mt=mem(t)
    for j in test:
        if j in R: continue
        m=mem(terms[j]); 
        if len(mt&m)/len(mt|m)>=0.3: R.add(j)
    return R
Tpool=[terms[j] for j in test if 20<=K[j]<=150]
dev_T=Tpool[0::2]; test_T=Tpool[1::2]
def gen(Tl,nrep,seed,expo):
    rs=np.random.RandomState(seed); out=[]
    for _ in range(nrep):
        t=Tl[rs.randint(len(Tl))]; mt=np.array(sorted(mem(t))); pl=rs.choice(mt,8,replace=False)
        mask=np.ones(N,bool); mask[mt]=False; idx=np.where(mask)[0]; w=nann[idx]**expo; bg=rs.choice(idx,92,replace=False,p=w/w.sum())
        out.append((t,np.concatenate([pl,bg])))
    return out
def evaluate(reps,gam):
    FP={'F':[],'A':[]};REC={'F':[],'A':[]}
    for t,L in reps:
        R=related(t); c=called(L,gam)
        for m in c: FP[m].append(len(c[m]-R)); REC[m].append(int(ti[t] in c[m]))
    return {m:np.array(v) for m,v in FP.items()},{m:np.array(v) for m,v in REC.items()}
devreps=gen(dev_T,100,31,1.0); dev={}
for g in (0.5,1.0,1.5):
    fp,rc=evaluate(devreps,g); dev[g]=dict(fpF=fp['F'].mean(),fpA=fp['A'].mean(),recF=rc['F'].mean(),recA=rc['A'].mean()); print('DEV',g,dev[g],flush=True)
ok=[g for g in dev if dev[g]['recA']>=dev[g]['recF']-0.05]; gam=min(ok,key=lambda g:(dev[g]['fpA'],g)) if ok else 1.0
print('gamma',gam,flush=True)
def verdict(fp,rc):
    d=fp['F']-fp['A']; rs=np.random.RandomState(7); bs=[d[rs.randint(0,len(d),len(d))].mean() for _ in range(10000)]; lo,hi=np.percentile(bs,[2.5,97.5])
    a=(fp['A'].mean()<=0.75*fp['F'].mean()) and lo>0; b=rc['A'].mean()>=rc['F'].mean()-0.05
    v='WIN' if a and b else ('NEGATIVE' if (hi<0 or (not b and fp['A'].mean()<fp['F'].mean())) else 'NULL')
    return dict(fpF=float(fp['F'].mean()),fpA=float(fp['A'].mean()),recF=float(rc['F'].mean()),recA=float(rc['A'].mean()),diff=float(d.mean()),ci=[float(lo),float(hi)],crit_a=bool(a),crit_b=bool(b),verdict=v)
fp,rc=evaluate(gen(test_T,300,32,1.0),gam); out=dict(dev=dev,gamma=gam,test=verdict(fp,rc))
fp2,rc2=evaluate(gen(test_T,300,33,0.5),gam); o2=verdict(fp2,rc2); o2.pop('verdict'); out['secondary_misspecified_sqrt']=o2
json.dump(out,open('results.json','w'),indent=1); print(json.dumps(out))
