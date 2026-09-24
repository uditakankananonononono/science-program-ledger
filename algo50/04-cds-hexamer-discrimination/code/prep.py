import os, subprocess, hashlib, time, json, random
from Bio import SeqIO
from Bio.Seq import Seq
STOPS={'TAA','TAG','TGA'}
os.makedirs('data',exist_ok=True)
def fetch(acc):
    p=f'data/{acc}.gb'
    if not os.path.exists(p):
        url=f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={acc}&rettype=gbwithparts&retmode=text'
        subprocess.run(['curl','-sL',url,'-o',p],check=True)
    return p
def orfs_genome_coords(genome):
    comp=str.maketrans('ACGT','TGCA'); res=[]; n=len(genome)
    for strand,seq in ((1,genome),(-1,genome.translate(comp)[::-1])):
        for frame in range(3):
            start=frame; i=frame
            while i+3<=n:
                if seq[i:i+3] in STOPS:
                    if i-start>=150:
                        res.append((start,i) if strand==1 else (n-i,n-start))
                    start=i+3
                i+=3
            if n-start>=150:
                res.append((start,n) if strand==1 else (0,n-start))
    return res
def cds_entries(recs):
    out=[]
    for r in recs:
        for f in r.features:
            if f.type!='CDS': continue
            try: s=str(f.extract(r.seq)).upper()
            except Exception: continue
            if len(s)<150 or set(s)-set('ACGT'): continue
            if '*' in str(Seq(s).translate(table=11))[:-1]: continue
            out.append((int(f.location.start),int(f.location.end),s))
    return out
final={}
for acc,name in (('NC_000913.3','ecoli'),('NC_000964.3','bsub'),('NC_000962.3','mtb')):
    recs=list(SeqIO.parse(fetch(acc),'gb'))
    genome=''.join(str(r.seq) for r in recs).upper()
    cds=cds_entries(recs)
    spans=[(a,b) for a,b,_ in cds]
    orfs=orfs_genome_coords(genome)
    comp=str.maketrans('ACGT','TGCA')
    def seq_of(a,b,strand_hint=None):
        return genome[a:b]
    shadow=[]
    for (a,b) in orfs:
        contained=False
        for (cs,ce) in spans:
            if a<=cs and b>=ce: contained=True; break
        if contained: continue
        s=genome[a:b]
        # ORF may be on minus strand; the ORF sequence in its own reading direction:
        # we stored coords only; reading direction unknown -> score both? No: keep both orientations as separate candidates is wrong.
        # Convention: score the plus-strand substring AND its revcomp as the same candidate is ambiguous.
        # Fix: regenerate with strand kept.
        shadow.append((a,b))
    # regenerate with strand info
    shadow_seqs=[]
    n=len(genome)
    for strand,seq in ((1,genome),(-1,genome.translate(comp)[::-1])):
        for frame in range(3):
            start=frame; i=frame
            while i+3<=n:
                if seq[i:i+3] in STOPS:
                    if i-start>=150:
                        a,b=(start,i) if strand==1 else (n-i,n-start)
                        if not any(a<=cs and b>=ce for cs,ce in spans):
                            shadow_seqs.append(seq[start:i])
                    start=i+3
                i+=3
            if n-start>=150:
                a,b=(start,n) if strand==1 else (0,n-start)
                if not any(a<=cs and b>=ce for cs,ce in spans):
                    shadow_seqs.append(seq[start:n])
    # 1:1 length-matched subsample, seed 1
    rng=random.Random(1)
    pos=[s for _,_,s in cds]
    sh_sorted=sorted(shadow_seqs,key=len)
    import bisect
    lens=[len(s) for s in sh_sorted]
    used=set(); neg=[]
    for p in pos:
        L=len(p); lo=bisect.bisect_left(lens,int(L*0.9)); hi=bisect.bisect_right(lens,int(L*1.1))
        cand=[k for k in range(lo,hi) if k not in used] or [k for k in range(len(sh_sorted)) if k not in used]
        if not cand: break
        k=rng.choice(cand); used.add(k); neg.append(sh_sorted[k])
    final[name]=dict(pos=pos,neg=neg,n_shadow_total=len(shadow_seqs))
    print(name,'pos',len(pos),'shadow',len(shadow_seqs),'neg_matched',len(neg))
json.dump(final,open('data/sets.json','w'))
open('data/retrieved_at.txt','w').write(time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
with open('data/SHA256_raw.txt','w') as f:
    for fn in sorted(os.listdir('data')):
        if fn.endswith('.gb'): f.write(hashlib.sha256(open('data/'+fn,'rb').read()).hexdigest()+'  '+fn+'\n')
    f.write(hashlib.sha256(open('data/sets.json','rb').read()).hexdigest()+'  sets.json\n')
