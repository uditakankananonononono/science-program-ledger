"""Bounded exact independent ternary convolution; no physical independence claim."""
from fractions import Fraction as F
from payload import rational

def independent_delivery(target_probabilities,offtarget_probabilities,payloads,required_target,max_offtarget,max_states=10000):
    p=list(map(rational,target_probabilities));q=list(map(rational,offtarget_probabilities));w=list(map(rational,payloads))
    required=rational(required_target);cap=rational(max_offtarget)
    if type(max_states) is not int or max_states<1:raise ValueError('max_states must be positive builtin integer')
    if not p or len(q)!=len(p) or len(w)!=len(p) or any(a<=0 for a in w):raise ValueError('shape/payload')
    if any(a<0 or b<0 or a+b>1 for a,b in zip(p,q)):raise ValueError('probabilities')
    total=sum(w)
    if required<=0 or required>total or cap<0 or cap>total:raise ValueError('thresholds')
    distribution={(F(0),F(0)):F(1)};peak=1
    for a,b,weight in zip(p,q,w):
        nxt={}
        for (target,off),mass in distribution.items():
            for key,prob in (((target+weight,off),a),((target,off+weight),b),((target,off),1-a-b)):
                if prob==0:continue
                if key not in nxt and len(nxt)>=max_states:raise RuntimeError('exact state budget exceeded; no truncated result')
                nxt[key]=nxt.get(key,F(0))+mass*prob
        if sum(nxt.values())!=1:raise RuntimeError('mass conservation failed')
        distribution=nxt;peak=max(peak,len(nxt))
    expected_target=sum(t*mass for (t,o),mass in distribution.items());expected_off=sum(o*mass for (t,o),mass in distribution.items())
    if expected_target!=sum(a*weight for a,weight in zip(p,w)) or expected_off!=sum(b*weight for b,weight in zip(q,w)):raise RuntimeError('expectation replay failed')
    return {'total_payload':total,'expected_target_payload':expected_target,'expected_offtarget_payload':expected_off,
            'target_threshold_probability':sum(mass for (t,o),mass in distribution.items() if t>=required),
            'offtarget_exceedance_probability':sum(mass for (t,o),mass in distribution.items() if o>cap),
            'delivery_within_collateral_cap_probability':sum(mass for (t,o),mass in distribution.items() if t>=required and o<=cap),
            'distribution_target_offtarget':distribution,'peak_states':peak,'max_states':max_states,
            'scope':'independent per-agent ternary outcomes assumed; bounded exact convolution, not physical safety'}
