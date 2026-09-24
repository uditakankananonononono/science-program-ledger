import numpy as np, json
rng=np.random.default_rng(53)
B='ACGT'
seeds={'contig8':[1]*8,'spaced8':[1,1,0,1,0,0,1,1,0,1,1,0,1,0,1,1,0,1,1],  # 10 ones of 19? count below
       'contig12':[1]*12}
seeds['spaced8']=[1,1,0,1,1,0,1,1]  # weight 6? fix: explicit weight-8 spaced, span 11
seeds['spaced8']=[1,1,0,1,0,1,1,0,1,1,1]
w8=sum(seeds['spaced8'])
assert w8==8, w8
def hit(a,b,pat):
    L=len(pat); care=[i for i,x in enumerate(pat) if x]
    for i in range(len(a)-L+1):
        if all(a[i+j]==b[i+j] for j in care): return True
    return False
res={}
for q in (0.70,0.80,0.90,0.95):
    row={}
    for name,pat in seeds.items():
        h=0; N=400
        for _ in range(N):
            a=''.join(rng.choice(list(B),200))
            b=''.join(c if rng.random()<q else rng.choice([x for x in B if x!=c]) for c in a)
            h+=hit(a,b,pat)
        row[name]=h/N
    res[str(q)]=row
    print(q,row,flush=True)
# background
bg={}
for name,pat in seeds.items():
    h=0; N=400
    for _ in range(N):
        a=''.join(rng.choice(list(B),200)); b=''.join(rng.choice(list(B),200))
        h+=hit(a,b,pat)
    bg[name]=h/N
res['bg']=bg
print('bg',bg,'weights',{k:sum(v) for k,v in seeds.items()},flush=True)
json.dump(res,open('results/results.json','w'),indent=1)
G1=res['0.8']['spaced8']>=res['0.8']['contig8']+0.10
G2=res['0.7']['spaced8']>=0.90 and res['0.7']['contig12']<=0.60
# theory: expected background ~ 1-(1-4^-w)^(200-span+1)
import math
th={n:1-(1-4**(-sum(p)))**(200-len(p)+1) for n,p in seeds.items()}
G3=all(0.5<=bg[n]/th[n]<=2 for n in bg)
G4=all(all(res[str(b)][n]<=res[str(a)][n]+1e-9 for a,b in zip((0.7,0.8,0.9),(0.8,0.9,0.95))) for n in seeds)
print('G1',G1,'G2',G2,'G3',G3,th,'G4',G4)
