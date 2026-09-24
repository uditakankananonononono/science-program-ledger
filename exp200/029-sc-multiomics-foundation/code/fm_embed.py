#!/usr/bin/env python3
"""fm_embed.py - embed single-cell RNA data with the pretrained DOC-1-029 encoder (256-dim).
Usage: python3 fm_embed.py --x X.npy --out Z.npy
Input: cells x 2000 float32 .npy, log1p-normalized, genes in the locked HVG order (results/local/hv.npy).
Output: cells x 256 embedding .npy.
Honest scope: the foundation-model protocol LOST to direct ridge regression on the locked benchmark
(probe 0.670 vs ridge 0.727 dev; 0.587 vs 0.644 frozen donor). The embedding recovers coarse PBMC
lineage structure (T/B/monocyte clusters unlabeled) but retains only ~12% of masked-gene variance;
use for visualization/QC, not for quantitative protein prediction - use the ridge baseline for that.
"""
import argparse, numpy as np, torch, torch.nn as nn
torch.set_num_threads(2)
ap=argparse.ArgumentParser(); ap.add_argument('--x', required=True); ap.add_argument('--out', default='Z.npy')
ap.add_argument('--weights', default='results/local/fm_encoder.pt')
a=ap.parse_args()
sd=torch.load(a.weights)
enc=nn.Sequential(nn.Linear(2000,256), nn.ReLU())
enc.load_state_dict({k[4:]:v for k,v in sd.items() if k.startswith('enc.')}); enc.eval()
X=torch.tensor(np.load(a.x).astype(np.float32))
with torch.no_grad(): Z=enc(X).numpy()
np.save(a.out, Z)
print(f'{Z.shape[0]} cells -> {Z.shape[1]}-dim embedding in {a.out}')
