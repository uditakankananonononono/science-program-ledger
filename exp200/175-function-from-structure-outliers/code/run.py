import json, numpy as np
from collections import Counter
from statsmodels.stats.contingency_tables import StratifiedTable
mot={f:v['motifs'] for f,v in json.load(open('data/motifs_from_180.json'))['families'].items()}
def ecs(r):
    pd_=r.get('proteinDescription',{}); out=[]
    for blk in [pd_.get('recommendedName',{})]+pd_.get('alternativeNames',[])+[c.get('recommendedName',{}) for c in pd_.get('contains',[])]:
        out+= [e['value'] for e in blk.get('ecNumbers',[])]
    return {'.'.join(e.split('.')[:3]) for e in out}
tables=[];per={}
for f,M in mot.items():
    R=json.load(open(f'data/{f}.json'))['results']; seen=set(); rows=[]
    for r in R:
        s=r['sequence']['value']
        if s in seen: continue
        seen.add(s); rows.append((any(m in s for m in M),ecs(r),r['primaryAccession'],r['proteinDescription'].get('recommendedName',{}).get('fullName',{}).get('value','')))
    withec=[e for _,e,_,_ in rows if e]
    if len(withec)<0.5*len(rows): per[f]={'excluded':'EC<50%','n':len(rows),'frac_ec':len(withec)/len(rows)}; continue
    modal=Counter(x for e in withec for x in e).most_common(1)[0][0]
    diff=[(not e) or (modal not in e) for _,e,_,_ in rows]; kept=[k for k,_,_,_ in rows]
    a=sum(1 for k,d in zip(kept,diff) if not k and d); b=sum(1 for k,d in zip(kept,diff) if not k and not d)
    c=sum(1 for k,d in zip(kept,diff) if k and d); dd=sum(1 for k,d in zip(kept,diff) if k and not d)
    orr=((a+.5)*(dd+.5))/((b+.5)*(c+.5))
    per[f]={'n':len(rows),'modal_ec':modal,'lost_diff':a,'lost_same':b,'kept_diff':c,'kept_same':dd,'OR':orr,
            'examples_lost_diff':[(acc,nm) for (k,e,acc,nm),d in zip(rows,diff) if not k and d][:6]}
    if a+b>=5: tables.append(np.array([[a,b],[c,dd]])+0.5)
st=StratifiedTable(tables)
el=[v for v in per.values() if 'OR' in v and v['lost_diff']+v['lost_same']>=5]
summ={'eligible_families':len(el),'MH_OR':float(st.oddsratio_pooled),'MH_p':float(st.test_null_odds().pvalue),
      'frac_fam_OR_gt1':float(np.mean([v['OR']>1 for v in el]))}
for f,v in per.items(): print(f,{k:v[k] for k in v if k!='examples_lost_diff'})
print(json.dumps(summ,indent=1)); json.dump({'families':per,'summary':summ},open('results/primary.json','w'),indent=1)
