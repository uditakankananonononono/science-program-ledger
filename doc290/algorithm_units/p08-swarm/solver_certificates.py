"""Floating equality-dual proposals converted to exact outer certificates."""
from itertools import product
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
from payload import rational
from dual_bounds import certify

def solver_certificates(p,q,w,required,cap):
    p=list(map(rational,p));q=list(map(rational,q));w=list(map(rational,w));required=rational(required);cap=rational(cap);n=len(p)
    if not 1<=n<=5 or len(q)!=n or len(w)!=n or any(a<=0 for a in w):raise ValueError('shape/N/payload')
    if any(a<0 or b<0 or a+b>1 for a,b in zip(p,q)) or not 0<required<=sum(w) or not 0<=cap<=sum(w):raise ValueError('marginals/thresholds')
    states=list(product((0,1,2),repeat=n));event=np.array([int(sum(a for a,s in zip(w,row) if s==1)>=required and sum(a for a,s in zip(w,row) if s==2)<=cap) for row in states],float)
    A=np.array([[1.]*len(states)]+[[float(row[j]==s) for row in states] for j in range(n) for s in (1,2)])
    rhs=np.array([1.]+[float(a) for pair in zip(p,q) for a in pair]);candidates=[];estimates={}
    for name,sign in (('minimum',1),('maximum',-1)):
        # No upper bound needed: nonnegative normalized masses imply <=1.
        r=linprog(sign*event,A_eq=A,b_eq=rhs,bounds=(0,None),method='highs')
        if not r.success:raise RuntimeError('candidate LP failed: '+r.message)
        dual=np.asarray(r.eqlin.marginals,float)
        if dual.shape!=(1+2*n,) or not np.isfinite(dual).all() or not np.isfinite(r.fun):raise RuntimeError('nonfinite/malformed candidate')
        # Maximization is solved as minimum -event, so equality multiplier sign flips.
        candidates.append([F.from_float(float(sign*a)) for a in dual]);estimates[name]=float(sign*r.fun)
    certificate=certify(p,q,w,required,cap,*candidates)
    return {'certificate':certificate,'floating_solver_estimates':estimates,
            'candidate_conversion':'exact binary-float Fraction, no denominator rounding',
            'scope':'solver candidates independently exact-verified as outer bounds; estimates not exact extrema or physical probabilities'}
