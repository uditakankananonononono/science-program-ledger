import json, random
import numpy as np
from Bio import SeqIO
from Bio.Seq import Seq
STOPS={'TAA','TAG','TGA'}
comp=str.maketrans('ACGT','TGCA')
def load(acc):
    recs=list(SeqIO.parse(f'data/{acc}.gb','gb'))
    g=''.join(str(r.seq) for r in recs).upper()
    starts=[]
    for r in recs:
        for f in r.features:
            if f.type!='CDS': continue
            try: s=str(f.extract(r.seq)).upper()
            except Exception: continue
            if len(s)<150 or set(s)-set('ACGT'): continue
            if '*' in str(Seq(s).translate(table=11))[:-1]: continue
            # upstream 100nt in reading direction
            if f.location.strand==1:
                st=int(f.location.start); up=g[max(0,st-100):st]
            else:
                st=int(f.location.end); up=g[st:st+100].translate(comp)[::-1]
            if len(up)==100: starts.append(up)
    # shadow ORF starts
    spans=[(int(f.location.start),int(f.location.end)) for r in recs for f in r.features if f.type=='CDS']
    n=len(g); shadows=[]
    for strand,sq in ((1,g),(-1,g.translate(comp)[::-1])):
        for frame in range(3):
            start=frame; i=frame
            while i+3<=n:
                if sq[i:i+3] in STOPS:
                    if i-start>=150:
                        a,b=(start,i) if strand==1 else (n-i,n-start)
                        if not any(a<=cs and b>=ce for cs,ce in spans):
                            up=sq[max(0,start-100):start]
                            if len(up)==100: shadows.append(up)
                    start=i+3
                i+=3
    return starts,shadows
def score(up,w):
    # w=(lo,hi) positions in 100nt upstream: index 99 = -1 (adjacent to start)
    # window -20..-5 => indices 80..94 ; -60..-45 => 40..54
    lo,hi=w; best=0
    cons='AGGAGG'
    seg=up[lo:hi+1]
    for i in range(len(seg)-5):
        m=sum(1 for a,b in zip(seg[i:i+6],cons) if a==b)
        best=max(best,m)
    return best
rng=random.Random(1)
out={}
for name,acc in (('ecoli','NC_000913.3'),('bsub','NC_000964.3'),('mtb','NC_000962.3')):
    pos,neg=load(acc)
    rng.shuffle(neg); neg=neg[:len(pos)]
    from sklearn.metrics import roc_auc_score
    y=[1]*len(pos)+[0]*len(neg)
    for wname,w in (('M1',(80,94)),('M2',(40,54))):
        s=[score(u,w) for u in pos]+[score(u,w) for u in neg]
        out[f'{name}_{wname}_auroc']=roc_auc_score(y,s)
    p5=np.mean([score(u,(80,94))>=5 for u in pos]); n5=np.mean([score(u,(80,94))>=5 for u in neg])
    out[f'{name}_frac_ge5']={'pos':float(p5),'neg':float(n5)}
    out[f'{name}_mean_M1']=float(np.mean([score(u,(80,94)) for u in pos]))
    out[f'{name}_mean_M2']=float(np.mean([score(u,(40,54)) for u in pos]))
    print(name,{k:round(v,3) if isinstance(v,float) else v for k,v in out.items() if k.startswith(name)})
json.dump(out,open('results/results.json','w'),indent=1)
print('G1',out['ecoli_M1_auroc']>=0.70,'G2',out['ecoli_frac_ge5']['pos']>=2*out['ecoli_frac_ge5']['neg'],
      'G3',out['ecoli_mean_M1']>=1.5*out['ecoli_mean_M2'],'G4',out['bsub_M1_auroc']>=0.65)
import hashlib,time
with open('data/SHA256_raw.txt','w') as f:
    for fn in ('NC_000913.3.gb','NC_000964.3.gb','NC_000962.3.gb'):
        f.write(hashlib.sha256(open('data/'+fn,'rb').read()).hexdigest()+'  '+fn+'\n')
open('data/retrieved_at.txt','w').write(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())+' (accessions as algo50/04)')
