"""Original edge topology independently rebuilt, no method/checker arcs."""
from model import Invalid,model,MAX

def topology(s):
    G=s['graph'];ids=[(a,i) for a in sorted(G) for i in range(len(G[a]))];pos={e:i+1 for i,e in enumerate(ids)};states=[{'kind':'source','vertex':s['start'],'incoming':None}]+[{'kind':'edge','vertex':G[a][i]['target'],'incoming':[a,i]} for a,i in ids]+[{'kind':'goal','vertex':s['goal'],'incoming':None}];sink=len(states)-1;arcs=[]
    forbidden={(tuple(r[0]),tuple(r[1])) for r in s['forbidden']}
    for i,e in enumerate(G[s['start']]):arcs.append((0,pos[(s['start'],i)],e['exposure']))
    if s['start']==s['goal']:arcs.append((0,sink,0))
    for incoming in ids:
        a,i=incoming;v=G[a][i]['target'];origin=pos[incoming]
        for j,e in enumerate(G[v]):
            out=(v,j)
            if (incoming,out) not in forbidden:arcs.append((origin,pos[out],e['exposure']))
        if v==s['goal']:arcs.append((origin,sink,0))
    return states,arcs

def distances(s):
    states,arcs=topology(s);d=[None]*len(states);d[-1]=0
    for _ in range(len(states)-1):
        old=d;d=old[:]
        for a,b,c in arcs:
            if old[b] is not None:
                value=c+old[b]
                if d[a] is None or value<d[a]:d[a]=value
    return states,d

def check(s,payload,certificate=True):
    model(s);p=payload.get('proof')
    if type(p) is not dict or set(p)!= {'states','distances','start_minimum'}:raise Invalid('full-state proof fields')
    states,d=distances(s)
    supplied=p['states']
    if type(supplied) is not list or len(supplied)!=len(states):raise Invalid('state list dimension')
    for state in supplied:
        if type(state) is not dict or set(state)!={'kind','vertex','incoming'} or type(state['kind']) is not str or state['kind'] not in ('source','edge','goal') or type(state['vertex']) is not str:raise Invalid('state fields/kind/vertex')
        incoming=state['incoming']
        if state['kind']=='edge':
            if type(incoming) is not list or len(incoming)!=2 or type(incoming[0]) is not str or type(incoming[1]) is not int or incoming[1]<0:raise Invalid('strict incoming original index')
        elif incoming is not None:raise Invalid('source/sink incoming None')
    if supplied!=states:raise Invalid('original canonical state ledger')
    v=p['distances']
    if type(v) is not list or len(v)!=len(d):raise Invalid('distance dimension')
    for c in v:
        if c is not None and (type(c) is not int or not 0<=c<=MAX*129):raise Invalid('distance type/cap')
    start=p['start_minimum']
    if start is not None and (type(start) is not int or start<0):raise Invalid('start type')
    if v!=d or v[-1]!=0 or start!=d[0]:raise Invalid('independent full-state exposure mismatch')

    if not certificate:return
    c=payload.get('certificate');names={'early_exit','reason','budget'}
    if type(c) is not dict or set(c)!=names or type(c['early_exit']) is not bool or type(c['budget']) is not int or c['budget']!=s['budget']:raise Invalid('certificate budget/schema')
    minimum=d[0];early=minimum is None or minimum>s['budget'];reason='no_allowed_turn_path' if minimum is None else 'budget_infeasible' if early else 'feasible_search'
    if c['early_exit']!=early or c['reason']!=reason:raise Invalid('reason/source/budget binding')
    if early:
        if payload['route'] is not None:raise Invalid('early route correspondence')
        for k in ('candidate_edges','forbidden_skipped','feasibility_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue'):
            if payload['counters'][k]!=0:raise Invalid('early exact-phase counter')
    elif payload['route'] is None:raise Invalid('feasible source but returned None')
