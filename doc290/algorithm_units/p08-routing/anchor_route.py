"""Enforced integer-cost, anchor-only, turn-free chain routing wrapper."""
from chain_aggregate import aggregate_chains,expand_route
from routing import exposure_budget_route,scenario_robust_route,budgeted_scenario_route


def route_integer_anchors(graph,start,goal,method,budget=None):
    if method not in ('budget','scenario','budget-scenario'):
        raise ValueError('unsupported objective; turn rules not supported')
    for edges in graph.values():
        for e in edges:
            if any(type(x) is not int for x in (e.time,e.exposure,*e.scenario_times)):
                raise ValueError('wrapper requires integer costs, not floats or booleans')
    if method=='scenario':
        if budget is not None:raise ValueError('scenario objective does not accept budget')
    elif type(budget) is not int or budget<0:
        raise ValueError('budget must be nonnegative integer')
    compressed,witnesses=aggregate_chains(graph)
    if start not in compressed or goal not in compressed:
        raise ValueError('endpoints must be compression anchors')
    if method=='budget':result=exposure_budget_route(compressed,start,goal,budget)
    elif method=='scenario':result=scenario_robust_route(compressed,start,goal)
    else:result=budgeted_scenario_route(compressed,start,goal,budget)
    return {'compressed_result':result,'expanded_pixel_path':expand_route(result,witnesses),
            'scope':'integer-cost anchor-only turn-free routing; fixture-tested, not arbitrary-graph proof or physiological validation'}
