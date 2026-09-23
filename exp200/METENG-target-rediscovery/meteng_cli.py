#!/usr/bin/env python3
"""meteng_cli.py - blind growth-coupled knockout scan CLI (METENG insert).
Usage: python3 meteng_cli.py <product_exchange_id> [KO_GENE ...]
  No KO args -> WT reference (gc90 export, no knockout).
  With KO genes -> gc90 product export for each single KO.
Model: Yeast8 + locked JEN1 edit (GATES.md). Solver: HiGHS."""
import sys, json
import numpy as np, cobra
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
from cobra.util.array import create_stoichiometric_matrix
from cobra.util.solver import linear_reaction_coefficients

def main():
    prod_rid=sys.argv[1]; kos=sys.argv[2:]
    m=cobra.io.read_sbml_model('data/yeast-GEM.xml')
    for rid in ['r_1254','r_1136','r_1207']:
        m.reactions.get_by_id(rid).lower_bound=-1000.0
    S=csr_matrix(create_stoichiometric_matrix(m,array_type='lil'))
    rlist=list(m.reactions); n=len(rlist); ridx={r.id:i for i,r in enumerate(rlist)}
    lb0=np.array([r.lower_bound for r in rlist]); ub0=np.array([r.upper_bound for r in rlist])
    cb=np.zeros(n)
    for i,r in enumerate(rlist):
        if r in linear_reaction_coefficients(m): cb[i]=1.0
    bi=int(np.argmax(cb)); beq=np.zeros(S.shape[0])
    def solve(c,lb_,ub_): return linprog(-c,A_eq=S,b_eq=beq,bounds=list(zip(lb_,ub_)),method='highs',options={'time_limit':20})
    cs=np.zeros(n); cs[ridx[prod_rid]]=1.0
    def strain(gid):
        lb2=lb0.copy(); ub2=ub0.copy()
        if gid:
            gene=m.genes.get_by_id(gid)
            for rxn in gene.reactions:
                if not rxn.gpr.eval({gid:False}):
                    i=ridx[rxn.id]; lb2[i]=0.; ub2[i]=0.
        g=-solve(cb,lb2,ub2).fun
        lbf=lb2.copy(); lbf[bi]=0.9*g
        return g,-solve(cs,lbf,ub2).fun
    wt=strain(None)
    out={'product_exchange':prod_rid,'wt':{'gmax':wt[0],'gc90_export':wt[1]},'knockouts':{}}
    for gid in kos:
        g,e=strain(gid)
        out['knockouts'][gid]={'gmax':g,'gc90_export':e,'delta_vs_wt':(e-wt[1] if e is not None else None)}
    print(json.dumps(out,indent=1))

if __name__=='__main__':
    if len(sys.argv)<2: print(__doc__); sys.exit(1)
    main()
