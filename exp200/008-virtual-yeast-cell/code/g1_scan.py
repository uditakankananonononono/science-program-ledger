import time,json,os,sys,cobra
which=sys.argv[1]; max_new=int(sys.argv[2])
path='data/yeast-GEM.xml' if which=='yeast8' else 'data/iMM904.json'
m=cobra.io.read_sbml_model(path) if which=='yeast8' else cobra.io.load_json_model(path)
pf=f'results/g1_{which}_parts.json'
parts=json.load(open(pf)) if os.path.exists(pf) else {}
wf=f'results/g1_{which}_wt.json'
wt=json.load(open(wf))['wt'] if os.path.exists(wf) else m.slim_optimize()
json.dump({'wt':float(wt),'n_genes_total':len(m.genes)},open(wf,'w'))
# precompute gene -> reactions map once
g2r={}
for g in m.genes:
    g2r[g.id]=[(r,r.lower_bound,r.upper_bound) for r in g.reactions]
genes=[g.id for g in m.genes]
todo=[g for g in genes if g not in parts][:max_new]
t0=time.time(); floor=0.01*wt
for n,gid in enumerate(todo):
    rxns=g2r[gid]
    for r,lb,ub in rxns: r.bounds=(0,0)
    v=m.slim_optimize(error_value=0.0)
    parts[gid]=bool(v is None or v<floor)
    for r,lb,ub in rxns: r.bounds=(lb,ub)
    if (n+1)%50==0:
        json.dump(parts,open(pf,'w')); print('done',n+1,'of',len(todo),'t',round(time.time()-t0,1))
json.dump(parts,open(pf,'w'))
print('TOTAL',which,len(parts),'of',len(genes),'essential',sum(parts.values()),'t',round(time.time()-t0,1))
