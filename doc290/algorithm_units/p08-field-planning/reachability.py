"""Analytic support bounds for a constant-map terminal reachable set."""
import numpy as np

def projection_bounds(initial,dt,actuation,limit,slew,previous,direction):
    x=np.asarray(initial,float);dt=np.asarray(dt,float);B=np.asarray(actuation,float)
    limit=np.asarray(limit,float);slew=np.asarray(slew,float);previous=np.asarray(previous,float);v=np.asarray(direction,float)
    if x.ndim!=1 or not len(x) or v.shape!=x.shape or B.ndim!=2 or B.shape[0]!=len(x) or not B.shape[1]:raise ValueError('state/map/direction shape')
    m=B.shape[1]
    if dt.ndim!=1 or not len(dt) or any(a.shape!=(m,) for a in (limit,slew,previous)):raise ValueError('time/bounds shape')
    if not all(np.isfinite(a).all() for a in (x,dt,B,limit,slew,previous,v)):raise ValueError('nonfinite input')
    if (dt<=0).any() or (limit<=0).any() or (slew<0).any() or (abs(previous)>limit).any() or not np.any(v):raise ValueError('invalid bounds/direction')
    with np.errstate(over='raise',invalid='raise'):
        t=np.cumsum(dt);upper=np.minimum(limit,previous+t[:,None]*slew);lower=np.maximum(-limit,previous-t[:,None]*slew)
        weights=v@B
        umax=np.where(weights>=0,upper,lower);umin=np.where(weights>=0,lower,upper)
        base=float(v@x);high=base+float(np.sum(dt[:,None]*(umax*weights)));low=base+float(np.sum(dt[:,None]*(umin*weights)))
    if not np.isfinite([low,high]).all() or not np.isfinite(umax).all() or not np.isfinite(umin).all():raise ValueError('support overflow')
    return {'projection_min':low,'projection_max':high,'minimizing_controls':umin.tolist(),'maximizing_controls':umax.tolist(),
            'scope':'terminal support for fixed constant map and independent componentwise control/slew only; no joint target feasibility from finite directions'}
