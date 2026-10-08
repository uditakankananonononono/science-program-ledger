"""Exact adjacency graph of supplied binary pixels, not vessel skeletonization."""
from routing import Edge,validate


def mask_to_graph(mask, connectivity, time, exposure, scenario_times=()):
    """Create bidirectional edges between selected neighboring foreground pixels.

    Caller supplies every cost. Pixel IDs are row,column. No skeletonization,
    anatomical flow inference, branch compression or diagonal correction.
    8-neighbor edges have the same supplied costs as 4-neighbor edges.
    """
    if type(connectivity) is not int or connectivity not in (4,8):
        raise ValueError('connectivity must be integer 4 or 8')
    if not isinstance(mask,list) or not mask or not all(isinstance(row,list) and row for row in mask):
        raise ValueError('mask must be a nonempty rectangular list of lists')
    width=len(mask[0])
    if any(len(row)!=width for row in mask):raise ValueError('ragged mask')
    if any(type(v) is not int or v not in (0,1) for row in mask for v in row):
        raise ValueError('mask entries must be integer 0 or 1')
    if not isinstance(scenario_times,tuple):raise ValueError('scenario_times must be a tuple')
    # Validate cost values even if the mask contains no edges or foreground.
    validate({'a':[Edge('b',time,exposure,scenario_times)],'b':[]},'a','b')
    foreground={(r,c) for r,row in enumerate(mask) for c,v in enumerate(row) if v==1}
    steps=[(-1,0),(0,-1),(0,1),(1,0)]
    if connectivity==8:steps += [(-1,-1),(-1,1),(1,-1),(1,1)]
    graph={}
    for r,c in sorted(foreground):
        graph[f'{r},{c}']=[Edge(f'{r+dr},{c+dc}',time,exposure,scenario_times)
                          for dr,dc in steps if (r+dr,c+dc) in foreground]
    return graph


def graph_payload(graph):
    """Serialize an extracted graph to the runner's graph field."""
    return {v:[{'target':e.target,'time':e.time,'exposure':e.exposure,
                'scenario_times':list(e.scenario_times)} for e in edges] for v,edges in graph.items()}
