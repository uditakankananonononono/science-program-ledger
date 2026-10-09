import os,sys,resource
try:
    resource.setrlimit(resource.RLIMIT_AS,(134217728,134217728));os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if resource.getrlimit(resource.RLIMIT_AS)!=(134217728,134217728) or len(os.sched_getaffinity(0))!=1:raise RuntimeError('caps')
    import time,json
    from core import gate,ROOT,devstatement
    from model import Invalid,load_bytes
    identity=gate();mode=sys.argv[1]
    if mode=='sleep':print('sleep-ready',flush=True);time.sleep(20)
    if mode=='memory':x=bytearray(268435456)
    if mode=='gatefail':raise Invalid('intentional gate refusal')
    if mode=='badjson':print('not-json');sys.exit(0)
    if mode not in ('subject','devsubject'):raise Invalid('mode')
    s=load_bytes((ROOT/'cases.json').read_bytes())[int(sys.argv[2])]['statement'] if mode=='subject' else devstatement()
    start=time.perf_counter();from generator import generate
    build=time.perf_counter()-start;start=time.perf_counter();result=generate(s);duration=time.perf_counter()-start
    print(json.dumps({'status':'OK','result':result,'build_seconds':build,'solve_seconds':duration,'rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'affinity':sorted(os.sched_getaffinity(0)),'as_limit_bytes':list(resource.getrlimit(resource.RLIMIT_AS)),'identity':identity},sort_keys=True))
except Exception as e:
    import json
    print(json.dumps({'status':'FAIL','exception_type':type(e).__name__,'exception':str(e)}));sys.exit(2)
