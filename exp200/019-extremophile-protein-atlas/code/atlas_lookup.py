#!/usr/bin/env python3
"""atlas_lookup.py PROTEIN.fasta - report how a protein set compares to the DOC-1-019 biome atlas
(IVYWREL / D+E fractions vs per-biome atlas values). NOTE: composition fingerprints dev-learnable
but NOT frozen-stable across studies (Arm S batch collapse, REPORT.md) - descriptive tool, not a classifier."""
import sys, json
def recs(p):
    out=[]
    for blk in open(p).read().split('\n>'):
        blk=blk.lstrip('>')
        if blk and '\n' in blk:
            h,s=blk.split('\n',1); out.append(s.replace('\n',''))
    return out
def frac(s,res): return sum(1 for c in s if c in res)/len(s)
g3=json.load(open('results/g3_mechanism.json'))
seqs=recs(sys.argv[1])
ivy=sum(frac(s,'IVYWREL') for s in seqs)/len(seqs); de=sum(frac(s,'DE') for s in seqs)/len(seqs)
print(f'n={len(seqs)} IVYWREL={ivy:.4f} D+E={de:.4f}')
for b,v in g3['atlas_table'].items():
    print(f'  {b:12s} IVYWREL={v["ivywrel"]:.4f} (delta {ivy-v["ivywrel"]:+.4f})  D+E={v["DE"]:.4f} (delta {de-v["DE"]:+.4f})')
