import heapq
from model import model,witness
from proof import check as proof_check

import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('t6_method',Path(__file__).resolve().parent.parent/'t6'/'method.py');t6=importlib.util.module_from_spec(spec);spec.loader.exec_module(t6)
spec=importlib.util.spec_from_file_location('t6_original_proof',Path(__file__).resolve().parent.parent/'t6'/'proof.py');original_proof=importlib.util.module_from_spec(spec);spec.loader.exec_module(original_proof)
t6.proof_check=original_proof.check
reverse=t6.reverse

def solve(s):
    G,n,forbidden,penalties,states,arcs=model(s);start=s['start'];goal=s['goal'];budget=s['budget'];c={k:0 for k in ('reverse_relaxations','candidate_edges','forbidden_skipped','feasibility_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue')};d=reverse(states,arcs,G,c);proof={'states':states,'distances':d,'start_minimum':d[0]};proof_check(s,{'proof':proof},certificate=False)
    source=d[0];early=source is None or source>budget;certificate={'early_exit':early,'reason':'no_allowed_turn_path' if source is None else 'budget_infeasible' if early else 'feasible_search','budget':budget}
    if early:return {'route':None,'counters':c,'proof':proof,'certificate':certificate}
    pos={(a,i):k+1 for k,(a,i) in enumerate((a,i) for a in sorted(G) for i in range(len(G[a])))}
    zero=(0,)*n;labels={(start,None):[(0,*zero)]};queue=[(0,0,0,zero,start,None,(start,),(),0)];serial=0;c['labels_inserted']=1;c['max_live_queue']=1
    while queue:
        worst,_,exposure,totals,node,incoming,path,indices,turn_cost=heapq.heappop(queue);c['pops']+=1
        if (exposure,*totals) not in labels[(node,incoming)]:c['stale_pops']+=1;continue
        if node==goal:
            r={'path':list(path),'edges':[{'source':a,'edge_index':i,'target':b} for a,b,i in zip(path,path[1:],indices)],'exposure':exposure,'scenario_totals':list(totals),'worst_time':worst,'turn_penalty':turn_cost};witness(s,r);return {'route':r,'counters':c,'proof':proof,'certificate':certificate}
        for index,e in enumerate(G[node]):
            c['candidate_edges']+=1;outgoing=(node,index);key=(incoming,outgoing)
            if incoming is not None and key in forbidden:c['forbidden_skipped']+=1;continue
            penalty=penalties.get(key,0) if incoming is not None else 0;risk=exposure+e['exposure'];suffix=d[pos[outgoing]]
            if risk>budget or suffix is None or risk+suffix>budget:c['feasibility_pruned']+=1;continue
            new=tuple(a+b+penalty for a,b in zip(totals,e['scenario_times']));vector=(risk,*new);state=(e['target'],outgoing);old_labels=labels.setdefault(state,[])
            if any(all(a<=b for a,b in zip(old,vector)) for old in old_labels):c['dominance_pruned']+=1;continue
            labels[state]=[old for old in old_labels if not all(a<=b for a,b in zip(vector,old))];labels[state].append(vector);serial+=1;heapq.heappush(queue,(max(new),serial,risk,new,e['target'],outgoing,path+(e['target'],),indices+(index,),turn_cost+penalty));c['labels_inserted']+=1;c['max_live_queue']=max(c['max_live_queue'],len(queue))
    from model import Invalid
    raise Invalid('feasible source exposure but full search returned None')
