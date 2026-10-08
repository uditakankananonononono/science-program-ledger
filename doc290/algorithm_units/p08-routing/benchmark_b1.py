"""Frozen B1 development shortest-step benchmark. See benchmark/PROTOCOL.md."""
import argparse,hashlib,heapq,json,statistics,subprocess,sys,time
from collections import deque
from pathlib import Path
from PIL import Image
import numpy as np
from mask_graph import mask_to_graph
from chain_compress import compress_chains
from chain_aggregate import aggregate_chains,expand_route
from routing import exposure_budget_route


def dijkstra(graph,start,goal):
    distances={start:0};parent={};queue=[(0,start)]
    while queue:
        cost,node=heapq.heappop(queue)
        if cost!=distances[node]:continue
        if node==goal:
            path=[goal]
            while path[-1]!=start:path.append(parent[path[-1]])
            return cost,list(reversed(path))
        for e in graph[node]:
            value=cost+e.time
            if value<distances.get(e.target,float('inf')):
                distances[e.target]=value;parent[e.target]=node;heapq.heappush(queue,(value,e.target))
    return None,None


def coordinate_bfs(mask,start):
    distance={start:0};q=deque([start])
    while q:
        v=q.popleft();y,x=map(int,v.split(','))
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                a,b=y+dy,x+dx
                if not (dy or dx) or not 0<=a<mask.shape[0] or not 0<=b<mask.shape[1] or not mask[a,b]:continue
                key=f'{a},{b}'
                if key not in distance:distance[key]=distance[v]+1;q.append(key)
    return distance


def check_path(mask,path,start,goal,steps):
    if path is None or path[0]!=start or path[-1]!=goal or len(path)-1!=steps:raise AssertionError('wrong route endpoints or objective')
    for a,b in zip(path,path[1:]):
        y,x=map(int,a.split(','));u,v=map(int,b.split(','))
        if not mask[y,x] or not mask[u,v] or max(abs(y-u),abs(x-v))!=1:raise AssertionError('invalid pixel step')


def worker(root,dataset):
    root=Path(root)
    records=json.loads((Path(__file__).parent/'data_audit/three_first_mask_unit_cost_routes.json').read_text())
    item=next(r for r in records if r['dataset']==dataset)
    mask=np.asarray(Image.open(root/(dataset+'_full_skeleton.png')))==255
    if hashlib.sha256(mask.tobytes()).hexdigest()!=item['skeleton_sha256']:raise ValueError('input hash mismatch')
    graph=mask_to_graph(mask.astype(int).tolist(),8,1,0,(1,2))
    anchors=compress_chains(graph)['anchors'];start=anchors[0];oracle=coordinate_bfs(mask,start)
    goals=sorted((a for a in anchors if a!=start and a in oracle),key=lambda a:(oracle[a],a),reverse=True)[:10]
    if not goals:raise ValueError('no benchmark target')
    preprocessing=[];compressed=None;witnesses=None
    for _ in range(5):
        before=time.perf_counter();compressed,witnesses=aggregate_chains(graph);preprocessing.append(time.perf_counter()-before)
    def original(goal):return dijkstra(graph,start,goal)
    def candidate(goal):
        r=exposure_budget_route(compressed,start,goal,0)
        return (None,None) if r is None else (r['time'],expand_route(r,witnesses))
    timings={name:[] for name in ('dijkstra','compressed')}
    queries=[{'start':start,'goal':g,'steps':oracle[g]} for g in goals]
    for goal in goals:
        for fn in (original,candidate):
            value,path=fn(goal)
            if value!=oracle[goal]:raise AssertionError('warmup objective mismatch')
            check_path(mask,path,start,goal,oracle[goal])
    for repetition in range(5):
        per={name:[] for name in timings}
        order=(('dijkstra',original),('compressed',candidate))
        if repetition%2:order=tuple(reversed(order))
        for goal in goals:
            for name,fn in order:
                before=time.perf_counter();value,path=fn(goal);elapsed=time.perf_counter()-before
                per[name].append(elapsed)
                if value!=oracle[goal]:raise AssertionError('scored objective mismatch')
                check_path(mask,path,start,goal,oracle[goal])
        for name in per:timings[name].append(per[name])
    sums={name:[sum(rep) for rep in timing] for name,timing in timings.items()}
    base=statistics.median(sums['dijkstra']);query=statistics.median(sums['compressed'])
    prep=statistics.median(preprocessing)
    combined=statistics.median([a+b for a,b in zip(preprocessing,sums['compressed'])])
    return {'dataset':dataset,'status':'passed-correctness','skeleton_sha256':item['skeleton_sha256'],'queries':queries,
            'preprocessing_seconds_raw':preprocessing,'query_seconds_raw':timings,
            'median_baseline_query_total_seconds':base,'median_candidate_query_total_seconds':query,
            'median_preprocessing_seconds':prep,'median_candidate_preprocess_plus_query_seconds':combined,
            'candidate_query_faster':query<base,'candidate_total_faster':combined<base,
            'scope':'fixed development unit-cost pixel graph; not physiology, difficult-minimax or novel algorithm'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root');p.add_argument('--worker',choices=('HRF','FIVES','FOVEA'))
    a=p.parse_args()
    if a.worker:print(json.dumps(worker(a.root,a.worker)))
    else:
        rows=[]
        for dataset in ('HRF','FIVES','FOVEA'):
            try:
                result=subprocess.run([sys.executable,__file__,a.root,'--worker',dataset],capture_output=True,text=True,timeout=90)
                rows.append(json.loads(result.stdout) if result.returncode==0 else {'dataset':dataset,'status':'failed','returncode':result.returncode,'stderr':result.stderr})
            except subprocess.TimeoutExpired:rows.append({'dataset':dataset,'status':'timeout','timeout_seconds':90})
        print(json.dumps({'records':rows},indent=2))
