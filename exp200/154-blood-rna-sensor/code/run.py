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
        else:
            gg=[x for x in m.split(' | ') if x.lower().startswith('group:')][0].lower()
            y.append(1 if 'bacteria' in gg else None if 'control' in gg else 0)
    return np.array([np.nan if v is None else v for v in y])
D={}
for g,p in [('GSE63990','GPL571'),('GSE42026','GPL6947'),('GSE40396','GPL10558')]:
    df,meta=load(g);y=lab(meta,g);k=~np.isnan(y);X=genes(df,p).iloc[:,np.where(k)[0]];D[g]=(X,y[k].astype(int))
    print(g,X.shape,'bacterial',int(y[k].sum()),'viral',int((1-y[k]).sum()),flush=True)
common=sorted(set.intersection(*[set(v[0].index) for v in D.values()]));print('common genes',len(common))
R=lambda X:np.apply_along_axis(lambda c:rankdata(c)/len(c),0,X.loc[common].values).T
Xtr,ytr=R(D['GSE63990'][0]),D['GSE63990'][1]
gs=GridSearchCV(LogisticRegression(penalty='l1',solver='liblinear',max_iter=5000),{'C':[0.03,0.1,0.3,1]},cv=StratifiedKFold(5,shuffle=True,random_state=0),scoring='roc_auc').fit(Xtr,ytr)
clf=gs.best_estimator_;w=pd.Series(clf.coef_[0],index=common);sel=w[w!=0].sort_values(key=abs,ascending=False)
print('C',gs.best_params_,'cv',round(gs.best_score_,3),'nsel',len(sel))
def z(X,gl):
    gl=[g for g in gl if g in X.index];v=X.loc[gl];return ((v.T-v.mean(1))/v.std(1)).T,gl
res={'C':gs.best_params_['C'],'cv_auroc':gs.best_score_,'n_selected':len(sel),'top_genes':{k:float(v) for k,v in sel.head(25).items()}}
pool={'m':[],'b1':[],'b2':[],'y':[]};miss={}
for g in ['GSE42026','GSE40396']:
    X,y=D[g];pm=clf.predict_proba(R(X))[:,1]
    zz,gl=z(X,['IFI44L','FAM89A']);b1=-(zz.loc['IFI44L']-zz.loc['FAM89A']).values if len(gl)==2 else np.zeros(len(y))
    up,gu=z(X,['HK3','TNIP1','GPAA1','CTSB']);dn,gd=z(X,['IFI27','JUP','LAX1']);b2=(up.mean(0)-dn.mean(0)).values
    miss[g]=dict(b1=gl,b2_up=gu,b2_dn=gd)
    res[g]=dict(n_bact=int(y.sum()),n_vir=int((1-y).sum()),model=roc_auc_score(y,pm),B1_Herberg=roc_auc_score(y,b1),B2_Sweeney=roc_auc_score(y,b2))
    for k,s in [('m',pm),('b1',b1),('b2',b2)]: pool[k]+=list(rankdata(s)/len(s))
    pool['y']+=list(y)
res['genes_used']=miss
P={k:np.array(v) for k,v in pool.items()};y=P['y']
pa={k:roc_auc_score(y,P[k]) for k in('m','b1','b2')};bb='b1' if pa['b1']>=pa['b2'] else 'b2'
rng=np.random.default_rng(0);i1=np.where(y==1)[0];i0=np.where(y==0)[0];d=[]
for _ in range(2000):
    s=np.concatenate([rng.choice(i1,len(i1)),rng.choice(i0,len(i0))]);d.append(roc_auc_score(y[s],P['m'][s])-roc_auc_score(y[s],P[bb][s]))
res['pooled']=dict(model=pa['m'],B1=pa['b1'],B2=pa['b2'],best_baseline=bb,diff=pa['m']-pa[bb],CI=[float(np.percentile(d,2.5)),float(np.percentile(d,97.5))])
res['G1']=bool(res['GSE42026']['model']>=0.85 and res['GSE40396']['model']>=0.85)
res['G2']=bool(res['pooled']['diff']>=0.02 and res['pooled']['CI'][0]>0)
print(json.dumps(res,indent=1));json.dump(res,open('results/main.json','w'),indent=1)
import pickle;pickle.dump((common,clf),open('results/model.pkl','wb'))
