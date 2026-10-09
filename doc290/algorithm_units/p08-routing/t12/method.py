import heapq
from model import model,witness
from proof import check as proof_check,scenario_check,incumbent_check,original_t7_proof,charged_check

import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('t6_method',Path(__file__).resolve().parent.parent/'t6'/'method.py');t6=importlib.util.module_from_spec(spec);spec.loader.exec_module(t6)
spec=importlib.util.spec_from_file_location('t6_original_proof',Path(__file__).resolve().parent.parent/'t6'/'proof.py');original_proof=importlib.util.module_from_spec(spec);spec.loader.exec_module(original_proof)
t6.proof_check=original_proof.check
reverse=t6.reverse

def solve(s):
    G,n,forbidden,penalties,states,arcs=model(s);start=s['start'];goal=s['goal'];budget=s['budget'];c={k:0 for k in ('reverse_relaxations','candidate_edges','forbidden_skipped','feasibility_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue','scenario_reverse_inspections','incumbent_inspections','objective_bound_pruned','charged_reverse_inspections','charged_bound_stronger','charged_strict_exclusions')};d=reverse(states,arcs,G,c);proof={'states':states,'distances':d,'start_minimum':d[0]};original_t7_proof.check(s,{'proof':proof},certificate=False)
    source=d[0];early=source is None or source>budget;certificate={'early_exit':early,'reason':'no_allowed_turn_path' if source is None else 'budget_infeasible' if early else 'feasible_search','budget':budget,'equality_exit':False,'lower':None,'upper':None,'old_lower':None,'charged_lambda':1,'source_bound_stronger':False}
    if early:return {'route':None,'counters':c,'proof':proof,'certificate':certificate,'scenario_proof':None,'incumbent':None,'charged_proof':None,'bound_trace':[],'activation':'exposure_exit'}
    ds=scenario_reverse(states,arcs,G,n,c);sp={'states':states,'distances':ds};scenario_check(s,sp)
    inc=incumbent(s,states,arcs,G,n,c);W=incumbent_check(s,inc)
    source_scenarios=[row[0] for row in ds]
    from model import Invalid
    if any(x is None for x in source_scenarios):raise Invalid('finite feasible exposure but scenario source None')
    oldL=max(source_scenarios)
    if oldL>W:raise Invalid('old lower above validated upper')
    if oldL==W:
        certificate.update(lower=oldL,upper=W,old_lower=oldL,equality_exit=True,reason='equality_exit')
        return {'route':inc,'counters':c,'proof':proof,'certificate':certificate,'scenario_proof':sp,'incumbent':inc,'charged_proof':None,'bound_trace':[],'activation':'old_bound_equality'}
    charged=charged_reverse(states,arcs,G,n,c);cp={'states':states,'distances':charged,'lambda':1};charged_check(s,cp)
    if any(row[0] is None for row in charged):raise Invalid('feasible charged source None')
    L=max(oldL,max(row[0] for row in charged)-budget);trace=[]
    if L>W:raise Invalid('lower above validated upper')
    certificate.update({'lower':L,'upper':W,'old_lower':oldL,'source_bound_stronger':L>oldL,'equality_exit':L==W,'reason':'equality_exit' if L==W else 'strict_gap_search'})
    if L==W:return {'route':inc,'counters':c,'proof':proof,'certificate':certificate,'scenario_proof':sp,'incumbent':inc,'charged_proof':cp,'bound_trace':trace,'activation':'charged_bound'}
    pos={(a,i):k+1 for k,(a,i) in enumerate((a,i) for a in sorted(G) for i in range(len(G[a])))}
    zero=(0,)*n;labels={(start,None):[(0,*zero)]};queue=[(0,0,0,zero,start,None,(start,),(),0)];serial=0;c['labels_inserted']=1;c['max_live_queue']=1
    while queue:
        worst,_,exposure,totals,node,incoming,path,indices,turn_cost=heapq.heappop(queue);c['pops']+=1
        if (exposure,*totals) not in labels[(node,incoming)]:c['stale_pops']+=1;continue
        if node==goal:
            r={'path':list(path),'edges':[{'source':a,'edge_index':i,'target':b} for a,b,i in zip(path,path[1:],indices)],'exposure':exposure,'scenario_totals':list(totals),'worst_time':worst,'turn_penalty':turn_cost};witness(s,r);return {'route':r,'counters':c,'proof':proof,'certificate':certificate,'scenario_proof':sp,'incumbent':inc,'charged_proof':cp,'bound_trace':trace,'activation':'charged_bound'}
        for index,e in enumerate(G[node]):
            c['candidate_edges']+=1;outgoing=(node,index);key=(incoming,outgoing)
            if incoming is not None and key in forbidden:c['forbidden_skipped']+=1;continue
            penalty=penalties.get(key,0) if incoming is not None else 0;risk=exposure+e['exposure'];suffix=d[pos[outgoing]]
            if risk>budget or suffix is None or risk+suffix>budget:c['feasibility_pruned']+=1;continue
            new=tuple(a+b+penalty for a,b in zip(totals,e['scenario_times']))
            suffixes=[row[pos[outgoing]] for row in ds]
            if any(x is None for x in suffixes):
                from model import Invalid
                raise Invalid('exposure-feasible but scenario suffix None')
            charged_suffixes=[row[pos[outgoing]] for row in charged]
            if any(x is None for x in charged_suffixes):raise Invalid('feasible charged suffix None')
            oldbound=max(a+b for a,b in zip(new,suffixes));bound=max(new[k]+max(suffixes[k],charged_suffixes[k]-(budget-risk)) for k in range(n))
            stronger=bound>oldbound;extra=bound>W and oldbound<=W
            c['charged_bound_stronger']+=int(stronger);c['charged_strict_exclusions']+=int(extra)
            trace.append({'path':list(path)+( [e['target']] ),'indices':list(indices)+[index],'state':pos[outgoing],'exposure':risk,'totals':list(new),'old_bound':oldbound,'new_bound':bound,'stronger':stronger,'extra_exclusion':extra,'pruned':bound>W})
            if bound>W:c['objective_bound_pruned']+=1;continue
            vector=(risk,*new);state=(e['target'],outgoing);old_labels=labels.setdefault(state,[])
            if any(all(a<=b for a,b in zip(old,vector)) for old in old_labels):c['dominance_pruned']+=1;continue
            labels[state]=[old for old in old_labels if not all(a<=b for a,b in zip(vector,old))];labels[state].append(vector);serial+=1;heapq.heappush(queue,(max(new),serial,risk,new,e['target'],outgoing,path+(e['target'],),indices+(index,),turn_cost+penalty));c['labels_inserted']+=1;c['max_live_queue']=max(c['max_live_queue'],len(queue))
    from model import Invalid
    raise Invalid('feasible source exposure but full search returned None')

