"""Inter-patient AAMI 5-class heartbeat classification, both DS directions."""
import json, os
import numpy as np
import pandas as pd
import wfdb
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

DATA = os.path.expanduser('~/work/beats49/data')
DS1 = ['101','106','108','109','112','114','115','116','118','119','122','124',
       '201','203','205','207','208','209','215','220','223','230']
DS2 = ['100','103','105','111','113','117','121','123','200','202','210','212',
       '213','214','219','221','222','228','231','232','233','234']
MAP = {}
for s in 'N L R e j'.split(): MAP[s] = 'N'
for s in 'A a J S'.split(): MAP[s] = 'S'
for s in 'V E'.split(): MAP[s] = 'V'
MAP['F'] = 'F'
for s in '/ f Q p'.split(): MAP[s] = 'Q'
FS = 360
PRE, POST, NPT = int(0.200 * FS), int(0.300 * FS), 25

def mlii_channel(rec):
    lines = open(os.path.join(DATA, rec + '.hea')).read().splitlines()
    for i, ln in enumerate(lines[1:], 0):
        if 'MLII' in ln.upper():
            return i
    return 0

def extract(rec):
    ch = mlii_channel(rec)
    sig = wfdb.rdrecord(os.path.join(DATA, rec)).p_signal[:, ch].astype(np.float64)
    if rec == '114':
        sig = -sig
    ann = wfdb.rdann(os.path.join(DATA, rec), 'atr')
    beats = [(int(s), MAP[sym]) for s, sym in zip(ann.sample, ann.symbol) if sym in MAP]
    peaks = np.array([b[0] for b in beats])
    rr = np.diff(peaks) / FS
    pre_rr = np.concatenate(([np.nan], rr))
    post_rr = np.concatenate((rr, [np.nan]))
    rows = []
    labels = []
    idx = np.arange(PRE, PRE + PRE + POST, (PRE + POST) // NPT)[:NPT]
    didx = idx[:-1]
    for i, (p, lab) in enumerate(beats):
        if p - PRE < 0 or p + POST > len(sig):
            continue
        win = sig[p - PRE:p + POST]
        rel = idx - PRE  # positions relative to window start
        if rel[-1] >= len(win):
            continue
        w = win[rel]
        wz = (w - w.mean()) / (w.std() + 1e-9)
        dwin = np.diff(win)
        rel_d = np.clip(idx - PRE - 1, 0, len(dwin) - 1)[:NPT - 1]
        dw = dwin[rel_d]
        if len(dw) < NPT:
            dw = np.pad(dw, (0, NPT - len(dw)))
        dwz = (dw - dw.mean()) / (dw.std() + 1e-9)
        loc = rr[max(0, i-20):i].mean() if i > 0 and len(rr[max(0, i-20):i]) else np.nan
        recmean = rr.mean()
        pre = pre_rr[i] if i < len(pre_rr) else np.nan
        post = post_rr[i] if i < len(post_rr) else np.nan
        pk = np.max(np.abs(win)); half = np.where(np.abs(win) > 0.2 * pk)[0]
        width = (half[-1] - half[0]) / FS if len(half) else 0.0
        rows.append(np.concatenate([
            [pre, post, pre / loc if loc and loc > 0 else 1.0,
             pre / recmean if recmean > 0 else 1.0,
             float(win.max()), float(win.min()), width,
             float(np.argmax(win) / len(win))],
            wz, dwz]).astype(np.float32))
        labels.append(lab)
    return np.array(rows, dtype=np.float32), labels

print('extracting...', flush=True)
cache = {}
for rec in DS1 + DS2:
    f = os.path.expanduser(f'~/work/beats49/cache/{rec}.npz')
    os.makedirs(os.path.dirname(f), exist_ok=True)
    if os.path.exists(f):
        z = np.load(f, allow_pickle=True)
        Xr, lr = z['X'], z['y'].tolist()
    else:
        Xr, lr = extract(rec)
        np.savez(f, X=Xr, y=np.array(lr))
    cache[rec] = (Xr, lr)
    print(rec, Xr.shape, flush=True)

def assemble(recs):
    Xs, ys = [], []
    for r in recs:
        Xr, lr = cache[r]
        Xs.append(Xr); ys += lr
    return np.vstack(Xs), np.array(ys)

X1, y1 = assemble(DS1)
X2, y2 = assemble(DS2)
print('DS1', X1.shape, 'DS2', X2.shape)

B0_IDX = [0, 1, 2, 3]
B1_IDX = list(range(0, 32))           # RR(4) + amp stats + width + 25 window
M1_IDX = list(range(0, X1.shape[1]))  # B1 + argmax pos + 25 diff window

def standardize(Xtr, Xte):
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd == 0] = 1.0
    Xtr = (Xtr - mu) / sd; Xte = (Xte - mu) / sd
    return np.nan_to_num(Xtr), np.nan_to_num(Xte)

