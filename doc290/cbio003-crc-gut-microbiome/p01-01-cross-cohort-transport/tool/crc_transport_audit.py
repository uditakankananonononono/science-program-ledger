#!/usr/bin/env python3
"""crc-transport-audit: P01-01 cross-cohort transport stress test.
Locked pipeline (gates frozen 2026-09-24 before any model was fit):
  features: genus relative abundance, genera nonzero in >=1% of samples
  model: RandomForestClassifier(500 trees, class_weight=balanced, seed=7)
  G1: unweighted mean held-out LOCO AUC >= 0.75 across >=6 cohorts (boot95 CI reported)
  G2: >=5 cohort pairs with Spearman rho >= 0.6 over top-20-union importance ranks (1000-perm p<0.05)
  G3: geography-only (cohort one-hot, logistic, 5-fold CV) AUC < 0.70 else G1 void
Importance: mean|SHAP| (TreeExplainer) per own-cohort model; permutation fallback (locked amendment).
Usage: python3 crc_transport_audit.py <data_dir> <results_dir>
"""
import sys, json, os
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import roc_auc_score
from scipy.stats import spearmanr

SEED=7
data, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
X = pd.read_csv(os.path.join(data,'genus_matrix.csv'), index_col=0)
M = pd.read_csv(os.path.join(data,'samples.csv'), index_col=0)
M = M.loc[X.index]
y = (M['label']=='CRC').astype(int).values
coh = M['cohort'].values
keep = (X.values!=0).mean(axis=0) >= 0.01
feats = X.columns[keep]; Xv = X.values[:, keep]
rng = np.random.RandomState(SEED)

def rf(): return RandomForestClassifier(n_estimators=500, class_weight='balanced', random_state=SEED, n_jobs=2)

cohorts = sorted(set(coh))
res = {'n_samples': int(len(y)), 'n_genera_used': int(len(feats)), 'cohorts': {}}
# within-cohort CV AUC
skf = StratifiedKFold(5, shuffle=True, random_state=SEED)
within = {}
for c in cohorts:
    m = coh==c
    p = cross_val_predict(rf(), Xv[m], y[m], cv=skf, method='predict_proba')[:,1]
    within[c] = float(roc_auc_score(y[m], p))
res['within_cohort_cv_auc'] = within
# LOCO
loco = {}
probs = {}
for c in cohorts:
    m = coh==c
    mdl = rf().fit(Xv[~m], y[~m])
    p = mdl.predict_proba(Xv[m])[:,1]
    probs[c]=p
    loco[c] = float(roc_auc_score(y[m], p))
res['loco_auc'] = loco
boot = [np.mean(rng.choice(list(loco.values()), len(loco))) for _ in range(10000)]
res['G1'] = {'mean_loco_auc': float(np.mean(list(loco.values()))),
             'boot95_ci': [float(np.percentile(boot,2.5)), float(np.percentile(boot,97.5))],
             'n_cohorts': len(loco)}
# G3 geography-only
onehot = pd.get_dummies(coh).values
lg = LogisticRegression(max_iter=2000)
pg = cross_val_predict(lg, onehot, y, cv=skf, method='predict_proba')[:,1]
res['G3'] = {'geography_only_auc': float(roc_auc_score(y, pg))}
# importance per cohort
imp = {}
try:
    import shap
    method='shap'
    for c in cohorts:
        m = coh==c
        mdl = rf().fit(Xv[m], y[m])
        ex = shap.TreeExplainer(mdl)
        sv = ex.shap_values(Xv[m])
        sv = sv[:,:,1] if isinstance(sv,np.ndarray) and sv.ndim==3 else (sv[1] if isinstance(sv,list) else sv)
        imp[c] = pd.Series(np.abs(sv).mean(axis=0), index=feats)
except Exception as e:
    method='permutation'
    from sklearn.inspection import permutation_importance
    for c in cohorts:
        m = coh==c
        mdl = rf().fit(Xv[m], y[m])
        pi = permutation_importance(mdl, Xv[m], y[m], n_repeats=20, random_state=SEED, scoring='roc_auc')
        imp[c] = pd.Series(pi.importances_mean, index=feats)
res['importance_method'] = method
pairs=[]
cs=cohorts
for i in range(len(cs)):
    for j in range(i+1,len(cs)):
        a,b = cs[i],cs[j]
        top = set(imp[a].nlargest(20).index) | set(imp[b].nlargest(20).index)
        top = sorted(top)
        rho,_ = spearmanr(imp[a][top].values, imp[b][top].values)
        # permutation null
        cnt=0; va=imp[a][top].values; vb=imp[b][top].values
        for _ in range(1000):
            if spearmanr(va, rng.permutation(vb))[0] >= rho: cnt+=1
        pairs.append({'pair': f'{a}|{b}', 'rho': float(rho), 'perm_p': float((cnt+1)/1001)})
res['G2'] = {'pairs': pairs,
             'n_pass_pairs': int(sum(1 for p in pairs if p['rho']>=0.6 and p['perm_p']<0.05))}
g1p = res['G1']['mean_loco_auc'] >= 0.75 and res['G1']['n_cohorts'] >= 6
g2p = res['G2']['n_pass_pairs'] >= 5
g3p = res['G3']['geography_only_auc'] < 0.70
res['gates'] = {'G1_pass': bool(g1p), 'G2_pass': bool(g2p), 'G3_pass': bool(g3p)}
pd.DataFrame([(k,v) for k,v in loco.items()], columns=['held_out_cohort','loco_auc']).to_csv(os.path.join(out,'loco_auc.csv'), index=False)
pd.DataFrame(pairs).to_csv(os.path.join(out,'transport_scores.csv'), index=False)
impdf = pd.DataFrame(imp); impdf.to_csv(os.path.join(out,'importance_ranks.csv'))
json.dump(res, open(os.path.join(out,'results.json'),'w'), indent=1)
print(json.dumps({'within':within,'loco':loco,'G1':res['G1'],'G2_pass_pairs':res['G2']['n_pass_pairs'],'G3':res['G3'],'gates':res['gates'],'imp':method}, indent=1))
