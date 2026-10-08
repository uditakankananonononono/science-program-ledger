"""Exact rational marginal-event dual certificate checks, supplied candidates."""
from itertools import product
from fractions import Fraction as F
from payload import rational

def certify(p,q,w,required,cap,lower_candidate,upper_candidate):
    p=list(map(rational,p));q=list(map(rational,q));w=list(map(rational,w));required=rational(required);cap=rational(cap);n=len(p)
    if not 1<=n<=5 or len(q)!=n or len(w)!=n or any(a<=0 for a in w):raise ValueError('shape/N/payload')
    if any(a<0 or b<0 or a+b>1 for a,b in zip(p,q)) or not 0<required<=sum(w) or not 0<=cap<=sum(w):raise ValueError('probability/threshold')
    lower=list(map(rational,lower_candidate));upper=list(map(rational,upper_candidate))
    if len(lower)!=1+2*n or len(upper)!=1+2*n:raise ValueError('dual shape')
    rhs=[F(1)]+[a for pair in zip(p,q) for a in pair];rows=[];events=[];independent=F(0)
    for states in product((0,1,2),repeat=n):
        row=[F(1)]+[F(int(states[j]==s)) for j in range(n) for s in (1,2)]
        event=F(int(sum(a for a,s in zip(w,states) if s==1)>=required and sum(a for a,s in zip(w,states) if s==2)<=cap))
        mass=F(1)
        for a,b,s in zip(p,q,states):mass*= (1-a-b,a,b)[s]
        independent+=mass*event;rows.append(row);events.append(event)
    dot=lambda a,b:sum(x*y for x,y in zip(a,b))
    # Every outcome normalization coefficient equals one, so shifting lambda0
    # makes each candidate globally dual-feasible for all nonnegative masses.
    lower_shift=max(F(0),max(dot(row,lower)-c for row,c in zip(rows,events)))
    upper_shift=max(F(0),max(c-dot(row,upper) for row,c in zip(rows,events)))
    lower[0]-=lower_shift;upper[0]+=upper_shift
    if any(dot(row,lower)>c or dot(row,upper)<c for row,c in zip(rows,events)):raise RuntimeError('exact dual verification failed')
    lo=dot(rhs,lower);hi=dot(rhs,upper)
    if not lo<=independent<=hi:raise RuntimeError('exact witness does not fit dual brackets')
    return {'certified_lower_on_minimum':lo,'certified_upper_on_maximum':hi,'independent_feasible_probability':independent,
            'lower_dual':lower,'upper_dual':upper,'lower_normalization_shift':lower_shift,'upper_normalization_shift':upper_shift,
            'scope':'exact supplied marginal-event model outer bounds; not necessarily tight, no physical probability guarantee'}
