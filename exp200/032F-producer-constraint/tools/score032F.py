import json, csv, numpy as np, pyreadr
from scipy.stats import spearmanr
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold

def norm(s): return ' '.join(s.replace('_',' ').split()[:2]).lower()
def load(fn):
    with open(fn) as f:
        r = csv.reader(f, delimiter='\t'); h = next(r); return h, list(r)
sec_h, sec = load('secretionProductTable.txt'); fer_h, fer = load('FermentationTable.txt')
bil_h, bil = load('BileAcidTable.txt')
def pset(h, rows, cols):
    idx = [h.index(c) for c in cols if c in h]; out = set()
    for row in rows:
        if any(i < len(row) and row[i].strip() == '1' for i in idx): out.add(norm(row[0]))
    return out
BUT = [c for c in fer_h if c.startswith('Butyrate')]; PRO = [c for c in fer_h if c.startswith('Propionate')]
prod = {
 'propionate': pset(fer_h, fer, PRO),
 'butyrate...isobutytare.': pset(fer_h, fer, BUT),
 'cholate': pset(bil_h, bil, ['Cholate']),
 'chenodeoxycholate': pset(bil_h, bil, ['Chenodeoxycholate']),
 'deoxycholic.acid': pset(bil_h, bil, ['Deoxycholate']),
 'lithocholic.acid': pset(bil_h, bil, ['Lithocholate']),
 'chenodeoxycholate.deoxycholate.': pset(bil_h, bil, ['Chenodeoxycholate','Deoxycholate']),
 'putrescine': pset(sec_h, sec, ['Putrescine']),
 'glutamate': pset(sec_h, sec, ['L-glutamate']),
 'N.acetylspermidine': pset(sec_h, sec, ['Spermidine']),
}
METS = list(prod)

# model.txt column order -> mpcomp cluster position (validated 25/25)
with open('/home/sandbox/hmp2_work/model.txt') as f: mhdr = next(csv.reader(f, delimiter='\t'))[1:]
with open('/home/sandbox/hmp2_work/mpcomp.txt') as f:
    r = csv.reader(f, delimiter='\t'); chdr_all = next(r)
    grows, rows = [], []
    for row in r: grows.append(row[0]); rows.append([float(x) for x in row[1:]])
chdr = chdr_all[1:]
Yfull = np.array(rows); g2i = {g: i for i, g in enumerate(grows)}
pos = {m: mhdr.index(m) for m in METS}
clusters = {m: chdr[pos[m]] for m in METS}
print('target clusters:', clusters)

# PRISM features
taxa = pyreadr.read_r('ibd_taxa.rda')['ibd_taxa']
meta = pyreadr.read_r('ibd_metadata.rda')['ibd_metadata']
prism_ids = list(taxa.columns)
g_of = dict(zip(meta.index.astype(str), meta['SRA_metagenome_name'].astype(str)))
prism_sp = [norm(s) for s in taxa.index]
Xp_raw = taxa.values.T.astype(np.float64)
keep = [i for i, p in enumerate(prism_ids) if g_of.get(p) in g2i]
assert len(keep) == 155
Xp = Xp_raw[keep]
Yp = np.column_stack([Yfull[[g2i[g_of[prism_ids[i]]] for i in keep], pos[m]] for m in METS])

# HMP2 frozen features + labels
ids = json.load(open('/home/sandbox/hmp2_work/paired_ids.json'))
sp_union = {}
mats = []
for s in ids:
    d = json.load(open(f'tax/{s}.biom'))
    rows_ = [r['id'] for r in d['rows']]
    vec = {}
    for ri, ci, v in d['data']:
        rid = rows_[ri]
        if '|s__' in rid and '|t__' not in rid:
            vec[norm(rid.split('|s__')[1])] = v / 100.0
    mats.append(vec)
    for k in vec: sp_union.setdefault(k, len(sp_union))
hsp = list(sp_union)
Xh = np.zeros((len(ids), len(hsp)))
for i, vec in enumerate(mats):
    for k, v in vec.items(): Xh[i, sp_union[k]] = v
meas = np.load('/home/sandbox/hmp2_work/hmp2_meas.npy')
midx_j = json.load(open('/home/sandbox/hmp2_work/hmp2_meas_index.json'))
mcol = {c: i for i, c in enumerate(midx_j['compounds'])}
ridx = {s: i for i, s in enumerate(midx_j['col_ids'])}
row_sel = [ridx[s] for s in ids]
assert all(m in mcol for m in METS), [m for m in METS if m not in mcol]
Yh = np.column_stack([meas[row_sel, mcol[m]] for m in METS])

