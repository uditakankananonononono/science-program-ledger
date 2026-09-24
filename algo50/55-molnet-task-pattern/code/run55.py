"""ClinTox + HIV: descriptor-gap pattern test. Featurization cached to npz.

Memory-note (sandbox has 2GB RAM, no swap): identical math to the locked
protocol, but arrays are downcast on load (binary ECFP -> uint8, count ECFP ->
uint16, MACCS -> uint8) and per-fold float32 copies are made only for the
current fold slice. Values are unchanged (0/1 and small integer counts are
exact in uint8/uint16->float32)."""
import json, os, sys, gc
import numpy as np
import pandas as pd
from rdkit import Chem, DataStructs, RDLogger
from rdkit.Chem import AllChem, MACCSkeys, Descriptors, Crippen, rdMolDescriptors
from rdkit.Chem.Scaffolds import MurckoScaffold
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
RDLogger.DisableLog('rdApp.*')

DATA = os.path.expanduser('~/work/pattern55/data')
CACHE = os.path.expanduser('~/work/pattern55/cache')
os.makedirs(CACHE, exist_ok=True)

def featurize_cached(tag, smiles_list):
    f = os.path.join(CACHE, tag + '.npz')
    if os.path.exists(f):
        z = np.load(f, allow_pickle=True)
        bin_fp = z['bin_fp'].astype(np.uint8); gc.collect()
        cnt_fp = z['cnt_fp'].astype(np.uint16); gc.collect()
        maccs  = z['maccs'].astype(np.uint8)
        desc   = z['desc'].astype(np.float32)
        scaf   = z['scaf']
        z.close()
        return bin_fp, cnt_fp, maccs, desc, scaf
    n = len(smiles_list)
    bin_fp = np.zeros((n, 2048), dtype=np.float32)
    cnt_fp = np.zeros((n, 2048), dtype=np.float32)
    maccs = np.zeros((n, 167), dtype=np.float32)
    desc = np.zeros((n, 8), dtype=np.float32)
    scaf = np.empty(n, dtype=object)
    fpg = AllChem.GetMorganGenerator(radius=2, fpSize=2048)
    for i, sm in enumerate(smiles_list):
        m = Chem.MolFromSmiles(max(str(sm).split('.'), key=len))
        if m is None:
            scaf[i] = None; continue
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
        scaf[i] = MurckoScaffold.MurckoScaffoldSmiles(mol=m, includeChirality=False)
        if i % 5000 == 0:
            print(tag, i, flush=True)
    np.savez(f, bin_fp=bin_fp, cnt_fp=cnt_fp, maccs=maccs, desc=desc, scaf=scaf)
    return (bin_fp.astype(np.uint8), cnt_fp.astype(np.uint16),
            maccs.astype(np.uint8), desc, scaf)

def scaffold_folds(scaf, k, seed=0):
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

def standardize32(Xtr, Xte):
    mu = Xtr.mean(0, dtype=np.float64).astype(np.float32)
    sd = Xtr.std(0, dtype=np.float64).astype(np.float32)
    sd[sd == 0] = 1.0
    A = Xtr.astype(np.float32); A -= mu; A /= sd
    B = Xte.astype(np.float32); B -= mu; B /= sd
    return A, B

def best_c(Xtr, ytr, fold_tr, rng):
    bc, ba = 1.0, -1
    for c in (0.1, 1.0, 10.0):
        aucs = []
        for f in np.unique(fold_tr):
            tr, te = fold_tr != f, fold_tr == f
            if len(np.unique(ytr[te])) < 2: continue
            tri = np.where(tr)[0]
            if len(tri) > 6000:
                tri = rng.choice(tri, 6000, replace=False)
            Xa, Xb = standardize32(Xtr[tri], Xtr[te])
            m = LogisticRegression(C=c, max_iter=1500).fit(Xa, ytr[tri])
            aucs.append(roc_auc_score(ytr[te], m.predict_proba(Xb)[:, 1]))
            del Xa, Xb, m; gc.collect()
        if aucs:
            a = float(np.mean(aucs))
            if a > ba: ba, bc = a, c
    return bc

GBM = dict(max_iter=300, learning_rate=0.06, max_leaf_nodes=31,
           min_samples_leaf=20, l2_regularization=1.0,
           early_stopping=False, random_state=1)

def load_members(tag, members):
    z = np.load(os.path.join(CACHE, tag + '.npz'), allow_pickle=True)
    out = {m: z[m] for m in members}
    z.close()
    return out

