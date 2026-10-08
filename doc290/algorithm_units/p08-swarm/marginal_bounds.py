"""Small-N LP bounds over arbitrary ternary dependence, supplied marginals."""
from itertools import product
import numpy as np
from scipy.optimize import linprog
from payload import rational

def bounds(target_probabilities,offtarget_probabilities,payloads,required_target,max_offtarget,tolerance=1e-8):
    p=list(map(rational,target_probabilities));q=list(map(rational,offtarget_probabilities));w=list(map(rational,payloads))
    n=len(p);required=rational(required_target);cap=rational(max_offtarget)
    if n<1 or n>5 or len(q)!=n or len(w)!=n:raise ValueError('N must be 1..5 with matching arrays')
    if any(a<0 or b<0 or a+b>1 for a,b in zip(p,q)) or any(a<=0 for a in w):raise ValueError('invalid marginals/payload')
    if required<=0 or required>sum(w) or cap<0 or cap>sum(w):raise ValueError('thresholds')
    if isinstance(tolerance,(bool,np.bool_,str)) or not np.isscalar(tolerance) or not np.isfinite(tolerance) or tolerance<=0:raise ValueError('tolerance')
    # 0 lost, 1 target, 2 off-target. Metric event computed in exact rational units.
    states=list(product((0,1,2),repeat=n));event=np.array([int(sum(a for a,s in zip(w,row) if s==1)>=required and sum(a for a,s in zip(w,row) if s==2)<=cap) for row in states],float)
    A=np.array([[1.]*len(states)]+[[float(row[j]==s) for row in states] for j in range(n) for s in (1,2)])
    rhs=np.array([1.]+[float(a) for pair in zip(p,q) for a in pair]);outputs={}
    for name,sign in (('minimum',1),('maximum',-1)):
        r=linprog(sign*event,A_eq=A,b_eq=rhs,bounds=(0,1),method='highs')
        if not r.success:raise RuntimeError('bound LP failed: '+r.message)
        mass=np.asarray(r.x,float)
        if mass.shape!=(len(states),) or not np.isfinite(mass).all():raise RuntimeError('invalid LP mass')
        prob=float(event@mass);residual=float(np.max(abs(A@mass-rhs)));negative=float(max(0,-np.min(mass)));above=float(max(0,np.max(mass)-1))
        if not np.isfinite([prob,residual,negative,above]).all() or residual>tolerance or negative>tolerance or above>tolerance or prob<0 or prob>1:raise RuntimeError('bound primal readback failed')
        outputs[name]={'probability':prob,'mass':mass.tolist(),'marginal_residual':residual,'negative_mass_violation':negative,'above_one_mass_violation':above}
    if outputs['minimum']['probability']>outputs['maximum']['probability']+tolerance:raise RuntimeError('bound ordering failed')
    return {'states':states,'event':event.tolist(),'bounds':outputs,'scope':'floating LP claimed extrema with checked primal distributions; no independently checked dual optimality certificate or physical marginals'}
