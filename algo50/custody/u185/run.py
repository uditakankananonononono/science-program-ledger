#!/usr/bin/env python3
"""ASEEG unit 185 runner. Stages: counts | feats | dev | perm | test. See PREREG.md. Serial, streams MATs."""
import sys, os, json, glob, hashlib, itertools
import numpy as np
SEED = 185
ROOT = os.environ.get('ASEEG_ROOT', '/tmp/w/data/mats')
XLSX = os.environ.get('ASEEG_XLSX', '/tmp/w/screen/zen18029536-participants info.xlsx')
OUT = os.environ.get('ASEEG_OUT', '/tmp/w/run/out'); os.makedirs(OUT, exist_ok=True)
FS = 128.0  # from publication; NOT stored in files
BANDS = [(1, 4), (4, 8), (8, 13), (13, 30), (30, 45.01)]
CGRID = [0.003, 0.01, 0.03, 0.1, 0.3, 1.0]
WIN_T = 0.03
NB, REPS, NPERM = 2000, 5, 20

def people():
    import openpyxl
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    out = []
    for sh, cls, pre in ((wb['Sheet2'], 'HC', 'n'), (wb['Sheet1'], 'SZ', 'sz')):
        for r in list(sh.iter_rows(values_only=True))[1:]:
            if r[0] is None: continue
            out.append(dict(pid=f'{cls}_{pre}{int(r[0])}', cls=cls, num=int(r[0]), file=f'{pre}{int(r[0])}',
                            sex=str(r[1]).strip().lower()[0], age=int(r[2])))
    out.sort(key=lambda p: (0 if p['cls'] == 'HC' else 1, p['num']))
    for i, p in enumerate(out): p['split'] = 'DEV' if i % 2 == 0 else 'TEST'; p['y'] = int(p['cls'] == 'SZ')
    return out

def matpath(p, cond):
    sub = 'sz' if p['cls'] == 'SZ' else 'normal'
    c = glob.glob(f"{ROOT}/{cond}/*/{p['file']}.mat") + glob.glob(f"{ROOT}/{cond}/{p['file']}.mat")
    c = [x for x in c if (('/sz/' in x) == (p['cls'] == 'SZ'))]
    return c[0] if c else None

def length(path):
    import h5py
    with h5py.File(path, 'r') as h: return int(h['preprocessed_data'].shape[0])

def counts():
    P = people()
    for p in P:
        for c in ('EC', 'EO'):
            mp = matpath(p, c); p[c + '_len'] = length(mp) if mp else None
    def ab(a): return '<20' if a < 20 else '20-29' if a < 30 else '30-39' if a < 40 else '40-49' if a < 50 else '50+'
    from collections import Counter
    res = {}
    for name, sel in (('ALL', P), ('DEV', [p for p in P if p['split'] == 'DEV']), ('TEST', [p for p in P if p['split'] == 'TEST'])):
        res[name] = dict(n=len(sel),
            label_sex=dict(Counter(f"{p['cls']}|{p['sex']}" for p in sel)),
            label_ageband=dict(Counter(f"{p['cls']}|{ab(p['age'])}" for p in sel)),
            label_avail=dict(Counter(f"{p['cls']}|{'EC+EO' if p['EO_len'] else 'EC-only'}" for p in sel)),
            label_length=dict(Counter(f"{p['cls']}|{c}|{'full38400' if p[c+'_len']==38400 else 'short' if p[c+'_len'] else 'absent'}" for p in sel for c in ('EC', 'EO'))))
    json.dump(dict(counts=res, people=P), open(f'{OUT}/counts.json', 'w'), indent=1, sort_keys=True)
    print(json.dumps(res, indent=1, sort_keys=True))

