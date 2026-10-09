"""Bounded adversarial family and independent original-edge witness checker."""
import random,json,hashlib,sys,os,time,resource,subprocess,selectors,signal,math,dataclasses,heapq
from pathlib import Path
ROOT=Path(__file__).resolve().parent
from model import integer,Invalid,Failure
def gate():
    expected=(ROOT/'../../p08-field-planning/f3/verify.py').resolve();loaded=sys.modules.get('verify')
    if loaded is None or Path(getattr(loaded,'__file__','')).resolve()!=expected:raise Invalid('loaded verify path')
    manifest=json.loads((ROOT/'manifest.json').read_text())
    for name,digest in manifest['files'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise Invalid('source identity '+name)
    env=json.loads((ROOT/'environment.json').read_text())
    if sys.version!=env['python']:raise Invalid('python version')
    for name,entry in env['sources'].items():
        if hashlib.sha256(Path(entry['path']).read_bytes()).hexdigest()!=entry['sha256']:raise Invalid('runtime identity '+name)
    for name in env['modules']:
        m=sys.modules.get(name)
        if m is None or str(Path(getattr(m,'__file__',sys.executable)).resolve())!=env['sources'][name]['path']:raise Invalid('loaded runtime '+name)
    if str(Path(sys.executable).resolve())!=env['sources']['python_executable']['path']:raise Invalid('executable path')
    return {'manifest_sha256':hashlib.sha256((ROOT/'manifest.json').read_bytes()).hexdigest(),'runtime_sha256':hashlib.sha256((ROOT/'environment.json').read_bytes()).hexdigest()}

def launch(args,timeout=5):
    begin=time.perf_counter();env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    try:p=subprocess.Popen([sys.executable,str(ROOT/'worker.py'),*map(str,args)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
    except OSError as e:return {'status':'FAIL','reason':'spawn '+str(e),'returncode':None,'timed_out':False,'kill_sent':False,'reaped':False,'stdout':'','stderr':''}
    timed=False;killed=False
    try:out,err=p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed=True;p.kill();killed=True;out,err=p.communicate() # includes prior partial output; do NOT append TimeoutExpired.output
    elapsed=time.perf_counter()-begin
    record={'status':'FAIL','worker_elapsed_seconds':elapsed,'returncode':p.returncode,'timed_out':timed,'kill_sent':killed,'reaped':p.poll() is not None,'stdout':out.decode('utf-8',errors='replace'),'stderr':err.decode('utf-8',errors='replace')}
    return validate_record(args,record)

def validate_record(args,record,validated_identity=None):
    import copy
    record=copy.deepcopy(record)
    record.pop('worker',None);record.pop('check',None);record.pop('reason',None);record['status']='FAIL'
    if record['timed_out']:record['reason']='worker timeout';return record
    if record['returncode']!=0:record['reason']='worker nonzero';return record
    try:
        payload=json.loads(record['stdout']);record['worker']=payload
        if type(payload) is not dict or payload.get('status')!='OK':raise Invalid('worker status')
        for k in ('solve_seconds','build_seconds'):
            v=payload[k]
            if type(v) not in (int,float) or not math.isfinite(v) or v<0:raise Invalid('worker timing type')
        integer(payload['rss_kib']);cpu=payload['affinity']
        if type(cpu) is not list or len(cpu)!=1 or type(cpu[0]) is not int:raise Invalid('worker affinity')
        if payload['as_limit_bytes']!=[134217728,134217728] or any(type(v) is not int for v in payload['as_limit_bytes']):raise Invalid('worker address cap')
        if payload.get('identity')!=(gate() if validated_identity is None else validated_identity):raise Invalid('worker source/runtime identity mismatch')
        if args[0] in ('subject','devsubject','devmissing','devdomain'):
            from model import load_bytes
            c=load_bytes((ROOT/'cases.json').read_bytes())[int(args[1])] if args[0]=='subject' else devcase(args[0])
            result=payload['result']
            if result['status']!=c['expected']:raise Failure('expected verdict mismatch')
            from proof import verify
            if result['status']!='INVALID':verify(c['statement'],result)
            else:
                from model import model
                try:model(c['statement'])
                except Exception:pass
                else:raise Failure('INVALID without independent invalid input')
            record['check']={'status':'PASS','verdict':result['status'],'candidate_count':len(result['weights'])}
        record['status']='PASS'
    except (ValueError,KeyError,TypeError,IndexError,Failure) as e:record['reason']=type(e).__name__+': '+str(e)
    return record

def devstatement():
    return {'graph':{'q':[{'target':'z','time':1,'exposure':0,'scenario_times':[2,2]}],'z':[{'target':'q','time':1,'exposure':0,'scenario_times':[1,1]}]},'start':'q','goal':'z','budget':0,'forbidden':[[['q',0],['z',0]]],'penalties':[],'route':{'path':['q','z'],'edges':[{'source':'q','edge_index':0,'target':'z'}],'scenario_totals':[2,2],'worst_time':2,'exposure':0,'turn_penalty':0}}

def devcase(mode):
    s=devstatement();expected='CERTIFIED_INTEGRATED'
    if mode=='devmissing':s['route']=None;expected='UNAVAILABLE'
    elif mode=='devdomain':s['graph']['z']*=6;expected='UNAVAILABLE_DOMAIN'
    elif mode!='devsubject':raise Invalid('development mode')
    return {'statement':s,'expected':expected}
