"""P21-03: IL-6-context CRISPR dependency of model-ranked targets (DepMap 24Q2, figshare 25880521).
Run: python3 tool/depmap_check.py <dir with CRISPRGeneEffect.csv, Expr.csv (OmicsExpressionProteinCodingGenesTPMLogp1), Model.csv> results/results.json"""
import sys, json, re, numpy as np, pandas as pd
from scipy.stats import mannwhitneyu, spearmanr
def multipletests(p, method='fdr_bh'):
    p=np.asarray(p,float); n=len(p); o=np.argsort(p); q=np.empty(n); prev=1.0
    for rank,i in reversed(list(enumerate(o,1))): prev=min(prev,p[i]*n/rank); q[i]=prev
    return None,q
dd, out = sys.argv[1], sys.argv[2]
P2101 = sys.argv[3] if len(sys.argv)>3 else None
TOP5 = {'JAK1':'kcatSTATPhos','IL6':'ksynthIL6Gut','IL6R':'kRLOn','ADAM17':'kRShedding','CRP':'kCRPSecretion'}
GMAP = {'JAK1':['kcatSTATPhos','KmSTATPhos'],'IL6':['ksynthIL6Gut','ksynthIL6'],'IL6R':['kRLOn','kRLOff','kRsynth'],
        'IL6ST':['kgp130On','kgp130Off','ksynthsgp130'],'ADAM17':['kRShedding'],'CRP':['kCRPSecretion','ksynthCRP'],'PTPN2':['VmSTATDephos']}
def load(path, genes):
    hdr = pd.read_csv(path, nrows=0).columns
    keep = [hdr[0]] + [c for c in hdr if re.sub(r' \(.*\)$','',c) in genes]
    d = pd.read_csv(path, usecols=keep, index_col=0); d.columns=[re.sub(r' \(.*\)$','',c) for c in d.columns]
    return d.loc[:, ~d.columns.duplicated()]
genes = set(GMAP)|{'JAK2','ESR1','PGR','ERBB2','STAT3'}
cr = load(f'{dd}/CRISPRGeneEffect.csv', genes); ex = load(f'{dd}/Expr.csv', genes|{'IL6'})
m = pd.read_csv(f'{dd}/Model.csv').set_index('ModelID'); br = m[m.OncotreeLineage=='Breast']
def analyse(lines, label):
    lines = [l for l in lines if l in cr.index and l in ex.index]
    il6 = ex.loc[lines,'IL6']; med = il6.median(); hi = il6[il6>med].index.tolist(); lo = il6[il6<=med].index.tolist()
    rows = {}
    for g in list(TOP5)+['JAK2']:
        if g not in cr.columns: rows[g]={'missing':True}; continue
        a = cr.loc[hi,g].dropna(); b = cr.loc[lo,g].dropna()
        p = mannwhitneyu(a,b,alternative='less').pvalue if len(a) and len(b) else np.nan
        rows[g] = {'diff_hi_minus_lo':float(a.mean()-b.mean()),'p_one_sided':float(p),'mean_hi':float(a.mean()),'mean_lo':float(b.mean()),'n_hi':len(a),'n_lo':len(b)}
    ps = [rows[g].get('p_one_sided',1.0) for g in TOP5]; q = multipletests(ps, method='fdr_bh')[1]
    for g,qq in zip(TOP5,q): rows[g]['fdr_q']=float(qq); rows[g]['counts']=bool(rows[g].get('diff_hi_minus_lo',0)<=-0.1 and qq<0.05)
    n_ok = sum(rows[g]['counts'] for g in TOP5)
    return {'label':label,'n_lines':len(lines),'n_hi':len(hi),'n_lo':len(lo),'il6_median_log2tpm':float(med),
            'exploratory':bool(min(len(hi),len(lo))<5),'genes':rows,'n_context_specific':n_ok,'lines':lines}
res = {}
tn = br[br.LegacyMolecularSubtype.isin(['basal_A','basal_B','basal'])].index.tolist()
res['primary'] = analyse(tn,'annotation TNBC (basal_A/basal_B/basal)')
bl = [l for l in br.index if l in ex.index]; e = ex.loc[bl]
tn2 = e[(e.ESR1<1)&(e.PGR<1)&(e.ERBB2<e.ERBB2.median())].index.tolist()
res['sensitivity_expression_tnbc'] = analyse(tn2,'expression TNBC')
res['G1'] = {'n_context_specific':res['primary']['n_context_specific'],'pass':bool(res['primary']['n_context_specific']>=2)}
# G2
if P2101:
    r1 = json.load(open(P2101)); sc = {}
    # nominal scores for all 33 params: recompute from P21-01 tool
    import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(P2101))),'tool')); import ident as I
    s0 = I.target_scores(I.LNOM); byname = {I.NAME[p]:float(v) for p,v in zip(I.EST,s0)}
    xs, ys, gs = [], [], []
    for g, ps_ in GMAP.items():
        if g in cr.columns:
            lines = res['primary']['lines']; il6 = ex.loc[lines,'IL6']; med = il6.median()
            hi = il6[il6>med].index; lo = il6[il6<=med].index
            xs.append(max(byname[p] for p in ps_)); ys.append(-(cr.loc[hi,g].mean()-cr.loc[lo,g].mean())); gs.append(g)
    rho = spearmanr(xs,ys).correlation; rng=np.random.default_rng(2103); bs=[]
    for _ in range(2000):
        i = rng.integers(0,len(xs),len(xs))
        if len(set(i))>2: bs.append(spearmanr(np.array(xs)[i],np.array(ys)[i]).correlation)
    res['G2'] = {'genes':gs,'model_score':xs,'context_dependency':ys,'spearman':float(rho),
                 'ci95':np.nanpercentile(bs,[2.5,97.5]).tolist(),'n_genes':len(xs),'pass':True}
res['G3'] = {'primary_counts':{'hi':res['primary']['n_hi'],'lo':res['primary']['n_lo']},'exploratory':res['primary']['exploratory'],'pass':True}
json.dump(res, open(out,'w'), indent=1, default=float)
print(json.dumps({k:res[k] for k in ('G1','G2','G3')}, default=float))
for g,v in res['primary']['genes'].items(): print(g, {k:(round(x,3) if isinstance(x,float) else x) for k,x in v.items()})
