"""P13-07 stage 3: gates G1-G4, variance decomposition (OLS R^2 + Shapley shares), pooled leave-one-cohort-out core signature."""
import math, numpy as np, json, itertools, sys, warnings; warnings.filterwarnings("ignore")
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from scipy.stats import rankdata
sys.path.insert(0,'tool'); from fetch import COH
PL=lambda a:"smartseq" if "Smart" in a else "bd" if "BD" in a else "10x5" if "5'" in a else "10x3" if "3'" in a else "multiome"
DC=lambda d:"viral" if d=="COVID-19" else "lymphoma" if "lymphoma" in d else "carcinoma"
R=[r for m in ["lr","hgb"] for l in ["L1","L2"] for r in json.load(open(f"results/tr_{m}_{l}.json"))]
info=json.load(open("results/prep_info.json")); cids=info["info"]["cohorts"]
out={"cohorts":cids,"kappa_L1_vs_L2":info["kappa"],"panel_size":info["info"]["panel_size"]}
for m in ["lr","hgb"]:
  for l in ["L1","L2"]:
    off=[r["auc"] for r in R if r["model"]==m and r["train_label"]==l and r["test_label"]==l and r["train"]!=r["test"]]
    diag=[r["auc"] for r in R if r["model"]==m and r["train_label"]==l and r["train"]==r["test"]]
    out[f"{m}_{l}"]=dict(n_pairs=len(off),median_cross=float(np.median(off)),worst_cross=float(np.min(off)),best_cross=float(np.max(off)),median_in=float(np.median(diag)))
g2=out["lr_L1"]; out["G1"]=dict(cohorts=len(cids),pass_=len(cids)>=8 and all("lo" in r for r in R))
out["G2"]=dict(median=g2["median_cross"],worst=g2["worst_cross"],portable=g2["median_cross"]>=0.75 and g2["worst_cross"]>=0.65)
def decomp(rows):
    ind={(r["model"],r["train"],r["train_label"]):r["auc"] for r in rows if r["train"]==r["test"]}
    X=[];y=[]
    for r in rows:
        if r["train"]==r["test"]: continue
        a,b=COH[r["train"]],COH[r["test"]]
        X.append([PL(a[3])!=PL(b[3]),a[2]!=b[2],DC(a[1])!=DC(b[1]),r["train_label"]!=r["test_label"]]); y.append(ind[(r["model"],r["train"],r["train_label"])]-r["auc"])
    X=np.array(X,float); y=np.array(y)
    def r2(cols):
        if not cols: return 0.0
        Z=np.c_[np.ones(len(y)),X[:,cols]]; b=np.linalg.lstsq(Z,y,rcond=None)[0]; return 1-((y-Z@b)**2).sum()/((y-y.mean())**2).sum()
    names=["platform","tissue","disease_class","label_definition"]; full=r2([0,1,2,3]); sh={}
    for j in range(4):
        o=[k for k in range(4) if k!=j]; v=0
        for s in range(4):
            for S in itertools.combinations(o,s):
                w=math.factorial(s)*math.factorial(3-s)/24; v+=w*(r2(list(S)+[j])-r2(list(S)))
        sh[names[j]]=float(v)
    # how much of the deficit is plain "different cohort" (intercept): mean deficit
    return dict(n=len(y),mean_deficit=float(y.mean()),R2=float(full),shapley=sh)
out["G3_lr"]=decomp([r for r in R if r["model"]=="lr"]); out["G3_hgb"]=decomp([r for r in R if r["model"]=="hgb"])
out["G3"]=dict(R2=out["G3_lr"]["R2"],pass_=out["G3_lr"]["R2"]>=0.60)
# pooled LOCO sparse core signature on L1
P=np.load("results/prep.npz"); panel=np.array(info["panel"])
def auc(y,p): r=rankdata(p); n1=y.sum(); n0=len(y)-n1; return (r[y==1].sum()-n1*(n1+1)/2)/(n1*n0)
loco={}; sel=[]
for c in cids:
    Xs=[];ys=[]
    for d in cids:
        if d==c: continue
        y=P[f"L1_{d}"]; m=y>=0; F=P[f"F_{d}"][m]; F=(F-F.mean(0))/(F.std(0)+1e-6); Xs.append(F); ys.append(y[m])
    X=np.vstack(Xs); y=np.concatenate(ys)
    mdl=LogisticRegression(penalty="l1",C=0.005,solver="liblinear").fit(X,y); w=mdl.coef_[0]; nz=np.where(w!=0)[0]; sel.append(set(panel[nz]))
    yt=P[f"L1_{c}"]; m=yt>=0; F=P[f"F_{c}"][m]; F=(F-F.mean(0))/(F.std(0)+1e-6)
    loco[c]=dict(auc=float(auc(yt[m],F@w)),n_genes=int(len(nz)))
core=sorted(set.intersection(*sel)); la=[v["auc"] for v in loco.values()]
out["core_signature"]=dict(loco=loco,median=float(np.median(la)),worst=float(np.min(la)),genes_in_all_folds=core,
    portable_by_G2_rule=float(np.median(la))>=0.75 and float(np.min(la))>=0.65)
json.dump(out,open("results/results.json","w"),indent=1)
json.dump(R,open("results/transport_matrix.json","w"))
print(json.dumps({k:out[k] for k in ["G1","G2","G3","lr_L1","lr_L2","hgb_L1","hgb_L2"]},indent=0)); print(json.dumps(out["G3_lr"])); print(json.dumps(out["G3_hgb"]))
print(json.dumps(out["core_signature"])[:1500])
