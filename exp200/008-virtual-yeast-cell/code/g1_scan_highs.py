import sys,json,time
import numpy as np, cobra
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
from cobra.util.array import create_stoichiometric_matrix
from cobra.util.solver import linear_reaction_coefficients

name,start,end = sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
if name=='yeast8':
    m=cobra.io.read_sbml_model('data/yeast-GEM.xml'); out='results/g1_yeast8_v2_parts.json'
else:
    m=cobra.io.load_json_model('data/iMM904.json'); out='results/g1_imm904_parts.json'
S=csr_matrix(create_stoichiometric_matrix(m,array_type='lil'))
rlist=list(m.reactions)
lb=np.array([r.lower_bound for r in rlist]); ub=np.array([r.upper_bound for r in rlist])
c=np.zeros(len(rlist))
coefs=linear_reaction_coefficients(m)
for i,r in enumerate(rlist):
    if r in coefs: c[i]=coefs[r]
beq=np.zeros(S.shape[0])
def solve(lb_,ub_):
    return linprog(-c,A_eq=S,b_eq=beq,bounds=list(zip(lb_,ub_)),method='highs',options={'time_limit':20})
wt_res=solve(lb,ub)
wt=-wt_res.fun
json.dump({'wt':wt,'n_rxns':len(rlist),'n_genes':len(m.genes),'solver':'HiGHS via scipy.linprog, time_limit 20s'},
          open(f'results/g1_{name}_wt_v2.json','w'))
try: parts=json.load(open(out))
except Exception: parts={}
ridx={r.id:i for i,r in enumerate(rlist)}
genes=[g.id for g in m.genes]
t0=time.time()
for gid in genes[start:end]:
    if gid in parts: continue
    gene=m.genes.get_by_id(gid)
    lb2=lb.copy(); ub2=ub.copy()
    for rxn in gene.reactions:
        if not rxn.gpr.eval({gid:False}):
            i=ridx[rxn.id]; lb2[i]=0.; ub2[i]=0.
    rr=solve(lb2,ub2)
    parts[gid]={'growth':(-rr.fun if rr.status==0 else None),'status':int(rr.status),'unsolvable':bool(rr.status!=0)}
    if len(parts)%50==0:
        json.dump(parts,open(out,'w'))
        print(f'checkpoint {len(parts)} genes, {time.time()-t0:.0f}s',flush=True)
json.dump(parts,open(out,'w'))
print('CHUNK DONE',name,start,end,'parts total',len(parts),'wt',round(wt,4))
