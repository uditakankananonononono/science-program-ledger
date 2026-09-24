import sys,json,numpy as np,pandas as pd
from sklearn.metrics import roc_auc_score
from scipy.stats import norm,hypergeom
sys.path.insert(0,'code'); import geo

def lab(meta,inj,ctl,excl=()):
    y=[]
    for m in meta:
        if any(e in m for e in excl): y.append(None)
        elif any(i in m for i in inj): y.append(1)
        elif any(c in m for c in ctl): y.append(0)
        else: y.append(None)
    return np.array(y,dtype=object)
C={}
d,m=geo.load('GSE30718');C['kidney']=(geo.genes(d,'GPL570'),lab(m,['AKI'],['protocol','Nephrectomy']))
d,m=geo.load('GSE38941');C['liver']=(geo.genes(d,'GPL570'),lab(m,['acute liver failure'],['normal']))
d,m=geo.load('GSE28914');C['skin']=(geo.genes(d,'GPL570'),lab(m,['3rd post','7th post'],['intact'],['acute wound']))
d,m=geo.load('GSE37013');C['jejunum']=(geo.genes(d,'GPL6947'),lab(m,['ischaemia'],['Control']))
e=pd.read_csv('data/GSE139061_QN.csv.gz',index_col=0);e=e[~e.index.duplicated()]
C_ext=(e,np.array([1 if c.startswith('AKI') else 0 for c in e.columns],dtype=object))
for k,(x,y) in C.items(): print(k,x.shape,sum(y==1),sum(y==0))
print('ext',e.shape,sum(C_ext[1]==1),sum(C_ext[1]==0))
U=set.intersection(*[set(x.index) for x,_ in C.values()])&set(e.index);U=sorted(U);print('shared genes',len(U))
def prep(x,y):
    k=np.array([v is not None for v in y]);x=x.loc[U].iloc[:,k].rank(pct=True);return x,y[k].astype(int)
C={k:prep(*v) for k,v in C.items()};E=prep(*C_ext)
def cd(x,y):
    a=x.values[:,y==1];b=x.values[:,y==0];s=np.sqrt((a.var(1,ddof=1)+b.var(1,ddof=1))/2)+1e-9
    return pd.Series((a.mean(1)-b.mean(1))/s,index=x.index)
def bar(tr,K=25,perm=None):
    D=pd.DataFrame({k:cd(C[k][0],C[k][1] if perm is None else perm[k]) for k in tr})
    z=D.sum(1)/np.sqrt(len(tr));z=z[(D>0).all(1)];return list(z.sort_values(ascending=False).index[:K])
def auc(x,y,g):
    g=[i for i in g if i in x.index];return roc_auc_score(y,x.loc[g].mean(0)) if g else np.nan
HS={s:[l.strip() for l in open(f'data/{s}.grp') if l.strip() and not l.startswith(('#','HALLMARK'))] for s in ['HALLMARK_INFLAMMATORY_RESPONSE','HALLMARK_TNFA_SIGNALING_VIA_NFKB','HALLMARK_P53_PATHWAY','HALLMARK_HYPOXIA','HALLMARK_UNFOLDED_PROTEIN_RESPONSE','HALLMARK_APOPTOSIS']}
B1=HS['HALLMARK_INFLAMMATORY_RESPONSE'];B2=HS['HALLMARK_TNFA_SIGNALING_VIA_NFKB']
R={};org=list(C)
for h in org:
    g=bar([o for o in org if o!=h]);x,y=C[h]
    rnd=[auc(x,y,list(np.random.default_rng(i).choice(U,25,replace=False))) for i in range(1000)]
    R[h]=dict(barcode=auc(x,y,g),B1=auc(x,y,B1),B2=auc(x,y,B2),rand_p=float(np.mean(np.array(rnd)>=auc(x,y,g))),genes=g)
    print(h,{k:(round(v,3) if isinstance(v,float) else v[:8]) for k,v in R[h].items()})
mb=np.mean([R[h]['barcode'] for h in org]);mbest=max(np.mean([R[h]['B1'] for h in org]),np.mean([R[h]['B2'] for h in org]))
wins=sum(R[h]['barcode']>=max(R[h]['B1'],R[h]['B2']) for h in org)
G1=bool(mb>=0.80 and mb-mbest>=0.05 and wins>=3)
# label-permutation null for LOOO pipeline
pn=[]
for i in range(50):
    rg=np.random.default_rng(100+i);P={k:rg.permutation(C[k][1]) for k in org}
    pn.append(np.mean([auc(*C[h],bar([o for o in org if o!=h],perm=P)) for h in org]))
F=bar(org);x,y=E
ext=dict(barcode=auc(x,y,F),B1=auc(x,y,B1),B2=auc(x,y,B2))
G2=bool(ext['barcode']>=0.75 and ext['barcode']>=max(ext['B1'],ext['B2']))
enr={}
for s in ['HALLMARK_TNFA_SIGNALING_VIA_NFKB','HALLMARK_P53_PATHWAY','HALLMARK_HYPOXIA','HALLMARK_UNFOLDED_PROTEIN_RESPONSE','HALLMARK_APOPTOSIS']:
    S=set(HS[s])&set(U);k=len(S&set(F));enr[s]=dict(overlap=k,genes=sorted(S&set(F)),p=float(hypergeom.sf(k-1,len(U),len(S),len(F))))
G3=bool(min(v['p'] for v in enr.values())<0.01)
out=dict(LOOO=R,mean_barcode=mb,mean_best_baseline=mbest,wins=int(wins),perm_null_mean=float(np.mean(pn)),perm_null_p=float(np.mean(np.array(pn)>=mb)),final_barcode=F,external=ext,enrichment=enr,G1=G1,G2=G2,G3=G3)
json.dump(out,open('results/results.json','w'),indent=1,default=float)
print(json.dumps({k:v for k,v in out.items() if k!='LOOO'},indent=1,default=float))