def feat_one(path):
    import h5py
    from scipy.signal import stft
    with h5py.File(path, 'r') as h: x = h['preprocessed_data'][:].astype(np.float64)
    f, _, Z = stft(x.T, fs=FS, nperseg=256, noverlap=128, window='hann', detrend='constant', boundary=None, padded=False)
    P = (np.abs(Z) ** 2)
    tot = P[:, (f >= 1) & (f <= 45), :].mean(2).sum(1)
    ab, rel, coh = [], [], []
    iu = np.triu_indices(19, 1)
    for lo, hi in BANDS:
        m = (f >= lo) & (f < hi)
        bp = P[:, m, :].mean(2).sum(1)
        ab.append(np.log10(bp)); rel.append(bp / tot)
        Zb = Z[:, m, :]
        S = np.einsum('cfs,dfs->cdf', Zb, Zb.conj()) / Zb.shape[2]
        d = np.real(np.einsum('ccf->cf', S))
        C = (np.abs(S) ** 2) / (d[:, None, :] * d[None, :, :])
        coh.append(C.mean(2)[iu])
    return dict(ABS=np.concatenate(ab), REL=np.concatenate(rel), COH=np.concatenate(coh), n=x.shape[0])

def feats(split):
    P = [p for p in people() if split == 'ALL' or p['split'] == split]
    for p in P:
        fn = f"{OUT}/feat_{p['pid']}.npz"
        if os.path.exists(fn): continue
        d = {}
        for c in ('EC', 'EO'):
            mp = matpath(p, c)
            if mp:
                r = feat_one(mp)
                for k in ('ABS', 'REL', 'COH', 'n'): d[f'{c}_{k}'] = r[k]
        np.savez(fn, **d)
    print('feats done', split, len(P))

def load(split):
    P = [p for p in people() if p['split'] == split]
    for p in P:
        z = np.load(f"{OUT}/feat_{p['pid']}.npz"); p['f'] = {k: z[k] for k in z.files}
        p['ec_len'] = int(p['f']['EC_n']); p['eo_len'] = int(p['f']['EO_n']) if 'EO_n' in p['f'] else p['ec_len']
        p['has_eo'] = 'EO_n' in p['f']
    return P

def X_of(P, member, cond='EC'):
    kind = member.split(':')[0]
    if kind == 'DEMO':
        return np.array([[1.0 if p['sex'] == 'm' else 0.0, p['age'], p['ec_len'], p['eo_len']] for p in P], float)
    rows = []
    for p in P:
        f = p['f']; g = lambda k: f[f'{cond}_{k}']
        if kind == 'ABS': rows.append(g('ABS'))
        elif kind == 'REL': rows.append(np.log10(g('REL')))
        elif kind == 'ABSREL': rows.append(np.concatenate([g('ABS'), np.log10(g('REL'))]))
        elif kind == 'LOCAL': rows.append(np.concatenate([np.log10(g('REL')), np.arctanh(np.clip(g('COH'), 0, 0.999999) ** 0.5)]))
    return np.array(rows, float)

BASE = ['ABS', 'REL', 'ABSREL']
GRID = [f'DEMO:{c}' for c in CGRID] + [f'{b}:{c}' for b in BASE for c in CGRID] + [f'LOCAL:{c}' for c in CGRID]

def model(c):
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    return make_pipeline(StandardScaler(), LogisticRegression(C=c, class_weight='balanced', max_iter=3000))

def fitpred(Xtr, ytr, Xte, c):
    m = model(c).fit(Xtr, ytr); return m.decision_function(Xte)

def auc(y, s):
    from sklearn.metrics import roc_auc_score
    return float(roc_auc_score(y, s)) if len(set(y)) == 2 else float('nan')

def cv_oof(X, y, c, reps=REPS, seed=SEED):
    from sklearn.model_selection import StratifiedKFold
    oof = np.zeros((reps, len(y)))
    for r in range(reps):
        for tr, te in StratifiedKFold(5, shuffle=True, random_state=seed + r).split(X, y):
            oof[r, te] = fitpred(X[tr], y[tr], X[te], c)
    return oof

def boot_idx(y, strata, rng):
    idx = []
    for s in sorted(set(strata)):
        ii = np.where(strata == s)[0]; idx.append(rng.choice(ii, len(ii), replace=True))
    return np.concatenate(idx)

