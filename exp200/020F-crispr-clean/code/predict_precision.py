#!/usr/bin/env python3
"""predict_precision.py - 020F clean-data CRISPR outcome-complexity model.
Ridge on 257 sequence/MH features (020's exact feature set), trained on Leenay 2019
primary-human-T-cell repair outcomes (figshare 6957125, depth-floor 10k, n=1685).
Usage: python3 predict_precision.py <55nt context, cut between 27|28>
Prints predicted log1p(outcome complexity) and the raw complexity estimate."""
import sys, pickle
import numpy as np
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
    return np.array(v)
if __name__ == '__main__':
    ctx = sys.argv[1] if len(sys.argv) > 1 else ''
    assert len(ctx) == 55 and set(ctx.upper()) <= set(AA), 'need 55nt ACGT context, cut at 27|28'
    model = pickle.load(open('model020F.pkl','rb'))
    ly = float(model.predict(feats(ctx).reshape(1,-1))[0])
    print(f'predicted log1p(complexity): {ly:.4f}')
    print(f'predicted unique indel classes: {np.expm1(ly):.1f}')
