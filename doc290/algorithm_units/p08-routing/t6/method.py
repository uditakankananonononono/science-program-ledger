import heapq
from model import model,witness
from proof import check as proof_check

def reverse(states,arcs,G,c):
    incoming=[[] for _ in states]
    for arc in arcs:
        cost=0 if arc['edge'] is None else G[arc['edge'][0]][arc['edge'][1]]['exposure'];incoming[arc['target']].append((arc['source'],cost))
    d=[None]*len(states);d[-1]=0;q=[(0,len(states)-1)]
    while q:
        cost,v=heapq.heappop(q)
        if cost!=d[v]:continue
        for a,x in incoming[v]:
            c['reverse_relaxations']+=1;new=cost+x
            if d[a] is None or new<d[a]:d[a]=new;heapq.heappush(q,(new,a))
    return d

def solve(s):
    G,n,forbidden,penalties,states,arcs=model(s);start=s['start'];goal=s['goal'];budget=s['budget'];c={k:0 for k in ('reverse_relaxations','candidate_edges','forbidden_skipped','feasibility_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue')};d=reverse(states,arcs,G,c);proof={'states':states,'distances':d,'start_minimum':d[0]};proof_check(s,{'proof':proof});pos={(a,i):k+1 for k,(a,i) in enumerate((a,i) for a in sorted(G) for i in range(len(G[a])))}
    zero=(0,)*n;labels={(start,None):[(0,*zero)]};queue=[(0,0,0,zero,start,None,(start,),(),0)];serial=0;c['labels_inserted']=1;c['max_live_queue']=1
    while queue:
        worst,_,exposure,totals,node,incoming,path,indices,turn_cost=heapq.heappop(queue);c['pops']+=1
        if (exposure,*totals) not in labels[(node,incoming)]:c['stale_pops']+=1;continue
        if node==goal:
            r={'path':list(path),'edges':[{'source':a,'edge_index':i,'target':b} for a,b,i in zip(path,path[1:],indices)],'exposure':exposure,'scenario_totals':list(totals),'worst_time':worst,'turn_penalty':turn_cost};witness(s,r);return {'route':r,'counters':c,'proof':proof}
        for index,e in enumerate(G[node]):
            c['candidate_edges']+=1;outgoing=(node,index);key=(incoming,outgoing)
            if incoming is not None and key in forbidden:c['forbidden_skipped']+=1;continue
            penalty=penalties.get(key,0) if incoming is not None else 0;risk=exposure+e['exposure'];suffix=d[pos[outgoing]]
            if risk>budget or suffix is None or risk+suffix>budget:c['feasibility_pruned']+=1;continue
            new=tuple(a+b+penalty for a,b in zip(totals,e['scenario_times']));vector=(risk,*new);state=(e['target'],outgoing);old_labels=labels.setdefault(state,[])
            if any(all(a<=b for a,b in zip(old,vector)) for old in old_labels):c['dominance_pruned']+=1;continue
            labels[state]=[old for old in old_labels if not all(a<=b for a,b in zip(vector,old))];labels[state].append(vector);serial+=1;heapq.heappush(queue,(max(new),serial,risk,new,e['target'],outgoing,path+(e['target'],),indices+(index,),turn_cost+penalty));c['labels_inserted']+=1;c['max_live_queue']=max(c['max_live_queue'],len(queue))
    return {'route':None,'counters':c,'proof':proof}
