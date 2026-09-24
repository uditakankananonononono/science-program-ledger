#!/usr/bin/env python3
"""amp_predict_family.py - DOC-1-031F: motif-augmented AMP classifier (ARM C: 3-mer
spectrum + 14 explicit Cys/cationic/biophysical features, logistic).
Usage: python3 amp_predict_family.py --model amp_model_family.npz --fasta candidates.faa --out scores.tsv
Output: TSV with header, sequence, AMP probability. Score >= 0.5 => predicted AMP.
NOTE (locked boundary, 2026-09-24): dev MCC 0.946 but frozen independent-cohort MCC 0.391.
The 14 motif features add +0.011 frozen MCC over the 3-mer baseline; family calibration
adds nothing (only 10.9% of family-disjoint positives retain a train homolog under
blastp-short). Treat rankings as hypothesis-generating, not validated predictions.
See REPORT.md."""
import argparse, numpy as np

def fasta_iter(p):
    h = None; s = []
    for line in open(p):
        line = line.strip()
        if line.startswith('>'):
            if h is not None: yield h, ''.join(s)
            h = line[1:]; s = []
        else: s.append(line)
    if h is not None: yield h, ''.join(s)

AA = 'ACDEFGHIKLMNPQRSTVWY'
AMAP = {c: i for i, c in enumerate(AA)}

def kmers(s):
    out = []
    for i in range(len(s) - 2):
        t = s[i:i+3]
        if all(c in AMAP for c in t):
            out.append((AMAP[t[0]] * 20 + AMAP[t[1]]) * 20 + AMAP[t[2]])
    return out

def motif_feats(s):
    L = len(s) or 1
    c = s.count('C')
    cc = s.count('CC')
    cxc = sum(1 for i in range(len(s) - 2) if s[i] == 'C' and s[i+2] == 'C')
    cxxc = sum(1 for i in range(len(s) - 3) if s[i] == 'C' and s[i+3] == 'C')
    cxxx = sum(1 for i in range(len(s) - 4) if s[i] == 'C' and s[i+4] == 'C')
    net = sum(s.count(x) for x in 'KR') - sum(s.count(x) for x in 'DE')
    return [L, c, c / L, cc, cxc, cxxc, cxxx, net / L,
            sum(s.count(x) for x in 'KR') / L,
            sum(s.count(x) for x in 'AILMFWYV') / L,
            s.count('G') / L, s.count('P') / L,
            sum(s.count(x) for x in ['RIV', 'RFG', 'RDY', 'GRL']) / L,
            sum(s.count(x) for x in ['CCV', 'GYC', 'CSR', 'CCL', 'TCY']) / L]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', required=True)
    ap.add_argument('--fasta', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    m = np.load(a.model)
    coef = m['coef']; b = float(m['intercept_'][0])
    with open(a.out, 'w') as o:
        o.write('header\tsequence\tamp_probability\n')
        for h, s in fasta_iter(a.fasta):
            s = s.upper()
            z = b
            for k in kmers(s): z += coef[k]
            for j, v in enumerate(motif_feats(s)): z += coef[8000 + j] * v
            p = 1.0 / (1.0 + np.exp(-z))
            o.write(f'{h}\t{s}\t{p:.4f}\n')
    print('wrote', a.out)

if __name__ == '__main__': main()
