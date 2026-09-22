from pathlib import Path
import pandas as pd,numpy as np,json,time
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression,Ridge
from sklearn.ensemble import RandomForestClassifier,HistGradientBoostingClassifier,RandomForestRegressor,HistGradientBoostingRegressor
from sklearn.metrics import roc_auc_score,average_precision_score,brier_score_loss,mean_squared_error
from sklearn.model_selection import StratifiedShuffleSplit,GroupShuffleSplit,ShuffleSplit,GroupKFold
from sklearn.feature_selection import SelectKBest,f_classif
R=Path(__file__).resolve().parents[2]; D=R/'experiment/data'; O=R/'experiment/results';O.mkdir(exist_ok=True)
rng=np.random.default_rng(20260921); rows=[]
def add(domain,config,model,split,metric,ntr,nte,extras={}):
 rows.append({'domain':domain,'config':config,'model':model,'split':split,'metric':float(metric),'n_train':ntr,'n_test':nte,**extras})
# diabetes: fixed practical feature set; IDs/outcome/postoutcome excluded
z=pd.read_csv(D/'diabetes.csv.gz',low_memory=False); y=z.target_30d.to_numpy(); groups=z.patient_nbr.to_numpy()
drop={'target_30d','readmitted','patient_nbr','encounter_id','encounter_order','discharge_disposition_id'}
X=z[[c for c in z.columns if c not in drop]].copy(); cat=X.select_dtypes(exclude=np.number).columns.tolist(); num=X.select_dtypes(include=np.number).columns.tolist()
prep=ColumnTransformer([('num',make_pipeline(SimpleImputer(strategy='median'),StandardScaler()),num),('cat',make_pipeline(SimpleImputer(strategy='most_frequent'),OneHotEncoder(handle_unknown='ignore',min_frequency=20)),cat)])
mods={'logistic':LogisticRegression(max_iter=1000,C=.2,class_weight='balanced',random_state=1)}
ss=StratifiedShuffleSplit(3,test_size=.25,random_state=11); gs=GroupShuffleSplit(3,test_size=.25,random_state=11)
for split,cv in [('naive',ss.split(X,y)),('rigorous_group',gs.split(X,y,groups))]:
 for rep,(tr,te) in enumerate(cv):
  for name,m in mods.items():
   pipe=make_pipeline(prep,m);t=time.time();pipe.fit(X.iloc[tr],y[tr]);p=pipe.predict_proba(X.iloc[te])[:,1]
   add('diabetes',f'{split}_r{rep}',name,split,roc_auc_score(y[te],p),len(tr),len(te),{'ap':average_precision_score(y[te],p),'brier':brier_score_loss(y[te],p),'seconds':time.time()-t})
# Parkinson: random rows vs grouped subjects; normalized RMSE score = 1-RMSE/SD(test)
z=pd.read_csv(D/'parkinsons.csv.gz');y=z.total_UPDRS.to_numpy();groups=z.subject.to_numpy();X=z.drop(columns=['total_UPDRS','motor_UPDRS','subject'])
mods={'ridge':make_pipeline(StandardScaler(),Ridge(alpha=10)),'random_forest':RandomForestRegressor(n_estimators=200,min_samples_leaf=5,max_features=.7,n_jobs=-1,random_state=2)}
ss=ShuffleSplit(5,test_size=.25,random_state=22); gkf=GroupKFold(6)
for split,cv in [('naive',ss.split(X,y)),('rigorous_group',gkf.split(X,y,groups))]:
 for rep,(tr,te) in enumerate(cv):
  for name,m in mods.items():
   t=time.time();m.fit(X.iloc[tr],y[tr]);p=m.predict(X.iloc[te]);rmse=mean_squared_error(y[te],p)**.5; score=1-rmse/np.std(y[te])
   add('parkinsons',f'{split}_r{rep}',name,split,score,len(tr),len(te),{'rmse':rmse,'seconds':time.time()-t})
# breast: common genes, LOSO versus pooled random. fixed top-500 variance selected within training only.
B=D/'breast'; stems=['study_16446_GPL570_all','study_20194_GPL96_all','study_22226_GPL1708_all','study_22358_GPL5325_all','study_32646_GPL570_all']
xs=[];ys=[];co=[]
common=None
for s in stems:
 x=pd.read_csv(B/f'{s}__expression.csv',index_col=0); common=set(x.index) if common is None else common&set(x.index)
common=sorted(common)
for s in stems:
 x=pd.read_csv(B/f'{s}__expression.csv',index_col=0).loc[common].T; c=pd.read_csv(B/f'{s}__clinical.csv'); ok=c.pCR.notna().to_numpy(); xs.append(x.iloc[np.where(ok)[0]]);ys.extend(c.loc[ok,'pCR'].astype(int));co.extend([s]*ok.sum())
X=pd.concat(xs).reset_index(drop=True);y=np.asarray(ys);co=np.asarray(co)
def breast_fit(tr,te,name):
 pipe=make_pipeline(SimpleImputer(strategy='median'),StandardScaler(),SelectKBest(f_classif,k=500),LogisticRegression(max_iter=3000,C=.1,class_weight='balanced',random_state=3));pipe.fit(X.iloc[tr],y[tr]);p=pipe.predict_proba(X.iloc[te])[:,1];return roc_auc_score(y[te],p),average_precision_score(y[te],p),brier_score_loss(y[te],p)
for rep,(tr,te) in enumerate(StratifiedShuffleSplit(5,test_size=.25,random_state=33).split(X,y)):
 au,ap,br=breast_fit(tr,te,'logistic');add('breast',f'naive_r{rep}','logistic','naive',au,len(tr),len(te),{'ap':ap,'brier':br})
for rep,s in enumerate(stems):
 te=np.where(co==s)[0];tr=np.where(co!=s)[0];au,ap,br=breast_fit(tr,te,'logistic');add('breast',f'rigorous_{s}','logistic','rigorous_group',au,len(tr),len(te),{'ap':ap,'brier':br})
out=pd.DataFrame(rows);out.to_csv(O/'primary_results.csv',index=False)
summary=out.groupby(['domain','model','split']).metric.agg(['mean','std','count']).reset_index();summary.to_csv(O/'primary_summary.csv',index=False);print(summary.to_string(index=False))