def fit_predict(Xtr, ytr, Xte, idx, kind):
    Xtr, Xte = Xtr[:, idx], Xte[:, idx]
    if kind == 'gbm':
        m = HistGradientBoostingClassifier(
            max_iter=300, learning_rate=0.06, max_leaf_nodes=31,
            min_samples_leaf=20, l2_regularization=1.0,
            early_stopping=False, random_state=1).fit(np.nan_to_num(Xtr), ytr)
        return m.predict(np.nan_to_num(Xte))
    from sklearn.model_selection import StratifiedKFold
    best_c, best_a = 1.0, -1
    if len(idx) > 4:
        skf = StratifiedKFold(5, shuffle=True, random_state=0)
        for c in (0.1, 1.0, 10.0):
            accs = []
            for tr_i, te_i in skf.split(Xtr, ytr):
                Xa, Xb = standardize(Xtr[tr_i], Xtr[te_i])
                m = LogisticRegression(C=c, max_iter=1000).fit(Xa, ytr[tr_i])
                accs.append(accuracy_score(ytr[te_i], m.predict(Xb)))
            a = float(np.mean(accs))
            if a > best_a:
                best_a, best_c = a, c
    Xa, Xb = standardize(Xtr, Xte)
    m = LogisticRegression(C=best_c, max_iter=2000).fit(Xa, ytr)
    return m.predict(Xb)

def run_direction(Xtr, ytr, Xte, yte):
    res = {}
    for name, idx, kind in [('B0', B0_IDX, 'logreg'), ('B1', B1_IDX, 'logreg'),
                            ('M1', M1_IDX, 'gbm')]:
        pred = fit_predict(Xtr, ytr, Xte, idx, kind)
        res[name] = {
            'acc': float(accuracy_score(yte, pred)),
            'per_class_sens': {c: float(np.mean(pred[yte == c] == c))
                               for c in 'NSVFQ' if (yte == c).sum() > 0},
            'n_test': {c: int((yte == c).sum()) for c in 'NSVFQ'},
        }
    return res

out = {'DS1_train_DS2_test': run_direction(X1, y1, X2, y2),
       'DS2_train_DS1_test': run_direction(X2, y2, X1, y1)}
d = out
def g1():
    return all(d[k]['M1']['acc'] >= d[k]['B1']['acc'] + 0.02 for k in d)
def g2():
    return all(d[k]['B1']['acc'] >= d[k]['B0']['acc'] + 0.05 for k in d)
def g3():
    return all(d[k]['M1']['per_class_sens'].get('V', 0) >= 0.75 for k in d)
def g4():
    return all(d[k]['M1']['per_class_sens'].get('S', 0) >= 0.55 for k in d)
out['gates'] = {'G1_M1_ge_B1+0.02_both': g1(), 'G2_B1_ge_B0+0.05_both': g2(),
                'G3_V_sens_ge_0.75_both': g3(), 'G4_S_sens_ge_0.55_both': g4()}
print(json.dumps(out, indent=1))
json.dump(out, open('results/results.json', 'w'), indent=1)
