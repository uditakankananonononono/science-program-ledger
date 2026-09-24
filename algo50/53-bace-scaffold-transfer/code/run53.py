"""BACE classification + BBBP->BACE transfer + pIC50 regression."""
import json, os
import numpy as np
import pandas as pd
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem, MACCSkeys, Descriptors, Crippen, rdMolDescriptors
from rdkit.Chem.Scaffolds import MurckoScaffold
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import roc_auc_score
from scipy.stats import spearmanr

DATA = os.path.expanduser('~/work/bace53/data')

def featurize(smiles_list):
    n = len(smiles_list)
    bin_fp = np.zeros((n, 2048), dtype=np.float32)
    cnt_fp = np.zeros((n, 2048), dtype=np.float32)
    maccs = np.zeros((n, 167), dtype=np.float32)
    desc = np.zeros((n, 8), dtype=np.float32)
    scaf = []
    fpg = AllChem.GetMorganGenerator(radius=2, fpSize=2048)
    for i, sm in enumerate(smiles_list):
        m = Chem.MolFromSmiles(max(str(sm).split('.'), key=len))
        if m is None:
            scaf.append(None); continue
        DataStructs.ConvertToNumpyArray(fpg.GetFingerprint(m), bin_fp[i])
        arr = np.zeros((2048,), dtype=np.float32)
        DataStructs.ConvertToNumpyArray(fpg.GetCountFingerprint(m), arr)
        cnt_fp[i] = arr
        DataStructs.ConvertToNumpyArray(MACCSkeys.GenMACCSKeys(m), maccs[i])
        desc[i] = [Crippen.MolLogP(m), Descriptors.MolWt(m),
                   rdMolDescriptors.CalcTPSA(m), rdMolDescriptors.CalcNumHBD(m),
                   rdMolDescriptors.CalcNumHBA(m), rdMolDescriptors.CalcNumRotatableBonds(m),
                   rdMolDescriptors.CalcFractionCSP3(m),
                   sum(1 for a in m.GetAtoms() if a.GetIsAromatic()) / max(m.GetNumAtoms(), 1)]
        scaf.append(MurckoScaffold.MurckoScaffoldSmiles(mol=m, includeChirality=False))
    return bin_fp, cnt_fp, maccs, desc, scaf

def scaffold_folds(scaf, k=5, seed=0):
    groups = {}
    for i, s in enumerate(scaf):
        groups.setdefault(s, []).append(i)
    order = sorted(groups.values(), key=len, reverse=True)
    folds = [[] for _ in range(k)]; sizes = [0] * k
    for g in order:
        f = int(np.argmin(sizes)); folds[f].extend(g); sizes[f] += len(g)
    fold_of = np.empty(len(scaf), dtype=int)
    for f, idxs in enumerate(folds):
        fold_of[idxs] = f
    return fold_of

def standardize(Xtr, Xte):
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd == 0] = 1.0
    return (Xtr - mu) / sd, (Xte - mu) / sd

def best_c(Xtr, ytr, fold_tr):
    bc, ba = 1.0, -1
    for c in (0.1, 1.0, 10.0):
        aucs = []
        for f in np.unique(fold_tr):
            tr, te = fold_tr != f, fold_tr == f
            if len(np.unique(ytr[te])) < 2: continue
            Xa, Xb = standardize(Xtr[tr], Xtr[te])
            m = LogisticRegression(C=c, max_iter=2000).fit(Xa, ytr[tr])
            aucs.append(roc_auc_score(ytr[te], m.predict_proba(Xb)[:, 1]))
        a = float(np.mean(aucs))
        if a > ba: ba, bc = a, c
    return bc

GBM_C = dict(max_iter=300, learning_rate=0.06, max_leaf_nodes=31,
             min_samples_leaf=20, l2_regularization=1.0,
             early_stopping=False, random_state=1)

