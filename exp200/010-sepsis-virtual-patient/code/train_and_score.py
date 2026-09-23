import csv, numpy as np, json, pickle
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
def load(path):
    rows=list(csv.reader(open(path)))
    hdr=rows[0]; pids=[]; y=[]; X=[]
    for r in rows[1:]:
        pids.append(r[0]); X.append([float(v) if v not in('nan','') else np.nan for v in r[1:-1]]); y.append(int(r[-1]))
    return hdr[1:-1],np.array(X,dtype=np.float32),np.array(y),pids
cols,XA,yA,pidA=load('results/features_A.csv')
_,XB,yB,pidB=load('results/features_B.csv')
print('A',XA.shape,'B',XB.shape)
Xtr,Xval,ytr,yval=train_test_split(XA,yA,test_size=0.2,random_state=42,stratify=yA)
m=HistGradientBoostingClassifier(max_iter=400,learning_rate=0.06,early_stopping=True,validation_fraction=0.15,random_state=42)
m.fit(Xtr,ytr)
pval=m.predict_proba(Xval)[:,1]
aucA=roc_auc_score(yval,pval); apA=average_precision_score(yval,pval)
print('A-val AUROC %.4f AUPRC %.4f'%(aucA,apA))
# ---- single frozen pass on set B ----
pB=m.predict_proba(XB)[:,1]
aucB=roc_auc_score(yB,pB); apB=average_precision_score(yB,pB)
ibase=cols.index('SIRS'); iqs=cols.index('qSOFA'); inews=cols.index('NEWS'); isofa=cols.index('SOFA_partial')
baseB={n:roc_auc_score(yB,XB[:,i]) for n,i in [('SIRS',ibase),('qSOFA',iqs),('NEWS',inews),('SOFA_partial',isofa)]}
baseA={n:roc_auc_score(yval,Xval[:,i]) for n,i in [('SIRS',ibase),('qSOFA',iqs),('NEWS',inews),('SOFA_partial',isofa)]}
print('B AUROC %.4f AUPRC %.4f  drop %.4f'%(aucB,apB,aucA-aucB))
print('baselines B:',{k:round(v,4) for k,v in baseB.items()})
print('baselines A-val:',{k:round(v,4) for k,v in baseA.items()})
best=max(baseB.values())
out={'aucA_val':aucA,'apA_val':apA,'aucB':aucB,'apB':apB,'drop':aucA-aucB,'baselines_B':baseB,'baselines_Aval':baseA,
     'G1_pass':bool(aucB>best),'G2_pass':bool(aucB>=0.75 and (aucA-aucB)<=0.08)}
json.dump(out,open('results/gate_scores.json','w'),indent=1)
print('G1(model>best baseline):',out['G1_pass'],' G2(frozen B):',out['G2_pass'])
# permutation importance on A-val (for G3 interpretation)
imp=permutation_importance(m,Xval,yval,n_repeats=3,random_state=42,scoring='roc_auc')
order=np.argsort(-imp.importances_mean)[:15]
json.dump([(cols[i],float(imp.importances_mean[i])) for i in order],open('results/top_features.json','w'),indent=1)
print('top features:',[cols[i] for i in order[:10]])
# save model + frozen-B predictions (for CLI and audit)
pickle.dump({'model':m,'cols':cols},open('results/model.pkl','wb'))
with open('results/preds_B.csv','w') as f:
    f.write('pid,label,risk\n')
    for p,l,s in zip(pidB,yB,pB): f.write(f'{p},{l},{s:.6f}\n')
