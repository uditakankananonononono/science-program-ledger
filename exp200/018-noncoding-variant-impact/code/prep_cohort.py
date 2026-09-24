#!/usr/bin/env python3
"""prep_cohort.py - build locked dev (chr21) and frozen (chr22) cohorts from clinvar_chr21_22_noncoding.tsv.
Dev: chr21 all P + 3:1 B subsample (seed 7). Frozen: chr22 all P + 3:1 B (seed 7). Frozen untouched until G2."""
import random
rows=[l.rstrip('\n').split('\t') for l in open('results/clinvar_chr21_22_noncoding.tsv')]
rng=random.Random(7)
for chrom,out in [('chr21','results/dev_chr21.tsv'),('chr22','results/frozen_chr22.tsv')]:
    P=[r for r in rows if r[0]==chrom and r[4]=='P']
    B=[r for r in rows if r[0]==chrom and r[4]=='B']
    Bs=rng.sample(B,3*len(P))
    with open(out,'w') as f:
        for r in P+Bs: f.write('\t'.join(r)+'\n')
    print(out, len(P),'P',len(Bs),'B')
