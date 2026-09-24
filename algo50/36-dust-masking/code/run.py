import numpy as np, json
rng=np.random.default_rng(7)
B='ACGT'
def rand(n): return ''.join(rng.choice(list(B),n))
# build test sequence with implants
regions=[]
parts=[]; pos=0
seq=[]
for i in range(40):
    seg=rand(rng.integers(4000,6000)); seq.append(seg); pos+=len(seg)
    L=int(rng.integers(100,600))
    if i<20:
        motif=rng.choice(['A','C','G','T','AC','GT','CAG','ATA'])
        r=(motif*(L//len(motif)+1))[:L]
    else:
        b=rng.choice(list(B)); r=''.join(rng.choice([b,'x'],L,p=[0.7,0.3])).replace('x',rng.choice([c for c in B if c!=b]))
    regions.append((pos,pos+L)); seq.append(r); pos+=L
seq=''.join(seq)
neg=rand(20000)
pilot=rand(20000)
def tri_scores(s,w=64):
    # score per window start
    t=np.zeros(len(s),dtype=np.int64)
    code={'A':0,'C':1,'G':2,'T':3}
    arr=np.frombuffer(s.encode(),dtype=np.uint8)
    c0=np.array([code[chr(x)] for x in arr])
    tr=c0[:-2]*16+c0[1:-1]*4+c0[2:]
    # sliding triplet counts via diff trick is complex; do window loop vectorized-ish
    sc=[]
    for i in range(0,len(s)-w+1,16):
        win=tr[i:i+w-2]
        cnt=np.bincount(win,minlength=64)
        sc.append((cnt*(cnt-1)//2).sum())
    return np.array(sc)
pilot_sc=tri_scores(pilot)
thr=pilot_sc.mean()+3*pilot_sc.std()
print('pilot threshold',thr,flush=True)
def mask_regions(s):
    sc=tri_scores(s)
    starts=np.where(sc>thr)[0]*16
    m=np.zeros(len(s),bool)
    for st in starts: m[st:st+64]=True
    return m
m=mask_regions(seq)
det=sum(1 for a,b in regions if m[a:b].mean()>=0.5)
mn=mask_regions(neg)
# alignment artifact test
s1=list(rand(50000)); s2=list(rand(50000))
ortho=[]
for i in range(50):
    k=rand(25); p1=rng.integers(0,len(s1)-25); p2=rng.integers(0,len(s2)-25)
    s1[p1:p1+25]=k; s2[p2:p2+25]=k; ortho.append(k)
spur=0
for i in range(5):
    motif=rng.choice(['A','CA','GT'])
    r=(motif*300)[:300]
    p1=rng.integers(0,len(s1)-300); p2=rng.integers(0,len(s2)-300)
    s1[p1:p1+300]=r; s2[p2:p2+300]=r
s1=''.join(s1); s2=''.join(s2)
def kmers(s,k=25):
    return set(s[i:i+k] for i in range(0,len(s)-k+1))
def masked_kmers(s,k=25):
    m=mask_regions(s)
    return set(s[i:i+k] for i in range(0,len(s)-k+1) if not m[i:i+k].any())
u1,u2=kmers(s1),kmers(s2)
shared_un=len(u1&u2)
m1,m2=masked_kmers(s1),masked_kmers(s2)
shared_m=len(m1&m2)
ortho_kept=sum(1 for k in ortho if k in m1 and k in m2)
spur_removed=shared_un-shared_m
res=dict(threshold=float(thr),recall=det/40,false_mask=float(mn.mean()),
         shared_unmasked=shared_un,shared_masked=shared_m,ortho_kept=ortho_kept,
         spur_removed_frac=spur_removed/max(shared_un-shared_m+ (shared_m - ortho_kept),1))
res['spurious_removed_frac']= (shared_un-shared_m)/shared_un if shared_un else 1.0
json.dump(res,open('results/results.json','w'),indent=1)
print(res,flush=True)
print('G1',det/40>=0.95,'G2',mn.mean()<=0.02,'G3',res['spurious_removed_frac']>=0.95 and ortho_kept>=49)
