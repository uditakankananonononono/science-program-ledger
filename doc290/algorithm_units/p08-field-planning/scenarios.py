"""Shared schedule for enumerated linear actuator maps; established scenario LP."""
import numpy as np
from scipy.optimize import linprog

def solve_scenarios(initial,dt,maps,limit,slew,previous,terminal_lower,terminal_upper,tolerance=1e-8):
    x=np.asarray(initial,float);dt=np.asarray(dt,float);Bs=np.asarray(maps,float)
    limit=np.asarray(limit,float);slew=np.asarray(slew,float);previous=np.asarray(previous,float)
    lo=np.asarray(terminal_lower,float);hi=np.asarray(terminal_upper,float)
    if x.ndim!=1 or not x.size or dt.ndim!=1 or not dt.size:raise ValueError('state/time shape')
    if Bs.ndim!=3 or not Bs.shape[0] or Bs.shape[1]!=x.size or not Bs.shape[2]:raise ValueError('map shape')
    s,d,m=Bs.shape;n=dt.size
    if any(a.shape!=(m,) for a in (limit,slew,previous)) or lo.shape!=(s,d) or hi.shape!=lo.shape:raise ValueError('bound shape')
    if not all(np.isfinite(a).all() for a in (x,dt,Bs,limit,slew,previous,lo,hi)):raise ValueError('nonfinite input')
    if (dt<=0).any() or (limit<=0).any() or (slew<0).any() or (abs(previous)>limit).any() or (lo>hi).any():raise ValueError('invalid bounds')
    if isinstance(tolerance,(bool,np.bool_,str)) or not np.isscalar(tolerance) or not np.isfinite(tolerance) or tolerance<=0:raise ValueError('invalid tolerance')
    rows=[];rhs=[]
    for k in range(n):
        for j in range(m):
            a=np.zeros(n*m);a[k*m+j]=1
            if k:a[(k-1)*m+j]=-1
            offset=previous[j] if k==0 else 0.
            rows.extend((a,-a));rhs.extend((slew[j]*dt[k]+offset,slew[j]*dt[k]-offset))
    for B,l,h in zip(Bs,lo,hi):
        terminal=np.hstack([t*B for t in dt]);rows.extend(terminal);rhs.extend(h-x);rows.extend(-terminal);rhs.extend(x-l)
    result=linprog(np.zeros(n*m),A_ub=np.array(rows),b_ub=np.array(rhs),bounds=[(-limit[j],limit[j]) for k in range(n) for j in range(m)],method='highs')
    if result.status==2:return {'status':'solver_infeasible','certificate':'no independently checked dual certificate'}
    if not result.success:raise RuntimeError(result.message)
    u=result.x.reshape(n,m);paths=np.array([np.vstack((x,x+np.cumsum(dt[:,None]*(u@B.T),axis=0))) for B in Bs])
    change=np.diff(np.vstack((previous,u)),axis=0)
    residuals={'actuator_violation':float(max(0,np.max(abs(u)-limit))),
               'slew_violation':float(max(0,np.max(abs(change)-dt[:,None]*slew))),
               'terminal_box_violation_per_scenario':[float(max(0,np.max(l-path[-1]),np.max(path[-1]-h))) for path,l,h in zip(paths,lo,hi)]}
    if not np.isfinite(paths).all() or not np.isfinite(u).all() or max([residuals['actuator_violation'],residuals['slew_violation']]+residuals['terminal_box_violation_per_scenario'])>tolerance:raise RuntimeError('primal readback failed')
    return {'status':'primal_checked','controls':u.tolist(),'scenario_trajectories':paths.tolist(),'residuals':residuals,
            'scope':'one shared schedule for enumerated constant maps only; no unlisted uncertainty or hardware guarantee'}
