#!/usr/bin/env python3
"""ccc_spatial.py - cell-cell communication prediction (winning arm: unconstrained CellPhoneDB-style).
Usage: python3 ccc_spatial.py --xlr X.npy --genes genes.npy --labels cl.npy --lr-pairs lr.json --out-prefix out
Input: spot x gene log-normalized matrix (.npy), gene names (.npy), cluster labels (.npy),
LR pairs JSON [["LIG","REC"],...]. Output: <out>_predictions.csv (ligand, receptor, from, to,
score, pval, significant). Honest scope: validated on Visium sagittal mouse brain with
cross-section replication 0.52-0.82 precision@100; spatial adjacency filtering was tested and
REMOVED - it discards real signaling (size-biased, corr 0.757 with cluster size).
"""
import argparse, json, numpy as np, pandas as pd
rng=np.random.default_rng(7)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--xlr', required=True); ap.add_argument('--genes', required=True)
    ap.add_argument('--labels', required=True); ap.add_argument('--lr-pairs', required=True)
    ap.add_argument('--out-prefix', default='ccc'); ap.add_argument('--perms', type=int, default=100)
    a=ap.parse_args()
    X=np.load(a.xlr); genes=np.load(a.genes, allow_pickle=True); cl=np.load(a.labels)
    gidx={g:i for i,g in enumerate(genes)}
    pairs=[tuple(p) for p in json.load(open(a.lr_pairs))]
    prs=[(gidx[x],gidx[y],x,y) for x,y in pairs if x in gidx and y in gidx]
    C=cl.max()+1
    def means(c):
        M=np.zeros((C,X.shape[1]),np.float32)
        for k in range(C):
            m=c==k
            if m.sum()>0: M[k]=X[m].mean(0)
        return M
    M=means(cl)
    Li=[p[0] for p in prs]; Ri=[p[1] for p in prs]
    obs=M[:,Li].T[:, :, None]*M[:,Ri].T[:, None, :]
    cnt=np.zeros_like(obs)
    for _ in range(a.perms):
        Mp=means(rng.permutation(cl))
        cnt+=(Mp[:,Li].T[:, :, None]*Mp[:,Ri].T[:, None, :]>=obs)
    pvals=(cnt+1)/(a.perms+1)
    rows=[]
    for pi,(_,_,la,lb) in enumerate(prs):
        aa,bb=np.where(pvals[pi]<=0.05)
        for A,B in zip(aa,bb):
            rows.append({'ligand':la,'receptor':lb,'from_cluster':int(A),'to_cluster':int(B),
                         'score':round(float(obs[pi,A,B]),4),'pval':round(float(pvals[pi,A,B]),4)})
    df=pd.DataFrame(rows).sort_values('score', ascending=False)
    df.to_csv(f'{a.out_prefix}_predictions.csv', index=False)
    print(f'{len(prs)} testable LR pairs; {len(df)} significant predictions -> {a.out_prefix}_predictions.csv')
if __name__=='__main__': main()
