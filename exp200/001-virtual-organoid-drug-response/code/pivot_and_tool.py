#!/usr/bin/env python3
import json, time, pickle
import numpy as np, pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold, KFold
t0=time.time()
gdsc = pd.read_excel('data/GDSC2.xlsx', usecols=['SANGER_MODEL_ID','DRUG_NAME','TCGA_DESC','LN_IC50']).dropna(subset=['SANGER_MODEL_ID','LN_IC50'])
model = pd.read_csv('data/Model.csv')
smap = model.dropna(subset=['SangerModelID']).drop_duplicates('SangerModelID').set_index('SangerModelID')['ModelID']
gdsc['ModelID'] = gdsc['SANGER_MODEL_ID'].map(smap)
panel = json.load(open('results/gate_summary.json'))['panel']
gdsc = gdsc[gdsc.DRUG_NAME.isin(panel)]
ids = sorted(set(gdsc.ModelID.dropna()))
# pre-filter expression to needed lines
hdr = pd.read_csv('data/expression.csv', nrows=0); genes=list(hdr.columns[1:])
dt = {c: np.float32 for c in genes}
chunks=[c for c in pd.read_csv('data/expression.csv', index_col=0, chunksize=200, dtype=dt) if len(c)]
expr = pd.concat(chunks); expr.index.name='ModelID'
expr = expr.loc[expr.index.isin(ids)]
ALPHAS=[0.1,1.0,10.0,100.0,1000.0]
def inner_alpha(X,y):
    best_a,best=ALPHAS[0],np.inf
    ikf=KFold(3,shuffle=True,random_state=1)
    for a in ALPHAS:
        ms=[np.mean((Ridge(alpha=a).fit(X[itr],y[itr]).predict(X[ite])-y[ite])**2) for itr,ite in ikf.split(X)]
        if np.mean(ms)<best: best,best_a=np.mean(ms),a
    return best_a
rows=[]; tool_models={}
allz=[]  # for abstention threshold: standardized training vectors
for drug in panel:
    d = gdsc[gdsc.DRUG_NAME==drug]
    lin = d.groupby('ModelID')['TCGA_DESC'].agg(lambda s: s.mode().iat[0] if len(s.mode()) else 'UNK')
    y = d.groupby('ModelID')['LN_IC50'].mean()
    common = y.index.intersection(expr.index)
    y = y.loc[common].values; lin = lin.loc[common].values
    X = expr.loc[common].values
    gkf = GroupKFold(5)
    oof_e = np.zeros(len(y)); oof_l = np.zeros(len(y)); oof_b = np.zeros(len(y))
    for tr,te in gkf.split(X,y,groups=common):
        v = X[tr].var(0); top=np.argsort(v)[-2000:]
        Xtr,Xte = X[tr][:,top], X[te][:,top]
        mu,sd = Xtr.mean(0), Xtr.std(0)+1e-8
        Xtr,Xte=(Xtr-mu)/sd,(Xte-mu)/sd
        a = inner_alpha(Xtr,y[tr])
        oof_e[te] = Ridge(alpha=a).fit(Xtr,y[tr]).predict(Xte)
        Ltr = pd.get_dummies(lin[tr]).values.astype(np.float32)
        Lte = pd.get_dummies(lin[te]).reindex(columns=pd.get_dummies(lin[tr]).columns, fill_value=0).values.astype(np.float32)
        oof_l[te] = Ridge(alpha=10.0).fit(Ltr,y[tr]).predict(Lte)
        oof_b[te] = y[tr].mean()
    rm = lambda p: float(np.sqrt(np.mean((p-y)**2)))
    re_, rl, rb = rm(oof_e), rm(oof_l), rm(oof_b)
    rows.append(dict(drug=drug, expr_red=1-re_/rb, lin_red=1-rl/rb, margin=(1-re_/rb)-(1-rl/rb)))
    # final tool model on all data
    v = X.var(0); top=np.argsort(v)[-2000:]
    Xa = X[:,top]; mu,sd = Xa.mean(0), Xa.std(0)+1e-8
    Za=(Xa-mu)/sd
    a = inner_alpha(Za,y)
    m = Ridge(alpha=a).fit(Za,y)
    tool_models[drug]=dict(genes=[genes[i] for i in top], mu=mu, sd=sd, coef=m.coef_, intercept=float(m.intercept_))
    allz.append(Za)
Z = np.concatenate(allz)
cent = Z.mean(0); Zc = Z-cent
cov = np.cov(Zc.T) + 1e-3*np.eye(Zc.shape[1])
prec = np.linalg.pinv(cov)
dists = np.einsum('ij,jk,ik->i', Zc, prec, Zc)
thr = float(np.quantile(dists, 0.95))
pickle.dump(dict(models=tool_models, prec=prec, dist_threshold=thr), open('results/tool_model.pkl','wb'))
R = pd.DataFrame(rows); R.to_csv('results/pivot_lineage_margins.csv', index=False)
g1_med = 0.21139074117473916
summary = dict(P1=dict(lineage_only_median_reduction=float(R.lin_red.median()), expr_median_reduction=g1_med,
                       margin_points=float(g1_med - R.lin_red.median()), PASS=bool(g1_med - R.lin_red.median() >= 0.05)),
               P2=dict(frac_drugs_positive_margin=float((R.margin>0).mean()), PASS=bool((R.margin>0).mean() >= 0.5)),
               abstention_threshold=thr, runtime_min=(time.time()-t0)/60)
json.dump(summary, open('results/pivot_summary.json','w'), indent=2)
print(json.dumps(summary, indent=2))
