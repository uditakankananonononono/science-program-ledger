import pandas as pd,numpy as np,json
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold,cross_val_predict
from sklearn.metrics import roc_auc_score
df=pd.read_csv('../results/pair_scores.tsv.gz',sep='\t'); y=df.y.values
F=[c for c in df.columns if c not in('y','a','b')]; assert len(F)==13
q=cross_val_predict(make_pipeline(StandardScaler(),LogisticRegression(C=1.0,max_iter=1000)),df[F].values,y,cv=StratifiedKFold(5,shuffle=True,random_state=31),method='decision_function')
res={'features':F,'auroc_Q':roc_auc_score(y,q),'auroc_ResBMA_BP':roc_auc_score(y,df.ResBMA_BP),'auroc_simGIC_ALL':roc_auc_score(y,df.simGIC_ALL)}
rng=np.random.default_rng(31); ip=np.flatnonzero(y==1); ineg=np.flatnonzero(y==0); B=[]
for r in range(1000):
    ii=np.r_[rng.choice(ip,len(ip)),rng.choice(ineg,len(ineg))]; yy=y[ii]; a=roc_auc_score(yy,q[ii])
    B.append([a-roc_auc_score(yy,df.ResBMA_BP.values[ii]),a-roc_auc_score(yy,df.simGIC_ALL.values[ii])])
B=np.array(B); ci=lambda v:[float(x) for x in np.percentile(v,[2.5,97.5])]
res['p1']=res['auroc_Q']-res['auroc_ResBMA_BP']; res['ci_p1']=ci(B[:,0]); res['p2']=res['auroc_Q']-res['auroc_simGIC_ALL']; res['ci_p2']=ci(B[:,1])
res['pivot_gates']={'P1':bool(res['p1']>=0.03 and res['ci_p1'][0]>0),'P2':bool(res['p2']>=0.005 and res['ci_p2'][0]>0)}
json.dump(res,open('../results/pivot_metrics.json','w'),indent=1,default=float); print(json.dumps(res,indent=1,default=float))
