"""Target-only monotone event robust bounds over supplied rectangular marginals."""
from payload import rational
from two_agent_allocation import interval

def uncertain_interval(probability_intervals,payloads,required):
    ranges=[tuple(map(rational,pair)) for pair in probability_intervals]
    if len(ranges) not in (1,2) or any(len(pair)!=2 for pair in ranges):raise ValueError('one/two pairs required')
    if any(not 0<=lo<=hi<=1 for lo,hi in ranges):raise ValueError('ordered probability ranges')
    payloads=list(map(rational,payloads));required=rational(required)
    lo=interval([a for a,b in ranges],payloads,required)
    hi=interval([b for a,b in ranges],payloads,required)
    return {'minimum':lo['minimum'],'maximum':hi['maximum'],'lower_endpoint_result':lo,'upper_endpoint_result':hi,
            'scope':'supplied rectangular marginal intervals plus arbitrary dependence; exact target-only model, not statistical confidence'}

def select_uncertain(menu,total_payload,required):
    total=rational(total_payload);required=rational(required)
    if not 0<required<=total:raise ValueError('budget/threshold')
    menu=list(menu)
    if not menu:raise ValueError('empty menu')
    results=[];seen=set()
    for name,ranges,w in menu:
        if not isinstance(name,str) or not name.strip() or name in seen:raise ValueError('unique nonempty labels')
        seen.add(name);w=list(map(rational,w))
        if sum(w)!=total:raise ValueError('unequal payload budget')
        results.append({'name':name,**uncertain_interval(ranges,w,required)})
    best=max(row['minimum'] for row in results)
    return {'results':results,'best_guaranteed_probability':best,'maximin_ties':[r['name'] for r in results if r['minimum']==best],
            'scope':'finite supplied menu, equal total payload only; no calibrated interval or physical guarantee'}
