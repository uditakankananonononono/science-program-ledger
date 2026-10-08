"""Reduced constant-map terminal LP. No corridor/coupled constraints."""
import numpy as np
from scipy.optimize import linprog

def solve_reduced(initial,target,dt,B,limit,slew,previous,tolerance=1e-8):
    x=np.asarray(initial,float);y=np.asarray(target,float);times=np.asarray(dt,float);B=np.asarray(B,float)
    cap=np.asarray(limit,float);rate=np.asarray(slew,float);prev=np.asarray(previous,float)
    if x.ndim!=1 or not x.size or y.shape!=x.shape or B.ndim!=2 or B.shape[0]!=x.size or not B.shape[1]:raise ValueError('state/map shape')
    m=B.shape[1]
    if times.ndim!=1 or not times.size or any(a.shape!=(m,) for a in (cap,rate,prev)):raise ValueError('bounds/time shape')
    if not all(np.isfinite(a).all() for a in (x,y,times,B,cap,rate,prev)):raise ValueError('nonfinite')
    if (times<=0).any() or (cap<=0).any() or (rate<0).any() or (abs(prev)>cap).any():raise ValueError('invalid bounds')
    if isinstance(tolerance,(bool,np.bool_,str)) or not np.isscalar(tolerance) or not np.isfinite(tolerance) or tolerance<=0:raise ValueError('invalid tolerance')
    with np.errstate(over='raise',invalid='raise'):
        elapsed=np.cumsum(times);low=np.maximum(-cap,prev-elapsed[:,None]*rate);high=np.minimum(cap,prev+elapsed[:,None]*rate)
        lower=times@low;upper=times@high
    if not np.isfinite(lower).all() or not np.isfinite(upper).all():raise ValueError('interval overflow')
    result=linprog(np.zeros(m),A_eq=B,b_eq=y-x,bounds=list(zip(lower,upper)),method='highs')
    if result.status==2:return {'status':'solver_infeasible','certificate':'no independent dual certificate'}
    if not result.success:raise RuntimeError(result.message)
    z=np.asarray(result.x,float)
    if z.shape!=(m,) or not np.isfinite(z).all():raise RuntimeError('invalid integral solver output')
    if (z<lower-tolerance).any() or (z>upper+tolerance).any():raise RuntimeError('integral bounds failed')
    # Solver near-boundary excursion is explicitly clamped; replay must still pass.
    clipped=np.clip(z,lower,upper);width=upper-lower;mix=np.zeros(m)
    np.divide(clipped-lower,width,out=mix,where=width!=0)
    controls=(1-mix)*low+mix*high
    with np.errstate(over='raise',invalid='raise'):
        paths=np.vstack([x,x+np.cumsum(times[:,None]*(controls@B.T),axis=0)])
        replay=times@controls;changes=np.diff(np.vstack([prev,controls]),axis=0)
        residuals={'terminal':float(np.max(abs(paths[-1]-y))),'integral_replay':float(np.max(abs(replay-clipped))),
                   'actuator':float(max(0,np.max(abs(controls)-cap))),'slew':float(max(0,np.max(abs(changes)-times[:,None]*rate))),
                   'solver_integral_clamp':float(np.max(abs(z-clipped)))}
    if not np.isfinite(controls).all() or not np.isfinite(paths).all() or not np.isfinite(list(residuals.values())).all() or max(residuals.values())>tolerance:raise RuntimeError('primal lift failed')
    return {'status':'primal_checked','controls':controls.tolist(),'trajectory':paths.tolist(),'integrals':clipped.tolist(),'residuals':residuals,
            'lp_variables':m,'scope':'constant-map independent control/slew terminal-only reduction; not novelty or speed claim'}
