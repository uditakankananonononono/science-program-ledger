"""Independent original turn topology, per-scenario Bellman-Ford audit."""
import importlib.util
from pathlib import Path
from model import Invalid,model,witness,MAX
spec=importlib.util.spec_from_file_location('t8_original_t7_proof',Path(__file__).resolve().parent.parent/'t7'/'proof.py');original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)

def distances(s):
    G,n,_,_,_,_=model(s)
    states,exposure_arcs=original.topology(s)
    ids=[(a,i) for a in sorted(G) for i in range(len(G[a]))];pos={e:k+1 for k,e in enumerate(ids)};sink=len(states)-1
    forbidden={(tuple(r[0]),tuple(r[1])) for r in s['forbidden']};penalties={(tuple(p['incoming']),tuple(p['outgoing'])):p['delay'] for p in s['penalties']};arcs=[]
    for j,e in enumerate(G[s['start']]):arcs.append((0,pos[(s['start'],j)],e['scenario_times'][:]))
    if s['start']==s['goal']:arcs.append((0,sink,[0]*n))
    for a,i in ids:
        v=G[a][i]['target'];inc=(a,i)
        for j,e in enumerate(G[v]):
            out=(v,j)
            if (inc,out) in forbidden:continue
            delay=penalties.get((inc,out),0);arcs.append((pos[inc],pos[out],[x+delay for x in e['scenario_times']]))
        if v==s['goal']:arcs.append((pos[inc],sink,[0]*n))
    ledgers=[]
    for k in range(n):
        d=[None]*len(states);d[-1]=0
        for _ in range(len(states)-1):
            old=d;d=old[:]
            for a,b,cost in arcs:
                if old[b] is not None:
                    value=cost[k]+old[b]
                    if d[a] is None or value<d[a]:d[a]=value
        ledgers.append(d)
    return states,ledgers

def scenario_check(s,p):
    states,d=distances(s)
    if type(p) is not dict or set(p)!={'states','distances'}:raise Invalid('scenario proof schema')
    supplied=p['states']
    if type(supplied) is not list or len(supplied)!=len(states):raise Invalid('scenario state dimension')
    for st in supplied:
        if type(st) is not dict or set(st)!={'kind','vertex','incoming'} or type(st['kind']) is not str or st['kind'] not in ('source','edge','goal') or type(st['vertex']) is not str:raise Invalid('scenario state schema')
        inc=st['incoming']
        if st['kind']=='edge':
            if type(inc) is not list or len(inc)!=2 or type(inc[0]) is not str or type(inc[1]) is not int or inc[1]<0:raise Invalid('scenario typed original incoming')
        elif inc is not None:raise Invalid('scenario source/sink incoming')
    if supplied!=states:raise Invalid('scenario canonical states')
    dd=p['distances']
    if type(dd) is not list or len(dd)!=len(d):raise Invalid('scenario count')
    for row in dd:
        if type(row) is not list or len(row)!=len(states):raise Invalid('scenario distance dimension')
        for value in row:
            if value is not None and (type(value) is not int or not 0<=value<=MAX*258):raise Invalid('scenario distance type/cap')
    if dd!=d:raise Invalid('independent scenario distances')

def incumbent_check(s,r):
    if r is None:raise Invalid('absent feasible incumbent')
    return witness(s,r)['worst_time']

def check(s,payload,certificate=True):
    original.check(s,payload,certificate=certificate)
    if not certificate:return
    early=payload['certificate']['early_exit']
    if early:
        if payload.get('scenario_proof') is not None or payload.get('incumbent') is not None:raise Invalid('early preprocessing metadata')
        for k in ('scenario_reverse_inspections','incumbent_inspections','objective_bound_pruned'):
            if payload['counters'][k]!=0:raise Invalid('early extra counters')
    else:
        scenario_check(s,payload.get('scenario_proof'));incumbent_check(s,payload.get('incumbent'))
