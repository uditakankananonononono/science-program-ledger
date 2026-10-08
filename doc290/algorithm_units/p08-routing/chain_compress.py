"""Lossless undirected simple-graph degree-two chain representation.
No routing costs or physiological lengths are assigned.
"""
from topology_audit import audit_topology


def compress_chains(graph):
    audit=audit_topology(graph)
    neighbors={v:sorted(e.target for e in edges) for v,edges in graph.items()}
    anchors={v for v,ns in neighbors.items() if len(ns)!=2}
    seen_nodes=set()
    # Each pure cycle gets one deterministic anchor so it is not lost.
    for root in sorted(graph):
        if root in seen_nodes:continue
        stack=[root];component=set();seen_nodes.add(root)
        while stack:
            v=stack.pop();component.add(v)
            for u in neighbors[v]:
                if u not in seen_nodes:seen_nodes.add(u);stack.append(u)
        if not component & anchors:anchors.add(min(component))
    covered=set();chains=[]
    for start in sorted(anchors):
        for following in neighbors[start]:
            edge=frozenset((start,following))
            if edge in covered:continue
            path=[start,following];covered.add(edge)
            previous,current=start,following
            while current not in anchors:
                onward=next(v for v in neighbors[current] if v!=previous)
                edge=frozenset((current,onward))
                if edge in covered:raise AssertionError('unexpected reused chain edge')
                covered.add(edge);path.append(onward);previous,current=current,onward
            chains.append({'source':start,'target':current,'pixel_path':path,'edge_steps':len(path)-1})
    if len(covered)!=audit['undirected_edges']:raise AssertionError('edge coverage mismatch')
    return {'anchors':sorted(anchors),'chains':chains,'original_topology':audit,
            'scope':'pixel adjacency chain representation, not physiological length or calibrated routing costs'}
