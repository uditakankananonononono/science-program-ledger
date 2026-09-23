#!/usr/bin/env python3
"""DOC-1-001: drug response from baseline expression. Locked-gate pipeline.
Implements GATES.md + GATES-addendum-1.md exactly. No outcome-driven edits."""
import json, hashlib, time
import numpy as np, pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold, KFold
from scipy.stats import mannwhitneyu

rng = np.random.default_rng(20260923)
t0 = time.time()

# ---- load GDSC2 panel drugs (IC50 side) ----
gdsc = pd.read_excel('data/GDSC2.xlsx', usecols=['SANGER_MODEL_ID','DRUG_NAME','PATHWAY_NAME','LN_IC50'])
gdsc = gdsc.dropna(subset=['SANGER_MODEL_ID','LN_IC50'])

# ---- map SANGER_MODEL_ID -> DepMap ModelID ----
model = pd.read_csv('data/Model.csv')
assert 'SangerModelID' in model.columns and 'ModelID' in model.columns
smap = model.dropna(subset=['SangerModelID']).drop_duplicates('SangerModelID').set_index('SangerModelID')['ModelID']
gdsc['ModelID'] = gdsc['SANGER_MODEL_ID'].map(smap)
print('lines with DepMap match:', gdsc.ModelID.notna().sum(), '/', len(gdsc))

# ---- load expression (chunked, float32) ----
hdr = pd.read_csv('data/expression.csv', nrows=0)
genes = [c for c in hdr.columns if c != hdr.columns[0]]
print('expression genes:', len(genes))
dt = {c: np.float32 for c in genes}
chunks = [c for c in pd.read_csv('data/expression.csv', index_col=0, chunksize=200, dtype=dt)]
expr = pd.concat(chunks)
del chunks
expr.index.name = 'ModelID'
print('expression matrix:', expr.shape)

# ---- join; apply frozen panel rule ----
have_expr = set(expr.index)
gdsc = gdsc[gdsc.ModelID.isin(have_expr)]
counts = gdsc.groupby('DRUG_NAME')['ModelID'].nunique()
qual = counts[counts >= 300].index
var = gdsc[gdsc.DRUG_NAME.isin(qual)].groupby('DRUG_NAME')['LN_IC50'].var().sort_values(ascending=False)
panel = list(var.head(30).index)
print('PANEL locked by rule:', len(panel), panel)
path = gdsc[['DRUG_NAME','PATHWAY_NAME']].drop_duplicates('DRUG_NAME').set_index('DRUG_NAME')['PATHWAY_NAME']

CYTOTOXIC = {'DNA replication','mitosis','genome integrity','metabolism'}  # addendum-1 frozen
def klass(p): return 'cytotoxic' if str(p).strip().lower() in CYTOTOXIC else 'targeted'

ALPHAS = [0.1, 1.0, 10.0, 100.0, 1000.0]
def fit_predict_drug(drug):
    d = gdsc[gdsc.DRUG_NAME == drug].groupby('ModelID')['LN_IC50'].mean()
    common = d.index.intersection(expr.index)
    y = d.loc[common].values
    X = expr.loc[common].values
    n = len(y)
    gkf = GroupKFold(5); oof = np.zeros(n); oof_base = np.zeros(n); fold_alphas = []
    for tr, te in gkf.split(X, y, groups=common):
        v = X[tr].var(0); top = np.argsort(v)[-2000:]
        Xtr, Xte = X[tr][:, top], X[te][:, top]
        mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-8
        Xtr, Xte = (Xtr-mu)/sd, (Xte-mu)/sd
        # inner CV for alpha
        best_a, best_mse = ALPHAS[0], np.inf
        ikf = KFold(3, shuffle=True, random_state=1)
        for a in ALPHAS:
            mses = []
            for itr, ite in ikf.split(Xtr):
                m = Ridge(alpha=a).fit(Xtr[itr], y[tr][itr])
                mses.append(np.mean((m.predict(Xtr[ite]) - y[tr][ite])**2))
            if np.mean(mses) < best_mse: best_mse, best_a = np.mean(mses), a
        fold_alphas.append(best_a)
        m = Ridge(alpha=best_a).fit(Xtr, y[tr])
        oof[te] = m.predict(Xte); oof_base[te] = y[tr].mean()
    rmse_m = float(np.sqrt(np.mean((oof-y)**2))); rmse_b = float(np.sqrt(np.mean((oof_base-y)**2)))
    ss = 1 - np.sum((oof-y)**2)/np.sum((y-y.mean())**2)
    # permutation null on R^2 (fold alphas reused per addendum)
    null = []
    for p in range(20):
        yp = rng.permutation(y); oofp = np.zeros(n)
        for k,(tr, te) in enumerate(gkf.split(X, y, groups=common)):
            v = X[tr].var(0); top = np.argsort(v)[-2000:]
            Xtr, Xte = X[tr][:, top], X[te][:, top]
            mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-8
            m = Ridge(alpha=fold_alphas[k]).fit((Xtr-mu)/sd, yp[tr])
            oofp[te] = m.predict((Xte-mu)/sd)
        null.append(1 - np.sum((oofp-yp)**2)/np.sum((yp-yp.mean())**2))
    pval = (1 + sum(1 for z in null if z >= ss)) / 21
    return dict(drug=drug, n=n, rmse_model=rmse_m, rmse_base=rmse_b,
                rel_reduction=1 - rmse_m/rmse_b, r2=float(ss), perm_p=float(pval),
                pathway=str(path.get(drug,'')), klass=klass(path.get(drug,'')))

results = [fit_predict_drug(d) for d in panel]
R = pd.DataFrame(results)
R.to_csv('results/per_drug_metrics.csv', index=False)
med_red = R.rel_reduction.median()
frac_sig = (R.perm_p <= 0.05).mean()
g1 = bool(med_red >= 0.05 and frac_sig >= 0.5)
cyt = R[R.klass=='cytotoxic'].r2; tgt = R[R.klass=='targeted'].r2
U, p_mw = mannwhitneyu(tgt, cyt, alternative='greater')
g2 = bool(p_mw <= 0.05)
summary = dict(panel=panel, G1=dict(median_rel_rmse_reduction=float(med_red), frac_drugs_perm_sig=float(frac_sig), PASS=g1),
               G2=dict(median_r2_targeted=float(tgt.median()), median_r2_cytotoxic=float(cyt.median()), mannwhitney_p=float(p_mw), PASS=g2),
               runtime_min=(time.time()-t0)/60)
json.dump(summary, open('results/gate_summary.json','w'), indent=2)
print(json.dumps(summary, indent=2))
