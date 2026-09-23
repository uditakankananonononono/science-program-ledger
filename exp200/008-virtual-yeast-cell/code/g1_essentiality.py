import json,sys,numpy as np,cobra
from cobra.flux_analysis import single_gene_deletion
truth=json.load(open('/tmp/sgd_truth.json'))
which=sys.argv[1]; a=int(sys.argv[2]); b=int(sys.argv[3])
m=cobra.io.read_sbml_model('data/yeast-GEM.xml') if which=='yeast8' else cobra.io.load_json_model('data/iMM904.json')
wt=m.slim_optimize()
genes=[g.id for g in m.genes][a:b]
res=single_gene_deletion(m, gene_list=genes, processes=1)
res['essential']=res['growth'].isna()|(res['growth']<0.01*wt)
part={(next(iter(i)) if isinstance(i,(frozenset,set,tuple,list)) else str(i)):bool(e) for i,e in zip(res.index,res['essential'])}
import os
pf=f'results/g1_{which}_parts.json'
parts=json.load(open(pf)) if os.path.exists(pf) else {}
parts.update(part); json.dump(parts,open(pf,'w'))
json.dump({'wt':float(wt),'n_genes_total':len(m.genes)},open(f'results/g1_{which}_wt.json','w'))
print(f'{which} chunk {a}:{b} done; total parts {len(parts)}')
if len(parts)>=len(m.genes):
    pred=parts
    json.dump({'pred':pred,'wt':float(wt)},open(f'results/g1_{which}.json','w'))
import sys as _s
if len(parts)<len(m.genes): _s.exit(0)
pred=parts
common=[g for g in pred if g in truth]
tp=sum(1 for g in common if pred[g] and truth[g]=='inviable')
tn=sum(1 for g in common if not pred[g] and truth[g]=='viable')
fp=sum(1 for g in common if pred[g] and truth[g]=='viable')
fn=sum(1 for g in common if not pred[g] and truth[g]=='inviable')
sens=tp/max(tp+fn,1); spec=tn/max(tn+fp,1); ba=(sens+spec)/2
out={'model_genes':len(pred),'genes_scored':len(common),'tp':tp,'tn':tn,'fp':fp,'fn':fn,
     'sensitivity':round(sens,4),'specificity':round(spec,4),'balanced_accuracy':round(ba,4),'wt_growth':float(wt)}
json.dump(out,open(f'results/g1_{which}_metrics.json','w'),indent=1)
print(which,json.dumps(out))
