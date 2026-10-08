"""Exact supplied primal joint witness and dual-gap checks."""
from fractions import Fraction as F
from payload import rational
from dual_bounds import certify

def verify(p,q,w,required,cap,outcomes,masses,lower_candidate,upper_candidate):
    p=list(map(rational,p));q=list(map(rational,q));w=list(map(rational,w));required=rational(required);cap=rational(cap)
    # Dual checker validates the model and candidates independently.
    certificate=certify(p,q,w,required,cap,lower_candidate,upper_candidate)
    ps=list(map(rational,masses));n=len(p)
    if not outcomes or len(outcomes)!=len(ps) or any(a<0 for a in ps) or sum(ps)!=1:raise ValueError('exact normalized nonnegative witness required')
    observed_p=[F(0)]*n;observed_q=[F(0)]*n;prob=F(0)
    for states,mass in zip(outcomes,ps):
        if len(states)!=n or any(type(s) is not int or s not in (0,1,2) for s in states):raise ValueError('integer states 0 lost, 1 target, 2 offtarget required')
        for j,s in enumerate(states):observed_p[j]+=mass*(s==1);observed_q[j]+=mass*(s==2)
        if sum(a for a,s in zip(w,states) if s==1)>=required and sum(a for a,s in zip(w,states) if s==2)<=cap:prob+=mass
    if observed_p!=p or observed_q!=q:raise ValueError('witness marginals not exact declared marginals')
    lo=certificate['certified_lower_on_minimum'];hi=certificate['certified_upper_on_maximum']
    if not lo<=prob<=hi:raise RuntimeError('primal dual contradiction')
    return {'verified_witness_probability':prob,'certificate':certificate,'gap_to_minimum_lower':prob-lo,'gap_to_maximum_upper':hi-prob,
            'minimum_exactly_certified':prob==lo,'maximum_exactly_certified':prob==hi,
            'scope':'gap closure only for supplied rational marginal-event model and exact feasible witness; no physical validity'}
