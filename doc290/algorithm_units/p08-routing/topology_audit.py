"""Undirected simple-graph representation audit, not anatomy validation."""
from routing import validate


def audit_topology(graph):
    if not graph:
        return {'vertices':0,'undirected_edges':0,'components':0,'isolated_vertices':0,'endpoints':0,'branch_vertices':0,'cycle_rank':0}
    node=next(iter(graph));validate(graph,node,node)
    neighbors={}
    for vertex,edges in graph.items():
        targets=[e.target for e in edges]
        if vertex in targets or len(set(targets))!=len(targets):
            raise ValueError('audit requires a simple graph without self edges or parallel edges')
        neighbors[vertex]=set(targets)
    for vertex,targets in neighbors.items():
        if any(vertex not in neighbors[target] for target in targets):
            raise ValueError('audit requires reciprocal adjacency')
    seen=set();components=0
    for vertex in graph:
        if vertex in seen:continue
        components+=1;stack=[vertex];seen.add(vertex)
        while stack:
            current=stack.pop()
            for target in neighbors[current]-seen:
                seen.add(target);stack.append(target)
    edge_count=sum(map(len,neighbors.values()))//2
    return {'vertices':len(graph),'undirected_edges':edge_count,'components':components,
            'isolated_vertices':sum(len(n)==0 for n in neighbors.values()),
            'endpoints':sum(len(n)==1 for n in neighbors.values()),
            'branch_vertices':sum(len(n)>2 for n in neighbors.values()),
            'cycle_rank':edge_count-len(graph)+components}
