# SUPPLEMENTARY (post-hoc characterization, not a gate): growth-coupled succinate
# potential = max succinate export s.t. biomass >= 90% of the strain's OWN max growth.
import sys,json,time
import numpy as np, cobra
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
from cobra.util.array import create_stoichiometric_matrix
from cobra.util.solver import linear_reaction_coefficients

start,end=int(sys.argv[1]),int(sys.argv[2])
m=cobra.io.read_sbml_model('data/yeast-GEM.xml')
S=csr_matrix(create_stoichiometric_matrix(m,array_type='lil'))
rlist=list(m.reactions); n=len(rlist)
ridx={r.id:i for i,r in enumerate(rlist)}
lb0=np.array([r.lower_bound for r in rlist]); ub0=np.array([r.upper_bound for r in rlist])
cb=np.zeros(n)
for i,r in enumerate(rlist):
    if r in linear_reaction_coefficients(m): cb[i]=1.0
biomass_i=int(np.argmax(cb))
cs=np.zeros(n); cs[ridx['r_2056']]=1.0
beq=np.zeros(S.shape[0])
def solve(cobj,lb_,ub_):
    return linprog(-cobj,A_eq=S,b_eq=beq,bounds=list(zip(lb_,ub_)),method='highs',options={'time_limit':20})
def ko_bounds(gid):
    lb2=lb0.copy(); ub2=ub0.copy()
    if gid is not None:
        gene=m.genes.get_by_id(gid)
        for rxn in gene.reactions:
            if not rxn.gpr.eval({gid:False}):
                i=ridx[rxn.id]; lb2[i]=0.; ub2[i]=0.
    return lb2,ub2
def strain_potential(gid):
    lb2,ub2=ko_bounds(gid)
    g=-solve(cb,lb2,ub2).fun
    if g is None or g<=1e-6: return {'gmax':g if g else 0.0,'succ_gc90':0.0}
    lbf=lb2.copy(); lbf[biomass_i]=0.9*g
    r=solve(cs,lbf,ub2)
    return {'gmax':g,'succ_gc90':(-r.fun if r.status==0 else None)}
wt=strain_potential(None)
json.dump(wt,open('results/g2_gc90_wt.json','w'))
g1=json.load(open('results/g1_yeast8_v2_parts.json'))
genes=[g.id for g in m.genes]
noness=[g for g in genes if g in g1 and not g1[g]['unsolvable'] and g1[g]['growth'] is not None and g1[g]['growth']>=0.01*json.load(open('results/g1_yeast8_wt_v2.json'))['wt']]
try: parts=json.load(open('results/g2_gc90_parts.json'))
except Exception: parts={}
t0=time.time()
for gid in noness[start:end]:
    if gid in parts: continue
    parts[gid]=strain_potential(gid)
    if len(parts)%100==0:
        json.dump(parts,open('results/g2_gc90_parts.json','w'))
        print(f'ckpt {len(parts)}, {time.time()-t0:.0f}s',flush=True)
json.dump(parts,open('results/g2_gc90_parts.json','w'))
print('GC CHUNK DONE',start,end,'parts',len(parts),'wt',wt)
