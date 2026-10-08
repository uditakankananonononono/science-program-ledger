"""B2 actual contiguous pipeline timing. Frozen protocol in benchmark/."""
import argparse,hashlib,json,subprocess,sys,time
from pathlib import Path
import numpy as np
from PIL import Image
from benchmark_b1 import coordinate_bfs,dijkstra,check_path
from mask_graph import mask_to_graph
from chain_aggregate import aggregate_chains,expand_route
from routing import exposure_budget_route


def worker(root,dataset,repetition):
    rows=json.loads((Path(__file__).parent/'benchmark/RESULTS.json').read_text())['records']
    row=next(r for r in rows if r['dataset']==dataset)
    mask=np.asarray(Image.open(Path(root)/(dataset+'_full_skeleton.png')))==255
    if hashlib.sha256(mask.tobytes()).hexdigest()!=row['skeleton_sha256']:raise ValueError('hash mismatch')
    graph=mask_to_graph(mask.astype(int).tolist(),8,1,0,(1,2))
    queries=row['queries'];oracle=coordinate_bfs(mask,queries[0]['start'])
    for q in queries:
        if oracle[q['goal']]!=q['steps']:raise AssertionError('query/oracle mismatch')
    def base():return [dijkstra(graph,q['start'],q['goal']) for q in queries]
    def candidate():
        g,w=aggregate_chains(graph);results=[]
        for q in queries:
            r=exposure_budget_route(g,q['start'],q['goal'],0)
            results.append((None,None) if r is None else (r['time'],expand_route(r,w)))
        return results
    timings={};order=[('dijkstra',base),('candidate_pipeline',candidate)]
    if repetition%2:order.reverse()
    for name,fn in order:
        before=time.perf_counter();results=fn();timings[name]=time.perf_counter()-before
        for q,(value,path) in zip(queries,results):
            if value!=q['steps']:raise AssertionError('objective mismatch')
            check_path(mask,path,q['start'],q['goal'],q['steps'])
    return {'dataset':dataset,'repetition':repetition,'status':'passed-correctness',
            'order':[n for n,_ in order],'timings_seconds':timings,'skeleton_sha256':row['skeleton_sha256'],
            'scope':'actual wall-timed artificial unit-cost development pipeline; magnitude not stable-superiority evidence'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root');p.add_argument('--worker');p.add_argument('--repetition',type=int,default=0);a=p.parse_args()
    if a.worker:print(json.dumps(worker(a.root,a.worker,a.repetition)))
    else:
        rows=[]
        for dataset in ('HRF','FIVES','FOVEA'):
            for rep in range(5):
                try:
                    r=subprocess.run([sys.executable,__file__,a.root,'--worker',dataset,'--repetition',str(rep)],capture_output=True,text=True,timeout=90)
                    rows.append(json.loads(r.stdout) if r.returncode==0 else {'dataset':dataset,'repetition':rep,'status':'failed','stderr':r.stderr})
                except subprocess.TimeoutExpired:rows.append({'dataset':dataset,'repetition':rep,'status':'timeout'})
        print(json.dumps({'records':rows},indent=2))
