#!/usr/bin/env python3
import json, time
import numpy as np, pandas as pd, anndata as ad
from scipy.stats import pearsonr
t0 = time.time()
rng = np.random.default_rng(20260923)
a = ad.read_h5ad('data/Dixit2016.h5ad', backed='r')
obs = a.obs[['perturbation','target']].copy()
obs['target'] = [t if isinstance(t,str) and not t.startswith('INTERGENIC') else None for t in obs.target]
unstim = np.ones(len(obs), dtype=bool)  # v5: single condition (13-day)
ctrl = unstim & (obs.perturbation == 'control').values
print('unstim cells:', unstim.sum(), 'controls:', ctrl.sum(), flush=True)
# counts per target (unstimulated)
cnt = obs[unstim & (obs.perturbation != 'control')].groupby('target').size()
cand = cnt[cnt >= 25].index.tolist()
print('targets >=25 cells:', len(cand), cand, flush=True)
# load unstimulated X (sparse)
X = a[unstim, :].to_memory() if hasattr(a[unstim,:],'to_memory') else None
import scipy.sparse as sp
Xs = a[unstim, :].X
if not sp.issparse(Xs): Xs = sp.csr_matrix(Xs)
print('X:', Xs.shape, Xs.dtype, 'max:', float(Xs.max()), flush=True)
raw = float(Xs.max()) > 60
genes = np.array(a.var_names)
ctrl_idx = np.where(ctrl[unstim])[0]
Xc = Xs[ctrl_idx]
# normalize if raw counts (CPM+log1p per cell) - control-only variance selection
def norm(M):
    if not raw: return M
    lib = np.asarray(M.sum(1)).ravel(); lib[lib==0]=1
    M = M.multiply(1e4/lib[:,None]).tocsr()
    return M.log1p()
# control-only variance on all genes (sparse moments)
Nc = norm(Xc)
mu = np.asarray(Nc.mean(0)).ravel()
m2 = np.asarray(Nc.multiply(Nc).mean(0)).ravel()
var = m2 - mu**2
top = np.argsort(var)[-500:]
sel = sorted(set(top) | {i for i,g in enumerate(genes) if g in set(cand)})
sel = np.array(sorted(sel))
print('selected genes:', len(sel), flush=True)
# dense matrix: unstim cells x selected genes, normalized
N = norm(Xs[:, sel]).toarray().astype(np.float32)
gsel = genes[sel]
gidx = {g:i for i,g in enumerate(gsel)}
# pseudobulk log2FC per target vs controls
cmean = N[ctrl_idx].mean(0)
de = {}
for t in cand:
    ri = np.where((obs.target.values[unstim] == t))[0]
    if len(ri) < 25: continue
    de[t] = N[ri].mean(0) - cmean
# v2: effect-presence filter via control-split null (locked in GATES-v2.md)
rng2 = np.random.default_rng(7)
ss = {t: float((v**2).sum()) for t, v in de.items()}
ok = {}
qrows = []
for t, v in de.items():
    n = int((obs.target.values[unstim] == t).sum())
    ns = []
    for _ in range(100):
        perm = rng2.permutation(ctrl_idx)
        h1, h2 = perm[:n], perm[n:2*n]
        if len(h2) < n: continue
        d = N[h1].mean(0) - N[h2].mean(0)
        ns.append(float((d**2).sum()))
    q = float(np.quantile(ns, 0.95)) if ns else float('nan')
    qrows.append(dict(target=t, n=n, ss_de=ss[t], null_q95=q, in_panel=ss[t] > q))
    if ss[t] > q: ok[t] = v
print('targets passing size-matched effect-presence:', len(ok), sorted(ok), flush=True)
panel = sorted(ok, key=lambda t: -ss[t])[:20]
pd.DataFrame(qrows).to_csv('results/v5_effect_presence_qc.csv', index=False)
# control correlation network on the 500 variable genes
top_in_sel = [i for i,g in enumerate(gsel) if g in set(genes[top])]
Nc_dense = N[ctrl_idx][:, top_in_sel]
C = np.corrcoef(Nc_dense.T)
gvar = gsel[top_in_sel]
res = []
for t in panel:
    selfeff = ok[t][gidx[t]]
    if t not in set(gvar):
        # target not among variable genes: prediction vector all-zero -> skip per frozen metrics
        continue
    ti = list(gvar).index(t)
    pred = C[ti] * selfeff
    obsde = ok[t][top_in_sel]
    # baseline: mean DE of other perturbations
    pool = [ok[o][top_in_sel] for o in panel if o != t and o in set(gvar)]
    if len(pool) == 0: continue
    others = np.mean(pool, axis=0)
    r_net = pearsonr(pred, obsde)[0]
    r_base = pearsonr(others, obsde)[0]
    # precision@20 (top |values|)
    p20 = len(set(np.argsort(np.abs(pred))[-20:]) & set(np.argsort(np.abs(obsde))[-20:])) / 20
    b20 = len(set(np.argsort(np.abs(others))[-20:]) & set(np.argsort(np.abs(obsde))[-20:])) / 20
    # permutation null: corr of obsde with other perturbations' predicted vectors
    null = [pearsonr(C[list(gvar).index(o)] * ok[o][gidx[o]], obsde)[0] for o in panel if o != t and o in set(gvar)]
    pval = (1 + sum(1 for z in null if z >= r_net)) / (1 + len(null))
    res.append(dict(target=t, n_cells=int((obs.target.values[unstim]==t).sum()), r_net=float(r_net),
                    r_base=float(r_base), p20_net=float(p20), p20_base=float(b20), perm_p=float(pval)))
    print(t, 'r_net=%.3f r_base=%.3f p=%.3f' % (r_net, r_base, pval), flush=True)
R = pd.DataFrame(res); R.to_csv('results/v5_per_target_metrics.csv', index=False)
dr = (R.r_net - R.r_base).median()
g1 = bool(dr >= 0.05 and (R.perm_p <= 0.05).mean() >= 0.5)
g2 = bool((R.p20_net - R.p20_base).median() > 0)
summary = dict(panel=list(R.target), n_targets=len(R),
               G1=dict(median_r_net=float(R.r_net.median()), median_r_base=float(R.r_base.median()),
                       median_delta=float(dr), frac_perm_sig=float((R.perm_p<=0.05).mean()), PASS=g1),
               G2=dict(median_p20_net=float(R.p20_net.median()), median_p20_base=float(R.p20_base.median()), PASS=g2),
               runtime_min=(time.time()-t0)/60)
json.dump(summary, open('results/v5_gate_summary.json','w'), indent=2)
print(json.dumps(summary, indent=2), flush=True)
