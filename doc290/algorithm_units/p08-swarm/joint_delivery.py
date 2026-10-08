"""Exact caller-supplied ternary delivery outcomes, not physical safety."""
from fractions import Fraction as F
from payload import rational

def delivery(outcomes,masses,payloads,required_target,max_offtarget):
    ws=list(map(rational,payloads));ps=list(map(rational,masses));required=rational(required_target);cap=rational(max_offtarget)
    if not ws or not outcomes or len(outcomes)!=len(ps) or any(w<=0 for w in ws):raise ValueError('shape/payload')
    total=sum(ws)
    if required<=0 or required>total or cap<0 or cap>total:raise ValueError('invalid thresholds')
    if any(p<0 for p in ps) or sum(ps)!=1:raise ValueError('exact nonnegative normalized masses required')
    distribution={};marginals=[{'target':F(0),'offtarget':F(0),'lost':F(0)} for w in ws]
    for states,p in zip(outcomes,ps):
        if len(states)!=len(ws) or any(type(s) is not str or s not in ('target','offtarget','lost') for s in states):raise ValueError('explicit ternary states required')
        target=sum(w for w,s in zip(ws,states) if s=='target');off=sum(w for w,s in zip(ws,states) if s=='offtarget');lost=total-target-off
        key=(target,off,lost);distribution[key]=distribution.get(key,F(0))+p
        for m,s in zip(marginals,states):m[s]+=p
    expected={name:sum(key[i]*p for key,p in distribution.items()) for i,name in enumerate(('target','offtarget','lost'))}
    if sum(expected.values())!=total:raise RuntimeError('payload mass conservation failure')
    return {'total_payload':total,'marginals':marginals,'expected_payloads':expected,'joint_payload_distribution':distribution,
            'target_threshold_probability':sum(p for (t,o,l),p in distribution.items() if t>=required),
            'offtarget_exceedance_probability':sum(p for (t,o,l),p in distribution.items() if o>cap),
            'delivery_within_collateral_cap_probability':sum(p for (t,o,l),p in distribution.items() if t>=required and o<=cap),
            'scope':'explicit outcome probability model only; collateral cap is a supplied metric, not validated biological safety'}
