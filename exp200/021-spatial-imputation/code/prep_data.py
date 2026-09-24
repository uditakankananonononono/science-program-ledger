#!/usr/bin/env python3
"""prep_data.py - build spatial + reference matrices (locked preprocessing: library-size 1e4, log1p), locked gene split."""
import h5py, numpy as np, pandas as pd, json, random
f=h5py.File('results/local/osmfish.loom','r')
genes=[g.decode() for g in f['row_attrs']['Gene'][:]]
M=f['matrix'][:].astype(np.float32)  # 33 x 6471
valid=f['col_attrs']['Valid'][:]==1
X=f['col_attrs']['X'][:][valid].astype(np.float32)
Y=f['col_attrs']['Y'][:][valid].astype(np.float32)
M=M[:,valid]
tot=M.sum(0); tot[tot==0]=1
Mn=np.log1p(M/tot*1e4)
print('spatial cells',Mn.shape[1],'genes',len(genes))
# reference: only shared genes
ref=pd.read_csv('results/local/zeisel_scvi.csv',index_col=0,usecols=lambda c: c in genes or c=='')
shared=[g for g in genes if g in ref.columns]
print('shared genes',len(shared))
R=ref[shared].values.astype(np.float32)
rtot=R.sum(1); rtot[rtot==0]=1
Rn=np.log1p(R/rtot[:,None]*1e4)
print('reference cells',Rn.shape)
rng=random.Random(7)
gs=shared[:]; rng.shuffle(gs)
dev=sorted(gs[:17]); frozen=sorted(gs[17:])
json.dump({'dev':dev,'frozen':frozen},open('results/gene_split.json','w'),indent=1)
np.savez('results/local/spatial.npz',M=Mn,genes=np.array(genes),X=X,Y=Y)
np.savez('results/local/reference.npz',R=Rn,genes=np.array(shared))
print('dev',dev); print('frozen',frozen)
