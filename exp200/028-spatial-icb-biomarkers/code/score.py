import numpy as np, json
from scipy.spatial import cKDTree
SECS=['m09','m10','m11','m12','m13','m14','m15s1','m15s2','m16s1','m16s2','m16s3']
TUMOR={'m09':'m09','m10':'m10','m11':'m11','m12':'m12','m13':'m13','m14':'m14',
       'm15s1':'m15','m15s2':'m15','m16s1':'m16','m16s2':'m16','m16s3':'m16'}
LABEL={'m09':'NR','m10':'NR','m11':'NR','m12':'NR','m13':'NR','m14':'NR','m15':'R','m16':'R'}
sec={}
for s in SECS:
    d=np.load(f'results/local/{s}.npz')
    chol,cd8,tpan=d['chol'],d['cd8'],d['tpan']
    C=np.stack([d['row'],d['col']],1).astype(np.float64)
    _,idx=cKDTree(C).query(C,7)
    neigh_cd8=cd8[idx[:,1:]].mean(1)
    f1=float(np.corrcoef(chol,neigh_cd8)[0,1])
    sec[s]={'F1':round(f1,4),'F2':round(float(chol.mean()),4),'F3':round(float(tpan.mean()),4)}
tum={}
for t in ['m09','m10','m11','m12','m13','m14','m15','m16']:
    ss=[s for s in SECS if TUMOR[s]==t]
    tum[t]={'label':LABEL[t]}
    for k in ['F1','F2','F3']:
        tum[t][k]=round(float(np.median([sec[s][k] for s in ss])),4)
def rank_desc(vals):  # rank 1 = highest
    order=sorted(vals, key=lambda x:-x[1])
    return {t:i+1 for i,(t,v) in enumerate(order)}
out={'per_section':sec,'per_tumor':tum}
for k in ['F1','F2','F3']:
    r=rank_desc([(t,tum[t][k]) for t in tum])
    out[f'{k}_ranks']={t:r[t] for t in tum}
# gates
f3r=out['F3_ranks']; g1 = f3r['m15']<=3 and f3r['m16']<=3
f1r=out['F1_ranks']; sep = f1r['m15']<=2 and f1r['m16']<=2
f2r=out['F2_ranks']
f2_nosep = not (f2r['m15']<=2 and f2r['m16']<=2)
out['gates']={'G1_sanity':bool(g1),'G2_F1_perfect_sep':bool(sep),'G2_F2_fails_sep':bool(f2_nosep)}
json.dump(out, open('results/scores.json','w'), indent=1)
print(json.dumps({'tumor':{t:tum[t] for t in tum},'ranks':{k:out[f'{k}_ranks'] for k in ['F1','F2','F3']},'gates':out['gates']}, indent=1))
