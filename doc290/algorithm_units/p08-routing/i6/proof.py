"""Independent indexed topology/path/choice/route and downstream reconstruction."""
import copy,json,importlib.util
from pathlib import Path
from model import model,i3,Invalid,Failure
spec=importlib.util.spec_from_file_location('i6_unchanged_i5_proof',Path(__file__).resolve().parent.parent/'i5/proof.py');down=importlib.util.module_from_spec(spec);spec.loader.exec_module(down)
audit=down.audit;guarded_potential=down.guarded_potential;reconcile=down.reconcile
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def verify(s,result):
    if type(result) is not dict:raise Failure('result dict')
    base={'status','reason','original'}
    if not base<=set(result) or type(result['reason']) is not str or canonical(result['original'])!=canonical(s):raise Failure('typed source/short reason')
    try:G,n,states,arcs,primal=model(s)
    except (Invalid,KeyError,TypeError,IndexError,AttributeError):
        if set(result)!=base or result['status']!='INVALID':raise Failure('original invalid precedence/schema')
        return
    if sum(len(v) for v in G.values())>6:
        if set(result)!=base or result['status']!='UNAVAILABLE_DOMAIN':raise Failure('model domain precedence/schema')
        return
    expected={}
    if s['route'] is not None:
        expected.update(route_source='supplied',completed_statement=copy.deepcopy(s),route_check=primal);status='PRESERVED'
    else:
        # Unchanged I5 parent owns independent raw indexed topology/iterative DFS.
        raw,overflow=down.raw_paths(s,n);expected['paths']=raw
        if overflow:
            if set(result)!=base|set(expected) or result['status']!='UNAVAILABLE_ENUMERATION' or canonical(result['paths'])!=canonical(raw):raise Failure('enumeration no-prefix schema')
            return
        feasible=[k for k,p in enumerate(raw) if p['exposure']<=s['budget']];objectives=[max(p['scenario_totals']) for p in raw];expected.update(feasible_indices=feasible,objectives=objectives)
        if not feasible:
            if set(result)!=base|set(expected) or result['status']!='NO_FEASIBLE_PATH' or any(canonical(result[k])!=canonical(v) for k,v in expected.items()):raise Failure('no feasible complete schema')
            return
        minimum=min(objectives[k] for k in feasible);chosen=next(k for k in feasible if objectives[k]==minimum)
        _,indexed=down.raw_topology(s);path=[s['start']];edges=[];ss=[0]*n;r=turn=0
        for k in raw[chosen]['arcs']:
            _,_,identity,delay=indexed[k]
            if identity is None:continue
            origin,j=identity;edge=G[origin][j];edges.append({'source':origin,'edge_index':j,'target':edge['target']});path.append(edge['target']);r+=edge['exposure'];turn+=delay
            for column in range(n):ss[column]+=edge['scenario_times'][column]+delay
        route={'path':path,'edges':edges,'exposure':r,'scenario_totals':ss,'worst_time':max(ss),'turn_penalty':turn};expected.update(selected_index=chosen,selected_route=route)
        if max(ss+[max(ss),r,turn])>i3.b3.MAX:
            if set(result)!=base|set(expected) or result['status']!='UNAVAILABLE_WITNESS_DOMAIN' or any(canonical(result[k])!=canonical(v) for k,v in expected.items()):raise Failure('selected witness domain/schema/type')
            return
        completed=copy.deepcopy(s);completed['route']=route
        try:checked=i3.b3.t2.helper.checked(completed)
        except (Invalid,KeyError,TypeError,IndexError,AttributeError) as e:raise Failure('parent selected reconstruction audit '+str(e)) from e
        if checked['status']!='FEASIBLE_WITNESS' or checked['scenario_totals']!=raw[chosen]['scenario_totals'] or checked['exposure']!=raw[chosen]['exposure']:raise Failure('parent path/witness agreement')
        expected.update(route_source='completed',completed_statement=completed,route_check=checked);status='COMPLETED'
    if set(result)!=base|set(expected)|{'downstream'} or result['status']!=status or any(canonical(result[k])!=canonical(v) for k,v in expected.items()):raise Failure('full exact reconstruction/preservation/schema')
    down.verify(expected['completed_statement'],result['downstream'])
