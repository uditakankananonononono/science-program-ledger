"""Pure preregistered eligibility/nearest-rank descriptive timing analysis."""
import math

def order(case_index,repeat):return ['variant','p3'] if (case_index+repeat)%2==0 else ['p3','variant']
def duration(v):return type(v) in (int,float) and math.isfinite(v) and v>0

def quartiles(values):
    if not values:return {'status':'UNAVAILABLE','count':0}
    xs=sorted(values)
    return {'status':'AVAILABLE','count':len(xs),'q25':xs[math.ceil(.25*len(xs))-1],'median':xs[math.ceil(.5*len(xs))-1],'q75':xs[math.ceil(.75*len(xs))-1]}

def paired_ratio(a,b):
    if not duration(a) or not duration(b):return {'eligible':False,'reason':'nonpositive_or_nonfinite_duration'}
    ratio=a/b
    if not math.isfinite(ratio) or ratio<=0:return {'eligible':False,'reason':'unrepresentable_ratio'}
    log=math.log(ratio)
    if not math.isfinite(log):return {'eligible':False,'reason':'unrepresentable_log'}
    return {'eligible':True,'ratio':ratio,'logratio':log}

def deterministic(subject):
    w=subject.get('worker',{})
    return {k:w.get(k) for k in ('route','counters','incumbent','beam_info','identity','affinity','as_limit_bytes')}

def summarize(rows,case_count=200):
    records=[];cases={};work={};exclusions={'worker_failure':0,'cpu_mismatch':0,'nonpositive_or_nonfinite_duration':0,'unrepresentable_ratio':0,'unrepresentable_log':0};cpu_mismatches=0
    for row in rows:
        rec={'case_index':row['case_index'],'name':row['name'],'repeat':row['repeat'],'order':row['order'],'eligible':False};subjects=row['subjects'];a=subjects['variant'];b=subjects['p3']
        if a['status']!='PASS' or b['status']!='PASS':reason='worker_failure'
        elif a['worker']['affinity']!=b['worker']['affinity']:reason='cpu_mismatch';cpu_mismatches+=1
        else:
            rec.update(paired_ratio(a['worker']['solve_seconds'],b['worker']['solve_seconds']));reason=rec.get('reason')
        if reason:rec.update(reason=reason);exclusions[reason]+=1
        if rec['eligible']:cases.setdefault(row['case_index'],{})[row['repeat']]=rec['ratio']
        if a['status']=='PASS' and b['status']=='PASS':
            work.setdefault(row['case_index'],{})[row['repeat']]={m:deterministic(subjects[m]) for m in ('variant','p3')}
        records.append(rec)
    case_medians=[];incomplete=0;repeat_check=[]
    for case_index in range(case_count):
        rs=cases.get(case_index,{})
        if set(rs)=={0,1,2}:case_medians.append({'case_index':case_index,'median':quartiles(list(rs.values()))['median']})
        else:incomplete+=1
        ws=work.get(case_index,{})
        repeat_check.append({'case_index':case_index,'status':'PASS' if set(ws)=={0,1,2} and ws[0]==ws[1]==ws[2] else 'FAIL' if set(ws)=={0,1,2} else 'UNAVAILABLE'})
    eligible=[r for r in records if r['eligible']];ratios=[r['ratio'] for r in eligible];logs=[r['logratio'] for r in eligible]
    return {'pairs':records,'pair_ratio_distribution':quartiles(ratios),'pair_log_distribution':quartiles(logs),'pair_exclusions':exclusions,'pair_denominator':len(rows),'eligible_pair_count':len(eligible),'descriptive_wins':sum(v<1 for v in ratios),'ties':sum(v==1 for v in ratios),'losses':sum(v>1 for v in ratios),'case_medians':case_medians,'case_ratio_distribution':quartiles([c['median'] for c in case_medians]),'case_denominator':case_count,'incomplete_case_exclusions':incomplete,'actual_pair_cpu_mismatch_count':cpu_mismatches,'deterministic_repeat_checks':repeat_check,'p4_first_pairs':sum(r['order'][0]=='variant' for r in rows),'p3_first_pairs':sum(r['order'][0]=='p3' for r in rows)}
