import resource,os,sys
try:
    resource.setrlimit(resource.RLIMIT_AS,(134217728,134217728));os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    if len(os.sched_getaffinity(0))!=1 or resource.getrlimit(resource.RLIMIT_AS)!=(134217728,134217728):raise RuntimeError('cap/affinity')
    import json,time
    from core import gate,ROOT,Invalid
    identity=gate();mode=sys.argv[1]
    if mode=='sleep':print('sleep-ready',flush=True);time.sleep(20)
    if mode=='memory':x=bytearray(268435456)
    if mode=='gatefail':raise Invalid('intentional gate refusal after real gate')
    if mode=='badjson':print('not-json');sys.exit(0)
    if mode not in ('subject','devsubject'):raise Invalid('unknownmode')
    if mode=='subject':cases=json.loads((ROOT/'cases.json').read_text());s=cases[int(sys.argv[2])]['statement']
    else:
        from fixtures import development
        s=development()[int(sys.argv[2])]['statement']
    method=sys.argv[3]
    from model import model
    G,ns,_,_,_,_=model(s);counters=None;inc=None;t=time.perf_counter()
    from bindings import load
    if method not in ('variant','t12'):raise Invalid('method')
    m,pm=load('t13' if method=='variant' else 't12');solve=m.solve
    build=time.perf_counter()-t;t=time.perf_counter();result=solve(s);duration=time.perf_counter()-t;r=result['route'];counters=result['counters'];proof=result['proof'];certificate=result.get('certificate');scenario_proof=result.get('scenario_proof');incumbent=result.get('incumbent')
    print(json.dumps({'status':'OK','route':r,'counters':counters,'proof':proof,'certificate':certificate,'scenario_proof':scenario_proof,'incumbent':incumbent,'charged_proof':result.get('charged_proof'),'bound_trace':result.get('bound_trace',[]),'activation':result.get('activation'),'candidate_ledger':result.get('candidate_ledger'),'incumbent_original_upper':result.get('incumbent_original_upper'),'incumbent_selected_upper':result.get('incumbent_selected_upper'),'selected_candidate':result.get('selected_candidate'),'solve_seconds':duration,'build_seconds':build,'rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'affinity':sorted(os.sched_getaffinity(0)),'as_limit_bytes':list(resource.getrlimit(resource.RLIMIT_AS)),'identity':identity},sort_keys=True))
except Exception as e:
    import json
    print(json.dumps({'status':'FAIL','exception_type':type(e).__name__,'exception':str(e)},sort_keys=True));sys.exit(2)
