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
lb=np.array([r.lower_bound for r in rlist]); ub=np.array([r.upper_bound for r in rlist])
c=np.zeros(n)
for i,r in enumerate(rlist):
    if r in linear_reaction_coefficients(m): c[i]=1.0
biomass_i=int(np.argmax(c))
beq=np.zeros(S.shape[0])
def solve(cobj,lb_,ub_):
    return linprog(-cobj,A_eq=S,b_eq=beq,bounds=list(zip(lb_,ub_)),method='highs',options={'time_limit':20})
wt=-solve(c,lb,ub).fun
floor=0.1*wt
succ_i=ridx['r_2056']
csucc=np.zeros(n); csucc[succ_i]=1.0
# theoretical max succinate export with biomass >= 10% WT
lbf=lb.copy(); lbf[biomass_i]=floor
tmax=-solve(csucc,lbf,ub).fun
# WT strain's own max succinate export under same floor (reference)
# (same as tmax but with no knockout: tmax IS the no-knockout value)
g1=json.load(open('results/g1_yeast8_v2_parts.json'))
genes=[g.id for g in m.genes]
noness=[g for g in genes if g in g1 and not g1[g]['unsolvable'] and g1[g]['growth'] is not None and g1[g]['growth']>=0.01*wt]
try: parts=json.load(open('results/g2_succinate_parts.json'))
except Exception: parts={}
t0=time.time()
for gid in noness[start:end]:
    if gid in parts: continue
    gene=m.genes.get_by_id(gid)
    lb2=lbf.copy(); ub2=ub.copy()
    for rxn in gene.reactions:
        if not rxn.gpr.eval({gid:False}):
            i=ridx[rxn.id]; lb2[i]=0.; ub2[i]=0.
    rr=solve(csucc,lb2,ub2)
    parts[gid]={'succ_export':(-rr.fun if rr.status==0 else None),'status':int(rr.status)}
    if len(parts)%100==0:
        json.dump(parts,open('results/g2_succinate_parts.json','w'))
        print(f'checkpoint {len(parts)}, {time.time()-t0:.0f}s',flush=True)
json.dump({'wt':wt,'biomass_floor':floor,'theoretical_max_export':tmax,'n_nonessential':len(noness)},
          open('results/g2_succinate_meta.json','w'))
json.dump(parts,open('results/g2_succinate_parts.json','w'))
print('CHUNK DONE',start,end,'parts',len(parts),'/',len(noness),'wt',round(wt,4),'floor',round(floor,5),'tmax',round(tmax,3))
