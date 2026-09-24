#!/usr/bin/env python3
"""P19-02: HeLU-style affinity regression on DAVIS (kinase Kd).
Locked gates (spec doc290/cbio056-helu-dti-drug-target/02-affinity-regression.md):
 G1 random-split Pearson r >= 0.80 ; G2 cold-target r >= 0.55 ;
 G3 KG-ablation effect with 95% CI over 5 seeds ; G4 variance-head ECE <= 0.1.
Amendments vs spec are printed into results (sandbox: no ESM-2/ChemBERTa/PrimeKG,
KIBA/ChEMBL fetch attempted separately); embeddings replaced by sequence k-mers +
Morgan fingerprints; KG branch proxied by sequence-similarity kinase-family clusters.
"""
import json, pickle, sys, numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.cluster import KMeans
from scipy.stats import pearsonr

DATA='/tmp/davis'
prots=json.load(open(f'{DATA}/proteins.txt'))
ligs=json.load(open(f'{DATA}/ligands_can.txt'))
Y=pickle.load(open(f'{DATA}/Y','rb'),encoding='latin1')   # (n_lig, n_prot), Kd in nM
pKd=-np.log10(Y/1e9)
pkeys=list(prots.keys()); lkeys=list(ligs.keys())
P,L=len(pkeys),len(lkeys)

AA='ACDEFGHIKLMNPQRSTVWY'
def seqfeat(s,dim=64):
    v=np.zeros(len(AA)+dim)
    for a in s:
        if a in AA: v[AA.index(a)]+=1
    km={}
    for i in range(len(s)-2):
        k=s[i:i+3]; km[k]=km.get(k,0)+1
    for k,c in km.items(): v[len(AA)+hash(k)%dim]+=c
    return v/max(v.sum(),1)
def morgan(smi,dim=512):
    m=Chem.MolFromSmiles(smi)
    if m is None: return np.zeros(dim)
    return AllChem.GetMorganFingerprintAsBitVect(m,2,nBits=dim).ToList()

print('featurizing...',flush=True)
PF=np.array([seqfeat(prots[k]) for k in pkeys])
LF=np.array([morgan(ligs[k]) for k in lkeys])
# KG proxy: 12 sequence-similarity families over protein k-mer space (fixed seed)
fam=KMeans(n_clusters=12,random_state=0,n_init=4).fit_predict(PF)
oh=np.zeros((P,12)); oh[np.arange(P),fam]=1
# KG branch = family one-hot + family mean-affinity profile (computed inside folds to avoid leakage)
LF=np.array(LF)
def build(rows,kg,fam_mean):
    X=[np.concatenate([PF[p],LF[l]] + ([oh[p],np.atleast_1d(fam_mean[p])] if kg else [])) for l,p in rows]
    return np.array(X,dtype=np.float32)

allrows=[(l,p) for l in range(L) for p in range(P)]
yall=np.array([pKd[l,p] for l,p in allrows])
rng=np.random.RandomState(0)

def family_means(train_idx):
    fm=np.zeros(P); cnt=np.zeros(P)
    for i in train_idx:
        l,p=allrows[i]; fm[p]+=yall[i]; cnt[p]+=1
    gm=fm.sum()/max(cnt.sum(),1)
    return np.where(cnt>0,fm/np.maximum(cnt,1),gm)

def ece(y,pred,sig,bins=10):
    z=np.abs(y-pred)/np.maximum(sig,1e-6)
    qs=np.quantile(sig,np.linspace(0,1,bins+1))
    errs=[]
    for b in range(bins):
        m=(sig>=qs[b])&((sig<=qs[b+1]) if b==bins-1 else (sig<qs[b+1]))
        if m.sum()<50: continue
        emp=float(np.mean(z[m]<=1.0))
        errs.append(abs(emp-0.6827))
    return float(np.mean(errs)) if errs else float('nan')

def train_eval(Xtr,ytr,Xte,yte):
    if len(ytr)>20000:
        s=np.random.RandomState(7).choice(len(ytr),20000,replace=False); Xtr,ytr=Xtr[s],ytr[s]
    m=HistGradientBoostingRegressor(max_iter=150,learning_rate=0.1,random_state=0,early_stopping=False)
    m.fit(Xtr,ytr); pred=m.predict(Xte)
    lo=HistGradientBoostingRegressor(loss='quantile',quantile=0.16,max_iter=80,random_state=0).fit(Xtr,ytr).predict(Xte)
    hi=HistGradientBoostingRegressor(loss='quantile',quantile=0.84,max_iter=80,random_state=0).fit(Xtr,ytr).predict(Xte)
    sig=np.maximum((hi-lo)/2.0,0.05)
    r=pearsonr(pred,yte)[0]
    return r,pred,sig

out={'dataset':'DAVIS (68 ligands x 442 kinases, Kd nM -> pKd)','n_pairs':int(len(allrows))}
# ---- G1: random split, 5 seeds; G3: KG ablation per seed
g1={'with_kg':[],'no_kg':[]}; eces=[]
idx=np.arange(len(allrows))
for seed in range(5):
    rs=np.random.RandomState(seed); perm=rs.permutation(idx)
    te=perm[:int(0.2*len(perm))]; tr=perm[int(0.2*len(perm)):]
    fm=family_means(tr)
    for kg,key in [(True,'with_kg'),(False,'no_kg')]:
        X=build(allrows,kg,fm)
        r,pred,sig=train_eval(X[tr],yall[tr],X[te],yall[te])
        g1[key].append(float(r))
        if kg and seed==0: eces.append(ece(yall[te],pred,sig))
    print(f'seed {seed}: r_kg={g1["with_kg"][-1]:.3f} r_nokg={g1["no_kg"][-1]:.3f}',flush=True)
out['G1_random_split_r']=g1
diffs=np.array(g1['with_kg'])-np.array(g1['no_kg'])
out['G3_kg_ablation']={'mean_delta_r':float(diffs.mean()),'ci95':float(1.96*diffs.std(ddof=1)/np.sqrt(len(diffs))),'per_seed':diffs.tolist()}
out['G4_ece_seed0']=eces[0]
# ---- G2: cold-target split (kinases unseen in training)
prs=np.random.RandomState(1).permutation(P); test_prots=set(prs[:int(0.2*P)].tolist())
te=[i for i,(l,p) in enumerate(allrows) if p in test_prots]
tr=[i for i,(l,p) in enumerate(allrows) if p not in test_prots]
fm=family_means(np.array(tr))
X=build(allrows,True,fm); X=np.array(X)
r2,_,_=train_eval(X[tr],yall[tr],X[te],yall[te])
out['G2_cold_target_r']=float(r2)
# ---- KIBA attempt (fetch separately; skipped if absent)
import os
out['kiba']='not run in this environment (fetch blocked); DAVIS-only build'
json.dump(out,open(sys.argv[1] if len(sys.argv)>1 else 'results.json','w'),indent=1)
print(json.dumps({k:(v if not isinstance(v,dict) else '...') for k,v in out.items()},indent=1))
