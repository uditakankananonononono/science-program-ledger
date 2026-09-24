import json
import numpy as np
from Bio import SeqIO
STOPS={'TAA','TAG','TGA'}
def genome_of(acc): return ''.join(str(r.seq) for r in SeqIO.parse(f'data/{acc}.gb','gb')).upper()
G={'ecoli':'NC_000913.3','shigella':'NC_004741','bsub':'NC_000964.3','mtb':'NC_000962.3'}
sets=json.load(open('../04-cds-hexamer-discrimination/data/sets.json'))
out={}
for name,acc in G.items():
    g=genome_of(acc)
    n=len(g)
    f={b:g.count(b)/n for b in 'ACGT'}
    pstop=f['T']*f['A']*f['A']+f['T']*f['A']*f['G']+f['T']*f['G']*f['A']
    pred=1/pstop
    lens=[]
    for frame in range(3):
        last=frame
        i=frame
        while i+3<=n:
            if g[i:i+3] in STOPS:
                lens.append((i-last)//3); last=i+3
            i+=3
    obs=float(np.mean(lens))
    sh=float(np.mean([len(s)//3 for s in sets[name]['neg']]))
    out[name]=dict(gc=sum(f[b] for b in 'GC'),pred=pred,obs=obs,ratio=obs/pred,shadow=sh,shadow_ratio=sh/pred)
    print(name,out[name])
json.dump(out,open('results/results.json','w'),indent=1)
print('G1',all(abs(v['ratio']-1)<=0.25 for v in out.values()))
ro=out['mtb']['obs']/out['ecoli']['obs']; rp=out['mtb']['pred']/out['ecoli']['pred']
print('G2',abs(ro/rp-1)<=0.25,ro,rp)
print('G3',all(0.5<=v['shadow_ratio']<=2 for v in out.values()))
