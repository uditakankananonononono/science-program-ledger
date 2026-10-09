import hashlib,json,os,sys,re,fractions,_hashlib,_json,_sre,collections,dataclasses,heapq,math
from pathlib import Path
from validate import validate,load_bytes,Invalid
ROOT=Path(__file__).resolve().parent

def gate():
    for name,digest in json.loads((ROOT/'manifest.json').read_text())['files'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise Invalid('source identity '+name)
    env=json.loads((ROOT/'environment.json').read_text())
    if sys.version!=env['python']:raise Invalid('python version')
    for name,ident in env['sources'].items():
        if hashlib.sha256(Path(ident['path']).read_bytes()).hexdigest()!=ident['sha256']:raise Invalid('runtime identity '+name)
    for name in env['modules']:
        m=sys.modules.get(name)
        if m is None or str(Path(getattr(m,'__file__',sys.executable)).resolve())!=env['sources'][name]['path']:raise Invalid('loaded module '+name)
    if str(Path(sys.executable).resolve())!=env['sources']['python_executable']['path']:raise Invalid('executable path')

def agreed(expected,result):return result['status']==expected

def run(output):
    gate();cases=load_bytes((ROOT/'cases.json').read_bytes());rows=[]
    for c in cases:
        result=validate(c['statement']);rows.append({'name':c['name'],'expected':c['expected'],'result':result,'agreement':agreed(c['expected'],result),'input_sha256':hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
    sys.path.insert(0,str(ROOT.parent));from routing import Edge,exposure_budget_route
    from chain_aggregate import aggregate_chains,expand_route
    baseline=[]
    for c in cases:
        if ':' in c['name']:continue
        s=c['statement'];G={v:[Edge(e['target'],e['time'],e['exposure'],tuple(e['scenario_times'])) for e in es] for v,es in s['original'].items()}
        try:
            comp,w=aggregate_chains(G);r=exposure_budget_route(comp,s['start'],s['goal'],s['budget']);p=expand_route(r,w);entry={'name':c['name'],'route':r,'expanded_path':p}
            if p is not None:
                ss=[0]*len(next(e.scenario_times for es in G.values() for e in es));time=exposure=0
                for a,b in zip(p,p[1:]):
                    edge=next(e for e in G[a] if e.target==b);time+=edge.time;exposure+=edge.exposure;ss=[x+y for x,y in zip(ss,edge.scenario_times)]
                entry['independent_original_totals']={'time':time,'exposure':exposure,'scenario_totals':ss,'worst_time':max(ss)}
        except Exception as e:entry={'name':c['name'],'exception_type':type(e).__name__,'exception':str(e)}
        baseline.append(entry)
    Path(output).write_text(json.dumps({'rows':rows,'row_count':len(rows),'agreement_count':sum(r['agreement'] for r in rows),'baseline':baseline,'scope':'integer anchor turn-free supplied witnesses, not optimality/equivalence'},sort_keys=True,indent=2)+'\n')
if __name__=='__main__':run(sys.argv[1])
