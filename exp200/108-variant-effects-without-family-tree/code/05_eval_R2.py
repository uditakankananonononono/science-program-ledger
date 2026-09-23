import pandas as pd, numpy as np, json, sys
sys.path.insert(0,'code')
from sklearn.metrics import roc_auc_score as A
exec(open('code/04_eval.py').read().split("y=e.label.values")[0].replace("results/scores.tsv","results/scores_R2.tsv"))
T=0.9071
c=e[e.site_entropy<=T].copy(); y=c.label.values
out={'n_R2':int(len(e)),'n_conf':int(len(c)),'coverage':len(c)/len(e),'pos_conf':int(y.sum())}
out['auc_conf_esm']=A(y,-c.s_esm); out['auc_conf_blosum']=A(y,-c.s_blosum)
out['auc_all_esm']=A(e.label,-e.s_esm); out['auc_all_blosum']=A(e.label,-e.s_blosum)
out['auc_nonconf_esm']=A(e.label[e.site_entropy>T],-e.s_esm[e.site_entropy>T])
rng=np.random.default_rng(2); genes=c.gene.unique(); gi={g:np.where(c.gene.values==g)[0] for g in genes}
b1=[];bd=[]
for _ in range(1000):
    idx=np.concatenate([gi[g] for g in rng.choice(genes,len(genes))]); yy=y[idx]
    if yy.min()==yy.max(): continue
    a=A(yy,-c.s_esm.values[idx]); b1.append(a); bd.append(a-A(yy,-c.s_blosum.values[idx]))
out['auc_conf_ci']=list(np.percentile(b1,[2.5,97.5])); out['diff_conf_ci']=list(np.percentile(bd,[2.5,97.5]))
out['H1']=bool(out['auc_conf_esm']>=0.75 and out['auc_conf_ci'][0]>=0.70 and out['coverage']>=0.20)
out['H2']=bool(out['auc_conf_esm']-out['auc_conf_blosum']>=0.05 and out['diff_conf_ci'][0]>0)
json.dump(out,open('results/metrics_R2.json','w'),indent=1,default=float); print(json.dumps(out,indent=1,default=float))
e.to_csv('results/scores_R2_full.tsv',sep='\t',index=False)
