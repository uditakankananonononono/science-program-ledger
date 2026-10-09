"""Fixed32 single-subject slots; durable M6-style state, no end-only execution."""
import json,time,sys,hashlib,math,fcntl
from pathlib import Path
from core import ROOT,gate,launch,validate_record
from model import load_bytes
from durable import transact,finalize,atomic,encoded,LockedFailure
IDENTITY=None

def context():
    identity=gate();cases=load_bytes((ROOT/'cases.json').read_bytes());plan=load_bytes((ROOT/'plan.json').read_bytes())
    expected=[{'case_index':k,'name':c['name'],'expected':c['expected'],'input_sha256':hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest()} for k,c in enumerate(cases)]
    if len(expected)!=32 or encoded(plan)!=encoded(expected):raise LockedFailure('unique fixed32 plan')
    return identity,plan

def validate(e,r):
    names={'status','worker_elapsed_seconds','returncode','timed_out','kill_sent','reaped','stdout','stderr'}
    if type(r) is not dict or not names<=set(r) or set(r)-names-{'worker','check','reason'}:raise LockedFailure('receipt schema')
    if any(type(r[k]) is not bool for k in ('timed_out','kill_sent','reaped')) or not r['reaped'] or type(r['returncode']) is not int or type(r['stdout']) is not str or type(r['stderr']) is not str:raise LockedFailure('receipt rc/reap/types')
    t=r['worker_elapsed_seconds']
    if type(t) not in (int,float) or not math.isfinite(t) or t<0:raise LockedFailure('receipt elapsed')
    checked=validate_record(['subject',e['case_index']],r,validated_identity=IDENTITY)
    if encoded(checked)!=encoded(r):raise LockedFailure('canonical checked result')

def synthesize(path,receipts):
    rows=[{'name':r['entry']['name'],'expected':r['entry']['expected'],'input_sha256':r['entry']['input_sha256'],'receipt':r['result'],'agreement':r['result']['status']=='PASS'} for r in receipts]
    atomic(path/'report.json',{'identity':IDENTITY,'rows':rows,'row_count':len(rows),'agreement_count':sum(r['agreement'] for r in rows),'scope':'finite incomplete certificate generator/durable fixed32'},True)

if __name__=='__main__':
    begin=time.monotonic();run=Path(sys.argv[2])
    try:IDENTITY,plan=context()
    except Exception as e:
        if run.exists():
            with open(run/'LOCK','a+b') as lock:
                fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
                if not (run/'FAIL.json').exists():atomic(run/'FAIL.json',{'status':'LOCKED_PREFLIGHT_FAILURE','reason':str(e)})
        raise
    if sys.argv[1]=='chunk':r=transact(run,plan,IDENTITY,validate,lambda e:launch(['subject',e['case_index']]),limit=4,ceiling=30,headroom=7,started=begin)
    elif sys.argv[1]=='finalize':r=finalize(run,plan,IDENTITY,validate,synthesize,started=begin)
    else:raise ValueError('chunk/finalize')
    print(json.dumps(r,sort_keys=True))
