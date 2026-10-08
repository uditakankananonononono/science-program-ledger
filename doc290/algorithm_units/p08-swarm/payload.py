"""Exact independent Bernoulli payload baseline, not swarm physics."""
from fractions import Fraction as F

def rational(value):
    if type(value) in (int,F,str):return F(value)
    raise ValueError('exact rational data required; floats/bools refused')

def independent_payload(target_probabilities,offtarget_probabilities,payloads,required_payload):
    ps=list(map(rational,target_probabilities));qs=list(map(rational,offtarget_probabilities));ws=list(map(rational,payloads));threshold=rational(required_payload)
    if not ps or len(qs)!=len(ps) or len(ws)!=len(ps):raise ValueError('shape')
    if any(p<0 or q<0 or p+q>1 for p,q in zip(ps,qs)) or any(w<=0 for w in ws):raise ValueError('invalid probability/payload')
    total=sum(ws)
    if threshold<=0 or threshold>total:raise ValueError('threshold must lie in (0,total payload]')
    # Exact delivered-payload distribution under target-arrival independence.
    distribution={F(0):F(1)}
    for p,w in zip(ps,ws):
        next_distribution={}
        for delivered,mass in distribution.items():
            next_distribution[delivered]=next_distribution.get(delivered,F(0))+mass*(1-p)
            next_distribution[delivered+w]=next_distribution.get(delivered+w,F(0))+mass*p
        distribution=next_distribution
    if sum(distribution.values())!=1:raise RuntimeError('probability conservation')
    return {'total_payload':total,'required_payload':threshold,
            'expected_target_payload':sum(p*w for p,w in zip(ps,ws)),
            'expected_offtarget_payload':sum(q*w for q,w in zip(qs,ws)),
            'threshold_success_probability':sum(mass for delivered,mass in distribution.items() if delivered>=threshold),
            'at_least_one_target_probability':1-distribution[F(0)],'target_payload_distribution':distribution,
            'scope':'exact independent target-arrival model only; no coordination, correlated failures, energy or information-budget guarantee'}
