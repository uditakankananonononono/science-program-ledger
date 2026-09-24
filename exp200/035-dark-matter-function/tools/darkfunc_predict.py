#!/usr/bin/env python3
"""darkfunc_predict.py - DOC-1-035: COG-letter prediction for prokaryote proteins from
genomic-context association evidence (ARM A: Huynen 2000 Type-II neighborhood transfer,
the validated frozen winner of 035: 24.34% on 3,497 temporally-frozen newly-lit proteins
vs 8.55% popularity, 26 classes).
Input: a protein FASTA from one of the 149 panel genomes (manifest035.json). Sequences are
matched to STRING v12 proteins by exact md5; predictions come from neighborhood-channel
weighted vote of 2014-labeled neighbors. Proteins with no labeled neighbor get NO CALL.
Usage: python3 darkfunc_predict.py proteins.faa --assets darkfunc_assets.npz [--min-score 400]
NOTE: frozen newly-lit accuracy 24.3% - hypothesis-generating, not validated annotation.
"""
import argparse, hashlib, sys
import numpy as np
ap = argparse.ArgumentParser()
ap.add_argument('fasta'); ap.add_argument('--assets', required=True)
ap.add_argument('--min-score', type=int, default=400)
a = ap.parse_args()
d = np.load(a.assets, allow_pickle=True)
E, c14 = d['E'], d['c14']
letters = sorted(set(x for x in c14 if x))
lidx = {l:i for i,l in enumerate(letters)}
NL = len(letters)
# build md5 -> index from the asset? assets carry no sequences; map via hash of input matched
# against per-protein md5 table stored alongside
import os, json
tab = np.load(os.path.join(os.path.dirname(a.assets), 'darkfunc_md5.npz'))
md5s = {bytes(m.tobytes()).hex(): i for i, m in enumerate(tab['md5'])}
N = len(c14)
F = np.zeros((N, NL), dtype=np.float32)
li = np.array([lidx.get(x, -1) for x in c14])
for x, y, nb, fu, co in E:
    if nb < a.min_score: continue
    w = nb/1000.0
    if li[y] >= 0: F[x, li[y]] += w
    if li[x] >= 0: F[y, li[x]] += w
cur, buf, n_call = None, [], 0
def flush():
    global n_call
    if cur is None: return
    h = hashlib.md5(''.join(buf).encode()).hexdigest()
    i = md5s.get(h)
    if i is None:
        print('%s\tNO_MATCH' % cur); return
    if F[i].sum() == 0:
        print('%s\tNO_CALL' % cur); return
    j = F[i].argmax()
    print('%s\t%s\t%.3f' % (cur, letters[j], F[i, j]/F[i].sum()))
    n_call += 1
for line in open(a.fasta):
    line = line.strip()
    if line.startswith('>'):
        flush(); cur = line[1:].split()[0]; buf = []
    else:
        buf.append(line)
flush()
print('# called: %d' % n_call, file=sys.stderr)