def run_task(tag, csv_path, smiles_col, label_col, k):
    print('=== task', tag, flush=True)
    df = pd.read_csv(csv_path, usecols=[smiles_col, label_col])
    df['_lf'] = df[smiles_col].map(lambda s: max(str(s).split('.'), key=len))
    conf = df.groupby('_lf')[label_col].nunique()
    n_conflict = int((conf > 1).sum())
    df = df.drop_duplicates('_lf', keep='first')
    smiles = df['_lf'].tolist()
    y_all = df[label_col].to_numpy().astype(int)
    del df, conf; gc.collect()
    cache_f = os.path.join(CACHE, tag + '.npz')
    if not os.path.exists(cache_f):
        featurize_cached(tag, smiles)
    del smiles; gc.collect()
    d0 = load_members(tag, ['scaf', 'desc'])
    scaf, desc = d0['scaf'], d0['desc'].astype(np.float32); del d0
    valid = np.array([s is not None for s in scaf])
    y = y_all[valid]; del y_all
    desc = desc[valid]
    scaf_v = scaf[valid]; del scaf
    fold_of = scaffold_folds(list(scaf_v), k)
    del scaf_v; gc.collect()
    n = len(y)
    print(tag, 'n', n, 'dropped', int((~valid).sum()), 'label_conflicts', n_conflict,
          'base %.4f' % y.mean(), flush=True)
    p = {kk: np.full(n, np.nan) for kk in ('B0', 'B1', 'M1')}
    rng = np.random.RandomState(0)
    # pass 1: B0 + B1 need only binary ECFP + descriptors
    d1 = load_members(tag, ['bin_fp'])
    bin_fp = d1['bin_fp'][valid].astype(np.uint8); del d1; gc.collect()
    for f in range(k):
        tr, te = fold_of != f, fold_of == f
        tri, tei = np.where(tr)[0], np.where(te)[0]
        Xa, Xb = standardize32(desc[tri, :3], desc[tei, :3])
        p['B0'][te] = LogisticRegression(C=1.0, max_iter=2000).fit(Xa, y[tr]).predict_proba(Xb)[:, 1]
        del Xa, Xb
        c = best_c(bin_fp[tri], y[tr], fold_of[tri], rng)
        mu = bin_fp[tri].mean(0, dtype=np.float64).astype(np.float32)
        sd = bin_fp[tri].std(0, dtype=np.float64).astype(np.float32)
        sd[sd == 0] = 1.0
        Xa = bin_fp[tri].astype(np.float32); Xa -= mu; Xa /= sd
        m = LogisticRegression(C=c, max_iter=2000).fit(Xa, y[tr])
        del Xa; gc.collect()
        Xb = bin_fp[tei].astype(np.float32); Xb -= mu; Xb /= sd
        p['B1'][te] = m.predict_proba(Xb)[:, 1]
        del Xb, m, mu, sd; gc.collect()
        print(tag, 'fold', f, 'B0+B1 done (B1 C=%s)' % c, flush=True)
    del bin_fp; gc.collect()
    # pass 2: M1 needs count ECFP + MACCS + descriptors
    d2 = load_members(tag, ['cnt_fp', 'maccs'])
    cnt_fp = d2['cnt_fp'][valid].astype(np.uint16)
    maccs = d2['maccs'][valid].astype(np.uint8); del d2; gc.collect()
    for f in range(k):
        tr, te = fold_of != f, fold_of == f
        tri, tei = np.where(tr)[0], np.where(te)[0]
        Xm1_tr = np.hstack([cnt_fp[tri].astype(np.float32), maccs[tri].astype(np.float32), desc[tri]])
        Xm1_te = np.hstack([cnt_fp[tei].astype(np.float32), maccs[tei].astype(np.float32), desc[tei]])
        m = HistGradientBoostingClassifier(**GBM).fit(Xm1_tr, y[tr])
        p['M1'][te] = m.predict_proba(Xm1_te)[:, 1]
        del Xm1_tr, Xm1_te, m; gc.collect()
        print(tag, 'fold', f, 'M1 done', flush=True)
    del cnt_fp, maccs, desc; gc.collect()
    auc = {kk: float(roc_auc_score(y, vv)) for kk, vv in p.items()}
    ap = {kk: float(average_precision_score(y, vv)) for kk, vv in p.items()}
    np.savez(os.path.join('results', 'oof_%s.npz' % tag), y=y,
             B0=p['B0'], B1=p['B1'], M1=p['M1'], fold_of=fold_of)
    return {'n': int(n), 'base_rate': float(y.mean()), 'label_conflicts': n_conflict,
            'auroc': auc, 'ap': ap, 'gap_B1_minus_B0': auc['B1'] - auc['B0']}, y, p

out = {}; keep = {}
out['clintox'], keep['ct_y'], keep['ct_p'] = run_task('clintox', os.path.join(DATA, 'clintox.csv'), 'smiles', 'CT_TOX', 5)
out['hiv'], keep['hiv_y'], keep['hiv_p'] = run_task('hiv', os.path.join(DATA, 'HIV.csv'), 'smiles', 'HIV_active', 3)

# locked reference numbers from algo50/51 and algo50/53
ref51 = json.load(open(os.path.expanduser('~/work/science-program-ledger/algo50/51-bbbp-fingerprint-ecfp/results/results.json')))
ref53 = json.load(open(os.path.expanduser('~/work/science-program-ledger/algo50/53-bace-scaffold-transfer/results/results.json')))
gap_bbbp = ref51['auroc']['B1'] - ref51['auroc']['B0']
gap_bace = ref53['bace_classification']['B1_binECFP'] - ref53['bace_classification']['B0_3desc']
out['reference_gaps'] = {'bbbp': gap_bbbp, 'bace': gap_bace}
g_ct = out['clintox']['gap_B1_minus_B0']; g_hiv = out['hiv']['gap_B1_minus_B0']
out['gates'] = {
    'G1_gap_clintox_lt_0.10': bool(g_ct < 0.10),
    'G2_gap_hiv_gt_0.05': bool(g_hiv > 0.05),
    'G3_M1_ge_B1+0.02_both': bool(out['clintox']['auroc']['M1'] >= out['clintox']['auroc']['B1'] + 0.02
                                   and out['hiv']['auroc']['M1'] >= out['hiv']['auroc']['B1'] + 0.02),
    'G4_sign_consistency_4tasks': bool(gap_bbbp < 0.05 and g_ct < 0.05 and gap_bace > 0.05 and g_hiv > 0.05),
}
print(json.dumps(out['gates'], indent=1))
json.dump(out, open('results/results.json', 'w'), indent=1)
