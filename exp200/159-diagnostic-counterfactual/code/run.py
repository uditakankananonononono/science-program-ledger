import sys,re,gzip,json,numpy as np,pandas as pd
sys.path.insert(0,'code');import geo
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from scipy.stats import hypergeom
d,m=geo.load('GSE87466');A=geo.genes(d,'GPL13158');yA=np.array([0 if 'Normal' in x else 1 for x in m])
d,m=geo.load('GSE38713');B=geo.genes(d,'GPL570');kB=np.array(['non-involved' not in x for x in m]);yB=np.array([1 if 'active disease (involved' in x else 0 for x in m])
B=B.iloc[:,kB];yB=yB[kB]
d,m=geo.load('GSE16879');Cx=geo.genes(d,'GPL570')
t=[x.strip().strip('"') for x in [l for l in gzip.open('data/GSE16879.txt.gz','rt') if l.startswith('!Sample_title')][0].split('\t')[1:]]
U=sorted(set(A.index)&set(B.index)&set(Cx.index));print('genes',len(U))
A,B,Cx=[z.loc[U].rank(pct=True) for z in (A,B,Cx)]
mu=A.mean(1).values;sd=A.std(1).values+1e-9
clf=LogisticRegression(penalty='l1',C=0.1,solver='liblinear',max_iter=5000).fit(((A.values.T-mu)/sd),yA)
w=clf.coef_[0];b=clf.intercept_[0];nz=np.flatnonzero(w);print('nonzero',len(nz))
def lg(v): return ((v-mu)/sd)@w+b
aucM=roc_auc_score(yB,[lg(B.values[:,i]) for i in range(B.shape[1])])
aucC=roc_auc_score(yB,B.loc[['S100A8','S100A9']].mean().values)
G1=bool(aucM>=0.90 and aucM>=aucC-0.02);print('G1',aucM,aucC,G1)
H=A.values[:,yA==0].mean(1)
def cf(v):
    v=v.copy();z=lg(v);order=[];
    gain={j:w[j]*(v[j]-H[j])/sd[j] for j in nz};gain={j:g for j,g in gain.items() if g>0}
    for j in sorted(gain,key=lambda j:-gain[j]):
        if z<0: break
        z-=gain[j];v[j]=H[j];order.append(j)
    return order,z
imp=[j for j in sorted(nz,key=lambda j:-abs(w[j]))][:10]
pairs={}
for i,s in enumerate(t):
    mm=re.match(r'(UC|CDc)(R|NR)(\d+)_(before|after)T',s)
    if mm: pairs.setdefault((mm.group(1),mm.group(2),mm.group(3)),{})[mm.group(4)]=i
pairs={k:v for k,v in pairs.items() if len(v)==2};print('pairs',len(pairs),sum(k[1]=='R' for k in pairs))
def prec(genes,dirs,pre,post): 
    dv=post-pre;return float(np.mean([np.sign(dv[j])==dd for j,dd in zip(genes,dirs)])) if len(genes) else np.nan
rows=[];CF={}
for k,v in pairs.items():
    pre=Cx.values[:,v['before']];post=Cx.values[:,v['after']];o,_=cf(pre);top=o[:10]
    dirs=[np.sign(H[j]-pre[j]) for j in top];CF[k]=(top,dirs)
    rows.append(dict(pt='_'.join(k),resp=k[1],p_pre=float(1/(1+np.exp(-lg(pre)))),p_post=float(1/(1+np.exp(-lg(post)))),n_cf=len(o),cf=prec(top,dirs,pre,post),imp=prec(imp,[-np.sign(w[j]) for j in imp],pre,post)))
R=pd.DataFrame(rows);R.to_csv('results/per_patient.tsv',sep='\t',index=False)
r=R[R.resp=='R'];print(R.groupby('resp')[['cf','imp','p_pre','p_post']].mean())
keys=[k for k in pairs if k[1]=='R'];rng=np.random.default_rng(0);nul=[]
for _ in range(2000):
    sh=rng.permutation(len(keys));vals=[]
    for a,bk in zip(keys,[keys[i] for i in sh]):
        pre=Cx.values[:,pairs[a]['before']];post=Cx.values[:,pairs[a]['after']];g,_d=CF[bk];vals.append(prec(g,[np.sign(H[j]-pre[j]) for j in g],pre,post))
    nul.append(np.nanmean(vals))
pn=float(np.mean(np.array(nul)>=r.cf.mean()))
G2=bool(r.cf.mean()>=0.70 and r.cf.mean()-r.imp.mean()>=0.10 and pn<0.05)
HS={s:set(l.strip() for l in open(f'data/{s}.grp') if l.strip() and not l.startswith(('#','HALLMARK'))) for s in ['HALLMARK_INFLAMMATORY_RESPONSE','HALLMARK_TNFA_SIGNALING_VIA_NFKB']}
un=sorted(set(U[j] for k in keys for j in CF[k][0]));enr={}
for s,S in HS.items():
    S=S&set(U);kk=len(S&set(un));enr[s]=dict(k=kk,n=len(un),genes=sorted(S&set(un)),p=float(hypergeom.sf(kk-1,len(U),len(S),len(un))))
G3=bool(min(e['p'] for e in enr.values())<0.01)
freq=pd.Series([U[j] for k in keys for j in CF[k][0]]).value_counts()
out=dict(G1=G1,auc_model=aucM,auc_calprotectin=aucC,n_nonzero=int(len(nz)),R_cf=r.cf.mean(),R_imp=r.imp.mean(),NR_cf=R[R.resp=='NR'].cf.mean(),NR_imp=R[R.resp=='NR'].imp.mean(),null_mean=float(np.mean(nul)),perm_p=pn,G2=G2,enrichment=enr,G3=G3,imp_genes=[U[j] for j in imp],cf_gene_freq=freq.head(20).to_dict())
json.dump(out,open('results/results.json','w'),indent=1,default=float);print(json.dumps(out,indent=1,default=float))
