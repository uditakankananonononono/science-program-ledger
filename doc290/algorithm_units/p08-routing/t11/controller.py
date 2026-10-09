import json,sys,time,hashlib,math,fcntl
from pathlib import Path
from core import ROOT,gate,launch,validate_record
from durable import transact,finalize,atomic,LockedFailure,encoded
IDENTITY=None
def order(i):return ['variant','t9'] if i%2==0 else ['t9','variant']
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
    rows=[]
    for k in range(0,len(receipts),2):
        a,b=receipts[k:k+2];e=a['entry']
        if e['order']!=[a['entry']['method'],b['entry']['method']] or any(e[key]!=b['entry'][key] for key in ('case_index','name','oracle','input_sha256','order')):raise LockedFailure('actual pair structure')
        subjects={r['entry']['method']:r['result'] for r in (a,b)};rows.append({key:e[key] for key in ('case_index','name','order','oracle','input_sha256')}|{'subjects':subjects,'agreement':all(s['status']=='PASS' for s in subjects.values())})
    comparable=[r for r in rows if r['agreement']];comparison={}
    for counter in ('labels_inserted','candidate_edges'):
        deltas=[r['subjects']['variant']['worker']['counters'][counter]-r['subjects']['t9']['worker']['counters'][counter] for r in comparable];comparison[counter]={'wins':sum(v<0 for v in deltas),'ties':sum(v==0 for v in deltas),'losses':sum(v>0 for v in deltas),'denominator':len(comparable),'failure_excluded':len(rows)-len(comparable)}
    from collections import Counter
    variants=[r['subjects']['variant']['worker'] for r in comparable];totals={k:sum(v['counters'][k] for v in variants) for k in variants[0]['counters']} if variants else {}
    p={'rows':rows,'pair_count':len(rows),'attempt_count':len(receipts),'agreement_count':len(comparable),'pass_count':sum(s['status']=='PASS' for r in rows for s in r['subjects'].values()),'comparison':comparison,'variant_classes':dict(Counter(v['certificate']['reason'] for v in variants)),'variant_counter_totals':totals,'source_bound_stronger':sum(v['certificate']['source_bound_stronger'] for v in variants),'extra_exclusion_cases':sum(v['counters']['charged_strict_exclusions']>0 for v in variants),'scope':'fresh synthetic paired400 one run, no timing superiority'}
    atomic(path/'report.json',p,True)
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
