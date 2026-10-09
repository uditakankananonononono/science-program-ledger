import json,sys,time,hashlib,math,fcntl
from pathlib import Path
from core import ROOT,gate,launch,validate_record
from durable import transact,finalize,atomic,LockedFailure,encoded
IDENTITY=None
def order(i):return ['variant','t16'] if i%2==0 else ['t16','variant']
def context():
    identity=gate();cases=json.loads((ROOT/'cases.json').read_text());plan=json.loads((ROOT/'plan.json').read_text());expected=[]
    for i,c in enumerate(cases):
        sha=hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        for m in order(i):expected.append({'case_index':i,'method':m,'order':order(i),'name':c['name'],'input_sha256':sha,'oracle':c['oracle']})
    if len(cases)!=200 or len(expected)!=400 or encoded(plan)!=encoded(expected):raise LockedFailure('exact400 pairedplan')
    return identity,plan

def validate(e,r):
    names={'status','worker_elapsed_seconds','returncode','timed_out','kill_sent','reaped','stdout','stderr'}
    if type(r) is not dict or not names<=set(r) or set(r)-names-{'reason','worker','check'}:raise LockedFailure('complete receipt schema')
    if any(type(r[k]) is not bool for k in ('timed_out','kill_sent','reaped')) or not r['reaped'] or type(r['returncode']) is not int or type(r['stdout']) is not str or type(r['stderr']) is not str:raise LockedFailure('receipt reap/rc/types')
    t=r['worker_elapsed_seconds']
    if type(t) not in (int,float) or not math.isfinite(t) or t<0:raise LockedFailure('receipt elapsed')
    checked=validate_record(['subject',e['case_index'],e['method']],r,validated_identity=IDENTITY)
    if encoded(checked)!=encoded(r):raise LockedFailure('canonical old receipt')

