import gzip,collections,numpy as np,pickle,math
# ontology
par=collections.defaultdict(set); ns={}; cur=None; obs=False
for l in open('../data/go-basic.obo'):
    l=l.strip()
    if l=='[Term]': cur=None; obs=False; continue
    if l.startswith('[') : cur=None; continue
    if l.startswith('id: GO:'): cur=l[4:]
    elif cur and l.startswith('namespace: '): ns[cur]=l[11:]
    elif cur and l.startswith('is_a: '): par[cur].add(l[6:16])
    elif cur and l.startswith('relationship: part_of '): par[cur].add(l[22:32])
    elif cur and l=='is_obsolete: true': ns.pop(cur,None); cur=None
anc={}
def A(t):
    if t in anc: return anc[t]
    s={t}
    for p in par.get(t,()): s|=A(p)
    anc[t]=frozenset(s); return anc[t]
import sys; sys.setrecursionlimit(10000)
ann=collections.defaultdict(set)
with gzip.open('../data/goa_human.gaf.gz','rt') as f:
    for l in f:
        if l[0]=='!': continue
        t=l.split('\t')
        if 'NOT' in t[3] or t[6]=='IPI' or t[4]=='GO:0005515' or t[4] not in ns: continue
        ann[t[2]].add(t[4])
# IC per namespace from propagated counts
IC={}
for o in ('biological_process','molecular_function','cellular_component'):
    cnt=collections.Counter(); n=0
    for g,ts in ann.items():
        s=set().union(*[A(t) for t in ts if ns[t]==o]) if any(ns[t]==o for t in ts) else set()
        if s: n+=1; cnt.update(s)
    for t,c in cnt.items(): IC[t]=-math.log(c/n)
info={}
with gzip.open('../data/9606.protein.info.v12.0.txt.gz','rt') as f:
    next(f)
    for l in f: t=l.split('\t'); info[t[0]]=t[1]
allp=set(); pos=set()
with gzip.open('../data/9606.protein.physical.links.detailed.v12.0.txt.gz','rt') as f:
    next(f)
    for l in f:
        a,b,e=l.split()[:3]; a,b=info.get(a),info.get(b)
        if not a or not b or a==b: continue
        k=tuple(sorted((a,b))); allp.add(k)
        if int(e)>=700: pos.add(k)
hasBP=lambda g:any(ns[t]=='biological_process' for t in ann.get(g,()))
pos=sorted(k for k in pos if hasBP(k[0]) and hasBP(k[1]))
rng=np.random.default_rng(31)
P=[pos[i] for i in rng.choice(len(pos),10000,replace=False)]
pool=[g for k in pos for g in k]; N=set()
while len(N)<10000:
    a,b=pool[rng.integers(len(pool))],pool[rng.integers(len(pool))]
    k=tuple(sorted((a,b)))
    if a!=b and k not in allp: N.add(k)
N=sorted(N); rng.shuffle(N)
print('terms',len(ns),'annotated genes',len(ann),'eligible pos pairs',len(pos),'sampled',len(P),len(N))
pickle.dump({'par':dict(par),'ns':ns,'ann':{g:set(v) for g,v in ann.items()},'IC':IC,'P':P,'N':N},open('../data/prep.pkl','wb'))
