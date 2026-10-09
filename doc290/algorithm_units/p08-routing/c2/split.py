"""Explicit integer interior-query chain splitting. No production integration."""
import sys,importlib.util,copy
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent/'c1'))
from validate import validate as c1_validate,Invalid,integer,vertex,load_bytes,keys

def prepare(s):
    keys(s,('original','compressed','witnesses','start','goal','budget','forbidden','penalties'))
    # The source representation, real costs, budget and actual turns are checked first.
    C=s['compressed']
    if type(C) is not dict or not C:raise Invalid('compressed source shape')
    anchor=next(iter(C));internal=copy.deepcopy(s);internal.update(start=anchor,goal=anchor,route=None)
    verdict=c1_validate(internal)
    if verdict['status']!='UNAVAILABLE':raise Invalid('source representation: '+verdict['reason'])
    start=vertex(s['start']);goal=vertex(s['goal'])
    if start not in s['original'] or goal not in s['original']:raise Invalid('requested query absent')
    integer(s['budget'])
    return set(C)|{start,goal}

def split(s):
    try:
        anchors=prepare(s);G=s['original'];C={a:[] for a in sorted(anchors)};W={a:[] for a in sorted(anchors)};P={a:[] for a in sorted(anchors)}
        lookup={a:{e['target']:e for e in es} for a,es in G.items()}
        for source in sorted(s['compressed']):
            for index,path in enumerate(s['witnesses'][source]):
                positions=[i for i,v in enumerate(path) if v in anchors]
                for first,last in zip(positions,positions[1:]):
                    seg=path[first:last+1];tot=[0,0]+[0]*len(s['compressed'][source][index]['scenario_times'])
                    for a,b in zip(seg,seg[1:]):
                        edge=lookup[a][b];tot=[integer(x+y) for x,y in zip(tot,[edge['time'],edge['exposure']]+edge['scenario_times'])]
                    a=seg[0];C[a].append({'target':seg[-1],'time':tot[0],'exposure':tot[1],'scenario_times':tot[2:]});W[a].append(seg);P[a].append({'source':source,'edge_index':index,'first_position':first,'last_position':last})
        result={'status':'SPLIT_REPRESENTATION','compressed':C,'witnesses':W,'provenance':P,'anchors':sorted(anchors)}
        verify_output(s,result);return result
    except Invalid as e:return {'status':'INVALID','reason':str(e)}

def verify_output(s,r):
    anchors=prepare(s);G=s['original'];lookup={a:{e['target']:e for e in es} for a,es in G.items()}
    if set(r['compressed'])!=anchors or set(r['witnesses'])!=anchors or set(r['provenance'])!=anchors or r['anchors']!=sorted(anchors):raise Invalid('output anchors')
    # Independent maximal-chain tracing starts at augmented anchors, never cuts source witnesses.
    traced=[]
    for a in sorted(anchors):
        for nxt in sorted(lookup[a]):
            path=[a,nxt];previous=a;current=nxt
            while current not in anchors:
                ns=[v for v in lookup[current] if v!=previous]
                if len(ns)!=1:raise Invalid('output continuation degree')
                previous,current=current,ns[0];path.append(current)
                if len(path)>len(G)+1:raise Invalid('output tracing loop')
            traced.append(tuple(path))
    actual=[];positions_seen=set();expected_positions=set();coverage={}
    for source,paths in s['witnesses'].items():
        for i,path in enumerate(paths):
            cuts=[j for j,v in enumerate(path) if v in anchors]
            expected_positions.update((source,i,a,b) for a,b in zip(cuts,cuts[1:]))
    for a,es in r['compressed'].items():
        if len(es)!=len(r['witnesses'][a]) or len(es)!=len(r['provenance'][a]):raise Invalid('output shape')
        for e,path,pr in zip(es,r['witnesses'][a],r['provenance'][a]):
            keys(pr,('source','edge_index','first_position','last_position'))
            source=pr['source'];i=integer(pr['edge_index']);first=integer(pr['first_position']);last=integer(pr['last_position'])
            if source not in s['witnesses'] or i>=len(s['witnesses'][source]) or not first<last<len(s['witnesses'][source][i]):raise Invalid('provenance positions')
            identity=(source,i,first,last)
            if identity in positions_seen or identity not in expected_positions:raise Invalid('provenance cuts')
            positions_seen.add(identity)
            if path!=s['witnesses'][source][i][first:last+1] or path[0]!=a or path[-1]!=e['target']:raise Invalid('provenance segment')
            actual.append(tuple(path));tot=[0,0]+[0]*len(e['scenario_times'])
            for v,t in zip(path,path[1:]):
                oe=lookup[v][t];coverage[(v,t)]=coverage.get((v,t),0)+1;tot=[integer(x+y) for x,y in zip(tot,[oe['time'],oe['exposure']]+oe['scenario_times'])]
            if tot!=[e['time'],e['exposure']]+e['scenario_times']:raise Invalid('output cost')
    if sorted(actual)!=sorted(traced) or positions_seen!=expected_positions:raise Invalid('maximal path/cut correspondence')
    if set(coverage)!={(v,t) for v in lookup for t in lookup[v]} or any(n!=1 for n in coverage.values()):raise Invalid('directed coverage')
    return True
