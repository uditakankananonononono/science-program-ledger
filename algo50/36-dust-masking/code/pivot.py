import numpy as np, json
rng=np.random.default_rng(7)
B='ACGT'
def rand(n): return ''.join(rng.choice(list(B),n))
regions=[]; seq=[]; pos=0
for i in range(40):
    seg=rand(rng.integers(4000,6000)); seq.append(seg); pos+=len(seg)
    L=int(rng.integers(100,600))
    if i<20:
        motif=rng.choice(['A','C','G','T','AC','GT','CAG','ATA']); r=(motif*(L//len(motif)+1))[:L]
    else:
        b=rng.choice(list(B)); r=''.join(rng.choice([b,'x'],L,p=[0.7,0.3])).replace('x',rng.choice([c for c in B if c!=b]))
    regions.append((pos,pos+L)); seq.append(r); pos+=L
seq=''.join(seq); neg=rand(20000); pilot=rand(20000)
code={'A':0,'C':1,'G':2,'T':3}
def scores(s,w=64):
    arr=np.frombuffer(s.encode(),dtype=np.uint8)
    c0=np.array([code[chr(x)] for x in arr])
    tr=c0[:-2]*16+c0[1:-1]*4+c0[2:]
    out=[]
    for i in range(0,len(s)-w+1,16):
        cnt=np.bincount(tr[i:i+w-2],minlength=64); out.append((cnt*(cnt-1)//2).sum())
    return np.array(out)
thr=scores(pilot).mean()+3*scores(pilot).std()
def mask(s):
    sc=scores(s); m=np.zeros(len(s),bool)
    for st in np.where(sc>thr)[0]*16: m[st:st+64]=True
    return m
m=mask(seq); det=sum(1 for a,b in regions if m[a:b].mean()>=0.5); mn=mask(neg)
# collision-free placement
def alloc(n,length,size):
    pos=sorted(rng.choice(np.arange(0,length-size-50),n,replace=False))
    out=[]; cur=0
    for p in pos:
        p=max(p,cur); out.append(p); cur=p+size+50
    return out
s1=list(rand(50000)); s2=list(rand(50000))
o1=alloc(50,50000,25); o2=alloc(50,50000,25)
q1=alloc(5,50000,300); q2=alloc(5,50000,300)
ortho=[]
for i in range(50):
    k=rand(25); s1[o1[i]:o1[i]+25]=list(k); s2[o2[i]:o2[i]+25]=list(k); ortho.append(k)
motifs=[]
for i in range(5):
    motif=rng.choice(['A','CA','GT']); motifs.append(motif)
    r=(motif*300)[:300]
    s1[q1[i]:q1[i]+300]=list(r); s2[q2[i]:q2[i]+300]=list(r)
s1=''.join(s1); s2=''.join(s2)
u1=set(s1[i:i+25] for i in range(len(s1)-24)); u2=set(s2[i:i+25] for i in range(len(s2)-24))
mm1=mask(s1); mm2=mask(s2)
def mk(s,m): return set(s[i:i+25] for i in range(len(s)-24) if not m[i:i+25].any())
k1,k2=mk(s1,mm1),mk(s2,mm2)
shared_u=u1&u2; shared_m=k1&k2
ortho_intact=sum(1 for k in ortho if k in u1 and k in u2)
ortho_kept=sum(1 for k in ortho if k in k1 and k in k2)
lowcomp_shared_u=len(shared_u)-ortho_intact
lowcomp_shared_m=len(shared_m)-ortho_kept
res=dict(recall=det/40,false_mask=float(mn.mean()),ortho_intact=ortho_intact,
         lowcomp_shared_unmasked=lowcomp_shared_u,lowcomp_shared_masked=lowcomp_shared_m,
         ortho_kept=ortho_kept)
json.dump(res,open('results/pivot_metrics.json','w'),indent=1)
print(res)
print('P1',ortho_intact==50 and det/40>=0.95 and mn.mean()<=0.02)
print('P2',lowcomp_shared_m<=0.05*max(lowcomp_shared_u,1) and ortho_kept>=49)
