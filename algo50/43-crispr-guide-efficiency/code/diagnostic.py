"""Diagnostic (not gated): ridge on M1 features - is the win features or model class?"""
import json
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.linear_model import Ridge
from features import build

ALPHAS = [0.1, 1.0, 10.0, 100.0]
def standardize(Xtr, Xte):
    Xtr, Xte = Xtr.copy(), Xte.copy()
    med = np.nanmedian(Xtr, axis=0)
    med = np.where(np.isnan(med), 0.0, med)
    for X in (Xtr, Xte):
        idx = np.where(np.isnan(X))
        X[idx] = np.take(med, idx[1])
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd == 0] = 1.0
    return (Xtr - mu) / sd, (Xte - mu) / sd
def fit_ridge(X, y, genes):
    best_a, best_s = None, -2
    for a in ALPHAS:
        sp = []
        for g in np.unique(genes):
            tr, te = genes != g, genes == g
            if te.sum() < 5: continue
            Xtr, Xte = standardize(X[tr], X[te])
            m = Ridge(alpha=a).fit(Xtr, y[tr])
            sp.append(spearmanr(m.predict(Xte), y[te]).statistic)
        s = float(np.mean(sp))
        if s > best_s: best_s, best_a = s, a
    return None, best_a

v1 = pd.read_csv('data/v1.csv')
v2 = pd.read_csv('data/v2.csv')
y1, g1 = v1['activity'].to_numpy(), v1['gene'].to_numpy()
Xm1, names = build(v1, extended=True)

sp = {}
for g in np.unique(g1):
    tr, te = g1 != g, g1 == g
    _, a = fit_ridge(Xm1[tr], y1[tr], g1[tr])
    Xtr, Xte = standardize(Xm1[tr], Xm1[te])
    m = Ridge(alpha=a).fit(Xtr, y1[tr])
    sp[g] = float(spearmanr(m.predict(Xte), y1[te]).statistic)
mean_ridge_m1 = float(np.mean(list(sp.values())))
print('LOGO mean Spearman ridge-on-M1-features: %.3f' % mean_ridge_m1)

# transfer
X2m1, _ = build(v2, extended=True)
_, a = fit_ridge(Xm1, y1, g1)
Xs1, Xs2 = standardize(Xm1, X2m1)
m = Ridge(alpha=a).fit(Xs1, y1)
t = float(spearmanr(m.predict(Xs2), v2['score'].to_numpy().astype(float)).statistic)
print('Transfer V2 ridge-on-M1-features: %.3f' % t)
json.dump({'logo_ridge_on_M1_features': mean_ridge_m1, 'per_gene': sp,
           'transfer_v2_ridge_on_M1_features': t},
          open('results/diagnostic.json', 'w'), indent=1)
