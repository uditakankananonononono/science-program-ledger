import sys,json,time
import numpy as np, cobra
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
from cobra.util.array import create_stoichiometric_matrix
from cobra.util.solver import linear_reaction_coefficients

PRODUCTS={'succinate':'r_2056','pyruvate':'r_2033','L-lactate':'r_1551','fumarate':'r_1798',
          'ethanol':'r_1761','23BDO':'r_1549'}
phase=sys.argv[1]  # 'ess' or 'scan'
start,end=int(sys.argv[2]),int(sys.argv[3])

m=cobra.io.read_sbml_model('data/yeast-GEM.xml')
for rid in ['r_1254','r_1136','r_1207']:  # locked JEN1 edit
    m.reactions.get_by_id(rid).lower_bound=-1000.0
S=csr_matrix(create_stoichiometric_matrix(m,array_type='lil'))
rlist=list(m.reactions); n=len(rlist); ridx={r.id:i for i,r in enumerate(rlist)}
lb0=np.array([r.lower_bound for r in rlist]); ub0=np.array([r.upper_bound for r in rlist])
cb=np.zeros(n)
for i,r in enumerate(rlist):
    if r in linear_reaction_coefficients(m): cb[i]=1.0
bi=int(np.argmax(cb)); beq=np.zeros(S.shape[0])
def solve(c,lb_,ub_): return linprog(-c,A_eq=S,b_eq=beq,bounds=list(zip(lb_,ub_)),method='highs',options={'time_limit':20})
wt=-solve(cb,lb0,ub0).fun
def ko(gid):
    lb2=lb0.copy(); ub2=ub0.copy()
    if gid:
        gene=m.genes.get_by_id(gid)
        for rxn in gene.reactions:
            if not rxn.gpr.eval({gid:False}):
                i=ridx[rxn.id]; lb2[i]=0.; ub2[i]=0.
    return lb2,ub2
genes=[g.id for g in m.genes]
if phase=='ess':
    out='results/ess_parts.json'
    try: parts=json.load(open(out))
    except Exception: parts={}
    for gid in genes[start:end]:
        if gid in parts: continue
        lb2,ub2=ko(gid)
        rr=solve(cb,lb2,ub2)
        parts[gid]={'growth':(-rr.fun if rr.status==0 else None),'unsolvable':rr.status!=0}
        if len(parts)%200==0: json.dump(parts,open(out,'w'))
    json.dump(parts,open(out,'w'))
    json.dump({'wt':wt,'edit':'JEN1 r_1254/r_1136/r_1207 reversible'},open('results/edited_wt.json','w'))
    print('ESS DONE',start,end,len(parts),'wt',round(wt,4))
else:
    ess=json.load(open('results/ess_parts.json'))
    noness=[g for g in genes if g in ess and not ess[g]['unsolvable'] and ess[g]['growth'] is not None and ess[g]['growth']>=0.01*wt]
    out='results/gc90_parts.json'
    try: parts=json.load(open(out))
    except Exception: parts={}
    t0=time.time()
    for gid in noness[start:end]:
        if gid in parts: continue
        lb2,ub2=ko(gid)
        g=ess[gid]['growth']  # gmax identical to essentiality-phase solve (same model+medium)
        rec={'gmax':g}
        if g and g>1e-6:
            lbf=lb2.copy(); lbf[bi]=0.9*g
            for pname,rid in PRODUCTS.items():
                c=np.zeros(n); c[ridx[rid]]=1.0
                rr=solve(c,lbf,ub2)
                rec[pname]=(-rr.fun if rr.status==0 else None)
        else:
            for pname in PRODUCTS: rec[pname]=0.0
        parts[gid]=rec
        if len(parts)%20==0:
            json.dump(parts,open(out,'w')); print('ckpt',len(parts),round(time.time()-t0),'s',flush=True)
    json.dump(parts,open(out,'w'))
    print('SCAN DONE',start,end,len(parts),'/',len(noness))
