import sys,json,time,re
import numpy as np, cobra
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
from cobra.util.array import create_stoichiometric_matrix
from cobra.util.solver import linear_reaction_coefficients

RICH=['alanine','arginine','asparagine','aspartate','cysteine','glutamate','glutamine',
'glycine','histidine','isoleucine','leucine','lysine','methionine','phenylalanine','proline',
'serine','threonine','tryptophan','tyrosine','valine','adenine','adenosine','guanine',
'guanosine','cytosine','cytidine','uracil','uridine','thymine','thymidine','biotin',
'thiamine','riboflavin','nicotinate','nicotinamide','pantothenate','pyridoxine','folate',
'myo-inositol','inositol','4-aminobenzoate','p-aminobenzoate','choline','ergosterol',
'palmitate','oleate','hexadecenoate','octadecanoate']
SUGARS=['glucose','fructose','galactose','sucrose','maltose','mannose','xylose','ribose',
'arabinose','lactose','trehalose','raffinose','glycerol','ethanol','acetate','pyruvate',
'lactate','citrate','malate','fumarate','alpha-ketoglutarate','2-oxoglutarate']

name,start,end = sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
if name=='yeast8':
    m=cobra.io.read_sbml_model('data/yeast-GEM.xml'); out='results/g1rich_yeast8_parts.json'
else:
    m=cobra.io.load_json_model('data/iMM904.json'); out='results/g1rich_imm904_parts.json'

# find exchange reactions and open rich uptakes
exch=[r for r in m.reactions if len(r.metabolites)==1 and list(r.metabolites.values())[0] in (-1,1)]
opened=[]
for r in exch:
    met=list(r.metabolites.keys())[0]
    nm=(met.name or '').lower().strip()
    nm=re.sub(r'\s*\[.*?\]\s*',' ',nm).strip()
    coef=list(r.metabolites.values())[0]
    if any(s in nm for s in SUGARS): continue
    if any(k in nm for k in RICH):
        # Addendum B2: uptake opened. In both yeast-GEM and BiGG JSON, exchange
        # reactions carry the extracellular metabolite as REACTANT (coef<0) and
        # uptake = negative flux (verified: glucose r_1714 lb=-1 in minimal medium).
        if coef<0: r.lower_bound=-10.0
        else: r.upper_bound=10.0
        opened.append({'rxn':r.id,'met':met.name})
json.dump(opened,open(f'results/rich_medium_{name}.json','w'),indent=1)

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
wt=-solve(lb,ub).fun
json.dump({'wt':wt,'medium':'rich (Addendum B2)','n_rich_opened':len(opened)},open(f'results/g1rich_{name}_wt.json','w'))
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
    if len(parts)%150==0:
        json.dump(parts,open(out,'w'))
        print(f'checkpoint {len(parts)}, {time.time()-t0:.0f}s',flush=True)
json.dump(parts,open(out,'w'))
print('CHUNK DONE',name,start,end,'parts',len(parts),'rich WT',round(wt,4),'opened',len(opened))
