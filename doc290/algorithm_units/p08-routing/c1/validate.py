"""Checked integer chain compression and supplied-route expansion, not optimality."""
import sys
from pathlib import Path
from collections import Counter
sys.path.append(str(Path(__file__).resolve().parents[2]/'p08-field-planning'/'f3'))
from verify import Invalid,keys,load_bytes
MAX=2**53-1

def integer(v):
    if type(v) is not int or not 0<=v<=MAX:raise Invalid('integer cost/index domain')
    return v

def vertex(v):
    if type(v) is not str or not 1<=len(v)<=80:raise Invalid('vertex identifier')
    return v

def graph(g,original):
    if type(g) is not dict or not 1<=len(g)<=32:raise Invalid('graph dimension')
    for v in g:vertex(v)
    count=0;dimensions=set()
    for v,es in g.items():
        if type(es) is not list:raise Invalid('adjacency shape')
        seen=set()
        for e in es:
            keys(e,('target','time','exposure','scenario_times'));t=vertex(e['target'])
            if t not in g:raise Invalid('unknown edge target')
            if original and (t==v or t in seen):raise Invalid('original simple topology')
            seen.add(t);integer(e['time']);integer(e['exposure'])
            ss=e['scenario_times']
            if type(ss) is not list or not 1<=len(ss)<=4:raise Invalid('scenario dimension')
            for s in ss:integer(s)
            dimensions.add(len(ss));count+=1
    if count>128 or len(dimensions)>1:raise Invalid('edge/scenario cap')
    return next(iter(dimensions),None)

def validate(statement):
    try:return checked(statement)
    except Invalid as e:return {'status':'INVALID','reason':str(e)}

def checked(s):
    keys(s,('original','compressed','witnesses','start','goal','budget','forbidden','penalties','route'))
    G=s['original'];C=s['compressed'];ns=graph(G,True);cs=graph(C,False)
    if ns!=cs:raise Invalid('scenario correspondence')
    if s['forbidden']!=[] or type(s['forbidden']) is not list or s['penalties']!=[] or type(s['penalties']) is not list:raise Invalid('turn rules unsupported')
    budget=integer(s['budget']);lookup={v:{e['target']:(i,e) for i,e in enumerate(es)} for v,es in G.items()}
    if any(v not in lookup[t] for v in G for t in lookup[v]):raise Invalid('nonreciprocal topology')
    anchors={v for v,es in G.items() if len(es)!=2};seen=set()
    for root in sorted(G):
        if root in seen:continue
        todo=[root];comp=set()
        while todo:
            v=todo.pop()
            if v in comp:continue
            comp.add(v);todo.extend(lookup[v])
        seen.update(comp)
        if not comp&anchors:anchors.add(min(comp))
    if set(C)!=anchors:raise Invalid('anchor correspondence')
    W=s['witnesses']
    if type(W) is not dict or set(W)!=anchors:raise Invalid('witness keys')
    coverage=Counter();paths={};original_edges={ (v,i) for v,es in G.items() for i,e in enumerate(es)}
    for a,es in C.items():
        if type(W[a]) is not list or len(W[a])!=len(es):raise Invalid('witness adjacency shape')
        for i,(e,p) in enumerate(zip(es,W[a])):
            if type(p) is not list or not 2<=len(p)<=256 or any(type(v) is not str or v not in G for v in p):raise Invalid('witness path shape/vertex')
            if p[0]!=a or p[-1]!=e['target']:raise Invalid('witness endpoints')
            body=p[:-1] if p[0]==p[-1] else p
            if len(body)!=len(set(body)):raise Invalid('witness repeated vertex')
            for j,v in enumerate(p[1:-1],1):
                if v in anchors or len(lookup[v])!=2:raise Invalid('witness internal anchor/degree')
                if p[j+1]==p[j-1]:raise Invalid('witness backtracking')
            totals=[0,0]+[0]*(ns or 0);ids=[]
            for v,t in zip(p,p[1:]):
                if t not in lookup[v]:raise Invalid('witness nonedge')
                index,oe=lookup[v][t];ids.append({'source':v,'edge_index':index,'target':t});coverage[(v,index)]+=1
                totals=[integer(x+y) for x,y in zip(totals,[oe['time'],oe['exposure']]+oe['scenario_times'])]
            if totals!=[e['time'],e['exposure']]+e['scenario_times']:raise Invalid('compressed cost correspondence')
            paths[(a,i)]=(p,ids,totals)
    if set(coverage)!=original_edges or any(n!=1 for n in coverage.values()):raise Invalid('whole directed coverage')
    start=vertex(s['start']);goal=vertex(s['goal'])
    if start not in anchors or goal not in anchors:raise Invalid('query must use anchors')
    R=s['route']
    if R is None:return {'status':'UNAVAILABLE','reason':'missing route after representation validation'}
    keys(R,('path','edges','time','exposure','scenario_totals','worst_time'))
    p=R['path'];edges=R['edges']
    if type(p) is not list or type(edges) is not list or not 1<=len(p)<=256 or len(edges)!=len(p)-1 or p[0]!=start or p[-1]!=goal:raise Invalid('route path shape/endpoints')
    total=[0,0]+[0]*(ns or 0);expanded=[start];ids=[]
    for node,target,edge in zip(p,p[1:],edges):
        keys(edge,('source','edge_index','target'));index=integer(edge['edge_index'])
        if type(node) is not str or node not in C or type(target) is not str or edge['source']!=node or edge['target']!=target or index>=len(C[node]) or C[node][index]['target']!=target:raise Invalid('route edge identity')
        segment,edgeids,cost=paths[(node,index)]
        if segment[0]!=expanded[-1]:raise Invalid('expanded continuity')
        expanded.extend(segment[1:]);ids.extend(edgeids)
        if len(expanded)>256:raise Invalid('expanded route cap')
        # Sum ORIGINAL steps, not compressed totals as trust source.
        for ei in edgeids:
            oe=G[ei['source']][ei['edge_index']]
            total=[integer(x+y) for x,y in zip(total,[oe['time'],oe['exposure']]+oe['scenario_times'])]
    if type(R['scenario_totals']) is not list or len(R['scenario_totals'])!=(ns or 0):raise Invalid('route scenario shape')
    reported=[integer(R['time']),integer(R['exposure'])]+[integer(v) for v in R['scenario_totals']]
    if total!=reported or integer(R['worst_time'])!=max(total[2:],default=0):raise Invalid('route totals correspondence')
    if total[1]>budget:raise Invalid('route exposure budget')
    return {'status':'FEASIBLE_WITNESS','reason':'checked integer chain route','expanded_path':expanded,'original_edges':ids,'time':total[0],'exposure':total[1],'scenario_totals':total[2:],'worst_time':max(total[2:],default=0)}
