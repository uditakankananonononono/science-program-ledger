#!/usr/bin/env python3
"""spatial_biomarker.py - cholesterol-CD8 spatial exclusion index for one Visium sample (DOC-1-028).
Usage: python3 spatial_biomarker.py --scores scores.npz --k 6
Input npz: chol, cd8 (per-spot log1p signature scores), row, col (array coords).
Output: JSON with exclusion_index (Pearson corr of CHOL vs neighbor-mean CD8) and bivariate Moran's I.
Honest scope: on the GSE284989 MC38 aPD1 cohort this index did NOT achieve locked tumor-level
separation of 6 NR vs 2 R (responders ranked 3rd and 5th of 8, not top-2; failure tree exhausted).
Section-level infiltration heterogeneity within mice is large (CD8 mean 0.04-0.23 across sections
of one responder), so tumor-level response labels carry substantial per-section noise.
"""
import argparse, json, numpy as np
from scipy.spatial import cKDTree
ap=argparse.ArgumentParser(); ap.add_argument('--scores', required=True); ap.add_argument('--k', type=int, default=6)
a=ap.parse_args()
d=np.load(a.scores)
C=np.stack([d['row'],d['col']],1).astype(np.float64)
_,idx=cKDTree(C).query(C,a.k+1)
chol,cd8=d['chol'],d['cd8']
excl=float(np.corrcoef(chol, cd8[idx[:,1:]].mean(1))[0,1])
zc=(chol-chol.mean())/chol.std(); zd=(cd8-cd8.mean())/cd8.std()
moran=float((zc*zd[idx[:,1:]].mean(1)).mean())
print(json.dumps({'exclusion_index':round(excl,4),'bivariate_moran':round(moran,4),'n_spots':int(len(chol))}))
