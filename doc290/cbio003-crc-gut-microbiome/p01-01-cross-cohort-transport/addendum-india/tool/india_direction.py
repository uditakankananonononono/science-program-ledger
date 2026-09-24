#!/usr/bin/env python3
"""P01-01 addendum (parent-approved 2026-09-24): transport to/from the open Indian CRC cohort.
Locked before results (lock evidence = the commit that adds this file, before results/ exists):
Data: curatedMetagenomicData 2021-03-31, 10 stool CRC cohorts incl. GuptaA_2019 (India, 30/30);
  ThomasAM_2019_c excluded (duplicate of YachidaS_2019, project QC rule). Genus = species summed by
  the first name token (MetaPhlAn2), relative abundance. Different profiler from the main P01-01
  benchmark (mOTU), so numbers are not pooled with the main report.
Main P01-01 gates G1-G3: rerun unchanged with tool/crc_transport_audit.py (identical copy).
Addendum gates:
  A1 (others -> India): held-out GuptaA_2019 LOCO AUC from the unchanged tool >= 0.75.
  A2 (India -> others, the parent's direction): RF (500 trees, balanced, seed 7 - parent recipe)
     trained on GuptaA_2019 only, scored on each of the other 9 cohorts; mean AUC >= 0.75.
  Reported, no gate: India within-cohort 5-fold CV AUC (compare with the parent's 0.992).
Usage: python3 india_direction.py <data_dir> <results_dir>
"""
import sys, os, json
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import roc_auc_score
SEED=7; data,out=sys.argv[1],sys.argv[2]; os.makedirs(out,exist_ok=True)
X=pd.read_csv(os.path.join(data,'genus_matrix.csv'),index_col=0); M=pd.read_csv(os.path.join(data,'samples.csv'),index_col=0); X=X.loc[M.index]
y=(M.label=='CRC').astype(int).values; coh=M.cohort.values; IN='GuptaA_2019'
def rf(): return RandomForestClassifier(500,class_weight='balanced',random_state=SEED,n_jobs=2)
mi=coh==IN
cv=float(roc_auc_score(y[mi],cross_val_predict(rf(),X.values[mi],y[mi],cv=StratifiedKFold(5,shuffle=True,random_state=SEED),method='predict_proba')[:,1]))
m=rf().fit(X.values[mi],y[mi])
a2={c:float(roc_auc_score(y[coh==c],m.predict_proba(X.values[coh==c])[:,1])) for c in sorted(set(coh)) if c!=IN}
res={'india_within_cv_auc':cv,'A2_india_to_others':a2,'A2_mean':float(np.mean(list(a2.values()))),'A2_pass':bool(np.mean(list(a2.values()))>=0.75)}
json.dump(res,open(os.path.join(out,'india_direction.json'),'w'),indent=1); print(json.dumps(res,indent=1))
