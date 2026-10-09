"""All cap/affinity enforcement precedes source reads and kernel imports."""
import resource,os,sys
try:
    resource.setrlimit(resource.RLIMIT_AS,(134217728,134217728))
    available=os.sched_getaffinity(0);os.sched_setaffinity(0,{min(available)})
    if len(os.sched_getaffinity(0))!=1 or resource.getrlimit(resource.RLIMIT_AS)!=(134217728,134217728):raise RuntimeError('cap/affinity verification')
    import json,time
    from core import gate,family,oracle,ROOT,Invalid
    identity=gate()
    mode=sys.argv[1]
    if mode=='sleep':
        print('sleep-ready',flush=True);time.sleep(20)
    if mode=='gatefail':raise Invalid('intentional gate refusal after real gate')
    if mode=='memory':x=bytearray(268435456)
    if mode=='badjson':print('not-json');sys.exit(0)
    if mode!='subject':raise Invalid('unknown mode')
    n=int(sys.argv[2]);method=sys.argv[3];O=oracle(n,method)
    sys.path.insert(0,str(ROOT.parent));from routing import Edge,scenario_robust_route,budgeted_scenario_route
    t=time.perf_counter();G={v:[Edge(e['target'],e['time'],e['exposure'],tuple(e['scenario_times'])) for e in es] for v,es in family(n).items()};build=time.perf_counter()-t
    t=time.perf_counter();r=scenario_robust_route(G,'v0',f'v{n}') if method=='scenario' else budgeted_scenario_route(G,'v0',f'v{n}',O['budget']);duration=time.perf_counter()-t
    print(json.dumps({'status':'OK','route':r,'solve_seconds':duration,'build_seconds':build,'rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'affinity':sorted(os.sched_getaffinity(0)),'as_limit_bytes':list(resource.getrlimit(resource.RLIMIT_AS)),'identity':identity},sort_keys=True))
except Exception as e:
    import json
    print(json.dumps({'status':'FAIL','exception_type':type(e).__name__,'exception':str(e)},sort_keys=True));sys.exit(2)
