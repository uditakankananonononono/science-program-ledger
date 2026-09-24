import numpy as np, json
def cluster_flow(T, labels):
    cats=sorted(set(labels))
    idx={c: np.where(labels==c)[0] for c in cats}
    F={}
    for a in cats:
        Ta=T[idx[a]]
        for b in cats:
            if a==b: continue
            F[(a,b)]=float(Ta[:,idx[b]].mean())
    return F
def score(F, edges):
    rec=0; wrong=0; detail={}
    for a,b in edges:
        net=F.get((a,b),0.0)-F.get((b,a),0.0)
        detail[f'{a}->{b}']={'net':round(net,6),'recovered':net>0}
        if net>0: rec+=1
        else: wrong+=1
    return {'recovered':rec,'total':len(edges),'wrong':wrong,'detail':detail}
