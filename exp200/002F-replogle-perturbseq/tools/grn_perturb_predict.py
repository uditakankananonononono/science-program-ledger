#!/usr/bin/env python3
"""grn_perturb_predict.py - DOC-1-002F: streaming Replogle K562-essential Perturb-seq pipeline.
Stages: pass1 (library sizes + control moments, gene-set selection), pass2 (sampled-row
collection), score (G1 effect-presence vs n-vs-full-reference null; G2 on-target repression).
RAM-safe on 1.9GB (5k-row blocks against chunked-gzip dense X). Usage: python3 grn_perturb_predict.py [pass1|pass2|score]
NOTE (locked 2026-09-24): G1 1088/1299 pass (repair CONFIRMED - 002 boundary was power/null),
G2 1141/1164 repressed; G3 network-from-controls does NOT beat the shared-program baseline
(median r 0.317 vs 0.621) - see REPORT.md."""
import h5py, numpy as np, json, sys, time
rng = np.random.default_rng(20260924)
t0 = time.time()
f = h5py.File('essential.h5ad', 'r')
X = f['X']; n_cells, n_genes = X.shape
pcats = [c.decode() if isinstance(c, bytes) else str(c) for c in f['obs']['perturbation']['categories'][:]]
pcode = f['obs']['perturbation']['codes'][:]
ctrl_code = pcats.index('control')
cidx = np.where(pcode == ctrl_code)[0]
assert len(cidx) == 10691
genes = np.array([g.decode() if isinstance(g, bytes) else str(g) for g in f['var']['gene_name'][:]])
tcnt = {}
for c in pcode:
    if c != ctrl_code: tcnt[c] = tcnt.get(c, 0) + 1
g1pool = sorted(c for c, n in tcnt.items() if n >= 100)
assert len(g1pool) == 1299, len(g1pool)
stage = sys.argv[1]

if stage == 'pass1':
    lib = np.zeros(n_cells, dtype=np.float64)
    csum = np.zeros(n_genes); csq = np.zeros(n_genes)
    for s in range(0, n_cells, 5000):
        e = min(s + 5000, n_cells)
        Bp = X[s:e].astype(np.float64)
        lib[s:e] = Bp.sum(1)
        m = np.isin(np.arange(s, e), cidx)
        if m.any():
            csum += Bp[m].sum(0); csq += (Bp[m] ** 2).sum(0)
        del Bp
        if s % 50000 == 0: print(f'pass1 {s}/{n_cells} {time.time()-t0:.0f}s', flush=True)
    np.savez('pass1.npz', lib=lib, csum=csum, csq=csq)
    mu = csum / len(cidx); var = csq / len(cidx) - mu ** 2
    top500 = set(np.argsort(var)[-500:].tolist())
    tnames = {pcats[c] for c in g1pool}
    tset = {i for i, g in enumerate(genes) if g in tnames}
    S = sorted(top500 | tset)
    json.dump({'S': S, 'n_in_S_targets': len(tset)}, open('selS.json', 'w'))
    print('S size:', len(S), 'target genes in matrix:', len(tset), flush=True)

elif stage == 'pass2':
    S = np.array(json.load(open('selS.json'))['S'])
    p1 = np.load('pass1.npz'); lib = p1['lib']
    # seeded per-target 100-cell samples
    tidx = {}
    for i, c in enumerate(pcode):
        if c != ctrl_code and c in set(g1pool): tidx.setdefault(c, []).append(i)
    sampled = {}
    for c in g1pool:
        idx = np.array(tidx[c])
        sampled[c] = rng.choice(idx, 100, replace=False)
    row2t = {}
    for c, rows in sampled.items():
        for r in rows: row2t[int(r)] = c
    sample_rows = np.array(sorted(row2t))
    Nc = np.zeros((len(cidx), len(S)), dtype=np.float32)
    Nt = np.zeros((len(sample_rows), len(S)), dtype=np.float32)
    cpos = {int(r): i for i, r in enumerate(cidx)}
    spos = {int(r): i for i, r in enumerate(sample_rows)}
    for s in range(0, n_cells, 5000):
        e = min(s + 5000, n_cells)
        Bp = X[s:e][:, S].astype(np.float32)
        l = lib[s:e].copy(); l[l == 0] = 1
        Nb = np.log1p(Bp * (1e4 / l[:, None])).astype(np.float32)
        for j, r in enumerate(range(s, e)):
            if r in cpos: Nc[cpos[r]] = Nb[j]
            elif r in spos: Nt[spos[r]] = Nb[j]
        del Bp, Nb
        if s % 50000 == 0: print(f'pass2 {s}/{n_cells} {time.time()-t0:.0f}s', flush=True)
    np.savez('pass2.npz', Nc=Nc, Nt=Nt, sample_rows=sample_rows,
             sample_t=np.array([row2t[int(r)] for r in sample_rows]))
    print('pass2 done', Nc.shape, Nt.shape, flush=True)

elif stage == 'score':
    S = json.load(open('selS.json'))['S']
    d = np.load('pass2.npz')
    Nc, Nt, sample_t = d['Nc'], d['Nt'], d['sample_t']
    nc = Nc.shape[0]
    cmean = Nc.mean(0)
    ctotal = Nc.sum(0)
    g1_names = [pcats[c] for c in g1pool]
    # null: 200 draws of 100 control rows vs rest
    nullss = np.zeros(200)
    nulld = np.zeros((200, Nc.shape[1]))
    for k in range(200):
        dr = rng.choice(nc, 100, replace=False)
        m = np.zeros(nc, bool); m[dr] = True
        dsum = Nc[m].sum(0); rmean = (ctotal - dsum) / (nc - 100)
        dk = dsum / 100 - rmean
        nullss[k] = (dk ** 2).sum(); nulld[k] = dk
    q95 = float(np.quantile(nullss, 0.95))
    res = []
    for ci, c in enumerate(g1pool):
        sub = Nt[sample_t == c]
        de = sub.mean(0) - cmean
        ss = float((de ** 2).sum())
        res.append({'target': pcats[c], 'ss': ss, 'pass': ss > q95})
        np.save(f'de_{c}.npy', de)
    npass = sum(r['pass'] for r in res)
    json.dump({'q95': q95, 'n_pass': npass, 'n_pool': len(res), 'per_target': res},
              open('g1_results.json', 'w'))
    print(f'G1: {npass}/{len(res)} pass (bar 650); q95={q95:.4f}', flush=True)
    # G2
    gidx = {g: i for i, g in enumerate(genes[S])}
    g2pass = 0; g2n = 0; g2rows = []
    q05 = np.quantile(nulld, 0.05, axis=0)
    for c in g1pool:
        t = pcats[c]
        if t not in gidx: continue
        j = gidx[t]
        sub = Nt[sample_t == c]
        dt = float(sub[:, j].mean() - cmean[j])
        rep = dt < q05[j]
        g2n += 1; g2pass += int(rep)
        g2rows.append({'target': t, 'd': dt, 'q05': float(q05[j]), 'repressed': bool(rep)})
    json.dump({'n': g2n, 'n_repressed': g2pass, 'per_target': g2rows}, open('g2_results.json', 'w'))
    print(f'G2: {g2pass}/{g2n} repressed (bar 698)', flush=True)
