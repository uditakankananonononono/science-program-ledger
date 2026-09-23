import json, numpy as np, pandas as pd
from collections import defaultdict
rng=np.random.default_rng(0)
mech=json.load(open('data/mechanisms.json')); tg=json.load(open('data/targets.json')); mo=json.load(open('data/molecules.json'))
t2u={}
for t in tg:
    if t.get('organism')!='Homo sapiens': continue
    acc={c['accession'] for c in t.get('target_components',[]) if c.get('accession')}
    if acc: t2u[t['target_chembl_id']]=acc
r=pd.read_csv('data/UniProt2Reactome.txt',sep='\t',header=None,usecols=[0,1,5],names=['u','p','sp'])
r=r[r.sp=='Homo sapiens']; u2p=r.groupby('u').p.apply(set).to_dict()
atc={m['id']:{a[:4] for a in m['atc']} for m in mo if m['atc']}
names={m['id']:m['name'] for m in mo}
dt=defaultdict(set)
for m in mech:
    if m.get('direct_interaction')==0: continue
    d=m['parent_molecule_chembl_id']; t=m['target_chembl_id']
    if d and t in t2u: dt[d]|=t2u[t]
drugs=[d for d in dt if d in atc and any(u in u2p for u in dt[d])]
fp={d:set().union(*[u2p.get(u,set()) for u in dt[d]]) for d in drugs}
n=len(drugs); print('drugs',n)
P=sorted(set().union(*fp.values())); pi={p:i for i,p in enumerate(P)}
X=np.zeros((n,len(P)),bool)
for i,d in enumerate(drugs): X[i,[pi[p] for p in fp[d]]]=True
Xi=X.astype(np.float32); inter=Xi@Xi.T; sz=X.sum(1); J=inter/(sz[:,None]+sz[None,:]-inter)
U=sorted(set().union(*[dt[d] for d in drugs])); ui={u:i for i,u in enumerate(U)}
T=np.zeros((n,len(U)),np.float32)
for i,d in enumerate(drugs): T[i,[ui[u] for u in dt[d]]]=1
TI=T@T.T; share=TI>0; ts=T.sum(1); TJ=TI/(ts[:,None]+ts[None,:]-TI)
np.fill_diagonal(J,-1); np.fill_diagonal(TJ,-1)
jit=rng.random((n,n))*1e-6
Jm=np.where(share,-1,J)+jit
nn=Jm.argmax(1); ok=Jm[np.arange(n),nn]>0.001
labs=[atc[d] for d in drugs]
def prec(L,nbr,mask): return float(np.mean([len(L[i]&L[nbr[i]])>0 for i in np.where(mask)[0]]))
obs=prec(labs,nn,ok)
null=[]
for _ in range(1000):
    pl=[labs[j] for j in rng.permutation(n)]; null.append(prec(pl,nn,ok))
null=np.array(null)
tnn=(TJ+jit).argmax(1); tok=TJ[np.arange(n),tnn]>0
res={'n_drugs':n,'n_pathways':len(P),'n_eval_noshared':int(ok.sum()),'precision_noshared':obs,'null_mean':float(null.mean()),
 'fold':obs/null.mean(),'p_emp':float((1+(null>=obs).sum())/1001),
 'target_NN_precision':prec(labs,tnn,tok),'target_NN_n':int(tok.sum())}
# stratify by NN similarity
sims=Jm[np.arange(n),nn]
for lo,hi in [(0,.25),(.25,.5),(.5,1.01)]:
    m=ok&(sims>=lo)&(sims<hi); res[f'noshared_prec_J{lo}-{hi}']=(prec(labs,nn,m) if m.any() else None, int(m.sum()))
ex=[(names[drugs[i]],names[drugs[nn[i]]],round(float(sims[i]),2),sorted(labs[i]&labs[nn[i]])) for i in np.where(ok)[0] if labs[i]&labs[nn[i]] and sims[i]>=.5]
res['examples_hit']=ex[:25]
pd.DataFrame([(drugs[i],names[drugs[i]],drugs[nn[i]],names[drugs[nn[i]]],float(sims[i]),'|'.join(sorted(labs[i])),'|'.join(sorted(labs[nn[i]])),bool(labs[i]&labs[nn[i]])) for i in np.where(ok)[0]],
  columns=['drug','name','nn_no_shared_target','nn_name','pathway_jaccard','atc3','nn_atc3','same_class']).to_csv('results/noshared_neighbours.csv',index=False)
print(json.dumps(res,indent=1,default=str)); json.dump(res,open('results/primary.json','w'),indent=1,default=str)
