import numpy as np, pandas as pd, json
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import roc_auc_score
from scipy.stats import ttest_ind
exec(open('code/run.py').read().split('gmt={}')[0])
rng=np.random.default_rng(0)
X1,l1=load('GSE87466','GPL13158','!Sample_characteristics_ch1')
X2,l2=load('GSE38713','GPL570','!Sample_source_name_ch1')
X3,l3=load('GSE9452','GPL570','!Sample_characteristics_ch1')
G=sorted(set(X1.index)&set(X2.index)&set(X3.index))
R=lambda X: X.loc[G].rank(axis=0,pct=True)
R1,R2,R3=R(X1),R(X2),R(X3)
y1=np.array([1 if 'Ulcerative' in s else 0 for s in l1])
top=R1.var(axis=1).sort_values(ascending=False).index[:2000]
m=LogisticRegressionCV(Cs=10,cv=5,penalty='l1',solver='liblinear',scoring='roc_auc',max_iter=2000,random_state=0).fit(R1.loc[top].T.values,y1)
t=ttest_ind(R1.loc[top].T.values[y1==1],R1.loc[top].T.values[y1==0]).statistic; g1=top[np.argmax(np.abs(t))]; sgn=np.sign(t[np.argmax(np.abs(t))])
def ev(Rx,idx_case,idx_ctrl):
    Xs=Rx.loc[top].T.values; y=np.r_[np.ones(len(idx_case)),np.zeros(len(idx_ctrl))]; ii=np.r_[idx_case,idx_ctrl]
    p=m.predict_proba(Xs[ii])[:,1]; a=roc_auc_score(y,p); b1=roc_auc_score(y,sgn*Rx.loc[g1].values[ii])
    bs=[]
    for _ in range(1000):
        k=rng.integers(0,len(y),len(y))
        if len(set(y[k]))==2: bs.append(roc_auc_score(y[k],p[k]))
    return {'n_case':len(idx_case),'n_ctrl':len(idx_ctrl),'auc':float(a),'ci':[float(np.percentile(bs,2.5)),float(np.percentile(bs,97.5))],'one_gene_auc':float(b1)}
w=lambda l,s: np.where(np.char.find(l,s)>=0)[0]
c2=w(l2,'non-inflammatory control'); ni2=np.r_[w(l2,'remission'),w(l2,'non-involved')]; a2=w(l2,'active disease (involved')
c3=w(l3,'Control'); ni3=np.where((np.char.find(l3,'Ulcerative')>=0)&(np.char.find(l3,'no macroscopic')>=0))[0]; i3=w(l3,'inflammation vissible')
res={'n_genes_shared':len(G),'C':float(m.C_[0]),'n_selected':int((m.coef_!=0).sum()),'one_gene':g1,
 'E1_GSE38713_noninflamed':ev(R2,ni2,c2),'E2_GSE9452_noninflamed':ev(R3,ni3,c3),
 'sanity_GSE38713_active':ev(R2,a2,c2),'sanity_GSE9452_inflamed':ev(R3,i3,c3),
 'E1_remission_only':ev(R2,w(l2,'remission'),c2),'E1_noninvolved_only':ev(R2,w(l2,'non-involved'),c2)}
coef=pd.Series(m.coef_[0],index=top); res['selected_genes']=coef[coef!=0].sort_values(key=abs,ascending=False).round(3).to_dict()
print(json.dumps(res,indent=1)); json.dump(res,open('results/pivot2.json','w'),indent=1)
