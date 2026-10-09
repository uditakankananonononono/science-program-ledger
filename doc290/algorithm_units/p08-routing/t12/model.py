import importlib.util,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('t2_helper',Path(__file__).resolve().parent.parent/'t2'/'certificate.py');t2=importlib.util.module_from_spec(spec);spec.loader.exec_module(t2)
Invalid,integer,keys,load_bytes=(getattr(t2,k) for k in ('Invalid','integer','keys','load_bytes'))
MAX=2**53-1;COST_MAX=MAX//256

def model(s):
    keys(s,('graph','start','goal','budget','forbidden','penalties'))
    G,f,p,states,arcs=t2.model({k:s[k] for k in ('graph','start','goal','forbidden','penalties')}|{'route':None,'potential':None});integer(s['budget'])
    ns=next((len(e['scenario_times']) for es in G.values() for e in es),0)
    if not 1<=ns<=4:raise Invalid('positive edge-established scenario dimension')
    for es in G.values():
        for e in es:
            for c in (e['time'],e['exposure'],*e['scenario_times']):
                if c>COST_MAX:raise Invalid('edge component cap')
    if any(v>COST_MAX for v in p.values()):raise Invalid('penalty cap')
    return G,ns,f,p,states,arcs

def witness(s,r):
    G,ns,f,p,states,arcs=model(s);keys(r,('path','edges','exposure','scenario_totals','worst_time','turn_penalty'))
    path=r['path'];edges=r['edges']
    if type(path) is not list or not 1<=len(path)<=130 or any(type(v) is not str or v not in G for v in path) or path[0]!=s['start'] or path[-1]!=s['goal'] or type(edges) is not list or len(edges)!=len(path)-1:raise Invalid('walk/query/cap')
    totals=[0]*ns;exposure=turn=0;incoming=None;seen={(s['start'],None)};ledger=[]
    for a,b,e in zip(path,path[1:],edges):
        keys(e,('source','edge_index','target'));index=integer(e['edge_index'])
        if type(e['source']) is not str or type(e['target']) is not str or e['source']!=a or e['target']!=b or index>=len(G[a]) or G[a][index]['target']!=b:raise Invalid('original indexed edge/query')
        out=(a,index);state=(b,out)
        if state in seen:raise Invalid('repeated incoming-edge state')
        if incoming is not None and (incoming,out) in f:raise Invalid('forbidden selected turn')
        delay=p.get((incoming,out),0) if incoming is not None else 0;seen.add(state)
        exposure=integer(exposure+G[a][index]['exposure']);turn=integer(turn+delay);totals=[integer(totals[k]+G[a][index]['scenario_times'][k]+delay) for k in range(ns)];ledger.append({'edge':[a,index],'delay':delay,'exposure':exposure,'scenarios':totals[:]});incoming=out
    if type(r['scenario_totals']) is not list or len(r['scenario_totals'])!=ns or [integer(v) for v in r['scenario_totals']]!=totals or integer(r['worst_time'])!=max(totals) or integer(r['exposure'])!=exposure or integer(r['turn_penalty'])!=turn or exposure>s['budget']:raise Invalid('original walk totals/budget')
    return {'ledger':ledger,'scenario_totals':totals,'worst_time':max(totals),'exposure':exposure,'turn_penalty':turn}