def synthesize(path,receipts):
    # Called only after frozen exact-400 execution and canonical receipt validation.
    if len(receipts)!=400:raise LockedFailure('synthesis exact400')
    rows=[]
    for k in range(0,400,2):
        a,b=receipts[k:k+2];e=a['entry']
        if a['slot']!=k or b['slot']!=k+1 or e['case_index']!=k//2 or e['order']!=order(k//2) or e['order']!=[a['entry']['method'],b['entry']['method']] or any(e[key]!=b['entry'][key] for key in ('case_index','name','oracle','input_sha256','order')):raise LockedFailure('actual pair structure')
        subjects={r['entry']['method']:r['result'] for r in (a,b)}
        if set(subjects)!={'variant','t16'}:raise LockedFailure('pair method coverage')
        rows.append({key:e[key] for key in ('case_index','name','order','oracle','input_sha256')}|{'subjects':subjects,'agreement':all(s['status']=='PASS' for s in subjects.values())})
    paired=[r for r in rows if r['agreement']]
    def counters(worker,counter,method):
        # Transport alignment only; baseline method payload/checker is unchanged.
        if counter=='weighted_candidate_inspections' and method=='t16':return 0
        return worker['counters'][counter]
    categories=('reverse_relaxations','scenario_reverse_inspections','incumbent_inspections','scalar_candidate_inspections','weighted_candidate_inspections','charged_reverse_inspections','labels_inserted','candidate_edges','pops','stale_pops','max_live_queue','forbidden_skipped','feasibility_pruned','dominance_pruned','objective_bound_pruned','charged_bound_stronger','charged_strict_exclusions')
    comparison={}
    for counter in categories:
        deltas=[counters(r['subjects']['variant']['worker'],counter,'variant')-counters(r['subjects']['t16']['worker'],counter,'t16') for r in paired]
        comparison[counter]={'wins':sum(v<0 for v in deltas),'ties':sum(v==0 for v in deltas),'losses':sum(v>0 for v in deltas),'denominator':len(paired),'failure_excluded':200-len(paired)}
    from collections import Counter
    methods={}
    for method in ('variant','t16'):
        attempts=[r['subjects'][method] for r in rows];passed=[r['worker'] for r in attempts if r['status']=='PASS']
        paired_workers=[r['subjects'][method]['worker'] for r in paired]
        active=[v for v in passed if v['candidate_prefix'] is not None]
        candidate_rows=[row for v in active for row in v['candidate_ledger']]
        def route_id(row):return encoded(row['route']['edges'])
        duplicates=sum(sum(route_id(row) in {route_id(prev) for prev in v['candidate_ledger'][:i]} for i,row in enumerate(v['candidate_ledger'])) for v in active)
        methods[method]={'attempt_count':200,'pass_count':len(passed),'failure_count':200-len(passed),'all_pass_counter_totals':{key:sum(counters(v,key,method) for v in passed) for key in categories},'paired_pass_counter_totals':{key:sum(counters(v,key,method) for v in paired_workers) for key in categories},'candidate_activation_classes':dict(Counter(v['candidate_activation'] for v in passed)),'prefix_terminal_classes':dict(Counter(v['candidate_prefix']['terminal_reason'] for v in active)),'produced_candidate_rows':len(candidate_rows),'eligible_candidate_rows':sum(row['audit']['eligible'] for row in candidate_rows),'overbudget_candidate_rows':sum(not row['audit']['eligible'] for row in candidate_rows),'duplicate_candidate_rows':duplicates,'positive_remaining_equality_prefix_count':sum(v['candidate_prefix']['terminal_reason']=='bound_equality' and bool(v['candidate_prefix']['remaining_scenario_indices']) for v in active),'last_equality_prefix_count':sum(v['candidate_prefix']['terminal_reason']=='bound_equality' and not v['candidate_prefix']['remaining_scenario_indices'] for v in active),'remaining_scenario_index_count':sum(len(v['candidate_prefix']['remaining_scenario_indices']) for v in active),'omitted_route_eligibility':'UNKNOWN, not constructed/audited'}
    weighted=[r for r in paired if r['subjects']['variant']['worker']['weighted_proof'] is not None]
    # Compare final incumbent W against baseline only on actual weighted activations.
    differences=[r['subjects']['variant']['worker']['incumbent_selected_upper']-r['subjects']['t16']['worker']['incumbent_selected_upper'] for r in weighted]
    weighted_rows=[r['subjects']['variant']['worker']['candidate_ledger'][-1] for r in weighted]
    selected_weighted=sum(r['subjects']['variant']['worker']['selected_candidate']==r['subjects']['variant']['worker']['weighted_proof']['weighted_index'] for r in weighted)
    report={'rows':rows,'attempt_count':400,'pair_count':200,'pass_count':sum(r['subjects'][m]['status']=='PASS' for r in rows for m in ('variant','t16')),'failure_count':sum(r['subjects'][m]['status']!='PASS' for r in rows for m in ('variant','t16')),'agreement_count':len(paired),'paired_failure_excluded':200-len(paired),'comparison':comparison,'methods':methods,'weighted_activated_W_vs_baseline':{'denominator':len(weighted),'improved':sum(v<0 for v in differences),'tied':sum(v==0 for v in differences),'worsened':sum(v>0 for v in differences),'excluded_early_original_charged_prefix_skips':len(paired)-len(weighted),'excluded_failed_pairs':200-len(paired),'eligible_rows':sum(row['audit']['eligible'] for row in weighted_rows),'overbudget_rows':sum(not row['audit']['eligible'] for row in weighted_rows),'selected_weighted_rows':selected_weighted},'scope':'one preregistered fixed400 T17/T16 run only after reviewed published freeze; no speed/total-work/invention claim','baseline_weighted_alignment':'comparison-layer zero only; immutable T16 payload/checker untouched'}
    atomic(path/'report.json',report,True)
if __name__=='__main__':
    start=time.monotonic();run=Path(sys.argv[2])
    try:IDENTITY,plan=context()
    except Exception as e:
        if run.exists():
            with open(run/'LOCK','a+b') as lock:
                fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
                if not (run/'FAIL.json').exists():atomic(run/'FAIL.json',{'status':'LOCKED_PREFLIGHT_FAILURE','reason':str(e)})
        raise
    if sys.argv[1]=='chunk':r=transact(run,plan,IDENTITY,validate,lambda e:launch(['subject',e['case_index'],e['method']]),limit=4,ceiling=30,headroom=7,started=start)
    elif sys.argv[1]=='finalize':r=finalize(run,plan,IDENTITY,validate,synthesize,started=start)
    else:raise ValueError('chunk/finalize')
    print(json.dumps(r,sort_keys=True))
