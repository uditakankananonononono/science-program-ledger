"""P2: 120-beat windows (stride 60), identical models and evaluation."""
import json, os, sys
import numpy as np
import wfdb
from scipy.signal import resample_poly
from scipy.stats import spearmanr
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
sys.path.insert(0, os.path.dirname(__file__))
from qrs import detect_qrs
from features47 import window_features, B0_IDX, B1_IDX

DATA = os.path.expanduser('~/work/afib47/data')
CACHE = os.path.expanduser('~/work/afib47/feat_cache120')
os.makedirs(CACHE, exist_ok=True)
RECS = ['04015','04043','04048','04126','04746','04908','04936','05091','05121',
        '05261','06426','06453','06995','07162','07859','07879','07910','08215',
        '08219','08378','08405','08434','08455']

def build_record(rec):
    f = os.path.join(CACHE, rec + '.npz')
    if os.path.exists(f):
        z = np.load(f); return z['X'], z['y']
    sig = wfdb.rdrecord(os.path.join(DATA, rec)).p_signal[:, 0]
    sig100 = resample_poly(sig, 2, 5)
    peaks = detect_qrs(sig100, fs=100)
    rr = np.diff(peaks) / 100.0
    clean = (rr >= 0.3) & (rr <= 2.0)
    rr_c = rr[clean]
    beat_t = peaks[1:][clean]
    ann = wfdb.rdann(os.path.join(DATA, rec), 'atr')
    marks = [(int(s), 'AFIB' if 'AFIB' in n else 'OTHER')
             for s, n in zip(ann.sample, ann.aux_note) if n and n.startswith('(')]
    m_s = np.array([m[0] for m in marks]); m_l = [m[1] for m in marks]
    WIN, STR = 120, 60
    X = window_features(rr_c, WIN, STR)
    y = []
    for w in range(X.shape[0]):
        cb = w * STR + WIN // 2
        if cb >= len(beat_t):
            y.append(-1); continue
        i = np.searchsorted(m_s, int(beat_t[cb] * 2.5), side='right') - 1
        y.append(1 if (i >= 0 and m_l[i] == 'AFIB') else 0)
    y = np.array(y); keep = y >= 0
    np.savez(f, X=X[keep], y=y[keep])
    print(rec, 'windows', int(keep.sum()), flush=True)
    return X[keep], y[keep]

Xs, ys, gs = [], [], []
for rec in RECS:
    X, y = build_record(rec)
    if len(y):
        Xs.append(X); ys.append(y); gs += [rec] * len(y)
X = np.vstack(Xs); y = np.concatenate(ys); groups = np.array(gs)

def standardize(Xtr, Xte):
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd == 0] = 1.0
    return (Xtr - mu) / sd, (Xte - mu) / sd

def best_c(X, y, g):
    rng = np.random.RandomState(0)
    bc, ba = None, -1
    for c in (0.1, 1.0, 10.0):
        aucs = []
        for r in np.unique(g):
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
            if a > ba: ba, bc = a, c
    return bc if bc is not None else 1.0

def logo(Xf, kind):
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
            c = best_c(Xf[tr], y[tr], groups[tr])
            Xtr, Xte = standardize(Xf[tr], Xf[te])
            m = LogisticRegression(C=c, max_iter=2000).fit(Xtr, y[tr])
            probs[te] = m.predict_proba(Xte)[:, 1]
    return probs

pB = logo(X[:, B1_IDX], 'logreg')
pM = logo(X, 'gbm')
aB = float(roc_auc_score(y, pB)); aM = float(roc_auc_score(y, pM))
out = {'n_windows_120': int(len(y)),
       'auroc_120': {'B1': aB, 'M1': aM, 'delta': aM - aB},
       'P2_gate_M1_ge_B1+0.02': bool(aM >= aB + 0.02)}
print(json.dumps(out, indent=1))
json.dump(out, open('results/amend1.json', 'w'), indent=1)
