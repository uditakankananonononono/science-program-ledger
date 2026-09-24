import numpy as np, json, sys, pickle
from collections import defaultdict
d = np.load('model_data035.npz')
AA, E = d['AA'], d['E']
_keep = set(open('keep_taxids.txt').read().split())
c20_l, c14_l = [], []
for line in open('joined035.tsv'):
    if line.startswith('taxid'): continue
    f = line.rstrip('\n').split('\t')
    if f[0] not in _keep: continue
    c20_l.append(f[2][:1]); c14_l.append(f[3][:1])
c20 = np.array(c20_l, dtype=object); c14 = np.array(c14_l, dtype=object)
del c20_l, c14_l
letters = sorted(set(x for x in c20 if x))
lidx = {l:i for i,l in enumerate(letters)}
NL = len(letters)
N = len(c20)
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
elif mode == 'armB':
    import torch, torch.nn as nn
    torch.manual_seed(0)
    f0, f1 = int(sys.argv[2]), int(sys.argv[3])
    ll = np.where((c20 != '') & (c14 != ''))[0]
    y = np.array([lidx[x] for x in c20[ll]])
    X = np.empty((len(ll), 3*NL + 20), dtype=np.float32)
    for j,ch in enumerate((0,1,2)):
        F = neighbor_letter_feats(ch, c14)
        X[:, j*NL:(j+1)*NL] = F[ll]
        del F
    X[:, 3*NL:] = AA[ll]
    rng = np.random.default_rng(0); folds = rng.permutation(len(ll)) % 10
    import os
    done = set()
    if os.path.exists('dev035_armB.jsonl'):
        for line in open('dev035_armB.jsonl'):
            done.add(json.loads(line)['fold'])
    out = open('dev035_armB.jsonl','a')
    Xt = torch.from_numpy(np.ascontiguousarray(X)); yt = torch.from_numpy(y)
    for f in range(f0, f1):
        if f in done: continue
        tr = np.where(folds != f)[0]; te = np.where(folds == f)[0]
        m = nn.Linear(X.shape[1], NL)
        opt = torch.optim.Adam(m.parameters(), lr=0.01)
        lossf = nn.CrossEntropyLoss()
        for ep in range(30):
            perm = torch.randperm(len(tr))[:100000]
            idx = torch.tensor(tr[perm.numpy()])
            opt.zero_grad()
            loss = lossf(m(Xt[idx]), yt[idx])
            loss.backward(); opt.step()
        with torch.no_grad():
            pred = m(Xt[torch.tensor(te)]).argmax(1).numpy()
        acc = (pred == y[te]).mean()
        print('fold', f, 'acc %.4f' % acc, flush=True)
        out.write(json.dumps({'fold': f, 'acc': float(acc)})+'\n'); out.flush()
    out.close()
elif mode == 'p1':
    import scipy.sparse as sp
    w = np.maximum.reduce([E[:,2], E[:,3], E[:,4]]).astype(np.float32)/1000.0
    rows = np.concatenate([E[:,0], E[:,1]]); cols = np.concatenate([E[:,1], E[:,0]])
    ww = np.concatenate([w, w])
    A = sp.coo_matrix((ww, (rows, cols)), shape=(N, N)).tocsr()
    deg = np.asarray(A.sum(1)).ravel(); deg[deg==0] = 1
    A = sp.diags(1.0/deg) @ A
    li14 = np.array([lidx.get(x, -1) for x in c14])
    ll = np.where((c20 != '') & (c14 != ''))[0]
    y20 = np.array([lidx[x] for x in c20[ll]])
    rng = np.random.default_rng(0); folds = rng.permutation(len(ll)) % 10
    import os
    done = set()
    if os.path.exists('dev035_p1.jsonl'):
        for line in open('dev035_p1.jsonl'):
            done.add(json.loads(line)['fold'])
    out = open('dev035_p1.jsonl','a')
    f0, f1 = int(sys.argv[2]), int(sys.argv[3])
    ll_set = np.zeros(N, dtype=bool); ll_set[ll] = True
    for f in range(f0, f1):
        if f in done: continue
        te_local = np.where(folds == f)[0]
        seed_mask = (li14 >= 0) & ll_set
        seed_mask[ll[te_local]] = False   # mask held-out proteins' own 2014 letters
        Y = np.zeros((N, NL), dtype=np.float32)
        Y[np.where(seed_mask)[0], li14[seed_mask]] = 1.0
        F = 0.9*(A @ Y) + 0.1*Y
        F = 0.9*(A @ F) + 0.1*Y
        pred = F[ll[te_local]].argmax(1)
        acc = (pred == y20[te_local]).mean()
        print('fold', f, 'acc %.4f' % acc, flush=True)
        out.write(json.dumps({'fold': f, 'acc': float(acc)})+'\n'); out.flush()
    out.close()
