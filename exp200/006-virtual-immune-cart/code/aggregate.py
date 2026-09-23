#!/usr/bin/env python3
"""Frozen per-patient aggregation (GATES.md): stream 10x matrix, keep panel genes only."""
import sys, tarfile
import numpy as np, pandas as pd
PANEL=['CD3D','CD3E','CD8A','CD8B','CD4','CCR7','SELL','TCF7','IL7R','CD27','PDCD1','HAVCR2','LAG3','TOX','TIGIT','NKG7','GZMB','PRF1','GZMK','GNLY','MKI67','TOP2A']
def agg(path):
    with tarfile.open(path,'r:gz') as tf:
        names=tf.getnames()
        gfile=[n for n in names if n.endswith('genes.tsv') or n.endswith('features.tsv')][0]
        mfile=[n for n in names if n.endswith('matrix.mtx') or n.endswith('matrix.mtx.gz')][0]
        genes=pd.read_csv(tf.extractfile(gfile),sep='\t',header=None,usecols=[1] if 'genes' not in gfile else None)
        genes=pd.read_csv(tf.extractfile(gfile),sep='\t',header=None)
        glist=genes[1].tolist() if genes.shape[1]>1 else genes[0].tolist()
        gidx={g:i for i,g in enumerate(glist)}
        pidx={g:gidx[g]+1 for g in PANEL if g in gidx}  # mtx is 1-based
        m=pd.read_csv(tf.extractfile(mfile),sep=' ',header=None,skiprows=3,names=['g','c','v'])
    lib=m.groupby('c')['v'].sum()
    sel=m[m['g'].isin(pidx.values())]
    inv={v:k for k,v in pidx.items()}
    sel=sel.assign(marker=sel['g'].map(inv))
    nC=int(lib.index.max())
    tcells=set(sel.loc[sel['marker'].isin(['CD3D','CD3E']),'c'][sel.loc[sel['marker'].isin(['CD3D','CD3E']),'v']>0])
    out={'n_cells':nC,'n_tcells':len(tcells)}
    for g in PANEL:
        if g not in pidx: out[f'fracpos_{g}']=None; out[f'meanlog_{g}']=None; continue
        sg=sel[sel['marker']==g]
        pos=set(sg.loc[sg['v']>0,'c']) & tcells
        out[f'fracpos_{g}']=len(pos)/max(len(tcells),1)
        vv=sg[sg['c'].isin(tcells)].groupby('c')['v'].sum()
        cpm=(vv/lib[vv.index]*1e6)
        out[f'meanlog_{g}']=float(np.log1p(cpm).mean())
    return out
if __name__=='__main__':
    import json
    print(json.dumps(agg(sys.argv[1]),indent=1))
