"""P19-03: split / Mondrian / similarity-weighted conformal DTI classification on DAVIS.
Run: python3 tool/conformal.py results/results.json   (data: DeepDTA DAVIS files in /tmp/davis; numpy, sklearn, rdkit)"""
import json, pickle, sys, zlib, numpy as np
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem
from sklearn.ensemble import HistGradientBoostingClassifier
DATA='/tmp/davis'; ALPHA=0.10
prots=json.load(open(f'{DATA}/proteins.txt')); ligs=json.load(open(f'{DATA}/ligands_can.txt'))
Y=pickle.load(open(f'{DATA}/Y','rb'),encoding='latin1'); pKd=-np.log10(Y/1e9)
pk=list(prots); lk=list(ligs); P,L=len(pk),len(lk)
AA='ACDEFGHIKLMNPQRSTVWY'
def seqfeat(s,dim=64):
    v=np.zeros(len(AA)+dim)
    for a in s:
        if a in AA: v[AA.index(a)]+=1
    for i in range(len(s)-2): v[len(AA)+zlib.crc32(s[i:i+3].encode())%dim]+=1
    return v/max(v.sum(),1)
PF=np.array([seqfeat(prots[k]) for k in pk])
mols=[Chem.MolFromSmiles(ligs[k]) for k in lk]; FPS=[AllChem.GetMorganFingerprintAsBitVect(m,2,nBits=512) for m in mols]
LF=np.array([list(f) for f in FPS],dtype=np.float32)
rows=np.array([(l,p) for l in range(L) for p in range(P)]); y=np.array([int(pKd[l,p]>=7.0) for l,p in rows])
X=np.hstack([PF[rows[:,1]],LF[rows[:,0]]]).astype(np.float32)
PN=PF/np.linalg.norm(PF,axis=1,keepdims=True); PSIM=PN@PN.T
LSIM=np.array([DataStructs.BulkTanimotoSimilarity(f,FPS) for f in FPS])
def split(kind,rng):
    if kind=='random':
        idx=rng.permutation(len(rows)); a,b=int(.6*len(idx)),int(.8*len(idx)); return idx[:a],idx[a:b],idx[b:]
    ax=0 if kind=='cold_drug' else 1; n=L if ax==0 else P; perm=rng.permutation(n); a,b=int(.6*n),int(.8*n)
    tr,ca,te=set(perm[:a]),set(perm[a:b]),set(perm[b:])
    return [np.where([r[ax] in s for r in rows])[0] for s in (tr,ca,te)]
def qhat(scores,alpha=ALPHA):
    n=len(scores); k=int(np.ceil((n+1)*(1-alpha))); return np.sort(scores)[min(k,n)-1] if k<=n else np.inf
def wquant(scores,w,wtest,alpha=ALPHA):
    o=np.argsort(scores); s=scores[o]; ww=w[o]; tot=ww.sum()+wtest; c=np.cumsum(ww)/tot
    i=np.searchsorted(c,1-alpha); return s[i] if i<len(s) else np.inf
def evaluate(sets,yte,pred):
    cov=float(np.mean(sets[np.arange(len(yte)),yte])); size=sets.sum(1); low=size!=1; err=pred!=yte
    return {'coverage':cov,'mean_set_size':float(size.mean()),'frac_low_conf':float(low.mean()),'point_error_rate':float(err.mean()),
            'frac_errors_in_low_conf':float(low[err].mean()) if err.any() else None,'n_test':int(len(yte))}
def run(kind):
    rng=np.random.RandomState(0); tr,ca,te=split(kind,rng)
    clf=HistGradientBoostingClassifier(random_state=0,max_iter=300).fit(X[tr],y[tr])
    pc,pt=clf.predict_proba(X[ca]),clf.predict_proba(X[te]); pred=pt.argmax(1)
    sc=1-pc[np.arange(len(ca)),y[ca]]; q=qhat(sc); sets=(1-pt)<=q
    out={'n_train':int(len(tr)),'base_rate_test':float(y[te].mean()),'split_conformal':evaluate(sets,y[te],pred),'qhat':float(q)}
    qm={c:qhat(sc[y[ca]==c]) for c in (0,1)}; setsm=np.stack([(1-pt[:,c])<=qm[c] for c in (0,1)],1)
    out['mondrian']=evaluate(setsm,y[te],pred)
    if kind!='random' and out['split_conformal']['coverage']<0.85:
        ax=0 if kind=='cold_drug' else 1; S=LSIM if ax==0 else PSIM; sw=[]
        cal_items=rows[ca][:,ax]
        for j,i in enumerate(te):
            w=np.exp(S[rows[i][ax],cal_items]/0.1); qq=wquant(sc,w,np.exp(1/0.1)); sw.append((1-pt[j])<=qq)
        out['weighted_pivot']=evaluate(np.array(sw),y[te],pred)
    return out
res={'alpha':ALPHA,'label':'pKd>=7','n_pairs':int(len(rows)),'positive_rate':float(y.mean())}
for k in ('random','cold_drug','cold_target'): res[k]=run(k); print(k,json.dumps(res[k]),flush=True)
c=res['random']['split_conformal']['coverage']
res['G1']={'coverage':c,'pass':bool(abs(c-0.9)<=0.02)}
g2={k:res[k]['split_conformal']['frac_errors_in_low_conf'] for k in ('cold_drug','cold_target')}
res['G2']={'frac_errors_in_low_conf':g2,'coverage_loss':{k:0.9-res[k]['split_conformal']['coverage'] for k in g2},
           'pass':bool(all(v is not None and v>=0.7 for v in g2.values()))}
res['G3']={'verdict':'NOT EVALUABLE - no post-cutoff ChEMBL release fetchable (A7)','pass':None}
json.dump(res,open(sys.argv[1],'w'),indent=1); print(json.dumps({k:res[k] for k in ('G1','G2')}))
