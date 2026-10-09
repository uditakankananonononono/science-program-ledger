"""Strict admitted integer graph, independent indexed witness reconstruction."""
MAX=2**53-1
EDGE_MAX=MAX//32
class Invalid(ValueError):pass
def integer(v,cap=MAX):
    if type(v) is not int or not 0<=v<=cap:raise Invalid('strict integer cap')
    return v
def model(s):
    if type(s) is not dict or set(s)!={'graph','start','goal'}:raise Invalid('statement fields')
    G=s['graph']
    if type(G) is not dict or not 1<=len(G)<=32 or any(type(v) is not str or not 1<=len(v)<=80 for v in G):raise Invalid('graph/vertex domain')
    ns=set();count=0
    for a,es in G.items():
        if type(es) is not list:raise Invalid('adjacency type')
        for e in es:
            if type(e) is not dict or set(e)!={'target','time','exposure','scenario_times'} or type(e['target']) is not str or e['target'] not in G:raise Invalid('edge fields/target')
            integer(e['time'],EDGE_MAX);integer(e['exposure'],EDGE_MAX);ss=e['scenario_times']
            if type(ss) is not list or not 1<=len(ss)<=4:raise Invalid('positive scenarios')
            for c in ss:integer(c,EDGE_MAX)
            ns.add(len(ss));count+=1
    if count>128 or len(ns)!=1:raise Invalid('edge/dimension cap')
    if type(s['start']) is not str or type(s['goal']) is not str or s['start'] not in G or s['goal'] not in G:raise Invalid('query')
    return G,next(iter(ns))

def witness(s,r):
    G,ns=model(s)
    if type(r) is not dict or set(r)!={'path','edges','scenario_totals','worst_time'}:raise Invalid('route fields')
    path=r['path'];edges=r['edges']
    if type(path) is not list or not 1<=len(path)<=32 or any(type(v) is not str or v not in G for v in path) or len(set(path))!=len(path) or path[0]!=s['start'] or path[-1]!=s['goal'] or type(edges) is not list or len(edges)!=len(path)-1:raise Invalid('simple route/query/cap')
    totals=[0]*ns;ledger=[]
    for a,b,e in zip(path,path[1:],edges):
        if type(e) is not dict or set(e)!={'source','target','edge_index'}:raise Invalid('indexed fields')
        i=integer(e['edge_index'])
        if type(e['source']) is not str or type(e['target']) is not str or e['source']!=a or e['target']!=b or i>=len(G[a]) or G[a][i]['target']!=b:raise Invalid('original indexed edge')
        totals=[integer(x+y) for x,y in zip(totals,G[a][i]['scenario_times'])];ledger.append({'edge':[a,i],'scenario_totals':totals[:]})
    if type(r['scenario_totals']) is not list or len(r['scenario_totals'])!=ns or [integer(v) for v in r['scenario_totals']]!=totals or integer(r['worst_time'])!=max(totals):raise Invalid('reported whole-scenario totals')
    return {'ledger':ledger,'scenario_totals':totals,'worst_time':max(totals)}
