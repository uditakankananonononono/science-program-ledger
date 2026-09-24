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
    return float(np.sum([lo.get(s[i:i+6],0.0) for i in range(0,len(s)-5,3)])) if len(s)>=9 else -9e9
test=genes[750:]
allstops={(b_,s_) for a_,b_,s_ in genes}
res={}
for flank in (1000,3000):
    okL=okS=0; N=0; Lerr_neigh=0; Lerr=0
    for a,b,strand in test:
        lo_a=max(0,a-flank); hi_b=min(len(g),b+flank)
        region=g[lo_a:hi_b]
        cand=[c for c in orfs(region,lo_a,strand) if c[2]>=99]
        if not cand: continue
        N+=1
        best_L=max(cand,key=lambda c:c[2])
        best_S=max(cand,key=lambda c:score(g[c[0]:c[1]]))
        okL+=best_L[1]==b; okS+=best_S[1]==b
        if best_L[1]!=b:
            Lerr+=1
            if (best_L[1],strand) in allstops: Lerr_neigh+=1
    res[f'f{flank}']=dict(N=N,longest=okL/N,scored=okS/N,Lerr_neighbor_frac=Lerr_neigh/max(Lerr,1))
    print(flank,res[f'f{flank}'],flush=True)
json.dump(res,open('results/pivot_metrics.json','w'),indent=1)
r=res
print('P1',all(r[f]['scored']>=r[f]['longest']+0.10 for f in ('f1000','f3000')))
print('P2',r['f1000']['scored']>=0.60)
print('P3',r['f3000']['Lerr_neighbor_frac']>=0.30)
