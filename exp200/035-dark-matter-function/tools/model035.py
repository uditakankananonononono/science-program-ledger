import numpy as np, json, sys, pickle
from collections import defaultdict
d = np.load('model_data035.npz')
AA, E = d['AA'], d['E']
prot = json.load(open('prot035.json'))
c20 = np.array([p[2] for p in prot], dtype=object)
c14 = np.array([p[3] for p in prot], dtype=object)
letters = sorted(set(x for x in c20 if x))
lidx = {l:i for i,l in enumerate(letters)}
NL = len(letters)
N = len(prot)
# adjacency per channel (directed both ways)
def neighbor_letter_feats(ch, lab):
    # weighted vote: for each protein, sum channel scores by neighbor letter
    F = np.zeros((N, NL), dtype=np.float32)
    mask = (lab != '')
    li = np.array([lidx.get(x, -1) for x in lab])
    for a, b, *s in E:
        w = s[ch]/1000.0
        if mask[b] and li[b] >= 0: F[a, li[b]] += w
        if mask[a] and li[a] >= 0: F[b, li[a]] += w
    return F
def armA(F):
    return np.array([letters[i] for i in F.argmax(1)], dtype=object), F.max(1)
mode = sys.argv[1]
if mode == 'dev':
    # long-lit dev 10-fold: label = 2020 letter, features from 2014 letters only
    ll = np.where((c20 != '') & (c14 != ''))[0]
    y = c20[ll]
    F14 = neighbor_letter_feats(0, c14)   # neighborhood channel, 2014 letters
    pred, conf = armA(F14)
    rng = np.random.default_rng(0); folds = rng.permutation(len(ll)) % 10
    accA = []
    for f in range(10):
        te = ll[folds == f]
        accA.append((pred[te] == c20[te]).mean())
    print('ARM A dev acc per fold:', [round(a,4) for a in accA])
    print('ARM A dev mean: %.4f' % np.mean(accA))
    # popularity
    vals, cnts = np.unique(y, return_counts=True)
    pop = cnts.max()/len(y)
    print('popularity: %.4f' % pop)
    json.dump({'armA_dev': accA, 'popularity': float(pop)}, open('dev035_armA.json','w'))
