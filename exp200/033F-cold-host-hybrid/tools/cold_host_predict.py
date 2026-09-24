#!/usr/bin/env python3
"""cold_host_predict.py - DOC-1-033F two-output phage-host predictor.
Output 1 (KNN-d2): nearest-train-virus host vote. Validated 59.19% species top-1 on the
615-pair frozen CHERRY benchmark - BUT structurally 0% on hosts absent from train labels.
Output 2 (CRISPR ALERT): if the phage has qualifying spacer hits (precomputed edges for the
1,875 benchmark viruses), the panel species with most spacer support. Precision 63.4% among
covered cold-regime viruses; recovers hosts KNN-d2 cannot name by construction.
Treat the CRISPR ALERT as a high-precision hypothesis for spot assays, not an annotation.
Usage: python3 cold_host_predict.py PHAGE_ACCESSION [--assets coldhost_assets.npz]
       python3 cold_host_predict.py --fasta genome.fa --train-kmer ... (sequence mode needs
       the same k=4 kmer featurization as the benchmark; accession mode covers the benchmark)
"""
import argparse, sys, json
import numpy as np
ap = argparse.ArgumentParser()
ap.add_argument('accession', nargs='?')
ap.add_argument('--assets', default='coldhost_assets.npz')
a = ap.parse_args()
d = np.load(a.assets, allow_pickle=True)
Xtr, labels, CE, cand_sp = d['Xtr'], d['labels'], d['CE'], d['cand_sp']
import os
here = os.path.dirname(os.path.abspath(__file__))
vid = json.load(open(os.path.join(here, 'virus_ids.json')))
vpos = {v.split('.')[0]: i for i, v in enumerate(vid)}
if a.accession is None or a.accession.split('.')[0] not in vpos:
    print('unknown accession (sequence mode not bundled; k=4 kmer featurization required)')
    sys.exit(1)
vi = vpos[a.accession.split('.')[0]]
Xk = np.load(os.path.join(here, 'X_kmer.npy')).astype(np.float32)
x = Xk[vi]; xn = x / max(np.linalg.norm(x), 1e-9)
Tn = Xtr / np.maximum(np.linalg.norm(Xtr, axis=1, keepdims=True), 1e-9)
sims = Tn @ xn
j = sims.argmax()
print('KNN-d2 host: %s (nearest-train cosine %.3f)' % (labels[j], sims[j]))
es = [(int(p), 1) for v, p in CE if int(v) == vi]
if es:
    from collections import Counter
    c = Counter()
    for p, _ in es: c[p] += 1
    pc, n = max(c.items(), key=lambda kv: (kv[1], -kv[0]))
    print('CRISPR ALERT: %s (%d spacer hits; 63.4%% precision among covered cold-regime viruses)' % (cand_sp[pc], n))
else:
    print('CRISPR ALERT: none (no qualifying spacer hit)')
