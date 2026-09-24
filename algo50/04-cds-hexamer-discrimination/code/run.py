import json, math, random
import numpy as np
from sklearn.metrics import roc_auc_score
data=json.load(open('data/sets.json'))
BASE='ACGT'
def gc(s): return (s.count('G')+s.count('C'))/len(s)
def gc3(s): return (sum(1 for i in range(2,len(s),3) if s[i] in 'GC')/max(1,len(range(2,len(s),3))))
codons=[a+b+c for a in BASE for b in BASE for c in BASE]
from Bio.Seq import CodonTable
aa_of={}
t=CodonTable.unambiguous_dna_by_id[11]
for c in codons:
    aa_of[c]=t.forward_table.get(c,'*')
def hexes(s):
    return [s[i:i+6] for i in range(0,len(s)-5,3)]
def aas(s):
    return [aa_of.get(s[i:i+3],'X') for i in range(0,len(s)-2,3)]
class LLR:
    def __init__(self,kind): self.kind=kind
    def fit(self,pos,neg):
        if self.kind=='HEX':
            cp={}; cn={}
            for s in pos:
                for h in hexes(s):
                    if set(h)<=set(BASE): cp[h]=cp.get(h,0)+1
            for s in neg:
                for h in hexes(s):
                    if set(h)<=set(BASE): cn[h]=cn.get(h,0)+1
            tp=sum(cp.values()); tn=sum(cn.values()); V=4**6
            self.lp={h:math.log((c+1)/(tp+V)) for h,c in cp.items()}
            self.ln={h:math.log((c+1)/(tn+V)) for h,c in cn.items()}
            self.defp=math.log(1/(tp+V)); self.defn=math.log(1/(tn+V))
        else:
            cp={}; cn={}
            for s in pos:
                for a in aas(s): cp[a]=cp.get(a,0)+1
            for s in neg:
                for a in aas(s): cn[a]=cn.get(a,0)+1
            tp=sum(cp.values()); tn=sum(cn.values()); V=21
            self.lp={a:math.log((c+1)/(tp+V)) for a,c in cp.items()}
            self.ln={a:math.log((c+1)/(tn+V)) for a,c in cn.items()}
            self.defp=math.log(1/(tp+V)); self.defn=math.log(1/(tn+V))
        return self
    def score(self,s):
        if self.kind=='HEX': items=[h for h in hexes(s) if set(h)<=set(BASE)]
        else: items=aas(s)
        return sum(self.lp.get(x,self.defp)-self.ln.get(x,self.defn) for x in items)/max(1,len(items))
def run_genome(name,model_names=('GC','GC3','LEN','DI','HEX'),k=5,seed=1):
    d=data[name]; pos=d['pos']; neg=d['neg']; n=len(pos)
    rng=random.Random(seed); idx=list(range(n)); rng.shuffle(idx)
    folds=[idx[i::k] for i in range(k)]
    y_true=[]; scores={m:[] for m in model_names}
    for f in range(k):
        test=set(folds[f]); train=[i for i in idx if i not in test]
        models={}
        models['HEX']=LLR('HEX').fit([pos[i] for i in train],[neg[i] for i in train])
        models['DI']=LLR('DI').fit([pos[i] for i in train],[neg[i] for i in train])
        for i in folds[f]:
            for label,s in ((1,pos[i]),(0,neg[i])):
                y_true.append(label)
                scores['GC'].append(gc(s)); scores['GC3'].append(gc3(s)); scores['LEN'].append(len(s))
                scores['DI'].append(models['DI'].score(s)); scores['HEX'].append(models['HEX'].score(s))
    return {m:roc_auc_score(y_true,scores[m]) for m in model_names}
def transfer(train_name,test_name):
    dtr=data[train_name]; dte=data[test_name]
    hexm=LLR('HEX').fit(dtr['pos'],dtr['neg']); di=LLR('DI').fit(dtr['pos'],dtr['neg'])
    res={}
    for mname,model in (('HEX',hexm),('DI',di)):
        y=[1]*len(dte['pos'])+[0]*len(dte['neg'])
        s=[model.score(x) for x in dte['pos']]+[model.score(x) for x in dte['neg']]
        res[mname]=roc_auc_score(y,s)
    for feat,fn in (('GC',gc),('GC3',gc3),('LEN',len)):
        y=[1]*len(dte['pos'])+[0]*len(dte['neg'])
        s=[fn(x) for x in dte['pos']]+[fn(x) for x in dte['neg']]
        res[feat]=roc_auc_score(y,s)
    return res
out={}
for name in ('ecoli','bsub','mtb'):
    out[name+'_cv']=run_genome(name)
    print(name,'CV',out[name+'_cv'])
for te in ('bsub','mtb'):
    out['ecoli_to_'+te]=transfer('ecoli',te)
    print('ecoli ->',te,out['ecoli_to_'+te])
json.dump(out,open('results/results.json','w'),indent=1)
b=max(out['ecoli_cv'][m] for m in ('GC','GC3','LEN'))
print('G1 HEX >= best-single + 0.05:',out['ecoli_cv']['HEX'],'vs',b)
print('G2 HEX >= 0.90:',out['ecoli_cv']['HEX'])
print('G3 ecoli->bsub HEX >= 0.85:',out['ecoli_to_bsub']['HEX'])
print('G4 mtb CV HEX >= 0.90:',out['mtb_cv']['HEX'])
