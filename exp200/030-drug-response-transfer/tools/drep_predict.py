#!/usr/bin/env python3
"""drep_predict.py - DOC-1-030: bulk-to-single-cell drug response transfer predictor.
Trains a ridge model on CCLE bulk expression (CSA benchmark, GDSCv2 AUC labels) and
predicts per-line and per-cell drug sensitivity from single-cell data.
Usage:
  python3 drep_predict.py --drug {lapatinib,afatinib} --bulk-expr bulk_expr.npz \
      --sc-sparse xcell_sparse.npz --line-of line_of.npy --lines LINES_JSON --out out.json
Outputs per-line predicted AUC (LODO) and predicted-sensitive cell fraction.
NOTE (locked boundary, 2026-09-24): on the 32-line breast atlas this model UNDERPERFORMS
the published ERBB2+EGFR biomarker (rho 0.21 vs 0.42 lapatinib). Provided for reproducibility
and negative-result inspection, not for prospective use - see REPORT.md."""
import argparse, json, numpy as np
from scipy.sparse import load_npz
from sklearn.linear_model import RidgeCV
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--drug',required=True,choices=['lapatinib','afatinib'])
    ap.add_argument('--bulk-expr',required=True); ap.add_argument('--sc-sparse',required=True)
    ap.add_argument('--line-of',required=True); ap.add_argument('--lines',required=True)
    ap.add_argument('--out',required=True)
    a=ap.parse_args()
    bulk=np.load(a.bulk_expr,allow_pickle=True)
    hvg=json.load(open(a.lines))['hvg']
    bidx={str(g):i for i,g in enumerate(bulk['genes'])}
    bsel=np.array([bidx[g] for g in hvg])
    Xb=np.log1p(bulk['X'].astype(np.float64))[:,bsel]
    auc=bulk['lap_auc' if a.drug=='lapatinib' else 'afa_auc'].astype(np.float64)
    tr=np.where(~np.isnan(auc))[0]
    mdl=RidgeCV(alphas=np.logspace(-2,3,20)).fit(Xb[tr],auc[tr])
    M=load_npz(a.sc_sparse).tocsr(); line_of=np.load(a.line_of)
    grid=np.linspace(0,1,20); qb=np.quantile(Xb[tr],grid,axis=0)
    thr=float(np.median(auc[tr])); out={}
    for li in sorted(set(line_of.tolist())):
        cells=np.where(line_of==li)[0]
        Xc=M[cells].toarray().astype(np.float64)
        for j in range(Xc.shape[1]):
            Xc[:,j]=np.interp(Xc[:,j],np.quantile(Xc[:,j],grid),qb[:,j])
        pred=mdl.predict(Xc)
        out[str(li)]={'pred_auc_mean':float(pred.mean()),'frac_sensitive':float((pred<thr).mean()),'n_cells':int(len(cells))}
    json.dump(out,open(a.out,'w'),indent=1)
    print(json.dumps({k:out[k] for k in list(out)[:3]},indent=1))
if __name__=='__main__': main()