# feature matrices per metabolite (producer-constrained), log1p(x*1e6)
# trainable feature universe = producer species present in the PRISM (train) feature
# space; HMP2 restricted to the SAME species (absent = 0 abundance). HMP2-only producers
# are untrainable -> excluded, counted for G4 coverage.
hsp_set = set(hsp) if 'hsp' in dir() else None
def feats(X, sp_list, p):
    idx = [i for i, s in enumerate(sp_list) if s in p]
    return np.log1p(X[:, idx] * 1e6), idx
def feats_aligned(X, sp_list, species):
    pos = {s: i for i, s in enumerate(sp_list)}
    M = np.zeros((X.shape[0], len(species)))
    for j, sp_ in enumerate(species):
        if sp_ in pos: M[:, j] = X[:, pos[sp_]]
    return np.log1p(M * 1e6)
alphas = np.logspace(-3, 3, 13)
kf = KFold(n_splits=5, shuffle=True, random_state=0)
dev_rhos, frz_rhos, drivers, cov = {}, {}, {}, {}
for mi, m in enumerate(METS):
    p = prod[m]
    train_species = [s for s in prism_sp if s in p]
    cov[m] = {'producers': len(p), 'trainable': len(train_species),
              'hmp2_present': len([s for s in train_species if s in set(hsp)])}
    Xp_m, pi = feats(Xp, prism_sp, p)
    Xh_m = feats_aligned(Xh, hsp, [prism_sp[j] for j in pi])
    # dev CV
    r_dev = []
    for tr, te in kf.split(Xp_m):
        if Xp_m.shape[1] == 0: break
        rg = RidgeCV(alphas=alphas).fit(Xp_m[tr], Yp[tr, mi])
        pr = rg.predict(Xp_m[te])
        r_dev.append(spearmanr(Yp[te, mi], pr).statistic if np.std(pr) > 0 else 0.0)
    dev_rhos[m] = float(np.mean(r_dev)) if r_dev else None
    # full fit + frozen
    if Xp_m.shape[1] == 0:
        frz_rhos[m] = None; continue
    rg = RidgeCV(alphas=alphas).fit(Xp_m, Yp[:, mi])
    pr = rg.predict(Xh_m)
    frz_rhos[m] = float(spearmanr(Yh[:, mi], pr).statistic) if np.std(pr) > 0 else 0.0
    order = np.argsort(-np.abs(rg.coef_))[:5]
    drivers[m] = [(prism_sp[pi[j]], float(rg.coef_[j])) for j in order]
    print(f'{m}: producers={len(p)} feats_p={Xp_m.shape[1]} feats_h={Xh_m.shape[1]} dev={dev_rhos[m]:.3f} frozen={frz_rhos[m]:.3f}')

# gates
g1 = float(np.nanmean([v for v in dev_rhos.values() if v is not None]))
armA = json.load(open('/home/sandbox/hmp2_work/armA_frozen_rho.json'))
armB = json.load(open('/home/sandbox/hmp2_work/armB_frozen_rho.json'))
def frac_well(d): 
    vals = [d[m] for m in METS if m in d]
    return sum(1 for v in vals if v >= 0.3) / len(vals), len(vals)
wp_c = sum(1 for m in METS if frz_rhos[m] is not None and frz_rhos[m] >= 0.3) / len(METS)
fA, nA = frac_well(armA); fB, nB = frac_well(armB)
print('\nG1 dev mean rho: %.4f (bar 0.10)' % g1)
print('frozen well-predicted: constrained %.3f (%d/10) | ARM A %.3f (%d compounds found) | ARM B %.3f' % (wp_c, sum(1 for m in METS if frz_rhos[m] and frz_rhos[m]>=0.3), fA, nA, fB))
print('G2 bar: >= %.3f (ARM A+5pp) and >= %.3f (ARM B+5pp)' % (fA + 0.05, fB + 0.05))
print('G3: propionate %.3f (bar 0.3), butyrate %.3f (bar 0.3)' % (frz_rhos['propionate'], frz_rhos['butyrate...isobutytare.']))
out = {'coverage': cov, 'dev_rhos': dev_rhos, 'frozen_rhos': frz_rhos, 'drivers': drivers,
       'g1_dev_mean': g1, 'frozen_well_predicted': wp_c,
       'armA_well': fA, 'armB_well': fB, 'clusters': clusters,
       'armA_rhos_on_10': {m: armA.get(m) for m in METS}, 'armB_rhos_on_10': {m: armB.get(m) for m in METS}}
json.dump(out, open('scores032F.json','w'), indent=1)
print('scores032F.json saved')
