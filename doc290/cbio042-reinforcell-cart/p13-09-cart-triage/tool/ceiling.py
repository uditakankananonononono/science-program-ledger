"""P13-09 summary-level information ceiling for labs-only CAR-T response triage.
Continuous markers: OR per Q3-vs-Q1 contrast (rms-style) -> d per SD = ln(OR)/1.349 (IQR of a normal = 1.349 SD, marker
assumed normal on the model scale) -> AUC = Phi(|d|/sqrt(2)) (binormal equal variance). CI carried from the OR CI.
Binary markers with only an OR: AUC depends on marker prevalence; reported as a range over stated prevalences.
2x2-derivable markers: AUC = (sens + spec)/2.
Combination ceiling: Mahalanobis D^2 = d' R^-1 d over markers, for assumed inter-marker correlation r (stated), AUC = Phi(D/sqrt2)."""
import numpy as np, json
from scipy.stats import norm
def auc_or_iqr(o): d=abs(np.log(o))/1.349; return norm.cdf(d/np.sqrt(2)), d
def auc_binary(OR,p_marker,p_out):  # OR = odds ratio of NON-response, marker-high vs marker-low
    # solve 2x2 with marker prevalence p and outcome (non-response) rate q given OR (marker-high -> lower response)
    from scipy.optimize import brentq
    q=p_out
    f=lambda a: (a/(p_marker-a))/((q-a)/(1-p_marker-q+a))-OR   # a = P(marker high & non-response)
    lo=max(0,q+p_marker-1)+1e-9; hi=min(p_marker,q)-1e-9
    a=brentq(f,lo,hi); sens=a/q; spec=(1-p_marker-q+a)/(1-q); return (sens+spec)/2
rows=[]
SRC_SIE="https://aacr.figshare.com/collections/Data_from_A_Multicenter_Real-life_Prospective_Study_of_Axicabtagene_Ciloleucel_versus_Tisagenlecleucel_Toxicity_and_Outcomes_in_Large_B-cell_Lymphomas/7429371"
# CART-SIE LBCL (Suppl. Table 1): OR for response per Q3 vs Q1 (OR<1: higher marker -> lower response)
for out,vals in {"ORR_d90":{"CRP":(0.35,0.23,0.55,408),"Ferritin":(0.40,0.25,0.63,352),"LDH":(0.36,0.24,0.56,408)},
                 "CRR_d90":{"CRP":(0.31,0.19,0.48,408),"Ferritin":(0.44,0.28,0.69,352),"LDH":(0.41,0.27,0.64,408)}}.items():
    for m,(o,l,u,n) in vals.items():
        a,d=auc_or_iqr(o); al,_=auc_or_iqr(u); au,_=auc_or_iqr(l)
        rows.append(dict(cohort="CART-SIE LBCL (axi/tisa)",outcome=out,marker=m,n=n,OR=o,OR_ci=[l,u],contrast="Q3 vs Q1",d_per_sd=round(d,3),implied_auc=round(a,3),auc_ci=[round(al,3),round(au,3)],source=SRC_SIE))
# HEMATOTOX high vs low, binary; prevalence of HT-high not in the supplement -> range over 0.3-0.6; non-response rate range 0.25-0.40
for out,(o,l,u) in {"ORR_d90":(0.34,0.20,0.59),"CRR_d90":(0.34,0.19,0.61)}.items():
    q=(0.25,0.40) if out=="ORR_d90" else (0.40,0.55)
    grid=[auc_binary(1/o,p,qq) for p in (0.3,0.45,0.6) for qq in q]
    rows.append(dict(cohort="CART-SIE LBCL (axi/tisa)",outcome=out,marker="CAR-HEMATOTOX high vs low",n=241,OR=o,OR_ci=[l,u],contrast="binary",
        implied_auc_range=[round(min(grid),3),round(max(grid),3)],assumption="HT-high prevalence 0.30-0.60; non-response rate "+str(q),source=SRC_SIE))
# Liu 2023 MM: VGPR-or-better 59% (ferritin upper quartile) vs 77%; n=109, upper quartile ~27 of 109 (quartile split)
nh,nl=27,82; rh,rl=0.59,0.77
nonh,nonl=nh*(1-rh),nl*(1-rl); sens=nonh/(nonh+nonl); spec=(nl*rl)/(nh*rh+nl*rl)
rows.append(dict(cohort="Liu 2023 R/R MM (CAR-T, n=109)",outcome=">=VGPR",marker="Ferritin upper quartile (>882 ng/mL)",n=109,implied_auc=round((sens+spec)/2,3),
    derivation="2x2 from reported 59% vs 77% with quartile split 27/82",source="https://www.frontiersin.org/articles/10.3389/fimmu.2023.1169071/full"))
# combination ceiling (CART-SIE, CRR), CRP+ferritin+LDH
ds=np.array([r["d_per_sd"] for r in rows if r["outcome"]=="CRR_d90" and "d_per_sd" in r]); comb={}
for rr in (0.0,0.3,0.5,0.7):
    R=np.full((3,3),rr); np.fill_diagonal(R,1); D=np.sqrt(ds@np.linalg.solve(R,ds)); comb[str(rr)]=round(float(norm.cdf(D/np.sqrt(2))),3)
dso=np.array([r["d_per_sd"] for r in rows if r["outcome"]=="ORR_d90" and "d_per_sd" in r]); combo={}
for rr in (0.0,0.3,0.5,0.7):
    R=np.full((3,3),rr); np.fill_diagonal(R,1); D=np.sqrt(dso@np.linalg.solve(R,dso)); combo[str(rr)]=round(float(norm.cdf(D/np.sqrt(2))),3)
out=dict(rows=rows,combination_ceiling_CRR={"markers":"CRP+ferritin+LDH","auc_by_assumed_r":comb},combination_ceiling_ORR={"markers":"CRP+ferritin+LDH","auc_by_assumed_r":combo})
json.dump(out,open("results/results.json","w"),indent=1)
for r in rows: print({k:r[k] for k in r if k not in ("source",)})
print(out["combination_ceiling_CRR"],out["combination_ceiling_ORR"])
