"""Explicit mask JSON CLI. No automatic physiological attributes or endpoints."""
import argparse,json,sys
from mask_graph import mask_to_graph,graph_payload
from runner import fields,solve,unique_object,reject_constant


def solve_mask(payload):
    fields(payload,('mask','connectivity','costs','query'))
    fields(payload['costs'],('time','exposure'),('scenario_times',))
    fields(payload['query'],('method','start','goal'),('budget','forbidden','penalties'))
    costs=payload['costs']
    scenarios=costs.get('scenario_times',[])
    if not isinstance(scenarios,list):raise ValueError('scenario_times must be a list')
    graph=mask_to_graph(payload['mask'],payload['connectivity'],costs['time'],costs['exposure'],tuple(scenarios))
    query=dict(payload['query']);query['graph']=graph_payload(graph)
    result=solve(query)
    result['input_scope']='supplied binary-mask adjacency, not vessel skeletonization or anatomy calibration'
    result['topology']={'vertices':len(graph),'directed_edges':sum(map(len,graph.values())),
                        'connectivity':payload['connectivity'],'diagonal_cost_correction':False}
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',help='mask JSON path, or - for stdin')
    args=parser.parse_args()
    try:
        if args.input=='-':raw=sys.stdin.read()
        else:
            with open(args.input,encoding='utf-8') as f:raw=f.read()
        payload=json.loads(raw,object_pairs_hook=unique_object,parse_constant=reject_constant)
        print(json.dumps(solve_mask(payload),allow_nan=False,sort_keys=True))
        return 0
    except (ValueError,TypeError,OverflowError,OSError,RecursionError) as exc:
        print(json.dumps({'status':'error','error':str(exc)}),file=sys.stderr)
        return 2

if __name__=='__main__':sys.exit(main())
