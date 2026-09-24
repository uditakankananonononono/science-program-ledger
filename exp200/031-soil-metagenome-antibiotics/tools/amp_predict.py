#!/usr/bin/env python3
"""amp_predict.py - DOC-1-031: antimicrobial-peptide discovery classifier (3-mer spectrum
logistic regression, homology-pruned training - the honest-generalization model).
Usage: python3 amp_predict.py --model amp_model_pruned.npz --fasta candidates.faa --out scores.tsv
Output: TSV with header, sequence, AMP probability. Score >= 0.5 => predicted AMP.
NOTE (locked boundary, 2026-09-24): this model achieves MCC 0.80 on the iAMP-2L test set under
80%-identity homology control, but only MCC 0.37 on an independent DRAMP cohort - treat
rankings as hypothesis-generating, not validated predictions. See REPORT.md."""
import argparse, numpy as np
def fasta_iter(p):
    h=None;s=[]
    for line in open(p):
        line=line.strip()
        if line.startswith('>'):
            if h is not None: yield h,''.join(s)
            h=line[1:];s=[]
        else: s.append(line)
    if h is not None: yield h,''.join(s)
def kmers(s):
    from itertools import product
    aa='ACDEFGHIKLMNPQRSTVWY'; amap={c:i for i,c in enumerate(aa)}
    out=[]
    for i in range(len(s)-2):
        t=s[i:i+3]
        if all(c in amap for c in t):
            out.append((amap[t[0]]*20+amap[t[1]])*20+amap[t[2]])
    return out
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--model',required=True); ap.add_argument('--fasta',required=True); ap.add_argument('--out',required=True)
    a=ap.parse_args()
    m=np.load(a.model); coef=m['coef']; b=float(m['intercept'][0])
    with open(a.out,'w') as o:
        o.write('header\tsequence\tamp_probability\n')
        for h,s in fasta_iter(a.fasta):
            z=b
            for k in kmers(s.upper()): z+=coef[k]
            p=1.0/(1.0+np.exp(-z))
            o.write(f'{h}\t{s}\t{p:.4f}\n')
    print('wrote',a.out)
if __name__=='__main__': main()
