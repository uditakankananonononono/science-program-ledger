"""Standard exact reverse-scenario lower-bound pruning, separate method."""
import heapq
from model import model,witness,Invalid

import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('p3_method',Path(__file__).resolve().parent.parent/'p3'/'method.py');p3=importlib.util.module_from_spec(spec);spec.loader.exec_module(p3)
route,reverse,incumbent,prunable=(getattr(p3,k) for k in ('route','reverse','incumbent','prunable'))

def solve(s):
    G,ns=model(s);c={k:0 for k in ('reverse_relaxations','incumbent_relaxations','candidate_edges','lb_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue')}
    ds=reverse(G,s['goal'],ns,c);inc=incumbent(s,G,ns,c)
    distances=[d[s['start']] for d in ds]
    if inc is None:
        if any(v is not None for v in distances):raise Invalid('forward/reverse unreachable contradiction')
        return {'route':None,'counters':c,'incumbent':None,'certificate':{'early_exit':False,'reason':'forward exhaustion','start_distances':distances,'lower_bound':None,'upper_bound':None}}
    for v in distances:
        if type(v) is not int or v<0:raise Invalid('reachable reverse distance contradiction')
    # Revalidate independently before granting pruning authority; no exception fallback.
    upper=witness(s,inc)['worst_time'];lower=max(distances);certificate={'early_exit':lower==upper,'reason':'exact equality' if lower==upper else 'strict bound gap','start_distances':distances,'lower_bound':lower,'upper_bound':upper}
    if lower>upper:raise Invalid('lower bound above incumbent')
    if lower==upper:return {'route':inc,'counters':c,'incumbent':inc,'certificate':certificate}
    zero=(0,)*ns;labels={v:[] for v in G};labels[s['start']]=[zero];q=[(0,zero,(s['start'],),())];c['labels_inserted']=1;c['max_live_queue']=1
    while q:
        worst,totals,path,indices=heapq.heappop(q);a=path[-1];c['pops']+=1
        if totals not in labels[a]:c['stale_pops']+=1;continue
        if a==s['goal']:return {'route':route(s,path,indices,totals),'counters':c,'incumbent':inc,'certificate':certificate}
        for i,e in enumerate(G[a]):
            c['candidate_edges']+=1;b=e['target'];new=tuple(x+y for x,y in zip(totals,e['scenario_times']))
            if prunable(new,b,ds,upper):c['lb_pruned']+=1;continue
            if any(all(x<=y for x,y in zip(old,new)) for old in labels[b]):c['dominance_pruned']+=1;continue
            labels[b]=[old for old in labels[b] if not all(x<=y for x,y in zip(new,old))];labels[b].append(new);heapq.heappush(q,(max(new),new,path+(b,),indices+(i,)));c['labels_inserted']+=1;c['max_live_queue']=max(c['max_live_queue'],len(q))
    return {'route':inc,'counters':c,'incumbent':inc,'certificate':certificate}
