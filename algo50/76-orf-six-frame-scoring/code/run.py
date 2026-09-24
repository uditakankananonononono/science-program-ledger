import numpy as np, json
from Bio import SeqIO
from collections import Counter
rec=next(SeqIO.parse('../04-cds-hexamer-discrimination/data/NC_000913.3.gb','genbank'))
g=str(rec.seq).upper()
cds=[f for f in rec.features if f.type=='CDS' and 'gene' in f.qualifiers and len(f)>=300]
# unique by (start,end)
seen=set(); genes=[]
for f in cds:
    k=(int(f.location.start),int(f.location.end),f.location.strand)
    if k in seen: continue
    seen.add(k); genes.append(k)
genes=genes[:1500]
print('genes',len(genes),flush=True)
stops={'TAA','TAG','TGA'}
def orfs(s,base,strand):
    out=[]
    for frame in range(3):
        i=frame
        while i<len(s)-2:
            c=s[i:i+3]
            if c=='ATG':
                j=i
                while j<len(s)-2 and s[j:j+3] not in stops: j+=3
                if j<len(s)-2:
                    out.append((base+i,base+j+3,j+3-i))
                    i=j+3; continue
            i+=3
    return out
# hexamer table: in-frame hexamers over a training half of genes vs shuffled background
def hexset(seq):
    return Counter(seq[i:i+6] for i in range(0,len(seq)-5))
train=genes[:750]
fg=Counter()
for a,b,_ in train:
    s=g[a:b]
    fg.update(hexset(s[:len(s)//3*3]))
bg=Counter()
rng=np.random.default_rng(0)
for a,b,_ in train:
    s=list(g[a:b]); rng.shuffle(s); bg.update(hexset(''.join(s)))
lo={}
allh=set(fg)|set(bg)
for h in allh:
    lo[h]=np.log((fg[h]+0.5)/(bg[h]+0.5))
def score(s):
    return float(np.mean([lo.get(s[i:i+6],0.0) for i in range(0,len(s)-5,3)])) if len(s)>=9 else -9
test=genes[750:]
okL=okS=0; dis=0; disS=0; N=0
for a,b,strand in test:
    lo_a=max(0,a-3000); hi_b=min(len(g),b+3000)
    region=g[lo_a:hi_b]
    cand=orfs(region,lo_a,strand)
    # true stop position
    tstop=b
    cand=[c for c in cand if c[2]>=99]
    if not cand: continue
    N+=1
    best_L=max(cand,key=lambda c:c[2])
    best_S=max(cand,key=lambda c:score(g[c[0]:c[1]]))
    okL+=best_L[1]==tstop; okS+=best_S[1]==tstop
    if best_L!=best_S:
        dis+=1; disS+=best_S[1]==tstop
res=dict(N=N,longest=okL/N,scored=okS/N,disagree=dis,disagree_scored_right=disS/max(dis,1))
json.dump(res,open('results/results.json','w'),indent=1)
print(res)
print('G1',okS/N>=okL/N+0.10,'G2',1-okL/N>=0.15,'G3',okS/N>=0.85,'G4',disS/max(dis,1)>=0.60)
