import gzip,json,numpy as np,pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV,StratifiedKFold
from sklearn.metrics import roc_auc_score
from scipy.stats import rankdata
np.random.seed(0)
def load(g):
    ch=[];rows=[];inT=False
    for l in gzip.open(f'data/{g}_series_matrix.txt.gz','rt'):
        if l.startswith('!Sample_characteristics_ch1') or l.startswith('!Sample_source_name_ch1'): ch.append([x.strip('"') for x in l.rstrip('\n').split('\t')[1:]])
        if l.startswith('!series_matrix_table_begin'): inT=True;continue
        if l.startswith('!series_matrix_table_end'): break
        if inT: rows.append(l.rstrip('\n').split('\t'))
    df=pd.DataFrame([r[1:] for r in rows[1:]],index=[r[0].strip('"') for r in rows[1:]],columns=[c.strip('"') for c in rows[0][1:]]).apply(pd.to_numeric,errors='coerce')
    meta=[' | '.join(c[i] for c in ch) for i in range(df.shape[1])];return df,meta
def annot(p):
    m={};h=None
    for l in gzip.open(f'data/{p}.annot.gz','rt'):
        f=l.rstrip('\n').split('\t')
        if h is None:
            if f[0]=='ID': h=f.index('Gene symbol')
            continue
        if len(f)>h and f[h]: m[f[0]]=f[h]
    return m
def genes(df,p):
    m=annot(p);df=df.copy();df['g']=[m.get(i) for i in df.index];df=df[df['g'].notna()&~df['g'].astype(str).str.contains('///')]
    if df.drop(columns='g').max().max()>100: df.iloc[:,:-1]=np.log2(df.iloc[:,:-1].clip(lower=1))
    df['mm']=df.drop(columns='g').mean(1);df=df.sort_values('mm',ascending=False).drop_duplicates('g');return df.set_index('g').drop(columns='mm')
def lab(meta,g):
    y=[]
    for m in meta:
        s=m.lower()
        if g=='GSE63990': y.append(1 if 'infection_status: bacterial' in s else 0 if 'infection_status: viral' in s else None)
        elif g=='GSE42026': y.append(1 if 'bacterial' in s else 0 if ('h1n1' in s or 'rsv' in s) else None)
        elif g=='GSE40396':
            gg=[x for x in m.split(' | ') if x.lower().startswith('group:')][0].lower();y.append(1 if 'bacteria' in gg else None if 'control' in gg else 0)
        elif g=='GSE6269': y.append(0 if 'influenza' in s else None if 'healthy' in s else 1 if ('aureus' in s or 'pneumoniae' in s or 'coli' in s) else None)
        elif g=='GSE60244': y.append(1 if 'condition: bacteria' in s else 0 if 'condition: virus' in s else None)
        elif g=='GSE68004': y.append(1 if 'final condition: gas' in s else 0 if 'final condition: hadv' in s else None)
    return np.array([np.nan if v is None else v for v in y])
C=[('GSE63990','GPL571'),('GSE42026','GPL6947'),('GSE40396','GPL10558'),('GSE6269','GPL96'),('GSE60244','GPL10558'),('GSE68004','GPL10558')]
D={}
for g,p in C:
    df,meta=load(g);y=lab(meta,g);k=~np.isnan(y);X=genes(df,p).iloc[:,np.where(k)[0]];D[g]=(X,y[k].astype(int))
    print(g,X.shape,'bact',int(y[k].sum()),'vir',int((1-y[k]).sum()),flush=True)
common=sorted(set.intersection(*[set(v[0].index) for v in D.values()]));print('common',len(common),flush=True)
R=lambda X:np.apply_along_axis(lambda c:rankdata(c)/len(c),0,X.loc[common].values).T
XR={g:R(v[0]) for g,v in D.items()};Y={g:v[1] for g,v in D.items()}
def sw(X):
    def z(gl):
        gl=[g for g in gl if g in X.index];v=X.loc[gl];return ((v.T-v.mean(1))/v.std(1)).T
    return (z(['HK3','TNIP1','GPAA1','CTSB']).mean(0)-z(['IFI27','JUP','LAX1']).mean(0)).values
cv=StratifiedKFold(5,shuffle=True,random_state=0);res={};S={}
def fit(gs_):
    Xa=np.vstack([XR[g] for g in gs_]);ya=np.concatenate([Y[g] for g in gs_])
    return GridSearchCV(LogisticRegression(penalty='l1',solver='liblinear',max_iter=5000),{'C':[0.03,0.1,0.3,1]},cv=cv,scoring='roc_auc').fit(Xa,ya)
for h,_ in C:
    m=fit([g for g,_ in C if g!=h]);pm=m.predict_proba(XR[h])[:,1];ps=sw(D[h][0]);S[h]=(pm,ps)
    res[h]=dict(C=m.best_params_['C'],model=roc_auc_score(Y[h],pm),sweeney=roc_auc_score(Y[h],ps));print(h,res[h],flush=True)
diff=np.mean([res[h]['model']-res[h]['sweeney'] for h in res]);rng=np.random.default_rng(0);bs=[]
for _ in range(2000):
    dd=[]
    for h in res:
        y=Y[h];i1=np.where(y==1)[0];i0=np.where(y==0)[0];s=np.r_[rng.choice(i1,len(i1)),rng.choice(i0,len(i0))]
        dd.append(roc_auc_score(y[s],S[h][0][s])-roc_auc_score(y[s],S[h][1][s]))
    bs.append(np.mean(dd))
ci=[float(np.percentile(bs,2.5)),float(np.percentile(bs,97.5))]
G1=bool(diff>=0.02 and ci[0]>0);G2=bool(sum(res[h]['model']>=0.85 for h in res)>=5)
full=fit([g for g,_ in C]).best_estimator_;w=pd.Series(full.coef_[0],index=common);top=w[w!=0].sort_values(key=abs,ascending=False).head(20)
bact={'OLAH','ITGA7','VNN1','HPGD','MMP8','CD177','ANXA3','ARG1','HP','TNIP1','HK3'}
isg=[g for g in top.index if top[g]<0 and (g.startswith(('IFI','IFIT','OAS','MX','ISG','RSAD2','HERC5','XAF1','LAMP3','SIGLEC1','EPSTI1','USP18','CMPK2')))]
bb=[g for g in top.index if top[g]>0 and g in bact]
G3=bool(len(isg)>=1 and len(bb)>=1)
pub={'HK3','TNIP1','GPAA1','CTSB','IFI27','JUP','LAX1','IFI44L','FAM89A'};nom=[g for g in top.index if top[g]>0 and g not in pub][:1]
out=dict(loco=res,mean_diff=diff,ci=ci,G1=G1,G2=G2,G3=G3,top20={k:float(v) for k,v in top.items()},isg=isg,bact_side=bb,nomination=nom)
json.dump(out,open('results/results.json','w'),indent=1,default=float);print(json.dumps(out,indent=1,default=float))
