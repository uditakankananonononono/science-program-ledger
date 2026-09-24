#!/usr/bin/env python3
"""Score samples with the frozen 25-gene pan-organ injury barcode (exp200/155).
Usage: score_injury.py matrix.tsv  (genes x samples, gene symbols in column 1; any scale)
Output: sample<TAB>score (mean within-sample percentile rank of barcode genes).
Caveat: boundary result - external kidney AUROC 0.60; tracks repair-phase proliferation/myeloid signal, not acute (<2 h) injury."""
import sys,json,os,pandas as pd
F=json.load(open(os.path.join(os.path.dirname(__file__),'..','results','results.json')))['final_barcode']
x=pd.read_csv(sys.argv[1],sep='\t',index_col=0);x=x[~x.index.duplicated()].rank(pct=True)
g=[i for i in F if i in x.index];sys.stderr.write(f"{len(g)}/{len(F)} barcode genes found\n")
for s,v in x.loc[g].mean().items(): print(f"{s}\t{v:.4f}")
