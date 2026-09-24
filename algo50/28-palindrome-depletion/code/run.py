import json
import numpy as np
from Bio import SeqIO
from itertools import product
comp=str.maketrans('ACGT','TGCA')
def genome_of(acc): return ''.join(str(r.seq) for r in SeqIO.parse(f'data/{acc}.gb','gb')).upper()
G={'ecoli':'NC_000913.3','shigella':'NC_004741','bsub':'NC_000964.3','mtb':'NC_000962.3'}
RS=['GAATTC','GGATCC','AAGCTT','CTGCAG','GATATC','GGTACC','GAGCTC','GTCGAC','TCTAGA','GCATGC']
def ispal(s): return s==s.translate(comp)[::-1]
hexamers=[''.join(p) for p in product('ACGT',repeat=6)]
pals=[h for h in hexamers if ispal(h)]
nonpals=[h for h in hexamers if not ispal(h)]
out={}
for name,acc in G.items():
    g=genome_of(acc); n=len(g)
    f1={b:g.count(b)/n for b in 'ACGT'}
    f2={}
    for a in 'ACGT':
        for b in 'ACGT': f2[a+b]=g.count(a+b)/(n-1)
    def expc(s):
        p=f1[s[0]]
        for i in range(5): p*=f2[s[i:i+2]]/f1[s[i]]
        return p*(n-5)
    oe={}
    for h in hexamers:
        c=g.count(h)
        oe[h]=c/max(1e-9,expc(h))
    pal_oe=np.array([oe[h] for h in pals])
    rs_oe=np.array([oe[h] for h in RS])
    other_oe=np.array([oe[h] for h in pals if h not in RS])
    nonp_oe=np.array([oe[h] for h in nonpals])
    out[name]=dict(pal_med=float(np.median(pal_oe)),rs_med=float(np.median(rs_oe)),
                   otherpal_med=float(np.median(other_oe)),nonpal_medabs=float(np.median(np.abs(nonp_oe-1))))
    print(name,out[name],flush=True)
json.dump(out,open('results/results.json','w'),indent=1)
v=list(out.values())
print('G1',sum(1 for x in v if x['pal_med']<0.9)>=3)
print('G2',sum(1 for x in v if x['rs_med']<x['otherpal_med'])>=3)
print('G3',out['mtb']['pal_med']<0.9 and out['mtb']['rs_med']<out['mtb']['otherpal_med'])
print('G4',all(x['nonpal_medabs']<0.2 for x in v))
