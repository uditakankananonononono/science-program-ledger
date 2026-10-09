"""Original-edge integer turn-aware route witness check, not optimality."""
import sys
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location('c1_validation',Path(__file__).resolve().parent.parent/'c1'/'validate.py')
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
integer,vertex,graph,keys,Invalid,load_bytes=(getattr(helper,k) for k in ('integer','vertex','graph','keys','Invalid','load_bytes'))

def edgeid(v,G):
    if type(v) is not list or len(v)!=2:raise Invalid('edge ID shape')
    source=vertex(v[0]);index=integer(v[1])
    if source not in G or index>=len(G[source]):raise Invalid('edge ID absent')
    return (source,index)

def rules(s,G):
    if type(s['forbidden']) is not list or type(s['penalties']) is not list or len(s['forbidden'])>128 or len(s['penalties'])>128:raise Invalid('rule shape/cap')
    forbidden=set();penalties={}
    def pair(a,b):
        incoming=edgeid(a,G);outgoing=edgeid(b,G)
        if G[incoming[0]][incoming[1]]['target']!=outgoing[0]:raise Invalid('nonconsecutive rule')
        return incoming,outgoing
    for r in s['forbidden']:
        if type(r) is not list or len(r)!=2:raise Invalid('forbidden shape')
        p=pair(*r)
        if p in forbidden:raise Invalid('duplicate forbidden')
        forbidden.add(p)
    for r in s['penalties']:
        keys(r,('incoming','outgoing','delay'));p=pair(r['incoming'],r['outgoing'])
        if p in penalties:raise Invalid('duplicate penalty')
        penalties[p]=integer(r['delay'])
    return forbidden,penalties

def checked(s):
    keys(s,('graph','start','goal','budget','forbidden','penalties','route'))
    G=s['graph'];ns=graph(G,False)
    if ns is None:raise Invalid('scenario dimension unestablished without edges')
    start=vertex(s['start']);goal=vertex(s['goal']);budget=integer(s['budget'])
    if start not in G or goal not in G:raise Invalid('query absent')
    forbidden,penalties=rules(s,G)
    r=s['route']
    if r is None:return {'status':'UNAVAILABLE','reason':'missing route after all input/rule checks'}
    keys(r,('path','edges','exposure','scenario_totals','worst_time','turn_penalty'))
    p=r['path'];edges=r['edges']
    if type(p) is not list or type(edges) is not list or not 1<=len(p)<=256 or len(edges)!=len(p)-1 or any(type(v) is not str or v not in G for v in p) or p[0]!=start or p[-1]!=goal:raise Invalid('route path/query shape')
    if type(r['scenario_totals']) is not list or len(r['scenario_totals'])!=ns:raise Invalid('reported scenario dimension')
    reported=[integer(v) for v in r['scenario_totals']];exposure=turn=0;totals=[0]*ns;ledger=[];previous=None
    for source,target,e in zip(p,p[1:],edges):
        keys(e,('source','edge_index','target'))
        identity=edgeid([e['source'],e['edge_index']],G);edge=G[identity[0]][identity[1]]
        if identity[0]!=source or e['target']!=target or edge['target']!=target:raise Invalid('route edge correspondence')
        delay=0
        if previous is not None:
            pair=(previous,identity)
            if pair in forbidden:raise Invalid('forbidden selected turn')
            delay=penalties.get(pair,0)
        exposure=integer(exposure+edge['exposure']);turn=integer(turn+delay)
        totals=[integer(v+c+delay) for v,c in zip(totals,edge['scenario_times'])]
        ledger.append({'edge':list(identity),'target':target,'previous':None if previous is None else list(previous),'delay':delay,'cumulative_exposure':exposure,'cumulative_scenarios':totals[:]});previous=identity
    if exposure!=integer(r['exposure']) or turn!=integer(r['turn_penalty']) or totals!=reported or max(totals)!=integer(r['worst_time']):raise Invalid('route totals correspondence')
    if exposure>budget:raise Invalid('route exposure budget')
    return {'status':'FEASIBLE_WITNESS','reason':'checked original-edge turn route','ledger':ledger,'exposure':exposure,'scenario_totals':totals,'worst_time':max(totals),'turn_penalty':turn}

def validate(s):
    try:return checked(s)
    except (KeyError,TypeError,IndexError,AttributeError) as e:return {'status':'INVALID','reason':'malformed container: '+type(e).__name__}
    except Invalid as e:return {'status':'INVALID','reason':str(e)}
