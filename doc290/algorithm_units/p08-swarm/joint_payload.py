"""Exact explicitly supplied joint target-arrival distribution baseline."""
from fractions import Fraction as F
from payload import rational

def joint_payload(outcomes,masses,payloads,required_payload):
    ws=list(map(rational,payloads));probs=list(map(rational,masses));threshold=rational(required_payload)
    if not ws or not outcomes or len(outcomes)!=len(probs) or any(w<=0 for w in ws):raise ValueError('shape/payload')
    if any(p<0 for p in probs) or sum(probs)!=1:raise ValueError('joint masses must be nonnegative and sum exactly to one')
    if threshold<=0 or threshold>sum(ws):raise ValueError('invalid threshold')
    dist={};marginals=[F(0)]*len(ws);any_prob=F(0)
    for bits,p in zip(outcomes,probs):
        if len(bits)!=len(ws) or any(type(b) is not int or b not in (0,1) for b in bits):raise ValueError('outcomes require exact 0/1 integers')
        delivered=sum(w*b for w,b in zip(ws,bits));dist[delivered]=dist.get(delivered,F(0))+p
        if any(bits):any_prob+=p
        for j,b in enumerate(bits):marginals[j]+=b*p
    expectation=sum(d*p for d,p in dist.items());linear=sum(w*p for w,p in zip(ws,marginals))
    if expectation!=linear:raise RuntimeError('marginal expectation mismatch')
    return {'total_payload':sum(ws),'target_marginals':marginals,'expected_target_payload':expectation,
            'threshold_success_probability':sum(p for d,p in dist.items() if d>=threshold),
            'at_least_one_target_probability':any_prob,'target_payload_distribution':dist,
            'scope':'explicit joint target-arrival outcomes only; no inferred physical correlations, off-target joint outcome, energy or information budget'}
