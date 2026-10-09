import hashlib,json,os,sys,re,fractions,_hashlib,_json,_sre,collections,dataclasses,heapq,math,warnings
from pathlib import Path
from certificate import check as validate,load_bytes,Invalid
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
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always');result=validate(c['statement'])
        rows.append({'name':c['name'],'expected':c['expected'],'result':result,'agreement':agreed(c['expected'],result),'warnings':[{'category':w.category.__name__,'message':str(w.message)} for w in caught],'input_sha256':hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest()})
    sys.path.insert(0,str(ROOT.parent));from routing import Edge,exposure_budget_route
    baseline=[]
    for c in cases:
        if ':' in c['name']:continue
        s=c['statement'];G={v:[Edge(e['target'],e['time'],e['exposure'],tuple(e['scenario_times'])) for e in es] for v,es in s['graph'].items()}
        try:
            r=exposure_budget_route(G,s['start'],s['goal'],s['budget'])
            entry={'name':c['name'],'route':r}
            if r is not None:
                statement=dict(s,route=r);entry['certificate_check_with_supplied_potential']=validate(statement)
        except Exception as e:entry={'name':c['name'],'exception_type':type(e).__name__,'exception':str(e)}
        baseline.append(entry)
    Path(output).write_text(json.dumps({'rows':rows,'row_count':len(rows),'agreement_count':sum(r['agreement'] for r in rows),'baseline':baseline,'scope':'scalar exposure Lagrange certificate is sufficient, not complete/search/clinical'},sort_keys=True,indent=2)+'\n')
if __name__=='__main__':run(sys.argv[1])
