import json, math, random
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
exec(open('code/run.py').read().split('def run_genome')[0])  # reuse gc/gc3/LLR + data load
def feats(seqs,di,hexm):
    X=[]
    for s in seqs:
        X.append([gc(s),gc3(s),len(s),di.score(s),hexm.score(s)])
    return np.array(X,float)
def cv_combo(name,k=5,seed=1):
    d=data[name]; pos=d['pos']; neg=d['neg']; n=len(pos)
    rng=random.Random(seed); idx=list(range(n)); rng.shuffle(idx)
    folds=[idx[i::k] for i in range(k)]
    y_true=[]; ps=[]
    for f in range(k):
        test=set(folds[f]); train=[i for i in idx if i not in test]
        di=LLR('DI').fit([pos[i] for i in train],[neg[i] for i in train])
        hexm=LLR('HEX').fit([pos[i] for i in train],[neg[i] for i in train])
        Xtr=feats([pos[i] for i in train]+[neg[i] for i in train],di,hexm)
        ytr=[1]*len(train)+[0]*len(train)
        mu=Xtr.mean(0); sd=Xtr.std(0)+1e-9
        clf=LogisticRegression(max_iter=2000).fit((Xtr-mu)/sd,ytr)
        te=folds[f]
        Xte=feats([pos[i] for i in te]+[neg[i] for i in te],di,hexm)
        p=clf.predict_proba((Xte-mu)/sd)[:,1]
        y_true+= [1]*len(te)+[0]*len(te); ps+=list(p)
    return roc_auc_score(y_true,ps)
def transfer_combo(te_name):
    dtr=data['ecoli']; dte=data[te_name]
    di=LLR('DI').fit(dtr['pos'],dtr['neg']); hexm=LLR('HEX').fit(dtr['pos'],dtr['neg'])
    Xtr=feats(dtr['pos']+dtr['neg'],di,hexm); ytr=[1]*len(dtr['pos'])+[0]*len(dtr['neg'])
    mu=Xtr.mean(0); sd=Xtr.std(0)+1e-9
    clf=LogisticRegression(max_iter=2000).fit((Xtr-mu)/sd,ytr)
    Xte=feats(dte['pos']+dte['neg'],di,hexm)
    p=clf.predict_proba((Xte-mu)/sd)[:,1]
    y=[1]*len(dte['pos'])+[0]*len(dte['neg'])
    return roc_auc_score(y,p)
out={}
for name in ('ecoli','bsub','mtb'):
    out[name]=cv_combo(name); print(name,'COMBO CV',out[name])
for te in ('bsub','mtb'):
    out['ecoli_to_'+te]=transfer_combo(te); print('ecoli ->',te,'COMBO',out['ecoli_to_'+te])
json.dump(out,open('results/pivot_metrics.json','w'),indent=1)
base=json.load(open('results/results.json'))
print('P1 COMBO >= DI-0.001 (ecoli):',out['ecoli'],base['ecoli_cv']['DI'])
print('P2 COMBO >= 0.98:',out['ecoli'])
print('P3 ecoli->mtb COMBO >= 0.95:',out['ecoli_to_mtb'])
