"""Frozen descriptive analysis over structurally checked report rows."""
import math,collections
CLASSES=('no_allowed_turn_path','budget_infeasible','equality_exit','strict_gap_search')
def order(i,r):return ['variant','t8'] if (i+r)%2==0 else ['t8','variant']
def quartiles(xs):
    if not xs:return {'count':0,'q25':None,'median':None,'q75':None}
    xs=sorted(xs);return {'count':len(xs),'q25':xs[math.ceil(.25*len(xs))-1],'median':xs[math.ceil(.5*len(xs))-1],'q75':xs[math.ceil(.75*len(xs))-1]}
def ratio(a,b):
    if type(a) not in (int,float) or type(b) not in (int,float) or not math.isfinite(a) or not math.isfinite(b) or a<0 or b<0:return {'eligible':False,'reason':'invalid_duration'}
    if a==0 or b==0:return {'eligible':False,'reason':'zero_duration'}
    r=a/b
    if not math.isfinite(r) or r<=0:return {'eligible':False,'reason':'numeric_ratio'}
    log=math.log(r)
    if not math.isfinite(log):return {'eligible':False,'reason':'numeric_log'}
    return {'eligible':True,'ratio':r,'logratio':log}
def deterministic(w):return {k:w.get(k) for k in ('route','counters','proof','scenario_proof','incumbent','certificate','identity','affinity','as_limit_bytes')}
def group(rows,indices):
    recs=[];cases={};work={};exc=collections.Counter()
    for row in rows:
        a=row['subjects']['variant'];b=row['subjects']['t8'];rec={k:row[k] for k in ('case_index','repeat','name','order','class')};rec['eligible']=False
        if a['status']!='PASS' or b['status']!='PASS':rec['reason']='worker_failure'
        elif a['worker']['affinity']!=b['worker']['affinity']:rec['reason']='cpu_mismatch'
        else:rec.update(ratio(a['worker']['solve_seconds'],b['worker']['solve_seconds']))
        if rec['eligible']:cases.setdefault(row['case_index'],{})[row['repeat']]=rec['ratio']
        else:exc[rec['reason']]+=1
        if a['status']=='PASS' and b['status']=='PASS':work.setdefault(row['case_index'],{})[row['repeat']]={m:deterministic(row['subjects'][m]['worker']) for m in ('variant','t8')}
        recs.append(rec)
    cms=[];checks=[]
    for i in indices:
        rr=cases.get(i,{})
        if set(rr)=={0,1,2}:cms.append({'case_index':i,'median':quartiles(list(rr.values()))['median']})
        ww=work.get(i,{})
        checks.append({'case_index':i,'status':'PASS' if set(ww)=={0,1,2} and ww[0]==ww[1]==ww[2] else 'FAIL' if set(ww)=={0,1,2} else 'UNAVAILABLE'})
    eligible=[r for r in recs if r['eligible']];rs=[r['ratio'] for r in eligible]
    return {'pairs':recs,'pair_denominator':len(rows),'eligible_pairs':len(eligible),'exclusions':dict(exc),'faster':sum(r<1 for r in rs),'ties':sum(r==1 for r in rs),'slower':sum(r>1 for r in rs),'ratio_distribution':quartiles(rs),'log_distribution':quartiles([r['logratio'] for r in eligible]),'case_denominator':len(indices),'complete_cases':len(cms),'incomplete_cases':len(indices)-len(cms),'case_medians':cms,'case_ratio_distribution':quartiles([r['median'] for r in cms]),'deterministic_checks':checks,'actual_order_counts':{'T9_first':sum(r['order'][0]=='variant' for r in rows),'T8_first':sum(r['order'][0]=='t8' for r in rows)}}
def summarize(rows,classes):
    expected={(i,r) for i in range(len(classes)) for r in range(3)};keys=[(r['case_index'],r['repeat']) for r in rows]
    if len(keys)!=len(expected) or set(keys)!=expected:raise ValueError('unique complete case/repeat structure')
    for r in rows:
        if r['order']!=order(r['case_index'],r['repeat']) or r['class']!=classes[r['case_index']]:raise ValueError('order/class structure')
    out={'all_cases':group(rows,list(range(len(classes)))),'classes':{}}
    for c in CLASSES:
        ids=[i for i,k in enumerate(classes) if k==c];out['classes'][c]=group([r for r in rows if r['class']==c],ids)
    return out
