#!/usr/bin/env python3
import json, time
import numpy as np, pandas as pd, h5py
from scipy.stats import pearsonr
t0=time.time(); rng=np.random.default_rng(20260923)
f=h5py.File('data/Dixit2016.h5ad','r')
Xg=f['X']; n_cells,n_genes=Xg.attrs['shape']
data=Xg['data']; indices=Xg['indices']; indptr=Xg['indptr']
print('X csr:', (n_cells,n_genes), flush=True)
def read_block(s,e,cols=None):
    # dense rows s..e from CSR
    d=indptr[s:e+1]
    nnz=int(d[-1]-d[0])
    dd=data[d[0]:d[0]+nnz]; ii=indices[d[0]:d[0]+nnz]
    import scipy.sparse as sp
    M=sp.csr_matrix((dd,ii,d-d[0]),shape=(e-s,n_genes))
    if cols is not None: M=M[:,cols]
    return M.toarray().astype(np.float32)
def read_col(gr, name):
    g = gr[name]
    if isinstance(g, h5py.Group):
        codes = g['codes'][:]
        cats = [c.decode() if isinstance(c,bytes) else str(c) for c in g['categories'][:]]
        return [cats[c] if c >= 0 else None for c in codes]
    return [x.decode() if isinstance(x,bytes) else str(x) for x in g[:]]
obs_target = read_col(f['obs'], 'target')
obs_pert = read_col(f['obs'], 'perturbation')
try:
    genes = np.array(read_col(f['var'], '_index'))
except Exception:
    genes = np.array(read_col(f['var'], f['var'].attrs['_index'].decode() if isinstance(f['var'].attrs.get('_index'), bytes) else f['var'].attrs['_index']))
ctrl=np.array([p=='control' for p in obs_pert])
targets=sorted({t for t in obs_target if t and t not in ('nan','None') and not t.startswith('INTERGENIC')})
tidx={t: np.array([i for i,x in enumerate(obs_target) if x==t]) for t in targets}
tidx={t:v for t,v in tidx.items() if len(v)>=25}
cidx=np.where(ctrl)[0]
print('controls:', len(cidx), 'targets:', len(tidx), flush=True)
# pass 1: control moments + library sizes (all rows)
csum=np.zeros(n_genes); csq=np.zeros(n_genes); lib=np.zeros(n_cells)
for s in range(0,n_cells,1000):
    e=min(s+1000,n_cells); B=read_block(s,e)
    lib[s:e]=B.sum(1)
    mask=np.intersect1d(np.arange(s,e),cidx)-s
    if len(mask): csum+=B[mask].sum(0); csq+=(B[mask]**2).sum(0)
nc=len(cidx); mu=csum/nc; var=csq/nc-mu**2
top=set(np.argsort(var)[-500:])
sel=np.array(sorted(top|{i for i,g in enumerate(genes) if g in tidx}))
print('selected genes:', len(sel), flush=True)
# pass 2: selected columns, CPM+log1p
N=np.zeros((n_cells,len(sel)),dtype=np.float32)
for s in range(0,n_cells,1000):
    e=min(s+1000,n_cells); B=read_block(s,e,cols=sel)
    l=lib[s:e]; l[l==0]=1
    N[s:e]=np.log1p(B*(1e4/l[:,None]))
gsel=genes[sel]; gidx={g:i for i,g in enumerate(gsel)}
ci=np.arange(n_cells)[ctrl]
cmean=N[ci].mean(0)
DE={}; ss={}; qrows=[]
for t,idx in tidx.items():
    sub=N[rng.choice(idx,100,replace=False)]
    de=sub.mean(0)-cmean
    DE[t]=de; ss[t]=float((de**2).sum())
    ns=[]
    for _ in range(100):
        p=rng.permutation(ci); d=N[p[:100]].mean(0)-N[p[100:200]].mean(0)
        ns.append(float((d**2).sum()))
    q=float(np.quantile(ns,0.95)); qrows.append(dict(target=t,ss_de=ss[t],null_q95=q,in_panel=ss[t]>q))
panel=[r['target'] for r in qrows if r['in_panel']][:20]
pd.DataFrame(qrows).to_csv('results/v5_effect_presence_qc.csv',index=False)
print('panel:', len(panel), panel, flush=True)
if len(panel)<5:
    json.dump(dict(panel=panel,underpowered=True),open('results/v5_gate_summary.json','w'))
    print('UNDER-POWERED', flush=True); raise SystemExit
top_in_sel=[i for i,g in enumerate(gsel) if i in top] if False else [i for i,g in enumerate(gsel) if genes[sel][i] in set(genes[list(top)])]
gv=set(genes[list(top)])
top_in_sel=[i for i,g in enumerate(gsel) if g in gv]
C=np.corrcoef(N[ci][:,top_in_sel].T)
gvar=gsel[top_in_sel]
res=[]
for t in panel:
    if t not in set(gvar): continue
    ti=list(gvar).index(t); pred=C[ti]*DE[t][gidx[t]]; obsde=DE[t][top_in_sel]
    pool=[DE[o][top_in_sel] for o in panel if o!=t and o in set(gvar)]
    if not pool: continue
    others=np.mean(pool,axis=0)
    r_net=pearsonr(pred,obsde)[0]; r_base=pearsonr(others,obsde)[0]
    p20=len(set(np.argsort(np.abs(pred))[-20:])&set(np.argsort(np.abs(obsde))[-20:]))/20
    b20=len(set(np.argsort(np.abs(others))[-20:])&set(np.argsort(np.abs(obsde))[-20:]))/20
    null=[pearsonr(C[list(gvar).index(o)]*DE[o][gidx[o]],obsde)[0] for o in panel if o!=t and o in set(gvar)]
    pval=(1+sum(1 for z in null if z>=r_net))/(1+len(null))
    res.append(dict(target=t,r_net=float(r_net),r_base=float(r_base),p20_net=float(p20),p20_base=float(b20),perm_p=float(pval)))
    print(t,'r_net=%.3f r_base=%.3f p=%.3f'%(r_net,r_base,pval),flush=True)
R=pd.DataFrame(res); R.to_csv('results/v5_per_target_metrics.csv',index=False)
dr=(R.r_net-R.r_base).median()
g1=bool(dr>=0.05 and (R.perm_p<=0.05).mean()>=0.5)
g2=bool((R.p20_net-R.p20_base).median()>0)
summary=dict(panel=list(R.target),G1=dict(median_r_net=float(R.r_net.median()),median_r_base=float(R.r_base.median()),median_delta=float(dr),frac_perm_sig=float((R.perm_p<=0.05).mean()),PASS=g1),G2=dict(median_p20_net=float(R.p20_net.median()),median_p20_base=float(R.p20_base.median()),PASS=g2),runtime_min=(time.time()-t0)/60)
json.dump(summary,open('results/v5_gate_summary.json','w'),indent=2)
print(json.dumps(summary,indent=2),flush=True)
