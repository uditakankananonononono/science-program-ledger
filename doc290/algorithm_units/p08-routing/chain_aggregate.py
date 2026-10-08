"""Additive chain-cost adapter. Anchor-only and turn-free scope."""
from chain_costs import serialize_chain_costs
from routing import Edge, finite_totals


def aggregate_chains(graph):
    serialized=serialize_chain_costs(graph)
    lengths={len(e.scenario_times) for edges in graph.values() for e in edges}
    if len(lengths)>1:raise ValueError('heterogeneous scenario-vector lengths')
    n=next(iter(lengths),0)
    output={a:[] for a in serialized['anchors']}
    witnesses={a:[] for a in serialized['anchors']}
    for chain in serialized['chains']:
        for direction in chain['directions']:
            steps=direction['steps']
            t=sum(s['time'] for s in steps)
            r=sum(s['exposure'] for s in steps)
            scenarios=tuple(sum(s['scenario_times'][i] for s in steps) for i in range(n))
            finite_totals(t,r,*scenarios)
            a,b=direction['source'],direction['target']
            output[a].append(Edge(b,t,r,scenarios))
            witnesses[a].append([steps[0]['source']]+[s['target'] for s in steps])
    return output,witnesses


def expand_route(result,witnesses):
    if result is None:return None
    path=[result['path'][0]]
    for edge in result['edges']:
        segment=witnesses[edge['source']][edge['edge_index']]
        if segment[0]!=path[-1] or segment[-1]!=edge['target']:
            raise ValueError('route/witness mismatch')
        path.extend(segment[1:])
    return path
