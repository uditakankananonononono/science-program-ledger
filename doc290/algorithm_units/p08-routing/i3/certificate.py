"""Integrated turn/joint model potential certificate, sufficient not complete."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('b3_helper',Path(__file__).resolve().parent.parent/'b3'/'certificate.py');b3=importlib.util.module_from_spec(spec);spec.loader.exec_module(b3)
Invalid,keys,integer,rational,capped,scalar_text,load_bytes=(getattr(b3,k) for k in ('Invalid','keys','integer','rational','capped','scalar_text','load_bytes'))

def check(s):
    try:
        keys(s,('graph','start','goal','budget','forbidden','penalties','route','weights','multiplier','potential'))
        m={k:s[k] for k in ('graph','start','goal','forbidden','penalties','route','potential')}
        G,f,p,states,arcs=b3.t2.model(m);budget=integer(s['budget'])
        ns=next((len(e['scenario_times']) for es in G.values() for e in es),0)
        if ns==0:raise Invalid('positive scenario dimension unestablished')
        if s['route'] is None or s['weights'] is None or s['multiplier'] is None or s['potential'] is None:return {'status':'UNAVAILABLE','reason':'missing route/proof after model checks'}
        primal=b3.t2.helper.checked({k:s[k] for k in ('graph','start','goal','budget','forbidden','penalties','route')})
        weights=s['weights']
        if type(weights) is not list or len(weights)!=ns:raise Invalid('simplex dimension')
        weights=[capped(rational(v)) for v in weights]
        if any(v<0 for v in weights) or sum(weights)!=1:raise Invalid('nonnegative simplex sum')
        lam=capped(rational(s['multiplier']))
        if lam<0:raise Invalid('negative multiplier')
        h=s['potential']
        if type(h) is not list or len(h)!=len(states):raise Invalid('potential state dimension')
        h=[capped(rational(v)) for v in h]
        if h[0]!=0:raise Invalid('source potential')
        ledger=[]
        for arc in arcs:
            if arc['edge'] is None:cost=0
            else:
                a,i=arc['edge'];edge=G[a][i];ss=[integer(v+arc['delay']) for v in edge['scenario_times']]
                cost=capped(sum(v*c for v,c in zip(weights,ss))+lam*edge['exposure'])
            slack=cost+h[arc['source']]-h[arc['target']]
            if slack<0:raise Invalid('weighted potential infeasible transition')
            ledger.append({'source':arc['source'],'target':arc['target'],'edge':arc['edge'],'delay':arc['delay'],'weighted_cost':scalar_text(cost),'slack':scalar_text(slack)})
        scenario_weighted=capped(sum(v*c for v,c in zip(weights,primal['scenario_totals'])));weighted=capped(scenario_weighted+lam*primal['exposure']);charge=capped(lam*budget);LB=capped(h[-1]-charge);worst=primal['worst_time']
        if LB>worst:raise Invalid('bound above feasible worst')
        return {'status':'CERTIFIED_INTEGRATED' if LB==worst else 'UNAVAILABLE','reason':'matching feasible worst/integrated bound' if LB==worst else 'feasible incomplete integrated bound','states':states,'transition_ledger':ledger,'primal':primal,'weighted_scenario_sum':scalar_text(scenario_weighted),'weighted_route_cost':scalar_text(weighted),'budget_charge':scalar_text(charge),'lower_bound':scalar_text(LB),'gap':scalar_text(worst-LB)}
    except (KeyError,TypeError,IndexError,AttributeError) as e:return {'status':'INVALID','reason':'malformed container '+type(e).__name__}
    except Invalid as e:return {'status':'INVALID','reason':str(e)}