def match_age(P, caliper=5):
    """within-sex greedy 1:1 nearest-age matching of the minority class to the other class; deterministic."""
    keep = []
    for sx in ('m', 'f'):
        a = [i for i, p in enumerate(P) if p['sex'] == sx and p['y'] == 1]
        b = [i for i, p in enumerate(P) if p['sex'] == sx and p['y'] == 0]
        small, big = (a, b) if len(a) <= len(b) else (b, a)
        used = set()
        for i in sorted(small, key=lambda i: P[i]['pid']):
            cands = [j for j in big if j not in used and abs(P[j]['age'] - P[i]['age']) <= caliper]
            if cands:
                j = min(cands, key=lambda j: (abs(P[j]['age'] - P[i]['age']), P[j]['pid'])); used.add(j); keep += [i, j]
    return np.array(sorted(keep), int)

def strat_stats(P, y, S):
    """S: dict name->score array. returns dict of stats (full, sexstrat mean, agematched)."""
    sex = np.array([p['sex'] for p in P]); out = {}
    am = match_age(P)
    for k, s in S.items():
        a_m, a_f = auc(y[sex == 'm'], s[sex == 'm']), auc(y[sex == 'f'], s[sex == 'f'])
        out[k] = dict(auc=auc(y, s), auc_male=a_m, auc_female=a_f, sexstrat=float(np.nanmean([a_m, a_f])),
                      agematched=auc(y[am], s[am]) if len(am) else float('nan'), n_matched=int(len(am)))
    return out

def boot_all(P, y, S, extra=None, nb=NB, seed=SEED):
    """subject bootstrap stratified by class x sex; returns percentile CIs for each stat and paired diffs."""
    rng = np.random.default_rng(seed); sexa = np.array([p['sex'] for p in P])
    strata = np.array([f"{a}{b}" for a, b in zip(y, sexa)])
    keys = list(S); store = {k: [] for k in keys}; diffs = {}
    pairs = extra or []
    for a, b in pairs: diffs[f'{a}-{b}'] = []
    for _ in range(nb):
        ii = boot_idx(y, strata, rng); Pb = [P[i] for i in ii]; yb = y[ii]
        st = strat_stats(Pb, yb, {k: S[k][ii] for k in keys})
        for k in keys: store[k].append((st[k]['auc'], st[k]['sexstrat'], st[k]['agematched']))
        for a, b in pairs: diffs[f'{a}-{b}'].append(st[a]['auc'] - st[b]['auc'])
    ci = lambda v: [float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))]
    res = {k: dict(auc_ci=ci([r[0] for r in store[k]]), sexstrat_ci=ci([r[1] for r in store[k]]), agematched_ci=ci([r[2] for r in store[k]])) for k in keys}
    return res, {k: ci(v) for k, v in diffs.items()}

def dev_stage():
    D = load('DEV'); y = np.array([p['y'] for p in D]); out = {}; oofs = {}
    for m in GRID:
        X = X_of(D, m); c = float(m.split(':')[1]); o = cv_oof(X, y, c); oofs[m] = o.mean(0)
        out[m] = dict(cv_auc=float(np.mean([auc(y, r) for r in o])), cv_auc_avgoof=auc(y, o.mean(0)))
    sel = lambda kinds: max([m for m in GRID if m.split(':')[0] in kinds], key=lambda m: out[m]['cv_auc'])
    B1, LOC, DEM = sel(BASE), sel(['LOCAL']), sel(['DEMO'])
    strongest = max([B1, DEM], key=lambda m: out[m]['cv_auc'])
    S = {'DEMO': oofs[DEM], 'B1': oofs[B1], 'LOCAL': oofs[LOC]}
    ci, dci = boot_all(D, y, S, [('LOCAL', 'B1'), ('LOCAL', 'DEMO'), ('B1', 'DEMO')], nb=1000)
    best = out[strongest]['cv_auc']
    gate = dict(strongest_baseline=strongest, strongest_cv_auc=best, headroom=1 - best,
                headroom_gt_2xWIN=bool(1 - best > 2 * WIN_T),
                skill=bool(best >= 0.60 and ci['B1' if strongest == B1 else 'DEMO']['auc_ci'][0] > 0.5))
    gate['PASS'] = bool(gate['headroom_gt_2xWIN'] and gate['skill'])
    res = dict(grid=out, selected=dict(B1=B1, LOCAL=LOC, DEMO=DEM), gate=gate, dev_ci=ci, dev_diff_ci=dci,
               dev_strat=strat_stats(D, y, S), n_dev=len(D))
    json.dump(res, open(f'{OUT}/dev_result.json', 'w'), indent=1)
    json.dump([dict(pid=p['pid'], cls=p['cls'], sex=p['sex'], age=p['age'], split='DEV', DEMO=float(S['DEMO'][i]), B1=float(S['B1'][i]), LOCAL=float(S['LOCAL'][i])) for i, p in enumerate(D)], open(f'{OUT}/per_subject_dev_oof.json', 'w'), indent=1)
    print(json.dumps(res, indent=1))