def scenario_reverse(states,arcs,G,n,c):
    incoming=[[] for _ in states]
    for a in arcs:
        costs=[0]*n if a['edge'] is None else [v+a['delay'] for v in G[a['edge'][0]][a['edge'][1]]['scenario_times']]
        incoming[a['target']].append((a['source'],costs))
    result=[]
    for k in range(n):
        d=[None]*len(states);d[-1]=0;q=[(0,len(states)-1)]
        while q:
            value,v=heapq.heappop(q)
            if value!=d[v]:continue
            for a,costs in incoming[v]:
                c['scenario_reverse_inspections']+=1;new=value+costs[k]
                if d[a] is None or new<d[a]:d[a]=new;heapq.heappush(q,(new,a))
        result.append(d)
    return result

def incumbent(s,states,arcs,G,n,c):
    from model import Invalid
    outgoing=[[] for _ in states]
    for a in arcs:outgoing[a['source']].append(a)
    d=[None]*len(states);d[0]=0;prev={};q=[(0,0,0)];serial=0;sink=len(states)-1
    while q:
        cost,_,v=heapq.heappop(q)
        if cost!=d[v]:continue
        if v==sink:break
        for a in outgoing[v]:
            c['incumbent_inspections']+=1;x=0 if a['edge'] is None else G[a['edge'][0]][a['edge'][1]]['exposure'];new=cost+x;b=a['target']
            if d[b] is None or new<d[b]:d[b]=new;prev[b]=a;serial+=1;heapq.heappush(q,(new,serial,b))
    if d[sink] is None or d[sink]>s['budget']:raise Invalid('missing budget-feasible incumbent')
    selected=[];v=sink;seen=set()
    while v!=0:
        if v in seen or v not in prev:raise Invalid('incumbent predecessor cycle/absence')
        seen.add(v);a=prev[v]
        if a['edge'] is not None:selected.append(a['edge'])
        v=a['source']
    selected.reverse();path=[s['start']];edges=[];totals=[0]*n;exposure=turn=0;incoming=None
    penalties={(tuple(p['incoming']),tuple(p['outgoing'])):p['delay'] for p in s['penalties']}
    for a,i in selected:
        e=G[a][i];out=(a,i);delay=penalties.get((incoming,out),0) if incoming is not None else 0
        edges.append({'source':a,'edge_index':i,'target':e['target']});path.append(e['target']);exposure+=e['exposure'];turn+=delay;totals=[x+y+delay for x,y in zip(totals,e['scenario_times'])];incoming=out
    r={'path':path,'edges':edges,'exposure':exposure,'scenario_totals':totals,'worst_time':max(totals),'turn_penalty':turn};witness(s,r);return r

def charged_reverse(states,arcs,G,n,c):
    incoming=[[] for _ in states]
    for a in arcs:
        costs=[0]*n if a['edge'] is None else [v+a['delay']+G[a['edge'][0]][a['edge'][1]]['exposure'] for v in G[a['edge'][0]][a['edge'][1]]['scenario_times']]
        incoming[a['target']].append((a['source'],costs))
    result=[]
    for k in range(n):
        d=[None]*len(states);d[-1]=0;q=[(0,len(states)-1)]
        while q:
            value,v=heapq.heappop(q)
            if value!=d[v]:continue
            for a,costs in incoming[v]:
                c['charged_reverse_inspections']+=1;new=value+costs[k]
                if d[a] is None or new<d[a]:d[a]=new;heapq.heappush(q,(new,a))
        result.append(d)
    return result
