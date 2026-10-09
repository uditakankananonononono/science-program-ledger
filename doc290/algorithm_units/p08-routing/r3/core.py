"""Bounded adversarial family and independent original-edge witness checker."""
import json,hashlib,sys,os,time,resource,subprocess,selectors,signal,math,dataclasses,heapq
from pathlib import Path
ROOT=Path(__file__).resolve().parent
class Invalid(ValueError):pass
MAX=2**53-1
def integer(v):
    if type(v) is not int or not 0<=v<=MAX:raise Invalid('strict integer cap')
    return v

def family(n):
    if type(n) is not int or not 1<=n<=10:raise Invalid('family n domain')
    G={f'v{i}':[{'target':f'v{i+1}','time':1,'exposure':2**i,'scenario_times':[2**i,0]},{'target':f'v{i+1}','time':1,'exposure':0,'scenario_times':[0,2**i]}] for i in range(n)};G[f'v{n}']=[]
    return G

def oracle(n,method):
    family(n);S=2**n-1
    if method=='scenario':return {'worst':2**(n-1),'budget':None,'minimizers':[2**(n-1)-1,2**(n-1)]}
    if method=='budget-scenario':
        B=2**(n-2)-1
        if n<2:raise Invalid('budget n domain')
        return {'worst':S-B,'budget':B,'minimizers':[B]}
    raise Invalid('method domain')

def witness(n,method,r):
    G=family(n);O=oracle(n,method)
    fields={'path','edges','scenario_totals','worst_time'}|({'exposure'} if method=='budget-scenario' else set())
    if type(r) is not dict or set(r)!=fields:raise Invalid('route fields')
    p=r['path'];es=r['edges']
    if type(p) is not list or p!=[f'v{i}' for i in range(n+1)] or any(type(v) is not str for v in p) or type(es) is not list or len(es)!=n:raise Invalid('route query/path')
    ss=[0,0];exposure=0;ledger=[]
    for a,b,e in zip(p,p[1:],es):
        if type(e) is not dict or set(e)!= {'source','edge_index','target'}:raise Invalid('witness fields')
        i=integer(e['edge_index'])
        if type(e['source']) is not str or type(e['target']) is not str or e['source']!=a or e['target']!=b or i>=len(G[a]) or G[a][i]['target']!=b:raise Invalid('edge index/identity')
        edge=G[a][i];ss=[integer(v+c) for v,c in zip(ss,edge['scenario_times'])];exposure=integer(exposure+edge['exposure']);ledger.append({'edge':[a,i],'scenarios':ss[:],'exposure':exposure})
    if type(r['scenario_totals']) is not list or len(r['scenario_totals'])!=2:raise Invalid('reported dimension')
    if [integer(v) for v in r['scenario_totals']]!=ss or integer(r['worst_time'])!=max(ss):raise Invalid('reported objective/totals')
    if method=='budget-scenario' and (integer(r['exposure'])!=exposure or exposure>O['budget']):raise Invalid('reported exposure/budget')
    if max(ss)!=O['worst']:raise Invalid('oracle objective mismatch')
    return {'status':'PASS','ledger':ledger,'reconstructed_exposure':exposure,'scenario_solver_exposure_field_absent':method=='scenario','oracle':O,'terminal_model_frontier':2**n,'observed_label_count':None}

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
        if args[0]=='subject':record['check']=witness(int(args[1]),args[2],payload['route'])
        record['status']='PASS'
    except (ValueError,KeyError,TypeError,IndexError) as e:record['reason']=type(e).__name__+': '+str(e)
    return record
