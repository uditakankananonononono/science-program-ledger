"""Exact scalar Lagrange exposure-budget certificate, explicitly incomplete."""
import sys,importlib.util
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]/'p08-field-planning'/'f3'))
from verify import rational,keys,Invalid,load_bytes,scalar_text
spec=importlib.util.spec_from_file_location('t2_helper',Path(__file__).resolve().parent.parent/'t2'/'certificate.py');t2=importlib.util.module_from_spec(spec);spec.loader.exec_module(t2)
integer=t2.integer;MAX=2**53-1

def capped(v):
    if abs(v)>MAX:raise Invalid('rational domain cap')
    return v

def check(s):
    try:
        keys(s,('graph','start','goal','budget','route','multiplier','potential'))
        # Reuse unchanged T2 model validation with NO turn rules; every original edge still validated.
        G=s['graph'];temp={'graph':G,'start':s['start'],'goal':s['goal'],'forbidden':[],'penalties':[],'route':None,'potential':None}
        t2.model(temp);budget=integer(s['budget'])
        if s['route'] is None or s['multiplier'] is None or s['potential'] is None:return {'status':'UNAVAILABLE','reason':'missing route/proof after model validation'}
        r=s['route'];keys(r,('path','edges','time','exposure'));path=r['path'];edges=r['edges']
        if type(path) is not list or type(edges) is not list or not 1<=len(path)<=256 or len(edges)!=len(path)-1 or any(type(v) is not str or v not in G for v in path) or path[0]!=s['start'] or path[-1]!=s['goal']:raise Invalid('route path/query')
        time=exposure=0;routeledger=[]
        for a,b,e in zip(path,path[1:],edges):
            keys(e,('source','edge_index','target'));i=integer(e['edge_index'])
            if e['source']!=a or e['target']!=b or i>=len(G[a]) or G[a][i]['target']!=b:raise Invalid('route edge identity')
            edge=G[a][i];time=integer(time+edge['time']);exposure=integer(exposure+edge['exposure']);routeledger.append({'edge':[a,i],'time':time,'exposure':exposure})
        if time!=integer(r['time']) or exposure!=integer(r['exposure']) or exposure>budget:raise Invalid('route totals/budget')
        lam=capped(rational(s['multiplier']))
        if lam<0:raise Invalid('negative multiplier')
        verts=sorted(G);h=s['potential']
        if type(h) is not list or len(h)!=len(verts):raise Invalid('potential vertex dimension')
        h=[capped(rational(v)) for v in h];potential=dict(zip(verts,h))
        if potential[s['start']]!=0:raise Invalid('source potential')
        ledger=[]
        for a in verts:
            for i,e in enumerate(G[a]):
                cost=capped(e['time']+lam*e['exposure']);slack=cost+potential[a]-potential[e['target']]
                if slack<0:raise Invalid('weighted potential infeasible')
                ledger.append({'edge':[a,i],'target':e['target'],'weighted_cost':scalar_text(cost),'slack':scalar_text(slack)})
        weightedpath=capped(time+lam*exposure);charge=capped(lam*budget);LB=capped(potential[s['goal']]-charge)
        if LB>time:raise Invalid('bound above feasible time')
        return {'status':'CERTIFIED_OPTIMAL' if LB==time else 'UNAVAILABLE','reason':'matching feasible route/Lagrange bound' if LB==time else 'feasible incomplete Lagrange bound','vertices':verts,'edge_ledger':ledger,'route_ledger':routeledger,'route_time':time,'route_exposure':exposure,'weighted_route_cost':scalar_text(weightedpath),'budget_charge':scalar_text(charge),'lower_bound':scalar_text(LB),'gap':scalar_text(time-LB)}
    except (KeyError,TypeError,IndexError,AttributeError) as e:return {'status':'INVALID','reason':'malformed container '+type(e).__name__}
    except Invalid as e:return {'status':'INVALID','reason':str(e)}
