import pandas as pd,numpy as np,pathlib,json
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score,roc_auc_score
from sklearn.model_selection import GroupKFold
B=pathlib.Path(__file__).resolve().parents[1]; d=pd.read_csv(B/'data/processed/residue_labels.csv'); E=np.load(B/'data/processed/esm2_embeddings.npy')
A=np.array(list('ARNDCQEGHILKMFPSTWYV')); m3={'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
aa=np.array([m3[x] for x in d.aa3]); O=(aa[:,None]==A).astype(float)
hydro={'A':1.8,'R':-4.5,'N':-3.5,'D':-3.5,'C':2.5,'Q':-3.5,'E':-3.5,'G':-.4,'H':-3.2,'I':4.5,'L':3.8,'K':-3.9,'M':1.9,'F':2.8,'P':-1.6,'S':-.8,'T':-.7,'W':-.9,'Y':-1.3,'V':4.2}
vol={'A':88.6,'R':173.4,'N':114.1,'D':111.1,'C':108.5,'Q':143.8,'E':138.4,'G':60.1,'H':153.2,'I':166.7,'L':166.7,'K':168.6,'M':162.9,'F':189.9,'P':112.7,'S':89,'T':116.1,'W':227.8,'Y':193.6,'V':140}
charge={x:(1 if x in 'RK' else -1 if x in 'DE' else .1 if x=='H' else 0) for x in A}
polar=set('RNDQEKHSTY'); aromatic=set('FWY')
P=np.array([[hydro[x],vol[x],charge[x],x in polar,x in aromatic,x=='G',x=='P'] for x in aa],float); OP=np.c_[O,P]
y=d.label.values; groups=d.pdb_id.values; pids=sorted(d.pdb_id.unique()); Cs=[.01,.1,1,10]; rng=np.random.default_rng(13013)
def transform_fit(X,tr,te,kind):
 sc=StandardScaler().fit(X[tr]); a=sc.transform(X[tr]);b=sc.transform(X[te])
 if kind=='esm':
  pc=PCA(n_components=min(32,len(tr)-1),random_state=13013).fit(a);a=pc.transform(a);b=pc.transform(b)
 return a,b
def chooseC(X,tr,kind,yy):
 ug=np.unique(groups[tr]); k=min(4,len(ug)); cv=GroupKFold(k);scores={c:[] for c in Cs}
 for a,b in cv.split(tr,yy[tr],groups[tr]):
  ia,ib=tr[a],tr[b]; xa,xb=transform_fit(X,ia,ib,kind)
  for c in Cs:
   z=LogisticRegression(C=c,class_weight='balanced',max_iter=2000,random_state=13013).fit(xa,yy[ia]).predict_proba(xb)[:,1]
   for g in np.unique(groups[ib]):
    ix=np.where(groups[ib]==g)[0];scores[c].append(average_precision_score(yy[ib][ix],z[ix]))
 return max(Cs,key=lambda c:(np.mean(scores[c]),-c))
def run(X,kind,yy=y,label=None):
 out=[]
 for pid in pids:
  te=np.where(groups==pid)[0];tr=np.where(groups!=pid)[0];c=chooseC(X,tr,kind,yy);xa,xb=transform_fit(X,tr,te,kind)
  pr=LogisticRegression(C=c,class_weight='balanced',max_iter=2000,random_state=13013).fit(xa,yy[tr]).predict_proba(xb)[:,1]
  k=max(1,int(np.ceil(.1*len(te))));top=np.argsort(pr)[-k:]
  out.append({'pdb_id':pid,'model':label or kind,'n':len(te),'positives':int(yy[te].sum()),'prevalence':float(yy[te].mean()),'auprc':average_precision_score(yy[te],pr),'auroc':roc_auc_score(yy[te],pr),'recall_top10pct':float(yy[te][top].sum()/yy[te].sum()),'C':c})
 return out
allr=[]
for X,k in [(O,'onehot'),(OP,'physchem'),(E,'esm')]:allr+=run(X,k)
# shuffled context ablation, fixed once within protein
Es=E.copy()
for pid in pids:
 ix=np.where(groups==pid)[0];Es[ix]=Es[rng.permutation(ix)]
allr+=run(Es,'esm',label='esm_shuffled')
# random label control using ESM
yp=y.copy()
for pid in pids:
 ix=np.where(groups==pid)[0];yp[ix]=rng.permutation(yp[ix])
rr=run(E,'esm',yp)
for x in rr:x['model']='random_label_esm'
allr+=rr
r=pd.DataFrame(allr);r.to_csv(B/'results/per_protein_metrics.csv',index=False)
summary=r.groupby('model').agg(auprc_mean=('auprc','mean'),auprc_sd=('auprc','std'),auroc_mean=('auroc','mean'),recall_top10pct_mean=('recall_top10pct','mean'),prevalence_mean=('prevalence','mean')).reset_index()
# paired protein bootstrap differences
boot=[]
base=r[r.model=='onehot'].set_index('pdb_id').auprc; esm=r[r.model=='esm'].set_index('pdb_id').auprc; dif=(esm-base).values
vals=np.array([rng.choice(dif,len(dif),replace=True).mean() for _ in range(10000)])
summary.to_csv(B/'results/summary_metrics.csv',index=False)
obj={'esm_minus_onehot_mean':float(dif.mean()),'bootstrap_95_ci':[float(np.quantile(vals,.025)),float(np.quantile(vals,.975))],'success':bool(dif.mean()>=.05 and np.quantile(vals,.025)>0),'seed':13013,'resamples':10000}
(B/'results/primary_inference.json').write_text(json.dumps(obj,indent=2)+'\n')
print(summary.to_string(index=False));print(obj)
