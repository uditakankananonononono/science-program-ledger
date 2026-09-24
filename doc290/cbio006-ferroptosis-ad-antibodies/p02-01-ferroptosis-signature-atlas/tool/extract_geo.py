#!/usr/bin/env python3
"""Extract GEO series matrix -> gene-level mean expression (float32 npz) + parsed sample phenotype CSV.
Probes mapped by platform annotation symbol; probes with no symbol or multiple symbols ('///') dropped."""
import sys, gzip, csv, numpy as np, pandas as pd, collections
gse, annot, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
def load_map(path):
    op=gzip.open if path.endswith('.gz') else open
    m={}; hdr=None
    with op(path,'rt',errors='replace') as f:
        for line in f:
            if hdr is None:
                if line.startswith('ID\t'):
                    hdr=line.rstrip('\n').split('\t'); si=hdr.index('Gene symbol') if 'Gene symbol' in hdr else hdr.index('GENE_SYMBOL')
                continue
            if line.startswith('!'): break
            p=line.rstrip('\n').split('\t')
            if len(p)>si and p[si] and '///' not in p[si]: m[p[0]]=p[si].strip()
    return m
pm=load_map(annot); print('probes mapped',len(pm),flush=True)
meta=collections.OrderedDict(); ids=None; sums=collections.defaultdict(lambda:None); cnt=collections.Counter()
with gzip.open(f'{gse}_series_matrix.txt.gz','rt',errors='replace') as f:
    intable=False
    for line in f:
        if line.startswith('!Sample_'):
            k=line.split('\t',1)[0]; vals=[v.strip().strip('"') for v in line.rstrip('\n').split('\t')[1:]]
            i=1; kk=k
            while kk in meta: i+=1; kk=f'{k}_{i}'
            meta[kk]=vals; continue
        if line.startswith('"ID_REF"'):
            ids=[v.strip('"') for v in line.rstrip('\n').split('\t')[1:]]; intable=True; continue
        if line.startswith('!series_matrix_table_end'): break
        if intable:
            p=line.rstrip('\n').split('\t'); g=pm.get(p[0].strip('"'))
            if not g: continue
            v=np.array([float(x) if x not in ('','null','NA','NaN') else np.nan for x in p[1:]],dtype=np.float64)
            sums[g]=v if sums[g] is None else sums[g]+v; cnt[g]+=1
genes=sorted(sums); X=np.vstack([sums[g]/cnt[g] for g in genes]).astype(np.float32)
np.savez_compressed(f'{outdir}/{gse}_expr.npz',X=X,genes=np.array(genes),samples=np.array(ids))
P=pd.DataFrame({'sample':meta['!Sample_geo_accession']})
for k,v in meta.items():
    if 'characteristics' in k or k.startswith('!Sample_source_name') or k.startswith('!Sample_title'):
        if len(v)==len(P): P[k.replace('!Sample_','')]=v
P.to_csv(f'{outdir}/{gse}_pheno.csv',index=False)
print(gse,'genes',X.shape,'samples',len(ids),'median value',float(np.nanmedian(X)),flush=True)
