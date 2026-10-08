"""Shared schedule for enumerated linear actuator maps; established scenario LP."""
import numpy as np
from scipy.optimize import linprog

def minimax_terminal(initial,dt,maps,limit,slew,previous,targets,tolerance=1e-8):
    x=np.asarray(initial,float);dt=np.asarray(dt,float);Bs=np.asarray(maps,float)
    limit=np.asarray(limit,float);slew=np.asarray(slew,float);previous=np.asarray(previous,float)
    lo=np.asarray(targets,float);hi=lo.copy()
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
    A=np.column_stack((np.array(rows),np.zeros(len(rows))))
    A[2*n*m:,-1]=-1
    objective=np.zeros(n*m+1);objective[-1]=1
    result=linprog(objective,A_ub=A,b_ub=np.array(rhs),bounds=[(-limit[j],limit[j]) for k in range(n) for j in range(m)]+[(0,None)],method='highs')
    if result.status==2:return {'status':'solver_infeasible','certificate':'no independently checked dual certificate'}
    if not result.success:raise RuntimeError(result.message)
    u=result.x[:-1].reshape(n,m);error_bound=float(result.x[-1]);paths=np.array([np.vstack((x,x+np.cumsum(dt[:,None]*(u@B.T),axis=0))) for B in Bs])
    change=np.diff(np.vstack((previous,u)),axis=0)
    residuals={'actuator_violation':float(max(0,np.max(abs(u)-limit))),
               'slew_violation':float(max(0,np.max(abs(change)-dt[:,None]*slew))),
               'terminal_box_violation_per_scenario':[float(max(0,np.max(l-path[-1]),np.max(path[-1]-h))) for path,l,h in zip(paths,lo,hi)]}
    actual=max(residuals['terminal_box_violation_per_scenario'])
    residuals['objective_readback_abs']=abs(actual-error_bound)
    if residuals['objective_readback_abs']>tolerance:raise RuntimeError('objective readback failed')
    if not np.isfinite(paths).all() or not np.isfinite(u).all() or max([residuals['actuator_violation'],residuals['slew_violation']])>tolerance:raise RuntimeError('primal readback failed')
    return {'status':'primal_checked','controls':u.tolist(),'worst_terminal_coordinate_error':actual,'solver_error_bound':error_bound,'scenario_trajectories':paths.tolist(),'residuals':residuals,
            'scope':'finite-scenario LP minimax terminal error; no independently checked dual optimality certificate'}
