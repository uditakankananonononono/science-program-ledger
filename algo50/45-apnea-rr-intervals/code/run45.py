"""Build per-minute features from all 35 records (cached per record), then
record-held-out evaluation. Writes results/results.json."""
import json, os, sys
import numpy as np
import pandas as pd
import wfdb
from scipy.stats import spearmanr
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score
sys.path.insert(0, os.path.dirname(__file__))
from qrs import detect_qrs
from features45 import minute_features, B0_IDX, B1_IDX

DATA = os.path.expanduser('~/work/apnea45/data')
CACHE = os.path.expanduser('~/work/apnea45/feat_cache')
os.makedirs(CACHE, exist_ok=True)
RECS = ([f'a{i:02d}' for i in range(1, 21)] + [f'b{i:02d}' for i in range(1, 6)]
        + [f'c{i:02d}' for i in range(1, 11)])

def build_record(rec):
    f = os.path.join(CACHE, rec + '.npz')
    if os.path.exists(f):
        z = np.load(f)
        return z['X'], z['y'], z['mins']
    sig = wfdb.rdrecord(os.path.join(DATA, rec)).p_signal[:, 0]
    ann = wfdb.rdann(os.path.join(DATA, rec), 'apn')
    peaks = detect_qrs(sig, fs=100)
    rr_t = peaks[1:] / 100.0
    rr_v = np.diff(peaks) / 100.0
    X, mins = minute_features(rr_t, rr_v)
    # labels: .apn symbols per minute ('A' or 'N'); ann.sample at minute starts
    lab = {}
    for s, sym in zip(ann.sample, ann.symbol):
        lab[int(s // 6000)] = 1 if sym == 'A' else 0
    y = np.array([lab.get(int(m), -1) for m in mins])
    keep = y >= 0
    X, y, mins = X[keep], y[keep], mins[keep]
    np.savez(f, X=X, y=y, mins=mins)
    print(rec, 'beats', len(peaks), 'minutes', len(y), 'apnea frac %.2f' % y.mean(), flush=True)
    return X, y, mins

rows, ys, gs = [], [], []
for rec in RECS:
    X, y, mins = build_record(rec)
    rows.append(X); ys.append(y); gs += [rec] * len(y)
X = np.vstack(rows); y = np.concatenate(ys); groups = np.array(gs)
print('total minutes', len(y), 'records', len(RECS))

def standardize(Xtr, Xte):
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd == 0] = 1.0
    return (Xtr - mu) / sd, (Xte - mu) / sd

def fit_logreg(X, y, g):
    if X.shape[1] == 1:
        return 1.0
    best_c, best_a = None, -1
    recs = np.unique(g)
    rng = np.random.RandomState(0)
    for c in (0.1, 1.0, 10.0):
        aucs = []
        for r in recs:
            tr, te = g != r, g == r
            if len(np.unique(y[te])) < 2:
                continue
            tri = np.where(tr)[0]
            if len(tri) > 6000:
                tri = rng.choice(tri, 6000, replace=False)
            Xtr, Xte = standardize(X[tri], X[te])
            m = LogisticRegression(C=c, max_iter=2000).fit(Xtr, y[tri])
            aucs.append(roc_auc_score(y[te], m.predict_proba(Xte)[:, 1]))
        if aucs:
            a = float(np.mean(aucs))
            if a > best_a:
                best_a, best_c = a, c
    return best_c if best_c is not None else 1.0

def logo_probs(Xf, kind):
    probs = np.full(len(y), np.nan)
    for r in np.unique(groups):
        tr, te = groups != r, groups == r
        if kind == 'gbm':
            m = HistGradientBoostingClassifier(
                max_iter=300, learning_rate=0.06, max_leaf_nodes=31,
                min_samples_leaf=20, l2_regularization=1.0,
                early_stopping=False, random_state=1).fit(Xf[tr], y[tr])
            probs[te] = m.predict_proba(Xf[te])[:, 1]
        else:
            c = fit_logreg(Xf[tr], y[tr], groups[tr])
            Xtr, Xte = standardize(Xf[tr], Xf[te])
            m = LogisticRegression(C=c, max_iter=2000).fit(Xtr, y[tr])
            probs[te] = m.predict_proba(Xte)[:, 1]
    return probs

p0 = logo_probs(X[:, B0_IDX], 'logreg')
pB = logo_probs(X[:, B1_IDX], 'logreg')
pM = logo_probs(X, 'gbm')

def auc(p):
    return float(roc_auc_score(y, p))

# record-level: mean prob per record, apnea(a) vs control(c)
rec_score = {}
for r in np.unique(groups):
    rec_score[r] = float(np.mean(pM[groups == r]))
ra = [rec_score[f'a{i:02d}'] for i in range(1, 21)]
rc = [rec_score[f'c{i:02d}'] for i in range(1, 11)]
g4 = float(roc_auc_score([1]*20 + [0]*10, ra + rc))

out = {
    'n_minutes': int(len(y)), 'apnea_fraction': float(y.mean()),
    'auroc': {'B0_mean_rr': auc(p0), 'B1_logreg_classic': auc(pB), 'M1_gbm': auc(pM)},
    'acc_M1_thr0.5': float(accuracy_score(y, pM > 0.5)),
    'acc_B1_thr0.5': float(accuracy_score(y, pB > 0.5)),
    'record_level_a_vs_c_auroc_M1': g4,
    'record_scores_M1': rec_score,
    'gates': {
        'G1_M1_ge_B1+0.02': bool(auc(pM) >= auc(pB) + 0.02),
        'G2_B1_ge_B0+0.05': bool(auc(pB) >= auc(p0) + 0.05),
        'G3_acc_M1_ge_0.80': bool(accuracy_score(y, pM > 0.5) >= 0.80),
        'G4_record_avc_auroc_ge_0.90': bool(g4 >= 0.90),
    },
}
print(json.dumps({k: v for k, v in out.items() if k != 'record_scores_M1'}, indent=1))
json.dump(out, open('results/results.json', 'w'), indent=1)
pd.DataFrame({'record': groups, 'y': y, 'pB1': pB, 'pM1': pM}).to_csv(
    'results/minute_predictions.csv', index=False)
