#!/usr/bin/env python3
"""predict_precision.py - predict Cas9 outcome complexity (log1p unique indels) for a 55nt context.
Usage: python3 predict_precision.py CONTEXT55
Model: ridge on 257 sequence/MH features, trained on inDelphi LibA mESC (Shen et al. 2018).
Transport: U2OS Spearman 0.657 (PASS); designed-library Spearman 0.279 (FAIL - see REPORT.md boundary).
Research use only."""
import sys, json, numpy as np
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
    ctx=ctx.upper(); v=[]
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
ctx=sys.argv[1].upper()
assert len(ctx)==55 and set(ctx)<=set(AA), 'need 55nt ACGT context with cut between 27|28'
f,bae=feats(ctx)
m=json.load(open('results/model_precision.json'))
z=[(f[i]-m['mean'][i])/m['std'][i] for i in range(len(f))]
pred=m['intercept']+sum(c*x for c,x in zip(m['coef'],z))
print(json.dumps({'context':ctx,'predicted_log1p_unique_indels':round(pred,3),
 'predicted_complexity_class':'high' if pred>5.9 else ('low' if pred<4.9 else 'medium'),
 'bae_mh_score':bae},indent=1))
