# POST-HOC exploratory (not gated): jejunum score by timepoint; immediate-early genes
import sys,json,numpy as np;sys.path.insert(0,'code');import geo
from sklearn.metrics import roc_auc_score
r=json.load(open('results/results.json'));F=r['final_barcode']
d,m=geo.load('GSE37013');x=geo.genes(d,'GPL6947').rank(pct=True)
IE=['FOS','FOSB','EGR1','ATF3','JUN','IER3','KLF6','HBEGF','NR4A1']
t=['120 min' if '120 min' in s else '30 min' if '30 min' in s else 'isch' if 'ischaemia' in s else 'ctl' for s in m]
f=[g for g in F if g in x.index];ie=[g for g in IE if g in x.index]
for k in ['ctl','isch','30 min','120 min']:
    i=[j for j,v in enumerate(t) if v==k];print(k,'barcode',round(x[f].T.iloc[i].mean(1).mean(),3) if False else round(x.loc[f].iloc[:,i].mean().mean(),3),'IE',round(x.loc[ie].iloc[:,i].mean().mean(),3))
y=np.array([0 if v=='ctl' else 1 for v in t]);print('IE AUROC jejunum',round(roc_auc_score(y,x.loc[ie].mean()),3))
y2=[i for i,v in enumerate(t) if v in('ctl','120 min')];print('IE AUROC ctl vs 120',round(roc_auc_score(y[y2],x.loc[ie].iloc[:,y2].mean()),3))
