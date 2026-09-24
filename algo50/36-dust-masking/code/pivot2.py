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
def alloc_all(length):
    # 55 disjoint intervals: 50x25 + 5x300, min 50 separation
    sizes=[25]*50+[300]*5
    pos=sorted(rng.choice(np.arange(0,length-400),55,replace=False))
    out=[]; cur=0
    for i,p in enumerate(pos):
        p=max(p,cur); out.append((p,sizes[i])); cur=p+sizes[i]+50
    return out
I1=alloc_all(50000); I2=alloc_all(50000)
s1=list(rand(50000)); s2=list(rand(50000))
ortho_pos=[]
for i in range(50):
    k=rand(25)
    p1,_=I1[i]; p2,_=I2[i]
    s1[p1:p1+25]=list(k); s2[p2:p2+25]=list(k)
    ortho_pos.append((p1,p2))
spur_pos=[]
for i in range(5):
    motif=rng.choice(['A','CA','GT']); r=(motif*300)[:300]
    p1,_=I1[50+i]; p2,_=I2[50+i]
    s1[p1:p1+300]=list(r); s2[p2:p2+300]=list(r)
    spur_pos.append((p1,p2))
s1=''.join(s1); s2=''.join(s2)
m1=mask(s1); m2=mask(s2)
ret=sum(1 for p1,p2 in ortho_pos if not m1[p1:p1+25].any() and not m2[p2:p2+25].any())
# spurious removal: fraction of interior 25-mers whose windows fully masked in at least one sequence
rem=0; tot=0
for p1,p2 in spur_pos:
    for off in range(0,300-24,25):
        tot+=1
        if m1[p1+off:p1+off+25].all() or m2[p2+off:p2+off+25].all(): rem+=1
res=dict(recall=det/40,false_mask=float(mn.mean()),ortho_retained=ret,spur_removed=rem,spur_total=tot)
json.dump(res,open('results/pivot_metrics.json','w'),indent=1)
print(res)
print('Q1',det/40>=0.95 and mn.mean()<=0.02)
print('Q2',rem/tot>=0.95 and ret>=49)
