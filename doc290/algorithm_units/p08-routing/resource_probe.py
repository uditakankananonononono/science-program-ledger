"""Bounded synthetic-grid characterization. Not a scalability guarantee."""
import argparse,json,resource,subprocess,sys,time
from mask_graph import mask_to_graph
from routing import integrated_route


def worker(size):
    before=time.perf_counter()
    graph=mask_to_graph([[1]*size for _ in range(size)],4,1,1,(1,2))
    build=time.perf_counter()-before
    before=time.perf_counter()
    result=integrated_route(graph,'0,0',f'{size-1},{size-1}',2*(size-1))
    elapsed=time.perf_counter()-before
    expected=2*(size-1)
    if result is None or result['exposure']!=expected or result['scenario_totals']!=[expected,2*expected]:
        raise AssertionError('uniform-grid Manhattan objective mismatch')
    return {'size':size,'vertices':len(graph),'directed_edges':sum(map(len,graph.values())),
            'build_seconds':build,'solve_seconds':elapsed,'peak_process_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'oracle':'unit-cost 4-neighbor full-grid Manhattan distance','expected_steps':expected,
            'status':'passed','scenario_totals':result['scenario_totals']}


def probe(sizes=(5,10,20,30),timeout=5):
    records=[]
    for size in sizes:
        try:
            p=subprocess.run([sys.executable,__file__,'--worker',str(size)],capture_output=True,text=True,timeout=timeout)
            if p.returncode==0:records.append(json.loads(p.stdout))
            else:records.append({'size':size,'status':'failed','returncode':p.returncode,'stderr':p.stderr})
        except subprocess.TimeoutExpired:
            records.append({'size':size,'status':'timeout','timeout_seconds':timeout})
    return {'scope':'synthetic uniform grids only; timings are observations, not performance gates',
            'rss_scope':'Linux worker whole-process lifetime peak, including interpreter and imports; not isolated solver allocation',
            'timeout_per_worker_seconds':timeout,'records':records}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker',type=int)
    args=parser.parse_args()
    if args.worker is not None:
        if not 2<=args.worker<=30:parser.error('worker size must be 2..30')
        print(json.dumps(worker(args.worker)))
    else:print(json.dumps(probe(),indent=2))
