"""Standard reverse-exposure feasibility pruning, original budgeted heap/order."""
import heapq
from model import model,witness

def reverse(G,goal,c):
    incoming={v:[] for v in G}
    for a,es in G.items():
        for i,e in enumerate(es):incoming[e['target']].append((a,i,e['exposure']))
    d={v:None for v in G};d[goal]=0;q=[(0,goal)]
    while q:
        value,v=heapq.heappop(q)
        if value!=d[v]:continue
        for a,i,cost in incoming[v]:
            c['reverse_relaxations']+=1;new=value+cost
            if d[a] is None or new<d[a]:d[a]=new;heapq.heappush(q,(new,a))
    return d

def solve(s):
    G,n=model(s);start=s['start'];goal=s['goal'];budget=s['budget'];c={k:0 for k in ('reverse_relaxations','candidate_edges','feasibility_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue')};d=reverse(G,goal,c);proof={'reverse_exposure':d,'start_minimum':d[start]}
    zero=(0,)*n;labels={v:[] for v in G};labels[start].append((0,*zero));queue=[(0,0,zero,(start,),())];c['labels_inserted']=1;c['max_live_queue']=1
    while queue:
        worst,exposure,totals,path,indices=heapq.heappop(queue);node=path[-1];c['pops']+=1
        if (exposure,*totals) not in labels[node]:c['stale_pops']+=1;continue
        if node==goal:
            r={'path':list(path),'exposure':exposure,'scenario_totals':list(totals),'worst_time':worst,'edges':[{'source':a,'edge_index':i,'target':b} for a,b,i in zip(path,path[1:],indices)]};witness(s,r);return {'route':r,'counters':c,'proof':proof}
        for index,e in enumerate(G[node]):
            c['candidate_edges']+=1;risk=exposure+e['exposure']
            if risk>budget or d[e['target']] is None or risk+d[e['target']]>budget:c['feasibility_pruned']+=1;continue
            new=tuple(a+b for a,b in zip(totals,e['scenario_times']));vector=(risk,*new)
            if any(all(a<=b for a,b in zip(old,vector)) for old in labels[e['target']]):c['dominance_pruned']+=1;continue
            labels[e['target']]=[old for old in labels[e['target']] if not all(a<=b for a,b in zip(vector,old))];labels[e['target']].append(vector);heapq.heappush(queue,(max(new),risk,new,path+(e['target'],),indices+(index,)));c['labels_inserted']+=1;c['max_live_queue']=max(c['max_live_queue'],len(queue))
    return {'route':None,'counters':c,'proof':proof}
