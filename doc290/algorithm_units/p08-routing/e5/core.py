"""Bounded adversarial family and independent original-edge witness checker."""
import random,json,hashlib,sys,os,time,resource,subprocess,selectors,signal,math,dataclasses,heapq
from pathlib import Path
ROOT=Path(__file__).resolve().parent
class Invalid(ValueError):pass
from model import integer
def gate():
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
    if timed:record['reason']='worker timeout';return record
    if p.returncode!=0:record['reason']='worker nonzero';return record
    try:
        payload=json.loads(out);record['worker']=payload
        if type(payload) is not dict or payload.get('status')!='OK':raise Invalid('worker status')
        for k in ('solve_seconds','build_seconds'):
            v=payload[k]
            if type(v) not in (int,float) or not math.isfinite(v) or v<0:raise Invalid('worker timing type')
        integer(payload['rss_kib']);cpu=payload['affinity']
        if type(cpu) is not list or len(cpu)!=1 or type(cpu[0]) is not int:raise Invalid('worker affinity')
        if payload['as_limit_bytes']!=[134217728,134217728] or any(type(v) is not int for v in payload['as_limit_bytes']):raise Invalid('worker address cap')
        if payload.get('identity')!=gate():raise Invalid('worker source/runtime identity mismatch')
        if args[0] in ('subject','devsubject'):
            c=json.loads((ROOT/'cases.json').read_text())[int(args[1])] if args[0]=='subject' else {'statement':{'graph':{'q':[{'target':'z','time':1,'exposure':0,'scenario_times':[3,4]}],'z':[]},'start':'q','goal':'z'},'oracle':4}
            from model import witness,integer as exact_int
            if c['oracle'] is None:
                if payload['route'] is not None:raise Invalid('oracle unreachable disagreement')
                record['check']={'status':'PASS','unreachable_oracle':True}
            else:
                check=witness(c['statement'],payload['route'])
                if check['worst_time']!=exact_int(c['oracle']):raise Invalid('exact oracle disagreement')
                record['check']=dict(check,status='PASS')
            if args[2] in ('variant','p3'):
                counters=payload.get('counters')
                names={'reverse_relaxations','incumbent_relaxations','candidate_edges','lb_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue'}
                if type(counters) is not dict or set(counters)!=names:raise Invalid('counter fields')
                for v in counters.values():exact_int(v)
                if payload['incumbent'] is not None:witness(c['statement'],payload['incumbent'])
                if args[2]=='variant':
                    cert=payload.get('certificate');names={'early_exit','reason','start_distances','lower_bound','upper_bound'}
                    if type(cert) is not dict or set(cert)!=names or type(cert['early_exit']) is not bool:raise Invalid('certificate fields')
                    ns=len(next(e for es in c['statement']['graph'].values() for e in es)['scenario_times'])
                    if type(cert['start_distances']) is not list or len(cert['start_distances'])!=ns:raise Invalid('distance dimension')
                    for v in cert['start_distances']:
                        if v is not None:exact_int(v)
                    for k in ('lower_bound','upper_bound'):
                        if cert[k] is not None:exact_int(cert[k])
                    if cert['early_exit']:
                        if cert['lower_bound']!=cert['upper_bound'] or cert['lower_bound']!=max(cert['start_distances']) or payload['route']!=payload['incumbent']:raise Invalid('equality certificate mismatch')
                        for k in ('candidate_edges','labels_inserted','pops','stale_pops','max_live_queue'):
                            if counters[k]!=0:raise Invalid('early exit phase counter')
        record['status']='PASS'
    except (ValueError,KeyError,TypeError,IndexError) as e:record['reason']=type(e).__name__+': '+str(e)
    return record
