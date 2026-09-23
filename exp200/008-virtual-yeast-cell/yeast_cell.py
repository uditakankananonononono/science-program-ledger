#!/usr/bin/env python3
"""yeast_cell.py - virtual yeast cell (Yeast8 FBA) for knockout growth + succinate design.
Usage:
  python3 yeast_cell.py WT
  python3 yeast_cell.py KO YKL141W [MORE_GENES...]
  python3 yeast_cell.py SUCC YPL262W      # max succinate export at biomass>=90% strain max
Solver: HiGHS via scipy (Addendum A). Model: data/yeast-GEM.xml (SHA in provenance).
"""
import sys, json
import numpy as np, cobra
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
from cobra.util.array import create_stoichiometric_matrix
from cobra.util.solver import linear_reaction_coefficients

def build():
    m=cobra.io.read_sbml_model('data/yeast-GEM.xml')
    S=csr_matrix(create_stoichiometric_matrix(m,array_type='lil'))
    rlist=list(m.reactions); n=len(rlist)
    lb=np.array([r.lower_bound for r in rlist]); ub=np.array([r.upper_bound for r in rlist])
    cb=np.zeros(n)
    for i,r in enumerate(rlist):
        if r in linear_reaction_coefficients(m): cb[i]=1.0
    return m,S,rlist,lb,ub,cb,int(np.argmax(cb)),np.zeros(S.shape[0])

def solve(S,beq,cobj,lb,ub):
    return linprog(-cobj,A_eq=S,b_eq=beq,bounds=list(zip(lb,ub)),method='highs',options={'time_limit':20})

def apply_kos(m,rlist,lb,ub,gids):
    ridx={r.id:i for i,r in enumerate(rlist)}
    lb2=lb.copy(); ub2=ub.copy()
    for gid in gids:
        gene=m.genes.get_by_id(gid)
        for rxn in gene.reactions:
            if not rxn.gpr.eval({gid:False}):
                i=ridx[rxn.id]; lb2[i]=0.; ub2[i]=0.
    return lb2,ub2

def main():
    mode=sys.argv[1].upper()
    m,S,rlist,lb,ub,cb,bi,beq=build()
    ridx={r.id:i for i,r in enumerate(rlist)}
    cs=np.zeros(len(rlist)); cs[ridx['r_2056']]=1.0
    gids=sys.argv[2:] if mode in ('KO','SUCC') else []
    lb2,ub2=apply_kos(m,rlist,lb,ub,gids)
    g=-solve(S,beq,cb,lb2,ub2).fun
    wt=-solve(S,beq,cb,lb,ub).fun
    out={'mode':mode,'knockouts':gids,'growth':g,'wt_growth':wt,
         'growth_pct_of_wt':(100*g/wt if g is not None else None),
         'predicted_essential':(g < 0.01*wt if g is not None else None)}
    if mode=='SUCC':
        lbf=lb2.copy(); lbf[bi]=0.9*g
        out['succinate_export_gc90']=-solve(S,beq,cs,lbf,ub2).fun
    print(json.dumps(out,indent=1))

if __name__=='__main__':
    if len(sys.argv)<2 or sys.argv[1].upper() not in ('WT','KO','SUCC'):
        print(__doc__); sys.exit(1)
    main()
