"""P1: S-oversampling for M1. P2: N/V/F/Q-only accuracy, M1 vs B1."""
import json, os
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

DS1 = ['101','106','108','109','112','114','115','116','118','119','122','124',
       '201','203','205','207','208','209','215','220','223','230']
DS2 = ['100','103','105','111','113','117','121','123','200','202','210','212',
       '213','214','219','221','222','228','231','232','233','234']
CACHE = os.path.expanduser('~/work/beats49/cache')

def assemble(recs):
    Xs, ys = [], []
    for r in recs:
        z = np.load(os.path.join(CACHE, r + '.npz'), allow_pickle=True)
        Xs.append(z['X']); ys += z['y'].tolist()
    return np.vstack(Xs), np.array(ys)

X1, y1 = assemble(DS1)
X2, y2 = assemble(DS2)
B1_IDX = list(range(0, 32))
M1_IDX = list(range(0, X1.shape[1]))

def standardize(Xtr, Xte):
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd == 0] = 1.0
    return np.nan_to_num((Xtr - mu) / sd), np.nan_to_num((Xte - mu) / sd)

def fit_gbm(Xtr, ytr, oversample_S=False):
    Xtr = np.nan_to_num(Xtr)
    if oversample_S:
        rng = np.random.RandomState(0)
        nN = int((ytr == 'N').sum())
        s_idx = np.where(ytr == 'S')[0]
        need = max(0, int(0.5 * nN) - len(s_idx))
        extra = rng.choice(s_idx, need, replace=True) if need and len(s_idx) else []
        if len(extra):
            Xtr = np.vstack([Xtr, Xtr[extra]])
            ytr = np.concatenate([ytr, ytr[extra]])
    return HistGradientBoostingClassifier(
        max_iter=300, learning_rate=0.06, max_leaf_nodes=31,
        min_samples_leaf=20, l2_regularization=1.0,
        early_stopping=False, random_state=1).fit(Xtr, ytr)

def fit_lr(Xtr, ytr):
    Xtr_s, _ = standardize(Xtr, Xtr)
    return LogisticRegression(C=1.0, max_iter=2000).fit(Xtr_s, ytr), (Xtr)

out = {}
p1, p2 = {}, {}
for name, (Xtr, ytr, Xte, yte) in {
        'DS1_train_DS2_test': (X1, y1, X2, y2),
        'DS2_train_DS1_test': (X2, y2, X1, y1)}.items():
    # P1: M1 with S oversampling
    m = fit_gbm(Xtr[:, M1_IDX], ytr, oversample_S=True)
    pred = m.predict(np.nan_to_num(Xte[:, M1_IDX]))
    s_sens = float(np.mean(pred[yte == 'S'] == 'S')) if (yte == 'S').sum() else None
    p1[name] = {'S_sens': s_sens, 'acc': float(accuracy_score(yte, pred)),
                'V_sens': float(np.mean(pred[yte == 'V'] == 'V'))}
    # P2: accuracy on N/V/F/Q
    keep = np.isin(yte, list('NVFQ'))
    mM = fit_gbm(Xtr[:, M1_IDX], ytr)
    pM = mM.predict(np.nan_to_num(Xte[:, M1_IDX]))
    _, Xte_s = standardize(Xtr[:, B1_IDX], Xte[:, B1_IDX])
    Xtr_s, _ = standardize(Xtr[:, B1_IDX], Xtr[:, B1_IDX])
    mB = LogisticRegression(C=1.0, max_iter=2000).fit(Xtr_s, ytr)
    pB = mB.predict(Xte_s)
    p2[name] = {'M1': float(accuracy_score(yte[keep], pM[keep])),
                'B1': float(accuracy_score(yte[keep], pB[keep]))}
    print(name, 'P1', p1[name], 'P2', p2[name], flush=True)

out = {
    'P1_S_oversample': p1,
    'P1_gate_S_sens_ge_0.55_both': all(p['S_sens'] >= 0.55 for p in p1.values()),
    'P2_NVFQ_accuracy': p2,
    'P2_gate_M1_ge_B1+0.02_both': all(p['M1'] >= p['B1'] + 0.02 for p in p2.values()),
}
print(json.dumps(out, indent=1))
json.dump(out, open('results/amend1.json', 'w'), indent=1)
