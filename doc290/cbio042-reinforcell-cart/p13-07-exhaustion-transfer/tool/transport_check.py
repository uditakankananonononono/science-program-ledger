"""Transport check auditor: score any proposed exhaustion signature (gene list) against the P13-07 cohort matrix.
Usage: python tool/transport_check.py GENE1 GENE2 ...   (needs results/prep.npz from tool/prep.py)
Score = mean z-scored expression of the listed genes within each cohort; AUC against both label definitions.
Verdict uses the locked G2 rule: portable only if median AUC >= 0.75 and worst >= 0.65.
Limit: only genes in the 1,748-gene shared panel are scored (the 9 EXH label genes are excluded by design)."""
import numpy as np, json, sys
from scipy.stats import rankdata
P=np.load("results/prep.npz"); info=json.load(open("results/prep_info.json")); panel=info["panel"]; cids=info["info"]["cohorts"]
genes=[g for g in sys.argv[1:] if g in panel]; miss=[g for g in sys.argv[1:] if g not in panel]
if not genes: sys.exit(f"none of the genes are in the shared panel: {miss}")
j=[panel.index(g) for g in genes]
def auc(y,p): r=rankdata(p); n1=y.sum(); n0=len(y)-n1; return (r[y==1].sum()-n1*(n1+1)/2)/(n1*n0)
out={}
for c in cids:
    F=P[f"F_{c}"][:,j]; s=((F-F.mean(0))/(F.std(0)+1e-6)).mean(1)
    out[c]={l:round(float(auc(P[f"{l}_{c}"][P[f"{l}_{c}"]>=0],s[P[f"{l}_{c}"]>=0])),3) for l in ["L1","L2"]}
for l in ["L1","L2"]:
    v=[out[c][l] for c in cids]; print(f"{l}: median {np.median(v):.3f} worst {min(v):.3f} ->", "PORTABLE" if np.median(v)>=0.75 and min(v)>=0.65 else "NOT PORTABLE")
print(json.dumps(out)); print("skipped (not in panel):",miss)
