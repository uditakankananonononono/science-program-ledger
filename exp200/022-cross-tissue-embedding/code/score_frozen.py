import numpy as np, json, sys, torch, pickle, pandas as pd
sys.path.insert(0,'code')
from common import dev_mean_acc
import harmonypy as hm
torch.set_num_threads(2)
split=json.load(open('results/split.json')); dev=split['dev']; fz=split['frozen'][0]
classes=json.load(open('results/class_list.json'))
fz_=np.load(f'results/local/{fz}_fit.npz') if False else None
# frozen Z via dev-fitted transform
fit=np.load('results/local/dev_fit.npz'); hv,mu,sd=fit['hv'],fit['mu'],fit['sd']
import os
p=f'results/local/{fz}_log.npy'
if not os.path.exists(p):
    Xr=np.load(f'results/local/{fz}_X.npy')
    lib=Xr.sum(1,keepdims=True); lib[lib==0]=1
    Xr/=lib; Xr*=1e4; np.log1p(Xr,out=Xr); np.save(p,Xr); del Xr
X=np.load(p); Zf=((X[:,hv]-mu)/sd).astype(np.float32); del X
y={t: np.load(f'results/local/{t}_y.npy', allow_pickle=True) for t in dev+[fz]}
svd=pickle.load(open('results/local/svd.pkl','rb'))
Pf=svd.transform(Zf).astype(np.float32)
# AE arm (pure out-of-sample)
ck=torch.load('results/local/ae.pt')
enc=torch.nn.Sequential(torch.nn.Linear(2000,512), torch.nn.GELU(), torch.nn.Linear(512,128))
enc.load_state_dict(ck['enc']); enc.eval()
Zdev={t: np.load(f'results/local/{t}_Z.npy') for t in dev}
with torch.no_grad():
    Edev={t: enc(torch.from_numpy(Zdev[t])).numpy().astype(np.float32) for t in dev}
    Ef=enc(torch.from_numpy(Zf)).numpy().astype(np.float32)
E=dict(Edev); E[fz]=Ef
acc_ae, per_ae = dev_mean_acc(E, y, classes, [fz])
# Harmony arm (unsupervised refit incl. frozen cells, per integration-benchmark practice)
Pdev={t: svd.transform(Zdev[t]).astype(np.float32) for t in dev}
Xall=np.vstack([Pdev[t] for t in dev]+[Pf])
meta=pd.DataFrame({'tissue': np.concatenate([[t]*len(Pdev[t]) for t in dev]+[[fz]*len(Pf)])})
ho=hm.run_harmony(Xall, meta, ['tissue'], random_state=7, verbose=False)
Z=ho.Z_corr; H=Z.T if Z.shape[0]==Xall.shape[1] else Z
i=0; Hdict={}
for t in dev+[fz]:
    Hdict[t]=H[i:i+(len(Pdev[t]) if t in dev else len(Pf))].astype(np.float32)
    i+=len(Pdev[t]) if t in dev else len(Pf)
acc_h, per_h = dev_mean_acc(Hdict, y, classes, [fz])
# PCA-only context
P=dict(Pdev); P[fz]=Pf
acc_p, per_p = dev_mean_acc(P, y, classes, [fz])
out={'ae':{'acc':acc_ae,'detail':per_ae},'harmony':{'acc':acc_h,'detail':per_h},'pca_only':{'acc':acc_p,'detail':per_p},
     'note':'Harmony refit unsupervised incl frozen cells (scIB practice); AE is pure out-of-sample transform'}
json.dump(out, open('results/frozen_scores.json','w'), indent=1)
ae_dev=json.load(open('results/ae_scores.json'))['mean']; h_dev=json.load(open('results/baseline_scores.json'))['harmony']['mean']
print('FROZEN Spleen: AE', round(acc_ae,4), '| Harmony', round(acc_h,4), '| PCA', round(acc_p,4))
print('G3a winner-stability: AE frozen', round(acc_ae,4), '>= dev-0.05 =', round(ae_dev-0.05,4), '->', 'PASS' if acc_ae>=ae_dev-0.05 else 'FAIL')
print('G3b vs Harmony frozen: AE', round(acc_ae,4), '>= Harmony_frozen-0.03 =', round(acc_h-0.03,4), '->', 'PASS' if acc_ae>=acc_h-0.03 else 'FAIL')
