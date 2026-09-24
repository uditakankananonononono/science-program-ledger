#!/usr/bin/env python3
"""spot_deconv.py - NNLS spatial deconvolution (winning arm of DOC-1-027 benchmark).
Usage: python3 spot_deconv.py --spots spots.csv --signature sig.csv --out pred.csv
--spots: spots x genes CSV (first col spot id), log1p-normalized expression.
--signature: celltypes x genes CSV (first col cell type), same gene columns, same normalization.
Output: pred.csv - spots x celltypes proportion estimates (rows sum to 1).
Honest scope: validated on simulated Visium-like mixtures from Tabula Muris FACS Lung
(mean per-type Pearson 0.686 dev / 0.727 frozen vs ground truth). A GNN with mean-aggregation
message passing was tested and REMOVED: smoothing regresses spots toward regional means and
destroyed per-spot compositional signal (-0.34 mean r vs an MLP without the graph). Supervised
fits also transferred worse than this mechanistic NNLS across a mixture-regime shift.
"""
import argparse, numpy as np, pandas as pd
from scipy.optimize import nnls
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--spots', required=True); ap.add_argument('--signature', required=True)
    ap.add_argument('--out', default='deconv_pred.csv')
    a=ap.parse_args()
    S=pd.read_csv(a.spots, index_col=0); G=pd.read_csv(a.signature, index_col=0)
    common=[c for c in S.columns if c in G.columns]
    S=S[common].values.astype(np.float64); G=G.loc[:, common].values.astype(np.float64)
    pred=np.zeros((len(S), len(G)))
    for i in range(len(S)):
        w,_=nnls(G.T, S[i]); s=w.sum()
        pred[i]= w/s if s>0 else np.full(len(G), 1.0/len(G))
    pd.DataFrame(pred, columns=pd.read_csv(a.signature, index_col=0).index,
                 index=pd.read_csv(a.spots, index_col=0).index).to_csv(a.out)
    print(f'{len(S)} spots x {len(G)} cell types -> {a.out}')
if __name__=='__main__': main()
