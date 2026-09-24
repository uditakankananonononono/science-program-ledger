#!/usr/bin/env python3
"""score_variant.py CHROM POS - score a non-coding UTR variant with the frozen DOC-1-018 model.
Fetches phyloP/phastCons live from UCSC (hg38); uses local chr21/chr22 fasta + cCRE caches when available.
Model: LR(f1-f6) trained on ClinVar chr21 UTR stratum, frozen-validated chr22 UTR AUROC 0.9015 (REPORT.md).
NOT a clinical tool; research use only."""
import sys, json, bisect, requests
chrom,pos=sys.argv[1],int(sys.argv[2])
API='https://api.genome.ucsc.edu/getData'
def track(tr,a,b):
    r=requests.get(f'{API}/track?genome=hg38;track={tr};chrom={chrom};start={a};end={b}',timeout=25)
    return {int(d['start']):float(d['value']) for d in r.json().get(tr,[])}
pv=track('phyloP100way',pos-10,pos+11); cv=track('phastCons100way',pos,pos+1)
import os
fa=f'results/local/{chrom}.fa'
if os.path.exists(fa):
    s=open(fa).read().split('\n',1)[1].replace('\n','')[pos-25:pos+26]
else:
    r=requests.get(f'{API}/sequence?genome=hg38;chrom={chrom};start={pos-25};end={pos+26}',timeout=25)
    s=r.json().get('dna','').upper()
cc=f'results/local/ccre_{chrom}.txt'; f6=0
if os.path.exists(cc):
    for l in open(cc):
        a,b=l.strip().split('-')
        if int(a)<pos+26 and int(b)>pos-25: f6=1; break
win=[pv.get(p) for p in range(pos-10,pos+11) if p in pv]
ft={'f1':pv.get(pos,0.0),'f2':cv.get(pos,0.0),'f3':sum(win)/len(win) if win else 0.0,
    'f4':(s.count('G')+s.count('C'))/max(1,len(s)),'f5':s.count('CG')/max(1,len(s)-1),'f6':f6}
m=json.load(open('results/model_utr.json'))
z=[(ft[k]-m['mean'][i])/m['std'][i] for i,k in enumerate(m['features'])]
logit=m['intercept']+sum(c*x for c,x in zip(m['coef'],z))
p=1/(1+2.718281828**(-logit))
print(json.dumps({'chrom':chrom,'pos':pos,'features':ft,'pathogenic_probability':round(p,4)},indent=1))
