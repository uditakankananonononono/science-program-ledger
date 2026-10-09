import sys,json,hashlib,importlib.util,warnings,dataclasses,heapq,math,collections,re,fractions,_hashlib,_json,_sre
from pathlib import Path
from split import split,verify_output,load_bytes,Invalid
ROOT=Path(__file__).resolve().parent

def gate():
    for name,digest in json.loads((ROOT/'manifest.json').read_text())['files'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise Invalid('source identity '+name)
    env=json.loads((ROOT/'environment.json').read_text())
    if sys.version!=env['python']:raise Invalid('python version')
    for name,i in env['sources'].items():
        if hashlib.sha256(Path(i['path']).read_bytes()).hexdigest()!=i['sha256']:raise Invalid('runtime identity '+name)
    for name in env['modules']:
        m=sys.modules.get(name)
        if m is None or str(Path(getattr(m,'__file__',sys.executable)).resolve())!=env['sources'][name]['path']:raise Invalid('loaded module '+name)
    if str(Path(sys.executable).resolve())!=env['sources']['python_executable']['path']:raise Invalid('executable path')

def oracle(G,start,goal,budget):
    best=None
    def visit(v,seen,time,exp):
        nonlocal best
        if exp>budget:return
        if v==goal:
            best=time if best is None else min(best,time);return
        for e in G[v]:
            if e['target'] not in seen:visit(e['target'],seen|{e['target']},time+e['time'],exp+e['exposure'])
    visit(start,{start},0,0);return best

def expansion(s,r,route):
    if route is None:return None
    G=s['original'];p=[s['start']];ids=[];ns=next((len(e['scenario_times']) for es in G.values() for e in es),0);tot=[0,0]+[0]*ns
    for edge in route['edges']:
        seg=r['witnesses'][edge['source']][edge['edge_index']]
        if seg[0]!=p[-1] or seg[-1]!=edge['target']:raise Invalid('expanded route continuity')
        for a,b in zip(seg,seg[1:]):
            i,e=next((i,e) for i,e in enumerate(G[a]) if e['target']==b);ids.append({'source':a,'edge_index':i,'target':b});tot=[x+y for x,y in zip(tot,[e['time'],e['exposure']]+e['scenario_times'])]
        p.extend(seg[1:])
    if p[-1]!=s['goal'] or tot[0]!=route['time'] or tot[1]!=route['exposure'] or tot[1]>s['budget']:raise Invalid('expanded totals/budget/query')
    return {'path':p,'edges':ids,'time':tot[0],'exposure':tot[1],'scenario_totals':tot[2:]}

def run(output):
    gate()
    # Protocol archive cap separate from per-row strict128KiB parser, eachJSONLrow ownlimit.
    data=(ROOT/'cases.jsonl').read_bytes()
    if len(data)>2097152:raise Invalid('protocol archive cap')
    lines=data.split(b'\n')
    if lines[-1]!=b'':raise Invalid('protocol final newline')
    if len(lines)-1!=231:raise Invalid('protocol row count')
    cases=[load_bytes(line) for line in lines[:-1]]
    sys.path.insert(0,str(ROOT.parent));from routing import Edge,exposure_budget_route
    rows=[]
    for c in cases:
        s=c['statement'];row={'name':c['name'],'expected':c['expected'],'input_sha256':hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest()}
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            try:
                result=split(s);row['result']=result;row['agreement']=result['status']==c['expected']
                if result['status']=='SPLIT_REPRESENTATION':
                    row['representation_checked']=verify_output(s,result)
                    def G(g):return {v:[Edge(e['target'],e['time'],e['exposure'],tuple(e['scenario_times'])) for e in es] for v,es in g.items()}
                    orig=exposure_budget_route(G(s['original']),s['start'],s['goal'],s['budget']);new=exposure_budget_route(G(result['compressed']),s['start'],s['goal'],s['budget']);best=oracle(s['original'],s['start'],s['goal'],s['budget'])
                    row.update(original_route=orig,split_route=new,oracle_time=best,expanded=expansion(s,result,new))
                    row['agreement']=row['agreement'] and (None if orig is None else orig['time'])==best and (None if new is None else new['time'])==best
            except Exception as e:row.update(exception_type=type(e).__name__,exception=str(e),agreement=False)
            row['warnings']=[{'category':w.category.__name__,'message':str(w.message)} for w in caught]
        rows.append(row)
    Path(output).write_text(json.dumps({'row_count':len(rows),'agreement_count':sum(r['agreement'] for r in rows),'rows':rows,'scope':'fixed integer query grid; no universal routing equivalence'},sort_keys=True,indent=2)+'\n')
if __name__=='__main__':run(sys.argv[1])
