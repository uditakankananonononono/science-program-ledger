#!/usr/bin/env python3
"""detect_rare.py - rare cell type detection (DOC-1-022...023 winning arm = PCA+Leiden).
Usage: python3 detect_rare.py --input counts.csv --target-label-column labels.csv(col) [--rare-fraction 0.05]
Input: counts CSV (cells x genes, first col cell id) and optional label CSV (cell,label).
Output: <out>_clusters.csv (cell, cluster, majority_label), <out>_rare_report.json listing clusters
under the rare-fraction threshold with their majority label and size.
Honest scope: validated on pancreatic PP detection at >=2% rarity (FACS mouse + Smart-seq2 human);
below ~1% rarity no tested method recovered the type - treat negatives there as uninformative.
"""
import argparse, json, numpy as np, pandas as pd, collections, igraph as ig, leidenalg
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input', required=True); ap.add_argument('--labels'); ap.add_argument('--out-prefix', default='rare')
    ap.add_argument('--rare-fraction', type=float, default=0.05)
    a=ap.parse_args()
    df=pd.read_csv(a.input, index_col=0)
    X=df.values.astype(np.float32)
    lib=X.sum(1,keepdims=True); lib[lib==0]=1
    X/=lib; X*=1e4; np.log1p(X,out=X)
    v=X.var(0); hv=np.sort(np.argsort(-v)[:2000])
    Z=X[:,hv]; mu=Z.mean(0); sd=Z.std(0); sd[sd==0]=1; Z=(Z-mu)/sd
    P=TruncatedSVD(n_components=min(50,len(df)-1), random_state=7).fit_transform(Z)
    nn=NearestNeighbors(n_neighbors=16).fit(P)
    _,I=nn.kneighbors(P)
    n=len(df); edges=[(i,j) for i in range(n) for j in I[i,1:]]
    g=ig.Graph(n=n, edges=edges).simplify()
    part=leidenalg.find_partition(g, leidenalg.RBConfigurationVertexPartition, resolution_parameter=1.0, seed=7)
    cl=np.array(part.membership)
    if a.labels:
        lab=pd.read_csv(a.labels, index_col=0).iloc[:,0]
        y=lab.reindex(df.index).fillna('unknown').values
    else:
        y=np.array(['']*n, dtype=object)
    maj={}
    for c in set(cl):
        m=cl==c
        maj[c]=collections.Counter(y[m].tolist()).most_common(1)[0][0] if a.labels else ''
    out=pd.DataFrame({'cell':df.index,'cluster':cl,'majority_label':[maj[c] for c in cl]})
    out.to_csv(f'{a.out_prefix}_clusters.csv', index=False)
    rep={'n_cells':n,'n_clusters':len(set(cl)),'rare_clusters':[
        {'cluster':int(c),'size':int((cl==c).sum()),'fraction':round(float((cl==c).mean()),4),'majority_label':maj[c]}
        for c in set(cl) if (cl==c).mean()<a.rare_fraction]}
    json.dump(rep, open(f'{a.out_prefix}_rare_report.json','w'), indent=1)
    print(f"{n} cells -> {len(set(cl))} clusters; {len(rep['rare_clusters'])} rare (<{a.rare_fraction:.0%})")
if __name__=='__main__': main()
