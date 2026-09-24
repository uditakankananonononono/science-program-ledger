#!/usr/bin/env python3
"""parse_features.py - parse Lindel txt -> features + labels (ADDENDUM A definitions)."""
import numpy as np
AA='ACGT'
def mh_features(sp):
    cut=17
    best=0; cnt=0; bae=0.0
    for dlen in range(2,11):
        for dstart in range(max(0,cut-dlen-3),min(len(sp)-dlen,cut+2)):
            left=sp[dstart:dstart+dlen]
            for ml in range(2,min(dlen,6)+1):
                if dstart+ml<=len(sp) and dstart+dlen+ml<=len(sp):
                    if sp[dstart+dlen-ml:dstart+dlen]==sp[dstart+2*dlen-ml:dstart+2*dlen] if dstart+2*dlen<=len(sp) else False:
                        pass
            # simple MH: sequence repeated immediately across the deletion boundaries
            if dstart+dlen+2<=len(sp):
                l2=0
                while (dstart+dlen+l2<len(sp) and dstart+l2<dstart+dlen and l2<dlen
                       and sp[dstart+l2]==sp[dstart+dlen+l2]): l2+=1
                if l2>=2:
                    cnt+=1; best=max(best,l2); bae+=l2*(2 if dlen<=4 else 1)
    return best,cnt,bae
def feats(sp):
    v=[]
    for i,c in enumerate(sp):
        v+= [1.0 if c==a else 0.0 for a in AA]
    di=[0.0]*16
    for i in range(len(sp)-1):
        a,b=sp[i],sp[i+1]
        if a in AA and b in AA: di[AA.index(a)*4+AA.index(b)]+=1
    v+=[x/(len(sp)-1) for x in di]
    gc=sum(1 for c in sp if c in 'GC')/len(sp)
    gcp=sum(1 for c in sp[-6:] if c in 'GC')/6
    v+=[gc,gcp]
    v+=[1.0 if sp[p]==a else 0.0 for p in [13,14,15,16] for a in AA]
    best,cnt,bae=mh_features(sp)
    v+=[best,cnt,bae]
    return v
def parse(path,out):
    X=[]; y1=[]; y2=[]; spacers=[]; dropped=0
    for line in open(path):
        p=line.rstrip('\n').split('\t')
        sp=p[0].upper()
        if len(sp)!=20 or not set(sp)<=set(AA): dropped+=1; continue
        lab=np.array([float(x) for x in p[1:]])
        n=int(lab.sum())
        if n==0: dropped+=1; continue
        spacers.append(sp); X.append(feats(sp)); y1.append(n); y2.append(1 if n<=3 else 0)
    np.savez(out,X=np.array(X),y1=np.array(y1),y2=np.array(y2),spacers=np.array(spacers))
    print(out,len(X),'guides, dropped',dropped,'| y1 mean',float(np.mean(y1)),'| y2 precise frac',float(np.mean(y2)))
parse('results/local/Lindel_training.txt','results/local/dev.npz')
parse('results/local/Lindel_test.txt','results/local/frozen.npz')
