"""Shortest turn-state potential proof; established certificate, not search."""
import importlib.util,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('t1_validation',Path(__file__).resolve().parent.parent/'t1'/'validate.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
Invalid,integer,vertex,keys,load_bytes,rules=(getattr(helper,k) for k in ('Invalid','integer','vertex','keys','load_bytes','rules'))
MAX=2**53-1

def signed(v):
    if type(v) is not int or abs(v)>MAX:raise Invalid('signed integer potential cap')
    return v

def model(s):
    keys(s,('graph','start','goal','forbidden','penalties','route','potential'))
    G=s['graph']
    if type(G) is not dict or not 1<=len(G)<=32:raise Invalid('graph cap')
    for v in G:vertex(v)
    dimensions=set();edgecount=0
    for v,es in G.items():
        if type(es) is not list:raise Invalid('adjacency shape')
        for e in es:
            keys(e,('target','time','exposure','scenario_times'));t=vertex(e['target'])
            if t not in G:raise Invalid('edge target absent')
            integer(e['time']);integer(e['exposure']);ss=e['scenario_times']
            if type(ss) is not list or len(ss)>4:raise Invalid('optional scenario shape')
            dimensions.add(len(ss))
            for value in ss:integer(value)
            edgecount+=1
    if edgecount>128 or len(dimensions)>1:raise Invalid('edge/scenario cap')
    start=vertex(s['start']);goal=vertex(s['goal'])
    if start not in G or goal not in G:raise Invalid('query absent')
    forbidden,penalties=rules(s,G)
    ids=[(a,i) for a in sorted(G) for i in range(len(G[a]))]
    states=[{'kind':'source','vertex':start,'incoming':None}]+[{'kind':'edge','vertex':G[a][i]['target'],'incoming':[a,i]} for a,i in ids]+[{'kind':'goal','vertex':goal,'incoming':None}]
    pos={e:k+1 for k,e in enumerate(ids)};end=len(states)-1;arcs=[]
    for i,e in enumerate(G[start]):arcs.append({'source':0,'target':pos[(start,i)],'cost':e['time'],'edge':[start,i],'delay':0})
    if start==goal:arcs.append({'source':0,'target':end,'cost':0,'edge':None,'delay':0})
    for incoming in ids:
        a,i=incoming;node=G[a][i]['target'];origin=pos[incoming]
        for j,e in enumerate(G[node]):
            out=(node,j);pair=(incoming,out)
            if pair in forbidden:continue
            delay=penalties.get(pair,0);cost=integer(e['time']+delay)
            arcs.append({'source':origin,'target':pos[out],'cost':cost,'edge':[node,j],'delay':delay})
        if node==goal:arcs.append({'source':origin,'target':end,'cost':0,'edge':None,'delay':0})
    return G,forbidden,penalties,states,arcs

def route_check(s,G,forbidden,penalties):
    r=s['route'];keys(r,('path','edges','time','turn_penalty'));p=r['path'];es=r['edges']
    if type(p) is not list or type(es) is not list or not 1<=len(p)<=256 or len(es)!=len(p)-1 or any(type(v) is not str or v not in G for v in p) or p[0]!=s['start'] or p[-1]!=s['goal']:raise Invalid('route query/path')
    total=turn=0;previous=None;ledger=[]
    for a,b,e in zip(p,p[1:],es):
        keys(e,('source','edge_index','target'));index=integer(e['edge_index'])
        if e['source']!=a or e['target']!=b or index>=len(G[a]) or G[a][index]['target']!=b:raise Invalid('route edge identity')
        out=(a,index);delay=0
        if previous is not None:
            pair=(previous,out)
            if pair in forbidden:raise Invalid('route forbidden turn')
            delay=penalties.get(pair,0)
        total=integer(total+G[a][index]['time']+delay);turn=integer(turn+delay)
        ledger.append({'edge':[a,index],'delay':delay,'total':total});previous=out
    if total!=integer(r['time']) or turn!=integer(r['turn_penalty']):raise Invalid('route reported total')
    return total,ledger

def check(s):
    try:
        G,f,p,states,arcs=model(s)
        if s['route'] is None or s['potential'] is None:return {'status':'UNAVAILABLE','reason':'missing route/potential after model checks'}
        total,ledger=route_check(s,G,f,p)
        h=s['potential']
        if type(h) is not list or len(h)!=len(states):raise Invalid('canonical potential dimension')
        h=[signed(v) for v in h]
        if h[0]!=0:raise Invalid('source potential nonzero')
        slacks=[arc['cost']+h[arc['source']]-h[arc['target']] for arc in arcs]
        if any(v<0 for v in slacks):raise Invalid('potential infeasible transition')
        if h[-1]>total:raise Invalid('lower bound above route')
        return {'status':'CERTIFIED_OPTIMAL' if h[-1]==total else 'UNAVAILABLE','reason':'matching exact feasible route/lower bound' if h[-1]==total else 'feasible lower bound slack','states':states,'transitions':arcs,'slacks':slacks,'route_ledger':ledger,'route_time':total,'lower_bound':h[-1]}
    except (KeyError,TypeError,IndexError,AttributeError) as e:return {'status':'INVALID','reason':'malformed container '+type(e).__name__}
    except Invalid as e:return {'status':'INVALID','reason':str(e)}
