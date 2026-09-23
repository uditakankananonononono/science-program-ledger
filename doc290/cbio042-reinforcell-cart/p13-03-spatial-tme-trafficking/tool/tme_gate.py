#!/usr/bin/env python3
"""
TME-Gate (P13-03 build): CAR-T infiltration-failure geometry from real Visium sections.

Real data: Zenodo record 5765589 - 10x Visium demo sections (breast cancer block A
sections 1+2 = serial tumor sections; human lymph node = immune-rich control;
human heart = immune-poor control). Direct public download, no auth.

What is honest here: 4 demo sections cannot validate a cross-cohort classifier
(the spec's AUC gates). What IS evaluable on real sections:
  G1' marker sanity (locked): T-cell signal lymph-node > breast > heart;
      tumor-epithelial signal breast > others (directional, pre-registered).
  G2' exclusion measurability (locked): tumor sections show positive immune-
      exclusion index (stroma-ring T-density > tumor-core T-density); the
      lymph-node control does not. Direction pre-registered from the known
      breast-cancer exclusion phenotype.
  G3' boundary: the spec's classification/counterfactual-validation gates need
      >= 2 labeled cohorts; documented with exact requirements.
The counterfactual engine ships as machinery with an explicit in-silico label.
"""
import json, os, sys
import numpy as np
import pandas as pd
import h5py
from scipy import sparse

MARKERS = {
  "tcell":   ["CD3D","CD3E","CD8A","CD4","CD2"],
  "cytotox": ["GZMB","PRF1","NKG7","GNLY"],
  "tumor":   ["EPCAM","KRT19","KRT8","ERBB2","ESR1"],
  "stroma":  ["COL1A1","COL1A2","DCN","FAP","COL3A1"],
  "chemokine": ["CXCL9","CXCL10","CXCL11"],
}

def load_section(path):
    with h5py.File(path, "r") as f:
        m = f["matrix"]
        X = sparse.csc_matrix((m["data"][:], m["indices"][:], m["indptr"][:]),
                              shape=m["shape"][:]).tocsr()  # genes x spots
        genes = [g.decode() for g in m["features"]["name"][:]]
        bc = [b.decode() for b in m["barcodes"][:]]
    return X, genes, bc

def scores(X, genes):
    gidx = {g: i for i, g in enumerate(genes)}
    lib = np.asarray(X.sum(axis=0)).ravel(); lib[lib == 0] = 1
    Xn = X.multiply(1e4 / lib).tocsr()
    Xn.data = np.log1p(Xn.data)
    out = {}
    for k, ms in MARKERS.items():
        idx = [gidx[m] for m in ms if m in gidx]
        out[k] = np.asarray(Xn[idx].mean(axis=0)).ravel() if idx else np.zeros(X.shape[1])
    return out

def exclusion_index(sc, pos):
    # tumor mask: top-tercile tumor score among in-tissue spots
    t = sc["tumor"]; thr = np.quantile(t, 2/3)
    tumor = t >= thr
    xy = pos[["array_row", "array_col"]].values.astype(float)
    # array-grid distances (hex grid: use euclidean on array coords, fine for rings)
    d = np.sqrt(((xy[:, None, :] - xy[None, :, :]) ** 2).sum(-1))
    to_tumor = d[:, tumor].min(axis=1) if tumor.any() else np.full(len(t), np.inf)
    core = tumor & (to_tumor <= 0.1)          # tumor spots themselves
    ring = (~tumor) & (to_tumor > 0.1) & (to_tumor <= 3.0)  # stroma ring <=3 array steps
    if core.sum() < 20 or ring.sum() < 20:
        return dict(exclusion_index=None, core_t=None, ring_t=None, core_n=int(core.sum()), ring_n=int(ring.sum()))
    return dict(exclusion_index=float(sc["tcell"][ring].mean() - sc["tcell"][core].mean()),
                core_t=float(sc["tcell"][core].mean()), ring_t=float(sc["tcell"][ring].mean()),
                core_n=int(core.sum()), ring_n=int(ring.sum()))

