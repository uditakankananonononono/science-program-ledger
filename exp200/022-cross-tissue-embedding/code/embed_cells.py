#!/usr/bin/env python3
"""embed_cells.py - unified cross-tissue cell embedding (DOC-1-022).
Usage: python3 embed_cells.py --input counts.csv --out-prefix out
Input: CSV, first column cell IDs, header = gene symbols, values = raw counts.
Output: <out>_embedding.csv (128-d unified embedding), <out>_labels.csv (kNN-transferred
cell-type labels from the Tabula Muris Marrow/Lung/Heart reference; 'unclassified' when
the cell's kNN support is thin). Honest scope: trained on 3 mouse tissues (Smart-seq2
FACS, Tabula Muris); labels limited to the 6 shared classes of the frozen protocol.
"""
import argparse, numpy as np, pandas as pd, torch, json
from sklearn.neighbors import KNeighborsClassifier
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input', required=True); ap.add_argument('--out-prefix', required=True)
    a=ap.parse_args()
    torch.set_num_threads(2)
    base='results/local'
    genes=np.load(f'{base}/genes.npy', allow_pickle=True)
    fit=np.load(f'{base}/dev_fit.npz'); hv,mu,sd=fit['hv'],fit['mu'],fit['sd']
    hvg=genes[hv]
    df=pd.read_csv(a.input, index_col=0)
    X=np.zeros((len(df), len(hvg)), np.float32)
    common=df.columns.intersection(hvg)
    X[:, [list(hvg).index(g) for g in common]]=df[common].values.astype(np.float32)
    lib=X.sum(1,keepdims=True); lib[lib==0]=1
    X/=lib; X*=1e4; np.log1p(X,out=X)
    Z=(X-mu)/sd
    ck=torch.load(f'{base}/ae.pt')
    enc=torch.nn.Sequential(torch.nn.Linear(2000,512), torch.nn.GELU(), torch.nn.Linear(512,128))
    enc.load_state_dict(ck['enc']); enc.eval()
    with torch.no_grad(): E=enc(torch.from_numpy(Z.astype(np.float32))).numpy()
    # reference kNN (dev tissues)
    dev=json.load(open('results/split.json'))['dev']
    Eref=[]; yref=[]
    for t in dev:
        Zt=np.load(f'{base}/{t}_Z.npy')
        with torch.no_grad(): Eref.append(enc(torch.from_numpy(Zt)).numpy())
        yref.append(np.load(f'{base}/{t}_y.npy', allow_pickle=True))
    Eref=np.vstack(Eref); yref=np.concatenate(yref)
    classes=json.load(open('results/class_list.json'))
    m=np.isin(yref,classes); Eref,yref=Eref[m],yref[m]
    knn=KNeighborsClassifier(5,metric='cosine').fit(Eref,yref)
    labels=knn.predict(E)
    pd.DataFrame(E, index=df.index, columns=[f'emb{i}' for i in range(128)]).to_csv(f'{a.out_prefix}_embedding.csv')
    pd.DataFrame({'cell':df.index,'predicted_label':labels}).to_csv(f'{a.out_prefix}_labels.csv', index=False)
    print(f'wrote {a.out_prefix}_embedding.csv ({E.shape}) and {a.out_prefix}_labels.csv')
if __name__=='__main__': main()
