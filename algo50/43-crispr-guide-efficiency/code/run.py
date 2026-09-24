"""LOGO evaluation on V1 + transfer to V2. Writes results/results.json.
Features standardized per training fold (mean/std of training genes only)."""
import json
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.ensemble import HistGradientBoostingRegressor
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
            if te.sum() < 5:
                continue
            Xtr, Xte = standardize(X[tr], X[te])
            m = Ridge(alpha=a).fit(Xtr, y[tr])
            sp.append(spearmanr(m.predict(Xte), y[te]).statistic)
        s = float(np.mean(sp))
        if s > best_s:
            best_s, best_a = s, a
    Xs, _ = standardize(X, X)
    return Ridge(alpha=best_a).fit(Xs, y), best_a

def fit_gbm(X, y):
    return HistGradientBoostingRegressor(
        loss='squared_error', max_iter=300, learning_rate=0.06,
        max_leaf_nodes=31, min_samples_leaf=20, l2_regularization=1.0,
        early_stopping=False, random_state=1).fit(X, y)

def logo(X, y, genes, kind):
    preds = np.full(len(y), np.nan)
    alphas = {}
    for g in np.unique(genes):
        tr, te = genes != g, genes == g
        if kind == 'ridge':
            m, a = fit_ridge(X[tr], y[tr], genes[tr])
            alphas[g] = a
            Xtr, Xte = standardize(X[tr], X[te])
            m2 = Ridge(alpha=a).fit(Xtr, y[tr])
            preds[te] = m2.predict(Xte)
        else:
            m = fit_gbm(X[tr], y[tr])
            preds[te] = m.predict(X[te])
    sp = {g: float(spearmanr(preds[genes == g], y[genes == g]).statistic)
          for g in np.unique(genes)}
    return preds, float(np.mean(list(sp.values()))), sp, alphas

v1 = pd.read_csv('data/v1.csv')
v2 = pd.read_csv('data/v2.csv')
y1, g1 = v1['activity'].to_numpy(), v1['gene'].to_numpy()

X0 = np.array([sum(c in 'GC' for c in s[4:24]) for s in v1['ext34']],
              dtype=np.float32).reshape(-1, 1)
Xb1, _ = build(v1, extended=False)
Xm1, _ = build(v1, extended=True)
print('dims', X0.shape, Xb1.shape, Xm1.shape)

out = {}
p0, s0, per0, _ = logo(X0, y1, g1, 'ridge')
pB, sB, perB, alB = logo(Xb1, y1, g1, 'ridge')
pM, sM, perM, _ = logo(Xm1, y1, g1, 'gbm')
out['logo'] = {'B0_gc_only': s0, 'B1_rs1_ridge': sB, 'M1_gbm': sM,
               'per_gene': {'B0': per0, 'B1': perB, 'M1': perM}, 'B1_alphas': alB}
print('LOGO mean Spearman  B0 %.3f  B1 %.3f  M1 %.3f' % (s0, sB, sM))

sel = np.zeros(len(y1), bool)
for g in np.unique(g1):
    idx = np.where(g1 == g)[0]
    k = max(1, int(round(0.10 * len(idx))))
    sel[idx[np.argsort(-pM[idx])[:k]]] = True
g4 = float(np.mean(v1['pct_rank'].to_numpy()[sel] >= 0.75))
out['g4_topdecile_precision_M1'] = g4
print('G4 pooled top-decile precision: %.3f (chance 0.25)' % g4)

X2b1, _ = build(v2, extended=False)
X2m1, _ = build(v2, extended=True)
y2 = v2['score'].to_numpy().astype(float)
g2 = v2['gene'].to_numpy()
mb1, a1 = fit_ridge(Xb1, y1, g1)
Xs1, Xs2 = standardize(Xb1, X2b1)
mb1 = Ridge(alpha=a1).fit(Xs1, y1)
mm1 = fit_gbm(Xm1, y1)
predB2, predM2 = mb1.predict(Xs2), mm1.predict(X2m1)
tB = float(spearmanr(predB2, y2).statistic)
tM = float(spearmanr(predM2, y2).statistic)
per_gene_t = {}
for g in np.unique(g2):
    m = g2 == g
    if m.sum() >= 20:
        per_gene_t[g] = {'B1': float(spearmanr(predB2[m], y2[m]).statistic),
                         'M1': float(spearmanr(predM2[m], y2[m]).statistic),
                         'n': int(m.sum())}
out['transfer_v2'] = {'B1': tB, 'M1': tM, 'per_gene': per_gene_t, 'B1_alpha': a1}
print('Transfer V2 Spearman  B1 %.3f  M1 %.3f' % (tB, tM))

out['gates'] = {
    'G1_M1_ge_B1+0.02': bool(sM >= sB + 0.02),
    'G2_B1_ge_B0+0.05': bool(sB >= s0 + 0.05),
    'G3_transfer': bool(tM >= 0.25 and tM >= tB - 0.01),
    'G4_topdecile_ge_0.50': bool(g4 >= 0.50),
}
print(json.dumps(out['gates'], indent=1))
json.dump(out, open('results/results.json', 'w'), indent=1)
pd.DataFrame({'gene': g1, 'y': y1, 'pB1': pB, 'pM1': pM}).to_csv(
    'results/logo_predictions.csv', index=False)
