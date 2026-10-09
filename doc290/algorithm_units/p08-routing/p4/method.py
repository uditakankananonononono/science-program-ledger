"""Standard exact reverse-scenario lower-bound pruning, separate method."""
import heapq
from model import model,witness,Invalid

import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('p3_method',Path(__file__).resolve().parent.parent/'p3'/'method.py');p3=importlib.util.module_from_spec(spec);spec.loader.exec_module(p3)
route,reverse,incumbent,prunable=(getattr(p3,k) for k in ('route','reverse','incumbent','prunable'))

def beam(s,G,ns):
    c={'beam_expansions':0,'beam_goal_candidates':0,'beam_kept':0,'beam_depths':0}
    if s['start']==s['goal']:return route(s,(s['start'],),(),(0,)*ns),c
    frontier=[((s['start'],),(),(0,)*ns)];best=None
    for depth in range(1,len(G)):
        c['beam_depths']+=1;groups={}
        for path,indices,totals in frontier:
            for i,e in enumerate(G[path[-1]]):
                c['beam_expansions']+=1;b=e['target']
                if b in path:continue
                pp=path+(b,);ii=indices+(i,);ss=tuple(x+y for x,y in zip(totals,e['scenario_times']))
                if b==s['goal']:
                    proposal=route(s,pp,ii,ss);witness(s,proposal);c['beam_goal_candidates']+=1
                    key=(proposal['worst_time'],ss,pp,ii)
                    if best is None or key<best[0]:best=(key,proposal)
                else:groups.setdefault(b,{})[(pp,ii)]=(pp,ii,ss)
        frontier=[]
        for v in sorted(groups):
            kept=sorted(groups[v].values(),key=lambda x:(max(x[2]),x[2],x[0],x[1]))[:2];frontier+=kept;c['beam_kept']+=len(kept)
    return None if best is None else best[1],c

def solve(s):
    G,ns=model(s);c={k:0 for k in ('reverse_relaxations','incumbent_relaxations','candidate_edges','lb_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue')}
    ds=reverse(G,s['goal'],ns,c);inc=incumbent(s,G,ns,c)
    if inc is None:return {'route':None,'counters':c,'incumbent':None,'beam_info':{'selected_source':'unreachable','old_worst':None,'beam_worst':None,'beam_expansions':0,'beam_goal_candidates':0,'beam_kept':0,'beam_depths':0}}
    oldW=witness(s,inc)['worst_time'];proposed,bc=beam(s,G,ns);beamW=None if proposed is None else witness(s,proposed)['worst_time'];selected='old'
    if beamW is not None and beamW<oldW:inc=proposed;selected='beam'
    info=dict(bc,selected_source=selected,old_worst=oldW,beam_worst=beamW)
    # Revalidate independently before granting pruning authority; no exception fallback.
    upper=witness(s,inc)['worst_time'];zero=(0,)*ns;labels={v:[] for v in G};labels[s['start']]=[zero];q=[(0,zero,(s['start'],),())];c['labels_inserted']=1;c['max_live_queue']=1
    while q:
        worst,totals,path,indices=heapq.heappop(q);a=path[-1];c['pops']+=1
        if totals not in labels[a]:c['stale_pops']+=1;continue
        if a==s['goal']:return {'route':route(s,path,indices,totals),'counters':c,'incumbent':inc,'beam_info':info}
        for i,e in enumerate(G[a]):
            c['candidate_edges']+=1;b=e['target'];new=tuple(x+y for x,y in zip(totals,e['scenario_times']))
            if prunable(new,b,ds,upper):c['lb_pruned']+=1;continue
            if any(all(x<=y for x,y in zip(old,new)) for old in labels[b]):c['dominance_pruned']+=1;continue
            labels[b]=[old for old in labels[b] if not all(x<=y for x,y in zip(new,old))];labels[b].append(new);heapq.heappush(q,(max(new),new,path+(b,),indices+(i,)));c['labels_inserted']+=1;c['max_live_queue']=max(c['max_live_queue'],len(q))
    return {'route':inc,'counters':c,'incumbent':inc,'beam_info':info}
