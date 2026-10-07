import numpy as np, pandas as pd, hashlib, json, os, sys, warnings, itertools
from rdkit import Chem, RDLogger
from rdkit.Chem import Descriptors, Crippen, rdMolDescriptors, Fragments, rdFingerprintGenerator
from rdkit.Chem.Scaffolds import MurckoScaffold
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GroupKFold
warnings.filterwarnings('ignore'); RDLogger.DisableLog('rdApp.*')
assert hashlib.sha256(open('freesolv.csv','rb').read()).hexdigest()=='1c71b2743d2bada476657d9f222847bf7ba98b5bee8d0841134ca2b32e4d264f'
d=pd.read_csv('freesolv.csv'); y=d.experimental_kcal_mol.values; mols=[Chem.MolFromSmiles(s) for s in d.smiles]; assert all(m is not None for m in mols)
gen=rdFingerprintGenerator.GetMorganGenerator(radius=2,fpSize=2048)
def morgan(m): return gen.GetCountFingerprintAsNumPy(m).astype(float)
FR=[(n,f) for n,f in Descriptors.descList if n.startswith('fr_')]
def pfg(m):
    lp=Crippen.MolLogP(m); tp=rdMolDescriptors.CalcTPSA(m)
    v=[f(m) for n,f in FR]+[lp,Crippen.MolMR(m),tp,rdMolDescriptors.CalcNumHBD(m),rdMolDescriptors.CalcNumHBA(m),rdMolDescriptors.CalcNumRotatableBonds(m),m.GetNumHeavyAtoms(),rdMolDescriptors.CalcFractionCSP3(m),rdMolDescriptors.CalcNumRings(m),sum(1 for a in m.GetAtoms() if a.GetFormalCharge()!=0),lp*tp/100]
    return np.array(v,float)
assert abs(Crippen.MolLogP(Chem.MolFromSmiles('c1ccccc1'))-1.6866)<0.02
assert np.array_equal(morgan(Chem.MolFromSmiles('OCC')),morgan(Chem.MolFromSmiles('CCO'))) and np.array_equal(pfg(mols[0]),pfg(mols[0]))
if os.environ.get('CHECK'): print('checks passed'); sys.exit()
XM=np.array([morgan(m) for m in mols]); XP=np.array([pfg(m) for m in mols])
sc=[MurckoScaffold.MurckoScaffoldSmiles(mol=m,includeChirality=False) for m in mols]; keys=[s if s else f'acyc_{i}' for i,s in enumerate(sc)]; grp=pd.factorize(pd.Series(keys))[0]
ug=np.unique(grp); perm=np.random.RandomState(51).permutation(len(ug)); devg=set(ug[perm[:len(ug)//2]]); isdev=np.array([g in devg for g in grp]); di=np.where(isdev)[0]; ti=np.where(~isdev)[0]; print('dev',len(di),'test',len(ti),'groups',len(ug),flush=True)
def cv(mk,X):
    se=0
    for tr,te in GroupKFold(5).split(di,groups=grp[di]):
        a,b=di[tr],di[te]; m=mk().fit(X[a],y[a]); se+=((m.predict(X[b])-y[b])**2).sum()
    return float(np.sqrt(se/len(di)))
cfg={}
for a in (0.1,1,10,100): cfg[('MR',a)]=(lambda a=a:Ridge(alpha=a),XM)
for mf,ml in itertools.product((0.1,0.3),(1,2)): cfg[('MRF',mf,ml)]=(lambda mf=mf,ml=ml:RandomForestRegressor(n_estimators=300,max_features=mf,min_samples_leaf=ml,random_state=0,n_jobs=1),XM)
for C in (1,10,100): cfg[('MSV',C)]=(lambda C=C:SVR(C=C,gamma='scale',epsilon=0.1),XM)
for a in (0.1,1,10,100): cfg[('PFGR',a)]=(lambda a=a:make_pipeline(StandardScaler(),Ridge(alpha=a)),XP)
for n,dp in itertools.product((200,400),(2,3)): cfg[('PFGB',n,dp)]=(lambda n=n,dp=dp:GradientBoostingRegressor(n_estimators=n,max_depth=dp,learning_rate=0.05,subsample=0.8,random_state=0),XP)
dev={k:cv(mk,X) for k,(mk,X) in cfg.items()}
bb={f:min((k for k in dev if k[0]==f),key=lambda k:dev[k]) for f in ('MR','MRF','MSV')}; head=min(bb,key=lambda f:dev[bb[f]])
bp=min((k for k in dev if k[0] in('PFGR','PFGB')),key=lambda k:dev[k]); print('DEV',{f:(bb[f],dev[bb[f]]) for f in bb},bp,dev[bp],flush=True)
def fitpred(k): mk,X=cfg[k]; return mk().fit(X[di],y[di]).predict(X[ti])
pred={f:fitpred(bb[f]) for f in bb}; pred['PFG']=fitpred(bp); yt=y[ti]
rm={n:float(np.sqrt(((p-yt)**2).mean())) for n,p in pred.items()}; ma={n:float(np.abs(p-yt).mean()) for n,p in pred.items()}; r2={n:float(1-((p-yt)**2).sum()/((yt-yt.mean())**2).sum()) for n,p in pred.items()}
gt=grp[ti]; ugt=np.unique(gt); ix={g:np.where(gt==g)[0] for g in ugt}; rs=np.random.RandomState(7); ds=[]
for _ in range(10000):
    s=np.concatenate([ix[g] for g in ugt[rs.randint(0,len(ugt),len(ugt))]]); ds.append(np.sqrt(((pred[head][s]-yt[s])**2).mean())-np.sqrt(((pred['PFG'][s]-yt[s])**2).mean()))
lo,hi=np.percentile(ds,[2.5,97.5]); diff=rm[head]-rm['PFG']; rel=diff/rm[head]; v='WIN' if rel>=.05 and lo>0 else ('NEGATIVE' if hi<0 else 'NULL')
res=dict(n_dev=len(di),n_test=len(ti),n_groups=len(ug),head=head,dev_best={f:[list(bb[f]),dev[bb[f]]] for f in bb},pfg_choice=[list(bp),dev[bp]],test_rmse=rm,test_mae=ma,test_r2=r2,diff=float(diff),rel=float(rel),ci=[float(lo),float(hi)],verdict=v)
json.dump(res,open('results.json','w'),indent=1); print(json.dumps(res))
