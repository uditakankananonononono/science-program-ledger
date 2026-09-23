import json, random
parts=json.load(open('results/gc90_parts.json'))
TARGETS={'pyruvate':['YLR044C','YLR134W','YGR087C'],
         'L-lactate':['YLR044C','YOL086C'],
         'fumarate':['YPL262W'],
         'ethanol':['YOL059W','YDL022W','YLL043W','YMR303C','YEL071W'],
         '23BDO':['YLR044C','YLR134W'],
         'succinate':['YPL262W','YLL041C','YKL141W']}  # calibration only
genes=sorted(parts.keys()); N=len(genes)
def percentiles(product):
    vals=sorted(((parts[g][product] if parts[g][product] is not None else -1) for g in genes))
    # average ranks for ties
    rank={}
    i=0
    sv=sorted(set(vals))
    for v in sv:
        idx=[j for j,x in enumerate(vals) if x==v]
        rank[v]=sum(j+1 for j in idx)/len(idx)
    return {g: (rank[parts[g][product] if parts[g][product] is not None else -1]-0.5)/N for g in genes}  # rank asc; high export -> high percentile (matches R3 'rank desc -> percentile')
out={'n_scanned':N,'products':{}}
for prod,tset in TARGETS.items():
    if any(t not in parts for t in tset):
        out['products'][prod]={'error':'target missing from scan'}; continue
    pc=percentiles(prod)
    score=sum(pc[t] for t in tset)/len(tset)
    nont=[g for g in genes if g not in tset]
    rng=random.Random(20260924)
    nulls=[]
    for _ in range(200):
        draw=rng.sample(nont,len(tset))
        nulls.append(sum(pc[d] for d in draw)/len(draw))
    out['products'][prod]={'targets':tset,'score':score,'null_max':max(nulls),'null_mean':sum(nulls)/len(nulls),
                           'pass':score>max(nulls),
                           'target_percentiles':{t:pc[t] for t in tset}}
    top=sorted(pc,key=lambda g:-pc[g])[:10]
    out['products'][prod]['top10']=top
json.dump(out,open('results/meteng_scores.json','w'),indent=1)
ev=['pyruvate','L-lactate','fumarate','ethanol','23BDO']
npass=sum(1 for p in ev if out['products'][p]['pass'])
npass_nofum=sum(1 for p in ev if p!='fumarate' and out['products'][p]['pass'])
print('succinate (calibration):',out['products']['succinate']['pass'],round(out['products']['succinate']['score'],3),'vs null max',round(out['products']['succinate']['null_max'],3))
for p in ev:
    r=out['products'][p]
    tps=', '.join('%s:%.2f' % (t, r['target_percentiles'][t]) for t in r['targets'])
    print('%-10s score %.4f vs null max %.4f -> %s  target pcts: %s' % (p, r['score'], r['null_max'], 'PASS' if r['pass'] else 'FAIL', tps))
print('EVALUATED pass:',npass,'/ 5 | without fumarate:',npass_nofum,'/ 4 | GATE:', 'PASS' if (npass>=3 and (npass>=3)==(npass_nofum>=3)) else 'FAIL')