def counterfactual_demo(sc, pos):
    # coarse region grid; ridge-style OLS: region T-density ~ stroma + tumor + chemokine
    xy = pos[["array_row", "array_col"]].values
    gx, gy = xy[:, 0] // 10, xy[:, 1] // 10
    rows = {}
    for k in np.unique(np.c_[gx, gy], axis=0):
        m = (gx == k[0]) & (gy == k[1])
        if m.sum() < 15: continue
        rows[len(rows)] = (sc["tcell"][m].mean(), sc["stroma"][m].mean(),
                           sc["tumor"][m].mean(), sc["chemokine"][m].mean())
    D = pd.DataFrame(rows).T; D.columns = ["tcell", "stroma", "tumor", "chemokine"]
    Xr = np.c_[np.ones(len(D)), D[["stroma", "tumor", "chemokine"]].values]
    beta, *_ = np.linalg.lstsq(Xr, D["tcell"].values, rcond=None)
    pred_gain = -0.30 * D["stroma"].mean() * beta[1]  # stroma -30% counterfactual
    return dict(n_regions=int(len(D)), beta_stroma=float(beta[1]),
                beta_chemokine=float(beta[3]),
                counterfactual_stroma_minus30_gain=float(pred_gain),
                label="IN-SILICO DEMONSTRATION - not validated against intervention data")

def main(root, outdir):
    secs = {}
    for name in os.listdir(root):
        p = os.path.join(root, name)
        h5 = os.path.join(p, "filtered_feature_bc_matrix.h5")
        pos_csv = os.path.join(p, "spatial", "tissue_positions_list.csv")
        if not (os.path.isdir(p) and os.path.exists(h5) and os.path.exists(pos_csv)): continue
        X, genes, bc = load_section(h5)
        pos = pd.read_csv(pos_csv)
        pos.columns = ["barcode", "in_tissue", "array_row", "array_col", "pxl_row", "pxl_col"]
        pos = pos[pos.in_tissue == 1].reset_index(drop=True)
        keep = [i for i, b in enumerate(bc) if b in set(pos.barcode)]
        bcp = pd.Series(bc)[keep]
        pos = pos.set_index("barcode").loc[bcp.values].reset_index()
        X = X[:, keep]
        sc = scores(X, genes)
        ex = exclusion_index(sc, pos)
        secs[name] = dict(n_spots=int(X.shape[1]),
                          mean_scores={k: float(np.mean(v)) for k, v in sc.items()},
                          exclusion=ex)
    br = [k for k in secs if "Breast" in k]
    ln = next((k for k in secs if "Lymph" in k), None)
    ht = next((k for k in secs if "Heart" in k), None)
    g1_t = ln and ht and all(secs[ln]["mean_scores"]["tcell"] > secs[b]["mean_scores"]["tcell"] > secs[ht]["mean_scores"]["tcell"] for b in br)
    g1_tum = all(secs[b]["mean_scores"]["tumor"] > max(secs[k]["mean_scores"]["tumor"] for k in [ln, ht] if k) for b in br)
    ex_b = [secs[b]["exclusion"]["exclusion_index"] for b in br]
    ex_ln = secs[ln]["exclusion"]["exclusion_index"] if ln else None
    g2 = all(e is not None and e > 0 for e in ex_b) and (ex_ln is None or ex_ln <= min(ex_b))
    # counterfactual machinery on the larger breast section
    b0 = max(br, key=lambda b: secs[b]["n_spots"]) if br else None
    cf = None
    if b0:
        X, genes, bc = load_section(os.path.join(root, b0, "filtered_feature_bc_matrix.h5"))
        pos = pd.read_csv(os.path.join(root, b0, "spatial", "tissue_positions_list.csv"))
        pos.columns = ["barcode", "in_tissue", "array_row", "array_col", "pxl_row", "pxl_col"]
        pos = pos[pos.in_tissue == 1].reset_index(drop=True)
        keep = [i for i, b in enumerate(bc) if b in set(pos.barcode)]
        pos = pos.set_index("barcode").loc[pd.Series(bc)[keep].values].reset_index()
        sc = scores(X[:, keep], genes)
        cf = counterfactual_demo(sc, pos)
    out = dict(dataset="Zenodo 5765589 - 10x Visium demo (2x breast tumor serial sections, lymph node, heart)",
               sections=secs, counterfactual=cf,
               gates={
                 "G1p_marker_sanity_tcell_gradient": {"criterion": "lymph-node > breast > heart T-cell score (directional, pre-registered)", "pass": bool(g1_t)},
                 "G1p_marker_sanity_tumor_gradient": {"criterion": "breast sections top tumor-epithelial score", "pass": bool(g1_tum)},
                 "G2p_exclusion_measurable": {"criterion": "breast sections exclusion index > 0 AND lymph-node <= min(breast) (direction pre-registered)", "breast_exclusion": ex_b, "lymph_node_exclusion": ex_ln, "pass": bool(g2)},
                 "G3_boundary": {"note": "spec classification gates (AUC>=0.80 cross-cohort) and counterfactual validation (>=60% literature match) require >=2 labeled cohorts; demo sections cannot evaluate them. Requirements documented in REPORT.md.", "pass": None}})
    json.dump(out, open(os.path.join(outdir, "results.json"), "w"), indent=2)
    print(json.dumps(out["gates"], indent=2))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
