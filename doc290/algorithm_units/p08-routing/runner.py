"""Strict JSON front end for routing kernels. No attribute inference."""
import argparse
import json
import sys
from routing import Edge, exposure_budget_route, scenario_robust_route, budgeted_scenario_route, turn_constrained_route, integrated_route


def unique_object(pairs):
    out={}
    for k,v in pairs:
        if k in out: raise ValueError('duplicate JSON key: '+k)
        out[k]=v
    return out


def reject_constant(value):
    raise ValueError('non-standard JSON constant: '+value)


def fields(obj, required, optional=()):
    if not isinstance(obj,dict) or set(obj)-set(required)-set(optional) or set(required)-set(obj):
        raise ValueError('missing or unknown object fields')


def edge_id(value):
    if not isinstance(value,list) or len(value)!=2 or not isinstance(value[0],str) or type(value[1]) is not int or value[1]<0:
        raise ValueError('edge ID must be [source_string, nonnegative_integer_index]')
    return tuple(value)


def solve(payload):
    fields(payload,('method','graph','start','goal'),('budget','forbidden','penalties'))
    method=payload['method']
    methods={'budget','scenario','budget-scenario','turn','integrated'}
    if not isinstance(method,str) or method not in methods: raise ValueError('unknown method')
    needs_budget=method in {'budget','budget-scenario','integrated'}
    uses_turns=method in {'turn','integrated'}
    if needs_budget != ('budget' in payload): raise ValueError('budget required only for budget methods')
    if not uses_turns and ('forbidden' in payload or 'penalties' in payload):
        raise ValueError('turn rules unsupported by selected method')
    if not isinstance(payload['start'],str) or not isinstance(payload['goal'],str):raise ValueError('start/goal must be strings')
    if not isinstance(payload['graph'],dict):raise ValueError('graph must be an object')
    graph={}
    for node,edges in payload['graph'].items():
        if not isinstance(node,str) or not isinstance(edges,list):raise ValueError('graph must map strings to edge lists')
        graph[node]=[]
        for e in edges:
            fields(e,('target','time','exposure'),('scenario_times',))
            scenarios=e.get('scenario_times',[])
            if not isinstance(e['target'],str) or not isinstance(scenarios,list):raise ValueError('bad edge target or scenarios')
            graph[node].append(Edge(e['target'],e['time'],e['exposure'],tuple(scenarios)))
    forbidden=set();penalties={}
    for name in ('forbidden','penalties'):
        if not isinstance(payload.get(name,[]),list):raise ValueError('turn rules must be lists')
    for rule in payload.get('forbidden',[]):
        if not isinstance(rule,list) or len(rule)!=2:raise ValueError('forbidden rule must be an edge-ID pair')
        key=(edge_id(rule[0]),edge_id(rule[1]))
        if key in forbidden:raise ValueError('duplicate forbidden rule')
        forbidden.add(key)
    for rule in payload.get('penalties',[]):
        fields(rule,('incoming','outgoing','delay'))
        key=(edge_id(rule['incoming']),edge_id(rule['outgoing']))
        if key in penalties:raise ValueError('duplicate turn penalty')
        penalties[key]=rule['delay']
    start,goal=payload['start'],payload['goal']
    if method=='budget': result=exposure_budget_route(graph,start,goal,payload['budget'])
    elif method=='scenario':result=scenario_robust_route(graph,start,goal)
    elif method=='budget-scenario':result=budgeted_scenario_route(graph,start,goal,payload['budget'])
    elif method=='turn':result=turn_constrained_route(graph,start,goal,forbidden,penalties)
    else:result=integrated_route(graph,start,goal,payload['budget'],forbidden,penalties)
    return {'status':'infeasible' if result is None else 'ok','method':method,'result':result,
            'evidence_scope':'optimization on supplied graph costs, not physiological validation'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',help='JSON input path, or - for stdin')
    args=parser.parse_args()
    try:
        if args.input=='-':raw=sys.stdin.read()
        else:
            with open(args.input,encoding='utf-8') as f:raw=f.read()
        payload=json.loads(raw,object_pairs_hook=unique_object,parse_constant=reject_constant)
        output=solve(payload)
        print(json.dumps(output,allow_nan=False,sort_keys=True))
        return 0
    except (ValueError,TypeError,OverflowError,OSError) as exc:
        print(json.dumps({'status':'error','error':str(exc)},allow_nan=False),file=sys.stderr)
        return 2

if __name__=='__main__':sys.exit(main())
