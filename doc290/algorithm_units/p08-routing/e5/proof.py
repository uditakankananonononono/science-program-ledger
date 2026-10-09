"""Independent Bellman-Ford relaxation audit, not imported method distances."""
from model import model,witness,Invalid

def distances(statement):
    G,ns=model(statement);out=[]
    for k in range(ns):
        d={v:None for v in G};d[statement['goal']]=0
        for _ in range(len(G)-1):
            previous=d;d=previous.copy()
            for a,edges in G.items():
                for e in edges:
                    suffix=previous[e['target']]
                    if suffix is not None:
                        value=e['scenario_times'][k]+suffix
                        if d[a] is None or value<d[a]:d[a]=value
        out.append(d[statement['start']])
    return out

def check(statement,payload):
    cert=payload.get('certificate');names={'early_exit','reason','start_distances','lower_bound','upper_bound'}
    if type(cert) is not dict or set(cert)!=names or type(cert['early_exit']) is not bool:raise Invalid('certificate fields')
    ds=distances(statement)
    if type(cert['start_distances']) is not list or len(cert['start_distances'])!=len(ds):raise Invalid('distance dimension')
    for v in cert['start_distances']:
        if v is not None and (type(v) is not int or v<0):raise Invalid('distance type')
    if cert['start_distances']!=ds:raise Invalid('independent original reverse distances')
    inc=payload['incumbent'];route=payload['route'];c=payload['counters']
    if inc is None:
        if any(v is not None for v in ds) or route is not None or cert['early_exit'] or cert['reason']!='forward exhaustion' or cert['lower_bound'] is not None or cert['upper_bound'] is not None:raise Invalid('unreachable certificate consistency')
        for k in ('candidate_edges','labels_inserted','pops','stale_pops','max_live_queue','lb_pruned','dominance_pruned'):
            if c[k]!=0:raise Invalid('unreachable phase counter')
        return
    W=witness(statement,inc)['worst_time']
    if any(v is None for v in ds):raise Invalid('reachable distance contradiction')
    L=max(ds)
    if type(cert['upper_bound']) is not int or cert['upper_bound']!=W or type(cert['lower_bound']) is not int or cert['lower_bound']!=L or L>W:raise Invalid('independent bound mismatch')
    early=L==W
    if cert['early_exit']!=early or cert['reason']!=('exact equality' if early else 'strict bound gap'):raise Invalid('bound classification/reason')
    if route is None:raise Invalid('reachable returned route absent')
    witness(statement,route)
    if early:
        if route!=inc:raise Invalid('early incumbent correspondence')
        for k in ('candidate_edges','labels_inserted','pops','stale_pops','max_live_queue','lb_pruned','dominance_pruned'):
            if c[k]!=0:raise Invalid('early exact-phase counter')
