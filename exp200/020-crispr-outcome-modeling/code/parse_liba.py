#!/usr/bin/env python3
"""parse_liba.py - parse inDelphi SupplementaryData.xlsx Tables 2/3 -> results/local/{dev,frozen_u2os,frozen_t3}.npz"""
import openpyxl, numpy as np
AA='ACGT'
def mh_features(ctx,cut=27):
    best=0; cnt=0; bae=0.0
    for dlen in range(2,21):
        for dstart in range(0,len(ctx)-dlen):
            if not (dstart<cut+2 and dstart+dlen>cut-2): continue
            l2=0
            while (dstart+dlen+l2<len(ctx) and l2<dlen and ctx[dstart+l2]==ctx[dstart+dlen+l2]): l2+=1
            if l2>=2: cnt+=1; best=max(best,l2); bae+=l2*(2 if dlen<=4 else 1)
    return best,cnt,bae
def feats(ctx):
    ctx=ctx.upper()
    v=[]
    for c in ctx: v+=[1.0 if c==a else 0.0 for a in AA]
    di=[0.0]*16
    for i in range(len(ctx)-1):
        a,b=ctx[i],ctx[i+1]
        if a in AA and b in AA: di[AA.index(a)*4+AA.index(b)]+=1
    v+=[x/max(1,len(ctx)-1) for x in di]
    v+=[sum(1 for c in ctx if c in 'GC')/len(ctx), sum(1 for c in ctx[18:28] if c in 'GC')/10]
    v+=[1.0 if ctx[p]==a else 0.0 for p in [23,24,25,26] for a in AA]
    best,cnt,bae=mh_features(ctx)
    v+=[best,cnt,bae]
    return v,bae
wb=openpyxl.load_workbook('results/local/SupplementaryData.xlsx',read_only=True)
def parse(sheet,out,y_col):
    ws=wb[sheet]; rows=list(ws.iter_rows(values_only=True))
    X=[]; y=[]; bae_s=[]; contexts=[]; rc=[]; dropped=0
    for r in rows[2:]:
        try:
            grna=str(r[2]).upper(); ctx=str(r[3]).upper(); yv=float(r[y_col])
        except Exception: dropped+=1; continue
        if not set(ctx)<=set(AA): dropped+=1; continue
        f,b=feats(ctx); X.append(f); bae_s.append(b); contexts.append(ctx); y.append(np.log1p(yv)); rc.append(float(r[5]))
    np.savez(out,X=np.array(X),y=np.array(y),bae=np.array(bae_s),readcount=np.array(rc),contexts=np.array(contexts))
    print(out,len(X),'guides, dropped',dropped,'| y mean',round(float(np.mean(y)),3),'std',round(float(np.std(y)),3))
parse('Supplementary Table 2','results/local/dev.npz',6)
parse('Supplementary Table 2','results/local/frozen_u2os.npz',8)
parse('Supplementary Table 3','results/local/frozen_t3.npz',6)
