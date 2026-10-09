"""Bounded missing witness completion, separate from I5's proof status."""
import copy,importlib.util
from pathlib import Path
from model import model,i3,Invalid,Failure
spec=importlib.util.spec_from_file_location('i6_unchanged_i5_generator',Path(__file__).resolve().parent.parent/'i5/generator.py');previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)

def reconstruct(s,arcs,indices,n):
    path=[s['start']];edges=[];totals=[0]*n;exposure=turn=0
    for index in indices:
        a=arcs[index];identity=a['edge']
        if identity is None:continue
        v,j=identity;e=s['graph'][v][j];path.append(e['target']);edges.append({'source':v,'edge_index':j,'target':e['target']})
        exposure+=e['exposure'];turn+=a['delay'];totals=[x+y+a['delay'] for x,y in zip(totals,e['scenario_times'])]
    return {'path':path,'edges':edges,'scenario_totals':totals,'worst_time':max(totals),'exposure':exposure,'turn_penalty':turn}

def generate(s):
    base={'status':None,'reason':'','original':copy.deepcopy(s)}
    try:G,n,states,arcs,primal=model(s)
    except (Invalid,KeyError,TypeError,IndexError,AttributeError) as e:return dict(base,status='INVALID',reason=str(e))
    if sum(map(len,G.values()))>6:return dict(base,status='UNAVAILABLE_DOMAIN',reason='six original edge research cap')
    if s['route'] is not None:
        return dict(base,status='PRESERVED',reason='valid supplied route preserved without search',route_source='supplied',completed_statement=copy.deepcopy(s),route_check=primal,downstream=previous.generate(s))
    raw,overflow=previous.paths(G,n,states,arcs);base['paths']=raw
    if overflow:return dict(base,status='UNAVAILABLE_ENUMERATION',reason='65th path; no prefix selection')
    feasible=[k for k,p in enumerate(raw) if p['exposure']<=s['budget']];objectives=[max(p['scenario_totals']) for p in raw];base.update(feasible_indices=feasible,objectives=objectives)
    if not feasible:return dict(base,status='NO_FEASIBLE_PATH',reason='complete bounded original-state exhaustion')
    chosen=min(feasible,key=lambda k:(objectives[k],k));route=reconstruct(s,arcs,raw[chosen]['arcs'],n);base.update(selected_index=chosen,selected_route=route)
    if any(type(x) is not int or not 0<=x<=i3.b3.MAX for x in route['scenario_totals']+[route['worst_time'],route['exposure'],route['turn_penalty']]):return dict(base,status='UNAVAILABLE_WITNESS_DOMAIN',reason='selected witness totals exceed unchanged integer cap')
    completed=copy.deepcopy(s);completed['route']=route
    try:checked=i3.b3.t2.helper.checked(completed)
    except (Invalid,KeyError,TypeError,IndexError,AttributeError) as e:raise Failure('selected reconstruction original audit '+str(e)) from e
    if checked['status']!='FEASIBLE_WITNESS' or checked['exposure']!=raw[chosen]['exposure'] or checked['scenario_totals']!=raw[chosen]['scenario_totals']:raise Failure('raw path vs witness audit')
    return dict(base,status='COMPLETED',reason='bounded best missing witness completed, proof status separate',route_source='completed',completed_statement=completed,route_check=checked,downstream=previous.generate(completed))
