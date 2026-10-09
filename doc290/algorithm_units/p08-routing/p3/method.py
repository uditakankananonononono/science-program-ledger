"""Standard exact reverse-scenario lower-bound pruning, separate method."""
import heapq
from model import model,witness,Invalid

def route(s,path,indices,totals):
    r={'path':list(path),'edges':[{'source':a,'edge_index':i,'target':b} for a,b,i in zip(path,path[1:],indices)],'scenario_totals':list(totals),'worst_time':max(totals)};witness(s,r);return r

def reverse(G,goal,ns,counters):
    incoming={v:[] for v in G}
    for a,es in G.items():
        for i,e in enumerate(es):incoming[e['target']].append((a,i,e))
    ds=[]
    for k in range(ns):
        d={v:None for v in G};d[goal]=0;q=[(0,goal)]
        while q:
            cost,v=heapq.heappop(q)
            if cost!=d[v]:continue
            for a,i,e in incoming[v]:
                counters['reverse_relaxations']+=1;new=cost+e['scenario_times'][k]
                if d[a] is None or new<d[a]:d[a]=new;heapq.heappush(q,(new,a))
        ds.append(d)
    return ds

def incumbent(s,G,ns,counters):
    start=s['start'];goal=s['goal'];d={start:0};pred={};q=[(0,start)]
    while q:
        cost,a=heapq.heappop(q)
        if cost!=d[a]:continue
        if a==goal:
            path=[goal];indices=[];seen={goal}
            while path[-1]!=start:
                source,i=pred[path[-1]]
                if source in seen:raise Invalid('incumbent predecessor cycle')
                seen.add(source);indices.append(i);path.append(source)
            path.reverse();indices.reverse();totals=[0]*ns
            for source,i in zip(path,indices):totals=[x+y for x,y in zip(totals,G[source][i]['scenario_times'])]
            return route(s,path,indices,totals)
        for i,e in enumerate(G[a]):
            counters['incumbent_relaxations']+=1;new=cost+e['scenario_times'][0];b=e['target']
            if b not in d or new<d[b]:d[b]=new;pred[b]=(a,i);heapq.heappush(q,(new,b))
    return None

def prunable(totals,vertex,distances,upper):
    return any(d[vertex] is None for d in distances) or max(t+d[vertex] for t,d in zip(totals,distances))>upper

def solve(s):
    G,ns=model(s);c={k:0 for k in ('reverse_relaxations','incumbent_relaxations','candidate_edges','lb_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue')}
    ds=reverse(G,s['goal'],ns,c);inc=incumbent(s,G,ns,c)
    if inc is None:return {'route':None,'counters':c,'incumbent':None}
    # Revalidate independently before granting pruning authority; no exception fallback.
    upper=witness(s,inc)['worst_time'];zero=(0,)*ns;labels={v:[] for v in G};labels[s['start']]=[zero];q=[(0,zero,(s['start'],),())];c['labels_inserted']=1;c['max_live_queue']=1
    while q:
        worst,totals,path,indices=heapq.heappop(q);a=path[-1];c['pops']+=1
        if totals not in labels[a]:c['stale_pops']+=1;continue
        if a==s['goal']:return {'route':route(s,path,indices,totals),'counters':c,'incumbent':inc}
        for i,e in enumerate(G[a]):
            c['candidate_edges']+=1;b=e['target'];new=tuple(x+y for x,y in zip(totals,e['scenario_times']))
            if prunable(new,b,ds,upper):c['lb_pruned']+=1;continue
            if any(all(x<=y for x,y in zip(old,new)) for old in labels[b]):c['dominance_pruned']+=1;continue
            labels[b]=[old for old in labels[b] if not all(x<=y for x,y in zip(new,old))];labels[b].append(new);heapq.heappush(q,(max(new),new,path+(b,),indices+(i,)));c['labels_inserted']+=1;c['max_live_queue']=max(c['max_live_queue'],len(q))
    return {'route':inc,'counters':c,'incumbent':inc}