elif mode == 'frozen':
    import torch, torch.nn as nn
    torch.manual_seed(0)
    ll = np.where((c20 != '') & (c14 != ''))[0]
    nl_ = np.where((c20 != '') & (c14 == ''))[0]
    ytr = np.array([lidx[x] for x in c20[ll]])
    yte = np.array([lidx[x] for x in c20[nl_]])
    # ARM A frozen: neighborhood vote with all 2014 letters
    F14 = neighbor_letter_feats(0, c14)
    predA = F14[nl_].argmax(1)
    accA = (predA == yte).mean()
    # ARM B frozen
    X = np.empty((N, 3*NL + 20), dtype=np.float32)
    for j,ch in enumerate((0,1,2)):
        F = neighbor_letter_feats(ch, c14) if ch>0 else F14
        X[:, j*NL:(j+1)*NL] = F[:, :]
        if ch>0: del F
    X[:, 3*NL:] = AA
    Xt = torch.from_numpy(X)
    m = nn.Linear(X.shape[1], NL)
    opt = torch.optim.Adam(m.parameters(), lr=0.01)
    lossf = nn.CrossEntropyLoss()
    yt = torch.from_numpy(ytr)
    for ep in range(30):
        perm = torch.randperm(len(ll))[:100000]
        idx = torch.tensor(ll[perm.numpy()])
        opt.zero_grad(); loss = lossf(m(Xt[idx]), yt[torch.tensor(perm)]); loss.backward(); opt.step()
    with torch.no_grad():
        predB = m(Xt[torch.tensor(nl_)]).argmax(1).numpy()
    accB = (predB == yte).mean()
    pop = np.bincount(ytr).max()/len(ytr)
    print('FROZEN newly-lit (n=%d): ARM A %.4f | ARM B %.4f | popularity(train) %.4f' % (len(nl_), accA, accB, pop))
    json.dump({'n_newly_lit': int(len(nl_)), 'armA': float(accA), 'armB': float(accB),
               'popularity': float(pop), 'predB': predB.tolist(), 'predA': predA.tolist(),
               'yte': yte.tolist(), 'nl_idx': nl_.tolist()}, open('frozen035.json','w'))
elif mode == 'ablate':
    import torch, torch.nn as nn
    torch.manual_seed(0)
    chans = [int(x) for x in sys.argv[2].split(',')]
    tag = sys.argv[3]
    ll = np.where((c20 != '') & (c14 != ''))[0]
    y = np.array([lidx[x] for x in c20[ll]])
    X = np.empty((len(ll), len(chans)*NL + 20), dtype=np.float32)
    for j,ch in enumerate(chans):
        F = neighbor_letter_feats(ch, c14)
        X[:, j*NL:(j+1)*NL] = F[ll]; del F
    X[:, len(chans)*NL:] = AA[ll]
    rng = np.random.default_rng(0); folds = rng.permutation(len(ll)) % 10
    Xt = torch.from_numpy(np.ascontiguousarray(X)); yt = torch.from_numpy(y)
    accs = []
    for f in range(10):
        tr = np.where(folds != f)[0]; te = np.where(folds == f)[0]
        m = nn.Linear(X.shape[1], NL)
        opt = torch.optim.Adam(m.parameters(), lr=0.01)
        lossf = nn.CrossEntropyLoss()
        for ep in range(30):
            perm = torch.randperm(len(tr))[:100000]
            idx = torch.tensor(tr[perm.numpy()])
            opt.zero_grad(); loss = lossf(m(Xt[idx]), yt[idx]); loss.backward(); opt.step()
        with torch.no_grad():
            pred = m(Xt[torch.tensor(te)]).argmax(1).numpy()
        accs.append(float((pred == y[te]).mean()))
    print(tag, 'mean %.4f' % np.mean(accs), [round(a,3) for a in accs], flush=True)
    json.dump({'tag': tag, 'accs': accs}, open(f'abl035_{tag}.json','w'))