def perm_stage():
    D, T = load('DEV'), load('TEST'); yd = np.array([p['y'] for p in D]); yt = np.array([p['y'] for p in T])
    Xd = {m: X_of(D, m) for m in GRID}; Xt = {m: X_of(T, m) for m in GRID}
    rows = {m: dict(dev=[], test=[]) for m in GRID}; gains = []
    for k in range(NPERM):
        rng = np.random.default_rng(SEED * 100 + k)
        yd2, yt2 = rng.permutation(yd), rng.permutation(yt)
        for m in GRID:
            c = float(m.split(':')[1]); o = cv_oof(Xd[m], yd2, c, reps=1, seed=SEED + k)[0]
            rows[m]['dev'].append(auc(yd2, o)); rows[m]['test'].append(auc(yt2, fitpred(Xd[m], yd2, Xt[m], c)))
        b1 = max([m for m in GRID if m.split(':')[0] in BASE], key=lambda m: np.mean(rows[m]['dev'][-1:]))
        lo = max([m for m in GRID if m.startswith('LOCAL')], key=lambda m: rows[m]['dev'][-1])
        gains.append(rows[lo]['test'][-1] - rows[b1]['test'][-1])
    summ = {m: dict(dev_mean=float(np.mean(v['dev'])), dev_min=float(np.min(v['dev'])), dev_max=float(np.max(v['dev'])),
                    test_mean=float(np.mean(v['test'])), test_min=float(np.min(v['test'])), test_max=float(np.max(v['test']))) for m, v in rows.items()}
    ok = all(0.40 <= s['dev_mean'] <= 0.60 and 0.45 <= s['test_mean'] <= 0.55 for s in summ.values())
    res = dict(n_perm=NPERM, members=summ, perm_gain_mean=float(np.mean(gains)), perm_gain_sd=float(np.std(gains, ddof=1)),
               gate_rule='every grid member: DEV-CV mean in [0.40,0.60] and TEST mean in [0.45,0.55] over shuffles', PASS=bool(ok))
    json.dump(res, open(f'{OUT}/perm_result.json', 'w'), indent=1); print(json.dumps(res, indent=1))

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def test_stage():
    here = os.path.dirname(os.path.abspath(__file__))
    lock = json.load(open(f'{here}/LOCK.json'))
    assert sha(f'{here}/run.py') == lock['run.py'] and sha(f'{here}/PREREG.md') == lock['PREREG.md'], 'LOCK mismatch'
    dev = json.load(open(f'{OUT}/dev_result.json')); sel = dev['selected']
    assert dev['gate']['PASS'], 'headroom gate failed'
    D, T = load('DEV'), load('TEST'); yd = np.array([p['y'] for p in D]); yt = np.array([p['y'] for p in T])
    S, cfg = {}, {'DEMO': sel['DEMO'], 'B1': sel['B1'], 'LOCAL': sel['LOCAL']}
    for k, m in cfg.items():
        S[k] = fitpred(X_of(D, m), yd, X_of(T, m), float(m.split(':')[1]))
    # residualised LOCAL: remove sex, age, lengths (fit on DEV features only)
    def cov(P): return np.array([[p['sex'] == 'm', p['age'], p['ec_len'], p['eo_len']] for p in P], float)
    from sklearn.linear_model import LinearRegression
    Xd, Xt = X_of(D, cfg['LOCAL']), X_of(T, cfg['LOCAL']); cd, ct = cov(D), cov(T)
    lr = LinearRegression().fit(cd, Xd); Rd, Rt = Xd - lr.predict(cd), Xt - lr.predict(ct)
    S['LOCAL_RESID'] = fitpred(Rd, yd, Rt, float(cfg['LOCAL'].split(':')[1]))
    # EO descriptive: same configs on EO features, persons with EO
    de, te = [i for i, p in enumerate(D) if p['has_eo']], [i for i, p in enumerate(T) if p['has_eo']]
    eo = {}
    for k in ('B1', 'LOCAL'):
        m = cfg[k]; Xa, Xb = X_of([D[i] for i in de], m, 'EO'), X_of([T[i] for i in te], m, 'EO')
        eo[k] = auc(yt[te], fitpred(Xa, yd[de], Xb, float(m.split(':')[1])))
    st = strat_stats(T, yt, S)
    pairs = [('LOCAL', 'B1'), ('LOCAL', 'DEMO'), ('B1', 'DEMO'), ('LOCAL_RESID', 'DEMO')]
    ci, dci = boot_all(T, yt, S, pairs)
    gain = st['LOCAL']['auc'] - st['B1']['auc']; gd = st['LOCAL']['auc'] - st['DEMO']['auc']
    c1, c2 = dci['LOCAL-B1'], dci['LOCAL-DEMO']
    robust = dict(sexstrat_ci_low_gt_half=bool(ci['LOCAL']['sexstrat_ci'][0] > 0.5), agematched_ci_low_gt_half=bool(ci['LOCAL']['agematched_ci'][0] > 0.5),
                  resid_auc_ci_low_gt_half=bool(ci['LOCAL_RESID']['auc_ci'][0] > 0.5))
    gainwin = gain >= WIN_T and c1[0] > 0 and gd >= WIN_T and c2[0] > 0
    if gainwin and all(robust.values()): verdict = 'WIN'
    elif gainwin: verdict = 'CONFOUND-FAIL (raw gain gates met, confound-robustness not met; not a WIN)'
    elif c1[1] < 0: verdict = 'NEGATIVE'
    else: verdict = 'NULL'
    # EC model in EO-available subset (availability strata)
    sub = np.array([p['has_eo'] for p in T]); avail = {k: auc(yt[sub], S[k][sub]) for k in S}
    avail['n_ec_only_test'] = int((~sub).sum()); avail['ec_only_mean_score'] = {k: float(S[k][~sub].mean()) if (~sub).any() else None for k in S}
    res = dict(selected=cfg, test_n=len(T), n_sz=int(yt.sum()), strat=st, ci=ci, diff_ci=dci, gain_LOCAL_minus_B1=gain, gain_LOCAL_minus_DEMO=gd,
               robustness=robust, verdict=verdict, auc_in_EO_available_subset=avail, eo_model_descriptive_auc=eo, perm=False)
    json.dump(res, open(f'{OUT}/result.json', 'w'), indent=1)
    rows = [dict(pid=p['pid'], cls=p['cls'], sex=p['sex'], age=p['age'], split='TEST', has_eo=p['has_eo'], ec_len=p['ec_len'], eo_len=p['eo_len'],
                 **{k: float(S[k][i]) for k in S}) for i, p in enumerate(T)]
    json.dump(rows, open(f'{OUT}/per_subject_test.json', 'w'), indent=1)
    print(json.dumps(res, indent=1))

if __name__ == '__main__':
    st = sys.argv[1]
    {'counts': counts, 'dev': dev_stage, 'perm': perm_stage, 'test': test_stage}.get(st, lambda: feats(sys.argv[2]))()
