from model import model,Invalid

def distances(s):
    G,ns=model(s);d={v:None for v in G};d[s['goal']]=0
    for _ in range(len(G)-1):
        old=d;d=old.copy()
        for a,es in G.items():
            for e in es:
                if old[e['target']] is not None:
                    value=e['exposure']+old[e['target']]
                    if d[a] is None or value<d[a]:d[a]=value
    return d

def ledger_check(s,p):
    G,ns=model(s)
    if type(p) is not dict or set(p)!={'reverse_exposure','start_minimum'}:raise Invalid('proof fields')
    d=p['reverse_exposure']
    if type(d) is not dict or set(d)!=set(G):raise Invalid('full vertex ledger')
    for v in d.values():
        if v is not None and (type(v) is not int or v<0):raise Invalid('ledger integer-or-None')
    start=p['start_minimum']
    if start is not None and (type(start) is not int or start<0):raise Invalid('start minimum type')
    if d!=distances(s) or d[s['goal']]!=0 or start!=d[s['start']]:raise Invalid('independent reverse exposure mismatch')


def check(s,payload,certificate=True):
    p=payload.get('proof');ledger_check(s,p)
    if not certificate:return
    c=payload.get('certificate');names={'early_exit','reason','budget'}
    if type(c) is not dict or set(c)!=names or type(c['early_exit']) is not bool or type(c['budget']) is not int or c['budget']!=s['budget']:raise Invalid('certificate fields/budget')
    start=p['start_minimum'];early=start is None or start>s['budget'];reason='graph_unreachable' if start is None else 'budget_infeasible' if early else 'feasible_search'
    if c['early_exit']!=early or c['reason']!=reason:raise Invalid('reason/start/budget binding')
    if early:
        if payload['route'] is not None:raise Invalid('early route correspondence')
        for k in ('candidate_edges','feasibility_pruned','dominance_pruned','labels_inserted','pops','stale_pops','max_live_queue'):
            if payload['counters'][k]!=0:raise Invalid('early exact-phase counters')
    elif payload['route'] is None:raise Invalid('feasible reverse bound but returned None')
