"""Build window features for all 23 AFDB records (cached), then LORO eval."""
import json, os, sys
import numpy as np
import pandas as pd
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
CACHE = os.path.expanduser('~/work/afib47/feat_cache')
os.makedirs(CACHE, exist_ok=True)
RECS = ['04015','04043','04048','04126','04746','04908','04936','05091','05121',
        '05261','06426','06453','06995','07162','07859','07879','07910','08215',
        '08219','08378','08405','08434','08455']

def rhythm_map(rec):
    ann = wfdb.rdann(os.path.join(DATA, rec), 'atr')
    marks = []
    for s, note in zip(ann.sample, ann.aux_note):
        if note and note.startswith('('):
            marks.append((int(s), 'AFIB' if 'AFIB' in note else 'OTHER'))
    return marks

def build_record(rec):
    f = os.path.join(CACHE, rec + '.npz')
    if os.path.exists(f):
        z = np.load(f)
        return z['X'], z['y']
    sig = wfdb.rdrecord(os.path.join(DATA, rec)).p_signal[:, 0]
    sig100 = resample_poly(sig, 2, 5)  # 250 -> 100 Hz
    peaks = detect_qrs(sig100, fs=100)
    rr = np.diff(peaks) / 100.0
    clean = (rr >= 0.3) & (rr <= 2.0)
    rr_c = rr[clean]
    beat_t = peaks[1:][clean]  # sample index at fs=100 of each clean RR's end beat
    marks = rhythm_map(rec)
    m_s = np.array([m[0] for m in marks])
    m_l = [m[1] for m in marks]
    X = window_features(rr_c)
    y = []
    for w in range(X.shape[0]):
        center_beat = w * 30 + 30  # window center in clean-beat index
        if center_beat >= len(beat_t):
            y.append(-1); continue
        samp100 = beat_t[center_beat]
        samp250 = int(samp100 * 2.5)
        i = np.searchsorted(m_s, samp250, side='right') - 1
        y.append(1 if (i >= 0 and m_l[i] == 'AFIB') else 0)
    y = np.array(y)
    keep = y >= 0
    X, y = X[keep], y[keep]
    np.savez(f, X=X, y=y)
    print(rec, 'windows', len(y), 'af frac %.2f' % (y.mean() if len(y) else -1), flush=True)
    return X, y

Xs, ys, gs = [], [], []
for rec in RECS:
    X, y = build_record(rec)
    if len(y):
        Xs.append(X); ys.append(y); gs += [rec] * len(y)
X = np.vstack(Xs); y = np.concatenate(ys); groups = np.array(gs)
print('total windows', len(y), 'AF frac %.3f' % y.mean())

def standardize(Xtr, Xte):
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd == 0] = 1.0
    return (Xtr - mu) / sd, (Xte - mu) / sd

def best_c(X, y, g):
    if X.shape[1] == 1:
        return 1.0
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
            if a > ba:
                ba, bc = a, c
    return bc if bc is not None else 1.0

def logo(Xf, kind):
    probs = np.full(len(y), np.nan)
    thr = {}
    for r in np.unique(groups):
        tr, te = groups != r, groups == r
        if kind == 'gbm':
            m = HistGradientBoostingClassifier(
                max_iter=300, learning_rate=0.06, max_leaf_nodes=31,
                min_samples_leaf=20, l2_regularization=1.0,
                early_stopping=False, random_state=1).fit(Xf[tr], y[tr])
            ptr = m.predict_proba(Xf[tr])[:, 1]
        else:
            c = best_c(Xf[tr], y[tr], groups[tr])
            Xtr, Xte = standardize(Xf[tr], Xf[te])
            m = LogisticRegression(C=c, max_iter=2000).fit(Xtr, y[tr])
            ptr = m.predict_proba(Xtr)[:, 1]
            probs[te] = m.predict_proba(Xte)[:, 1]
        if kind == 'gbm':
            probs[te] = m.predict_proba(Xf[te])[:, 1]
        # Youden threshold on training records
        fpr_t, tpr_t, ths = [], [], np.arange(0.05, 0.96, 0.01)
        yt = y[tr]
        for t in ths:
            pred = ptr > t
            tp = float(np.mean(pred[yt == 1])); tn = float(np.mean(~pred[yt == 0]))
            fpr_t.append(1 - tn); tpr_t.append(tp)
        j = int(np.argmax(np.array(tpr_t) - np.array(fpr_t)))
        thr[r] = float(ths[j])
    return probs, thr

p0, t0 = logo(X[:, B0_IDX], 'logreg')
pB, tB = logo(X[:, B1_IDX], 'logreg')
pM, tM = logo(X, 'gbm')

def auc(p): return float(roc_auc_score(y, p))

def sens_spec(p, thr):
    pred = np.zeros(len(y), bool)
    for r in np.unique(groups):
        pred[groups == r] = p[groups == r] > thr[r]
    sens = float(np.mean(pred[y == 1])); spec = float(np.mean(~pred[y == 0]))
    return sens, spec

sM, spM = sens_spec(pM, tM)

true_burden, pred_burden = [], []
for r in np.unique(groups):
    m = groups == r
    true_burden.append(float(y[m].mean()))
    pred_burden.append(float(pM[m].mean()))
g4 = float(spearmanr(true_burden, pred_burden).statistic)

out = {
    'n_windows': int(len(y)), 'af_fraction': float(y.mean()),
    'auroc': {'B0_rmssd': auc(p0), 'B1_poincare_logreg': auc(pB), 'M1_gbm': auc(pM)},
    'M1_sens_spec_youden': [sM, spM],
    'af_burden_spearman_M1': g4,
    'true_burden': true_burden, 'pred_burden': pred_burden,
    'gates': {
        'G1_M1_ge_B1+0.02': bool(auc(pM) >= auc(pB) + 0.02),
        'G2_B1_ge_B0+0.05': bool(auc(pB) >= auc(p0) + 0.05),
        'G3_sens_spec_ge_0.90': bool(sM >= 0.90 and spM >= 0.90),
        'G4_burden_spearman_ge_0.90': bool(g4 >= 0.90),
    },
}
print(json.dumps({k: v for k, v in out.items() if 'burden' not in k or k == 'af_burden_spearman_M1'}, indent=1))
json.dump(out, open('results/results.json', 'w'), indent=1)
pd.DataFrame({'record': groups, 'y': y, 'pB1': pB, 'pM1': pM}).to_csv(
    'results/window_predictions.csv', index=False)
