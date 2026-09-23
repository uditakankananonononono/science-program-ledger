# Scores, metrics, paired bootstrap, gates. Run after docking completes.
import numpy as np, json, ifp
from rdkit import Chem; from rdkit.Chem import AllChem, DataStructs
from sklearn.metrics import roc_auc_score
from scipy.stats import rankdata
rec=ifp.read_receptor(); cm,clig=ifp.crystal_lig()
CX=np.array([x for x,t in clig]); res,idx=ifp.site(rec,CX); ref=ifp.ifp(rec,res,idx,clig)
lib={l.split('\t')[0]:l.rstrip('\n').split('\t') for l in list(open('../data/library.tsv'))[1:]}
cfp=AllChem.GetMorganFingerprintAsBitVect(Chem.RemoveHs(cm),2,2048)
rows=[]
for l in open('../results/scores.tsv'):
    cid,lab,en,st=l.rstrip('\n').split('\t')
    if cid=='CRYSTAL': continue
    m=Chem.MolFromSmiles(lib[cid][1])
    s2d=DataStructs.TanimotoSimilarity(cfp,AllChem.GetMorganFingerprintAsBitVect(m,2,2048))
    if st!='ok': rows.append((cid,int(lab),np.nan,np.nan,s2d,m.GetNumHeavyAtoms())); continue
    sv=-float(en.split(';')[0])
    si=max(ifp.tani(ifp.ifp(rec,res,idx,p),ref) for p in ifp.poses('../results/dock/%s.pdbqt'%cid))
    rows.append((cid,int(lab),sv,si,s2d,m.GetNumHeavyAtoms()))
y=np.array([r[1] for r in rows]); S={'vina':np.array([r[2] for r in rows]),'ifp':np.array([r[3] for r in rows]),'2d':np.array([r[4] for r in rows]),'size':np.array([r[5] for r in rows],float)}
for k in S: S[k]=np.where(np.isnan(S[k]),np.nanmin(S[k])-1,S[k])  # failed docks ranked last
pr=lambda v: rankdata(v)/len(v); S['cons']=(pr(S['vina'])+pr(S['ifp']))/2
rng=np.random.default_rng(9); S['random']=rng.random(len(y))
def ef(y,s,f=0.05):
    n=int(round(f*len(y))); o=np.argsort(-s,kind='stable')[:n]; return y[o].mean()/y.mean()
def bedroc(y,s,a=20.0):
    N=len(y);n=y.sum();r=np.argsort(np.argsort(-s,kind='stable'))[y==1]+1;Ra=n/N
    rie=np.sum(np.exp(-a*r/N))/(n*(1-np.exp(-a))/(N*(np.exp(a/N)-1)))
    return rie*Ra*np.sinh(a/2)/(np.cosh(a/2)-np.cosh(a/2-a*Ra))+1/(1-np.exp(a*(1-Ra)))
M={k:{'auroc':roc_auc_score(y,v),'ef5':ef(y,v),'bedroc20':bedroc(y,v)} for k,v in S.items()}
pos=np.where(y==1)[0];neg=np.where(y==0)[0];B={}
for a,b in [('cons','vina'),('cons','2d'),('ifp','vina')]:
    d=[];e=[]
    for _ in range(2000):
        i=np.concatenate([rng.choice(pos,len(pos)),rng.choice(neg,len(neg))])
        d.append(roc_auc_score(y[i],S[a][i])-roc_auc_score(y[i],S[b][i]))
    B[a+'-'+b]={'dAUROC':M[a]['auroc']-M[b]['auroc'],'ci95':[float(np.percentile(d,2.5)),float(np.percentile(d,97.5))]}
G={'G1':B['cons-vina']['dAUROC']>=0.05 and B['cons-vina']['ci95'][0]>0,'G2':M['cons']['ef5']>=1.5*M['vina']['ef5'],'G3':B['cons-2d']['ci95'][0]>0}
out={'n':len(y),'n_act':int(y.sum()),'dock_fail':int(sum(np.isnan(r[2]) for r in rows)),'site_residues':res,'metrics':M,'bootstrap':B,'gates':G}
json.dump(out,open('../results/metrics.json','w'),indent=1,default=float)
with open('../results/per_compound.tsv','w') as f:
    f.write('id\tlabel\tS_vina\tS_ifp\tS_2d\theavy_atoms\n')
    for r in rows: f.write('\t'.join(map(str,r))+'\n')
print(json.dumps({k:{m:round(v,3) for m,v in d.items()} for k,d in M.items()},indent=0)); print(B); print(G)
