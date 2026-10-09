"""Exact ALL turn-state exposure distances, supplied-model certificate only."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('t2_helper',Path(__file__).resolve().parent.parent/'t2'/'certificate.py');t2=importlib.util.module_from_spec(spec);spec.loader.exec_module(t2)
Invalid,keys,integer,load_bytes=(getattr(t2,k) for k in ('Invalid','keys','integer','load_bytes'))
MAX=2**53-1

def model(s):
    keys(s,('graph','start','goal','budget','forbidden','penalties','distances'))
    G,f,p,states,arcs=t2.model({k:s[k] for k in ('graph','start','goal','forbidden','penalties')}|{'route':None,'potential':None});budget=integer(s['budget'])
    ns=next((len(e['scenario_times']) for es in G.values() for e in es),0)
    if not 1<=ns<=4:raise Invalid('positive edge-established scenario dimension')
    exposure=[]
    for arc in arcs:
        cost=0 if arc['edge'] is None else G[arc['edge'][0]][arc['edge'][1]]['exposure']
        exposure.append({'source':arc['source'],'target':arc['target'],'edge':arc['edge'],'exposure':cost,'delay_ignored':arc['delay']})
    return G,states,exposure,budget

def check(s):
    try:
        G,states,arcs,budget=model(s)
        if s['distances'] is None:return {'status':'UNAVAILABLE','reason':'missing certificate after model checks'}
        values=s['distances']
        if type(values) is not list or len(values)!=len(states):raise Invalid('full state distance dimension')
        for v in values:
            if v is not None and (type(v) is not int or not 0<=v<=MAX*129):raise Invalid('state distance cap/type')
        d=[None]*len(states);d[-1]=0
        for _ in range(len(states)-1):
            old=d;d=old[:]
            for arc in arcs:
                suffix=old[arc['target']]
                if suffix is not None:
                    value=arc['exposure']+suffix
                    if d[arc['source']] is None or value<d[arc['source']]:d[arc['source']]=value
        if values!=d:raise Invalid('independent all-state distance mismatch')
        status='CERTIFIED_NO_TURN_PATH' if d[0] is None else 'CERTIFIED_BUDGET_INFEASIBLE' if d[0]>budget else 'UNAVAILABLE'
        reason='no allowed turn path' if d[0] is None else 'all allowed paths over exposure budget' if d[0]>budget else 'minimum exposure feasible, no optimal scenario claim'
        return {'status':status,'reason':reason,'states':states,'exposure_arcs':arcs,'distances':d,'source_minimum':d[0],'budget':budget}
    except (KeyError,TypeError,IndexError,AttributeError) as e:return {'status':'INVALID','reason':'malformed container '+type(e).__name__}
    except Invalid as e:return {'status':'INVALID','reason':str(e)}
