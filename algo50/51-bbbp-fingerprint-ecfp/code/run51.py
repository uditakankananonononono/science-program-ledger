"""BBBP: scaffold-grouped 5-fold CV. B0 desc-only / B1 binary ECFP logreg /
B2 Tanimoto 1-NN / M1 GBM on count-ECFP+MACCS+desc."""
import json
import numpy as np
import pandas as pd
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem, MACCSkeys, Descriptors, Crippen, rdMolDescriptors
from rdkit.Chem.Scaffolds import MurckoScaffold
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

df = pd.read_csv(__file__.rsplit('/code/', 1)[0] + '/../data_src_placeholder') if False else None
import os
DATA = os.path.expanduser('~/work/bbbp51/data/BBBP.csv')
df = pd.read_csv(DATA)

mols, ys, names = [], [], []
failed = 0
for _, row in df.iterrows():
    sm = str(row['smiles'])
    frags = sm.split('.')
    sm = max(frags, key=len)  # desalt: largest fragment
    m = Chem.MolFromSmiles(sm)
    if m is None:
        failed += 1
        continue
    mols.append(m); ys.append(int(row['p_np'])); names.append(row['name'])
y = np.array(ys)
print('parsed', len(mols), 'failed', failed, 'base rate %.3f' % y.mean())

# features
n = len(mols)
bin_fp = np.zeros((n, 2048), dtype=np.float32)
cnt_fp = np.zeros((n, 2048), dtype=np.float32)
maccs = np.zeros((n, 167), dtype=np.float32)
desc = np.zeros((n, 8), dtype=np.float32)
fpg = AllChem.GetMorganGenerator(radius=2, fpSize=2048)
fpgc = AllChem.GetMorganGenerator(radius=2, fpSize=2048, includeChirality=False)
for i, m in enumerate(mols):
    bv = fpg.GetFingerprint(m)
    DataStructs.ConvertToNumpyArray(bv, bin_fp[i])
    cf = fpg.GetCountFingerprint(m)
    arr = np.zeros((2048,), dtype=np.float32)
    DataStructs.ConvertToNumpyArray(cf, arr)
    cnt_fp[i] = arr
    ma = MACCSkeys.GenMACCSKeys(m)
    DataStructs.ConvertToNumpyArray(ma, maccs[i])
    desc[i] = [Crippen.MolLogP(m), Descriptors.MolWt(m),
               rdMolDescriptors.CalcTPSA(m), rdMolDescriptors.CalcNumHBD(m),
               rdMolDescriptors.CalcNumHBA(m), rdMolDescriptors.CalcNumRotatableBonds(m),
               rdMolDescriptors.CalcFractionCSP3(m),
               sum(1 for a in m.GetAtoms() if a.GetIsAromatic()) / max(m.GetNumAtoms(), 1)]

# Murcko scaffold split: greedy size-balanced, seed 0
scaffolds = {}
for i, m in enumerate(mols):
    scaf = MurckoScaffold.MurckoScaffoldSmiles(mol=m, includeChirality=False)
    scaffolds.setdefault(scaf, []).append(i)
rng = np.random.RandomState(0)
groups = sorted(scaffolds.values(), key=len, reverse=True)
folds = [[] for _ in range(5)]
sizes = [0] * 5
order = list(range(len(groups)))
rng.shuffle(order)
for gi in order:
    f = int(np.argmin(sizes))
    folds[f].extend(groups[gi])
    sizes[f] += len(groups[gi])
fold_of = np.empty(n, dtype=int)
for f, idxs in enumerate(folds):
    fold_of[idxs] = f
print('fold sizes', [len(f) for f in folds], 'scaffolds', len(groups))

def standardize(Xtr, Xte):
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd == 0] = 1.0
    return (Xtr - mu) / sd, (Xte - mu) / sd

def best_c(Xtr_all, ytr_all, fold_tr):
    bc, ba = 1.0, -1
    for c in (0.1, 1.0, 10.0):
        aucs = []
        for f in np.unique(fold_tr):
            tr, te = fold_tr != f, fold_tr == f
            if len(np.unique(ytr_all[te])) < 2:
                continue
            Xa, Xb = standardize(Xtr_all[tr], Xtr_all[te])
            m = LogisticRegression(C=c, max_iter=2000).fit(Xa, ytr_all[tr])
            aucs.append(roc_auc_score(ytr_all[te], m.predict_proba(Xb)[:, 1]))
        a = float(np.mean(aucs))
        if a > ba:
            ba, bc = a, c
    return bc

X0 = desc[:, :3]
Xm1 = np.hstack([cnt_fp, maccs, desc])
probs = {k: np.full(n, np.nan) for k in ('B0', 'B1', 'B2', 'M1')}
# Tanimoto 1-NN needs bit vectors
fp_bits = [fpg.GetFingerprint(m) for m in mols]
for f in range(5):
    tr, te = fold_of != f, fold_of == f
    tri, tei = np.where(tr)[0], np.where(te)[0]
    # B0
    Xa, Xb = standardize(X0[tr], X0[te])
    m = LogisticRegression(C=1.0, max_iter=2000).fit(Xa, y[tr])
    probs['B0'][te] = m.predict_proba(Xb)[:, 1]
    # B1
    c = best_c(bin_fp[tr], y[tr], fold_of[tr])
    Xa, Xb = standardize(bin_fp[tr], bin_fp[te])
    m = LogisticRegression(C=c, max_iter=2000).fit(Xa, y[tr])
    probs['B1'][te] = m.predict_proba(Xb)[:, 1]
    # B2: 1-NN Tanimoto
    base = y[tr].mean()
    for j in tei:
        sims = DataStructs.BulkTanimotoSimilarity(fp_bits[j], [fp_bits[t] for t in tri])
        k = int(np.argmax(sims))
        probs['B2'][j] = float(y[tri[k]]) if sims[k] > 0 else float(base)
    # M1
    m = HistGradientBoostingClassifier(
        max_iter=300, learning_rate=0.06, max_leaf_nodes=31,
        min_samples_leaf=20, l2_regularization=1.0,
        early_stopping=False, random_state=1).fit(Xm1[tr], y[tr])
    probs['M1'][te] = m.predict_proba(Xm1[te])[:, 1]
    print('fold', f, 'done', flush=True)

auc = {k: float(roc_auc_score(y, p)) for k, p in probs.items()}
base_rate = float(y.mean())
k10 = max(1, int(0.10 * n))
top = np.argsort(-probs['M1'])[:k10]
prec10 = float(y[top].mean())
out = {
    'n': int(n), 'parse_failed': int(failed), 'base_rate': base_rate,
    'auroc': auc, 'top_decile_precision_M1': prec10,
    'gates': {
        'G1_M1_ge_B1+0.02': bool(auc['M1'] >= auc['B1'] + 0.02),
        'G2_B1_ge_B0+0.05': bool(auc['B1'] >= auc['B0'] + 0.05),
        'G3_M1_ge_Tanimoto1NN+0.02': bool(auc['M1'] >= auc['B2'] + 0.02),
        'G4_topdecile_ge_1.5x_base': bool(prec10 >= 1.5 * base_rate),
    },
}
print(json.dumps(out, indent=1))
json.dump(out, open('results/results.json', 'w'), indent=1)
pd.DataFrame({'name': names, 'y': y, **{f'p{k}': v for k, v in probs.items()},
              'fold': fold_of}).to_csv('results/predictions.csv', index=False)
