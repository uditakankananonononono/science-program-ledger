"""Exact rational support for restricted terminal constant-map reachability."""
from fractions import Fraction as F

def rational(x):
    if type(x) is int or type(x) is F:return F(x)
    if type(x) is str:return F(x)
    raise ValueError('use exact integer, Fraction or rational/decimal string; floats/bools refused')

def support(initial,dt,B,limit,slew,previous,direction,target):
    x=list(map(rational,initial));times=list(map(rational,dt));matrix=[list(map(rational,row)) for row in B]
    cap=list(map(rational,limit));rate=list(map(rational,slew));prev=list(map(rational,previous));v=list(map(rational,direction));y=list(map(rational,target))
    d=len(x);m=len(cap)
    if not d or not m or not times or len(matrix)!=d or any(len(row)!=m for row in matrix) or len(v)!=d or len(y)!=d or len(rate)!=m or len(prev)!=m:raise ValueError('shape')
    if any(t<=0 for t in times) or any(c<=0 for c in cap) or any(r<0 for r in rate) or any(abs(p)>c for p,c in zip(prev,cap)) or not any(v):raise ValueError('invalid bounds/direction')
    low=[];high=[];elapsed=F(0)
    for t in times:
        elapsed+=t;low.append([max(-c,p-r*elapsed) for c,p,r in zip(cap,prev,rate)]);high.append([min(c,p+r*elapsed) for c,p,r in zip(cap,prev,rate)])
    weights=[sum(v[a]*matrix[a][j] for a in range(d)) for j in range(m)]
    umin=[[lo[j] if weights[j]>=0 else hi[j] for j in range(m)] for lo,hi in zip(low,high)]
    umax=[[hi[j] if weights[j]>=0 else lo[j] for j in range(m)] for lo,hi in zip(low,high)]
    def projection(u):return sum(a*b for a,b in zip(v,x))+sum(t*sum(w*c for w,c in zip(weights,row)) for t,row in zip(times,u))
    lower=projection(umin);upper=projection(umax);requested=sum(a*b for a,b in zip(v,y))
    return {'min':lower,'max':upper,'target_projection':requested,'separates_target':requested<lower or requested>upper,
            'min_controls':umin,'max_controls':umax,'scope':'exact rational supplied model support only; nonseparation does not prove joint feasibility'}
