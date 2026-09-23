import pandas as pd, numpy as np, json
from collections import defaultdict
rng=np.random.default_rng(0)
GLOBAL=set(range(1100,1250))
def load(tax,org):
    k=pd.read_csv(f'data/kegg_{org}.tsv',sep='\t',header=None,names=['g','p'])
    k['g']=k.g.str.split(':').str[1]; k['num']=k.p.str[-5:].astype(int)
    k=k[~k.num.isin(GLOBAL)]
    lab=k.groupby('g').p.apply(frozenset).to_dict()
    L=pd.read_csv(f'data/{tax}.protein.links.detailed.v11.0.txt.gz',sep=' ')
    L['a']=L.protein1.str.split('.',n=1).str[1]; L['b']=L.protein2.str.split('.',n=1).str[1]
    allg=set(L.a)|set(L.b)
    return lab,L,allg
def evaluate(lab,L,ch,labels=None):
    labels=labels if labels is not None else lab
    E=L[L[ch]>=400][['a','b',ch]].values
    nb=defaultdict(list)
    for a,b,s in E: nb[a].append((b,s))
    known=list(labels.keys()); pred=0; hit=0
    for g in known:
        v=defaultdict(float)
        for b,s in nb.get(g,[]):
            if b in labels and b!=g:
                for p in labels[b]: v[p]+=s
        if v:
            pred+=1; top=max(v,key=v.get)
            hit+= top in labels[g]
    return pred/len(known), (hit/pred if pred else 0), pred
out={}
for tax,org in [('511145','eco'),('224308','bsu')]:
    lab,L,allg=load(tax,org)
    r={'n_known':len(lab),'n_genes_string':len(allg)}
    for ch in ['cooccurence','neighborhood','coexpression','experimental','textmining','database']:
        cov,prec,n=evaluate(lab,L,ch); r[ch]={'coverage':cov,'precision':prec,'n_pred':n}
    keys=list(lab.keys()); vals=list(lab.values()); nulls={}
    for ch in ['cooccurence','neighborhood']:
        ns=[]
        for i in range(200):
            perm=dict(zip(keys,[vals[j] for j in rng.permutation(len(vals))]))
            ns.append(evaluate(lab,L,ch,perm)[1])
        ns=np.array(ns); obs=r[ch]['precision']
        r[ch].update(null_mean=float(ns.mean()),fold=float(obs/ns.mean()),p_emp=float((1+(ns>=obs).sum())/201))
    out[org]=r
print(json.dumps(out,indent=1)); json.dump(out,open('results/primary.json','w'),indent=1)
