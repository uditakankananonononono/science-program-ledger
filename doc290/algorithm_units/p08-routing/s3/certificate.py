"""Whole-path scenario simplex potential proof, sufficient not complete."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('b3_helper',Path(__file__).resolve().parent.parent/'b3'/'certificate.py');b3=importlib.util.module_from_spec(spec);spec.loader.exec_module(b3)
Invalid,keys,integer,rational,capped,scalar_text,load_bytes=(getattr(b3,k) for k in ('Invalid','keys','integer','rational','capped','scalar_text','load_bytes'))

def check(s):
    try:
        keys(s,('graph','start','goal','route','weights','potential'))
        G=s['graph'];temp={'graph':G,'start':s['start'],'goal':s['goal'],'forbidden':[],'penalties':[],'route':None,'potential':None}
        b3.t2.model(temp)
        ns=next((len(e['scenario_times']) for es in G.values() for e in es),0)
        if ns==0:raise Invalid('positive scenario dimension unestablished')
        if s['route'] is None or s['weights'] is None or s['potential'] is None:return {'status':'UNAVAILABLE','reason':'missing route/proof after model checks'}
        r=s['route'];keys(r,('path','edges','scenario_totals','worst_time'));path=r['path'];edges=r['edges']
        if type(path) is not list or type(edges) is not list or not 1<=len(path)<=256 or len(edges)!=len(path)-1 or any(type(v) is not str or v not in G for v in path) or path[0]!=s['start'] or path[-1]!=s['goal']:raise Invalid('route path/query')
        if type(r['scenario_totals']) is not list or len(r['scenario_totals'])!=ns:raise Invalid('reported scenario dimension')
        reported=[integer(v) for v in r['scenario_totals']];totals=[0]*ns;routeledger=[]
        for a,b,e in zip(path,path[1:],edges):
            keys(e,('source','edge_index','target'));i=integer(e['edge_index'])
            if e['source']!=a or e['target']!=b or i>=len(G[a]) or G[a][i]['target']!=b:raise Invalid('route edge identity')
            totals=[integer(v+c) for v,c in zip(totals,G[a][i]['scenario_times'])];routeledger.append({'edge':[a,i],'scenario_totals':totals[:]})
        worst=max(totals)
        if totals!=reported or worst!=integer(r['worst_time']):raise Invalid('whole-path scenario totals/worst')
        weights=s['weights']
        if type(weights) is not list or len(weights)!=ns:raise Invalid('simplex dimension')
        weights=[capped(rational(v)) for v in weights]
        if any(v<0 for v in weights) or sum(weights)!=1:raise Invalid('nonnegative simplex sum')
        verts=sorted(G);h=s['potential']
        if type(h) is not list or len(h)!=len(verts):raise Invalid('potential vertex dimension')
        h=[capped(rational(v)) for v in h];potential=dict(zip(verts,h))
        if potential[s['start']]!=0:raise Invalid('source potential')
        ledger=[]
        for a in verts:
            for i,e in enumerate(G[a]):
                cost=capped(sum(v*c for v,c in zip(weights,e['scenario_times'])));slack=cost+potential[a]-potential[e['target']]
                if slack<0:raise Invalid('weighted potential infeasible')
                ledger.append({'edge':[a,i],'target':e['target'],'weighted_cost':scalar_text(cost),'slack':scalar_text(slack)})
        weighted=capped(sum(v*c for v,c in zip(weights,totals)));LB=capped(potential[s['goal']])
        if LB>worst:raise Invalid('bound above feasible worst')
        return {'status':'CERTIFIED_MINIMAX' if LB==worst else 'UNAVAILABLE','reason':'matching feasible worst/simplex bound' if LB==worst else 'feasible incomplete simplex bound','vertices':verts,'edge_ledger':ledger,'route_ledger':routeledger,'scenario_totals':totals,'route_worst':worst,'weighted_route_cost':scalar_text(weighted),'lower_bound':scalar_text(LB),'gap':scalar_text(worst-LB)}
    except (KeyError,TypeError,IndexError,AttributeError) as e:return {'status':'INVALID','reason':'malformed container '+type(e).__name__}
    except Invalid as e:return {'status':'INVALID','reason':str(e)}
