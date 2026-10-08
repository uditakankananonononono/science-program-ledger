"""Exact candidate integral witness lift under independent actuator slew constraints."""
from fractions import Fraction as F
from rational_support import rational

def lift(dt,limit,slew,previous,integrals):
    times=list(map(rational,dt));cap=list(map(rational,limit));rate=list(map(rational,slew));prev=list(map(rational,previous));z=list(map(rational,integrals));m=len(cap)
    if not times or not m or any(len(a)!=m for a in (rate,prev,z)):raise ValueError('shape')
    if any(t<=0 for t in times) or any(c<=0 for c in cap) or any(r<0 for r in rate) or any(abs(p)>c for p,c in zip(prev,cap)):raise ValueError('invalid bounds')
    low=[];high=[];elapsed=F(0)
    for t in times:
        elapsed+=t;low.append([max(-c,p-r*elapsed) for c,p,r in zip(cap,prev,rate)]);high.append([min(c,p+r*elapsed) for c,p,r in zip(cap,prev,rate)])
    lower=[sum(t*row[j] for t,row in zip(times,low)) for j in range(m)];upper=[sum(t*row[j] for t,row in zip(times,high)) for j in range(m)]
    if any(a<l or a>h for a,l,h in zip(z,lower,upper)):raise ValueError('candidate integral outside exact interval')
    mix=[F(0) if h==l else (a-l)/(h-l) for a,l,h in zip(z,lower,upper)]
    u=[[(1-w)*l+w*h for w,l,h in zip(mix,lo,hi)] for lo,hi in zip(low,high)]
    replay=[sum(t*row[j] for t,row in zip(times,u)) for j in range(m)]
    old=prev
    for t,row in zip(times,u):
        if any(abs(a)>c or abs(a-p)>r*t for a,c,p,r in zip(row,cap,old,rate)):raise RuntimeError('exact witness bound violation')
        old=row
    if replay!=z:raise RuntimeError('exact integral replay failed')
    return {'controls':u,'replayed_integrals':replay,'lower_integrals':lower,'upper_integrals':upper,'mixing_weights':mix,
            'scope':'candidate integral lift only; no search for joint terminal target or physical admission'}
