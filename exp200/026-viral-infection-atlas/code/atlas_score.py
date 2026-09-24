#!/usr/bin/env python3
"""atlas_score.py - viral infection response scoring (winning arm: curated ISG signature).
Usage: python3 atlas_score.py --counts counts.csv [--labels labels.csv] --out-prefix out
Input: cells x genes RAW counts CSV (first col cell id). Optional labels CSV (cell,disease,cell_type).
Output: <out>_scores.csv (cell, isg_score), <out>_auroc.json if labels given (per-cell-type AUROC,
infected vs normal). Honest scope: validated on PBMCs (COVID/influenza vs healthy, Lee 2020);
pooled-severity AUROC 0.59-0.62 mean. A data-driven dev-fit program was tested and REMOVED - it
learned cohort-specific genes (0/5 canonical ISGs) and failed to transfer to the held-out virus.
"""
import argparse, json, numpy as np, pandas as pd, urllib.request
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--counts', required=True); ap.add_argument('--labels')
    ap.add_argument('--out-prefix', default='atlas')
    a=ap.parse_args()
    txt=urllib.request.urlopen('https://maayanlab.cloud/Enrichr/geneSetLibrary?mode=text&libraryName=MSigDB_Hallmark_2020', timeout=60).read().decode()
    isg=set()
    for line in txt.splitlines():
        f=line.split('\t')
        if f[0] in ('Interferon Alpha Response','Interferon Gamma Response'):
            isg|={g.upper() for g in f[2:] if g}
    df=pd.read_csv(a.counts, index_col=0)
    up={c.upper():c for c in df.columns}
    cols=[up[g] for g in isg if g in up]
    X=df[cols].values.astype(np.float32)
    lib=df.values.sum(1, keepdims=True).astype(np.float32); lib[lib==0]=1
    X=np.log1p(X/lib*1e4)
    score=X.mean(1)
    pd.DataFrame({'cell':df.index,'isg_score':score}).to_csv(f'{a.out_prefix}_scores.csv', index=False)
    print(f'{len(cols)} ISG genes scored for {len(df)} cells')
    if a.labels:
        from sklearn.metrics import roc_auc_score
        lab=pd.read_csv(a.labels, index_col=0).reindex(df.index)
        out={}
        for ct in sorted(lab.iloc[:,1].dropna().unique()):
            m=(lab.iloc[:,1]==ct).values
            y=(lab.iloc[:,0].values[m]!='normal').astype(int)
            if y.sum()>=10 and (1-y).sum()>=10:
                out[ct]=round(float(roc_auc_score(y, score[m])),3)
        json.dump(out, open(f'{a.out_prefix}_auroc.json','w'), indent=1)
        print('AUROC:', out)
if __name__=='__main__': main()
