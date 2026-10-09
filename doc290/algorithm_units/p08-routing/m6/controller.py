import json,sys,time,hashlib,math,fcntl
from pathlib import Path
from core import ROOT,gate,launch,validate_record
from durable import transact,finalize,atomic,LockedFailure,encoded
from classes import classify
from analysis import summarize,order

def context():
    identity=gate();cases=json.loads((ROOT/'cases.json').read_text());classes=json.loads((ROOT/'classes.json').read_text());plan=json.loads((ROOT/'plan.json').read_text())
    if len(cases)!=200 or classes!=[classify(c['statement']) for c in cases]:raise LockedFailure('independent classes')
    expected=[]
    for i,c in enumerate(cases):
        sha=hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        for r in range(3):
            for m in order(i,r):expected.append({'case_index':i,'repeat':r,'method':m,'order':order(i,r),'name':c['name'],'class':classes[i],'input_sha256':sha,'oracle':c['oracle']})
    if encoded(plan)!=encoded(expected) or len(plan)!=1200:raise LockedFailure('unique ordered global plan')
    return identity,plan,classes

VALIDATED_IDENTITY=None
def validate(entry,result):
    names={'status','worker_elapsed_seconds','returncode','timed_out','kill_sent','reaped','stdout','stderr'}
    if type(result) is not dict or not names<=set(result) or set(result)-names-{'reason','worker','check'}:raise LockedFailure('complete receipt result schema')
    for k in ('timed_out','kill_sent','reaped'):
        if type(result[k]) is not bool:raise LockedFailure('receipt bool')
    if not result['reaped'] or type(result['returncode']) is not int or type(result['stdout']) is not str or type(result['stderr']) is not str:raise LockedFailure('receipt reap/rc/text')
    t=result['worker_elapsed_seconds']
    if type(t) not in (int,float) or not math.isfinite(t) or t<0:raise LockedFailure('receipt elapsed')
    checked=validate_record(['subject',entry['case_index'],entry['method']],result,validated_identity=VALIDATED_IDENTITY)
    if checked!=result:raise LockedFailure('saved checked payload mismatch')

def synthesize(path,receipts,classes):
    begin=time.monotonic();rows=[]
    for k in range(0,len(receipts),2):
        a,b=receipts[k:k+2];e=a['entry']
        if e['order']!=[a['entry']['method'],b['entry']['method']] or any(e[key]!=b['entry'][key] for key in ('case_index','repeat','name','class','oracle','input_sha256','order')):raise LockedFailure('pair structure')
        subjects={r['entry']['method']:r['result'] for r in (a,b)}
        rows.append({key:e[key] for key in ('case_index','repeat','name','class','order','oracle','input_sha256')}|{'subjects':subjects,'agreement':all(s['status']=='PASS' for s in subjects.values())})
    p={'rows':rows,'pair_count':len(rows),'attempt_count':len(receipts),'agreement_count':sum(r['agreement'] for r in rows),'pass_count':sum(s['status']=='PASS' for r in rows for s in r['subjects'].values()),'analysis':summarize(rows,classes),'scope':'fresh segmented global run/reused corpus/one local environment descriptive only'}
    atomic(path/'report.json',p,True)
    return time.monotonic()-begin

if __name__=='__main__':
    start=time.monotonic();run=Path(sys.argv[2])
    try:
        identity,plan,classes=context();VALIDATED_IDENTITY=identity
    except Exception as e:
        if run.exists():
            with open(run/'LOCK','a+b') as lock:
                fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
                if not (run/'FAIL.json').exists():atomic(run/'FAIL.json',{'status':'LOCKED_PREFLIGHT_FAILURE','reason':str(e)})
        raise
    if sys.argv[1]=='chunk':r=transact(run,plan,identity,validate,lambda e:launch(['subject',e['case_index'],e['method']]),started=start)
    elif sys.argv[1]=='finalize':r=finalize(run,plan,identity,validate,lambda p,rs:synthesize(p,rs,classes),started=start)
    else:raise ValueError('chunk or finalize')
    print(json.dumps(r,sort_keys=True))