# ---- BACE ----
bace = pd.read_csv(os.path.join(DATA, 'bace.csv'))
smiles = bace['mol'].tolist()
bin_fp, cnt_fp, maccs, desc, scaf = featurize(smiles)
valid = np.array([s is not None for s in scaf])
yb = bace['Class'].to_numpy()[valid]
pic50 = bace['pIC50'].to_numpy()[valid]
bin_fp, cnt_fp, maccs, desc = bin_fp[valid], cnt_fp[valid], maccs[valid], desc[valid]
scaf = [s for s in scaf if s is not None]
fold_of = scaffold_folds(scaf)
n = len(yb)
print('BACE parsed', n, 'failed', int((~valid).sum()), 'base rate %.3f' % yb.mean())

X0 = desc[:, :3]
Xm1 = np.hstack([cnt_fp, maccs, desc])
pB0 = np.full(n, np.nan); pB1 = np.full(n, np.nan); pM1 = np.full(n, np.nan)
sRidge = np.full(n, np.nan); sGBM = np.full(n, np.nan)
for f in range(5):
    tr, te = fold_of != f, fold_of == f
    Xa, Xb = standardize(X0[tr], X0[te])
    pB0[te] = LogisticRegression(C=1.0, max_iter=2000).fit(Xa, yb[tr]).predict_proba(Xb)[:, 1]
    c = best_c(bin_fp[tr], yb[tr], fold_of[tr])
    Xa, Xb = standardize(bin_fp[tr], bin_fp[te])
    pB1[te] = LogisticRegression(C=c, max_iter=2000).fit(Xa, yb[tr]).predict_proba(Xb)[:, 1]
    m = HistGradientBoostingClassifier(**GBM_C).fit(Xm1[tr], yb[tr])
    pM1[te] = m.predict_proba(Xm1[te])[:, 1]
    Xa, Xb = standardize(desc[tr], desc[te])
    sRidge[te] = Ridge(alpha=1.0).fit(Xa, pic50[tr]).predict(Xb)
    mg = HistGradientBoostingRegressor(**GBM_C).fit(Xm1[tr], pic50[tr])
    sGBM[te] = mg.predict(Xm1[te])
    print('fold', f, 'done', flush=True)

aucB0 = float(roc_auc_score(yb, pB0)); aucB1 = float(roc_auc_score(yb, pB1)); aucM1 = float(roc_auc_score(yb, pM1))
spR = float(spearmanr(sRidge, pic50).statistic); spG = float(spearmanr(sGBM, pic50).statistic)

# ---- transfer: train M1 on ALL BBBP, score BACE ----
bbbp = pd.read_csv(os.path.join(DATA, 'BBBP.csv'))
bbsm = bbbp['smiles'].tolist()
bb_bin, bb_cnt, bb_mac, bb_desc, bb_scaf = featurize(bbsm)
bvalid = np.array([s is not None for s in bb_scaf])
ybb = bbbp['p_np'].to_numpy()[bvalid]
Xbb = np.hstack([bb_cnt[bvalid], bb_mac[bvalid], bb_desc[bvalid]])
mt = HistGradientBoostingClassifier(**GBM_C).fit(Xbb, ybb)
p_transfer = mt.predict_proba(Xm1)[:, 1]
aucT = float(roc_auc_score(yb, p_transfer))

out = {
    'n_bace': int(n), 'parse_failed_bace': int((~valid).sum()), 'base_rate_bace': float(yb.mean()),
    'bace_classification': {'B0_3desc': aucB0, 'B1_binECFP': aucB1, 'M1_gbm': aucM1},
    'transfer_bbbp_to_bace_M1': aucT,
    'regression_pIC50': {'ridge_8desc_spearman': spR, 'gbm_full_spearman': spG},
    'gates': {
        'G1_B1_ge_B0+0.05': bool(aucB1 >= aucB0 + 0.05),
        'G2_M1_ge_B1+0.02': bool(aucM1 >= aucB1 + 0.02),
        'G3_transfer_ge_0.60': bool(aucT >= 0.60),
        'G4_gbm_ge_ridge+0.05': bool(spG >= spR + 0.05),
    },
}
print(json.dumps(out, indent=1))
json.dump(out, open('results/results.json', 'w'), indent=1)
pd.DataFrame({'y': yb, 'pIC50': pic50, 'pB0': pB0, 'pB1': pB1, 'pM1': pM1,
              'p_transfer': p_transfer, 'sRidge': sRidge, 'sGBM': sGBM,
              'fold': fold_of}).to_csv('results/predictions.csv', index=False)
