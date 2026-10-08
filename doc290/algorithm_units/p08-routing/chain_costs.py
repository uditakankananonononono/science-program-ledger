"""Serialize existing directed costs on topological chains. No cost inference."""
from chain_compress import compress_chains


def serialize_chain_costs(graph):
    result=compress_chains(graph)
    lookup={v:{e.target:e for e in edges} for v,edges in graph.items()}
    for chain in result['chains']:
        path=chain['pixel_path']
        directions=[]
        for sequence in (path,list(reversed(path))):
            steps=[]
            for a,b in zip(sequence,sequence[1:]):
                e=lookup[a][b]
                steps.append({'source':a,'target':b,'time':e.time,'exposure':e.exposure,
                              'scenario_times':list(e.scenario_times)})
            directions.append({'source':sequence[0],'target':sequence[-1],'steps':steps})
        chain['directions']=directions
    result['scope']='topological pixel paths plus original directed per-step costs; not aggregated routing input or physiology'
    return result
