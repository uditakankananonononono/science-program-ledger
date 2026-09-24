#!/usr/bin/env python3
"""phage_host_predict.py - rank candidate prokaryote hosts for a phage genome.

Uses the frozen ARM A KNN-d2 predictor (the validated winner of DOC-1-033:
59.35% species / 68.29% genus top-1 on the frozen 615-pair cohort, vs 12.20%
for the graph model). Given a phage FASTA, compute k=4 kmer frequencies,
d2 (cosine) distance to the 1,260 labeled train phages, similarity-weighted
vote over the k nearest neighbors.

Usage: python3 phage_host_predict.py phage.fa [--k 5] [--assets DIR]
Assets: X_kmer.npy, virus_ids.json, train_labels.json (built from manifest).
"""
import argparse, json, sys
import numpy as np

def kmer_freq(seq, k=4):
    v = np.zeros(4**k, dtype=np.float64)
    idx = {c: i for i, c in enumerate('ACGT')}
    n = 0
    for i in range(len(seq)-k+1):
        w = seq[i:i+k]
        try:
            j = 0
            for c in w: j = j*4 + idx[c]
            v[j] += 1; n += 1
        except KeyError:
            pass
    return v/n if n else v

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fasta'); ap.add_argument('--k', type=int, default=5)
    ap.add_argument('--assets', default='.')
    a = ap.parse_args()
    X = np.load(f'{a.assets}/X_kmer_train.npy')
    labels = json.load(open(f'{a.assets}/train_labels.json'))
    seq = ''.join(l.strip() for l in open(a.fasta) if not l.startswith('>')).upper()
    q = kmer_freq(seq)
    sim = (X @ q) / (np.linalg.norm(X, axis=1)*np.linalg.norm(q) + 1e-12)
    top = np.argsort(-sim)[:a.k]
    votes = {}
    for t in top:
        sp = labels[t]['host_species']
        votes[sp] = votes.get(sp, 0) + float(sim[t])
    ranked = sorted(votes.items(), key=lambda kv: -kv[1])
    print('query:', a.fasta, '| k =', a.k)
    for sp, sc in ranked[:5]:
        print('%.4f\t%s' % (sc, sp))

if __name__ == '__main__':
    main()
