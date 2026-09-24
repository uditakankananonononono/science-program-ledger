#!/usr/bin/env python3
"""trajectory_ot.py - developmental trajectory reconstruction (winning arm: scVelo velocity graph).
Usage: python3 trajectory_ot.py --h5ad input.h5ad --label-column clusters [--canonical-edges edges.json]
Input: h5ad with spliced/unspliced layers and a cluster label column.
Output: <out>_transitions.csv (cluster-pair net flows), <out>_edge_score.json (if edges given).
Honest scope: velocity-graph arm validated on E15.5 pancreas endocrinogenesis (7/7 canonical edges)
and dentate gyrus (4/5; granule maturation edge reverses). OT refinement added NOTHING - see REPORT.
"""
import argparse, json, sys, numpy as np
sys.path.insert(0,'code')
from flows import cluster_flow, score
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--h5ad', required=True); ap.add_argument('--label-column', default='clusters')
    ap.add_argument('--canonical-edges'); ap.add_argument('--out-prefix', default='traj')
    a=ap.parse_args()
    import scvelo as scv, scanpy as sc, pandas as pd
    ad=sc.read_h5ad(a.h5ad)
    scv.pp.filter_and_normalize(ad, min_shared_counts=20)
    Xl=ad.X.toarray() if hasattr(ad.X,'toarray') else np.asarray(ad.X)
    hv=np.argsort(-Xl.var(0))[:2000]
    ad=ad[:,sorted(hv)].copy(); del Xl
    scv.pp.moments(ad, n_pcs=30, n_neighbors=30)
    scv.tl.velocity(ad, mode='stochastic'); scv.tl.velocity_graph(ad)
    T=ad.uns['velocity_graph'].toarray().astype(np.float32)
    labels=ad.obs[a.label_column].values
    F=cluster_flow(T, labels)
    rows=[{'from':x,'to':b,'net_flow':round(v,6)} for (x,b),v in sorted(F.items())]
    pd.DataFrame(rows).to_csv(f'{a.out_prefix}_transitions.csv', index=False)
    print(f'wrote {a.out_prefix}_transitions.csv ({len(rows)} pairs)')
    if a.canonical_edges:
        edges=json.load(open(a.canonical_edges))
        res=score(F, edges)
        json.dump(res, open(f'{a.out_prefix}_edge_score.json','w'), indent=1)
        print('canonical edge score:', res['recovered'],'/',res['total'])
if __name__=='__main__': main()
