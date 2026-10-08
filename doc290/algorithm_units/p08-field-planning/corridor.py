"""Abstract linear actuator schedule LP baseline, not magnetic field simulation."""
import numpy as np
from scipy.optimize import linprog

def solve_corridor(initial,target,dt,actuation,limit,slew,previous,lower,upper,tolerance=1e-8):
    initial=np.asarray(initial,float);target=np.asarray(target,float);dt=np.asarray(dt,float)
    B=np.asarray(actuation,float);limit=np.asarray(limit,float);slew=np.asarray(slew,float);previous=np.asarray(previous,float)
    if initial.ndim!=1 or not initial.size or target.shape!=initial.shape:raise ValueError('state/target shape')
    if B.ndim!=2 or B.shape[0]!=len(initial) or B.shape[1]==0:raise ValueError('actuation shape')
    m=B.shape[1]
    if dt.ndim!=1 or not len(dt) or limit.shape!=(m,) or slew.shape!=(m,) or previous.shape!=(m,):raise ValueError('schedule/bound shape')
    if not all(np.isfinite(a).all() for a in (initial,target,dt,B,limit,slew,previous)):raise ValueError('nonfinite input')
    if (dt<=0).any() or (limit<=0).any() or (slew<0).any() or (np.abs(previous)>limit).any():raise ValueError('invalid bounds')
    if not np.isscalar(tolerance) or not np.isfinite(tolerance) or tolerance<=0:raise ValueError('invalid tolerance')
    n=len(dt);Aeq=np.hstack([d*B for d in dt]);rhs=target-initial;rows=[];bounds=[]
    for k in range(n):
        for j in range(m):
            row=np.zeros(n*m);row[k*m+j]=1
            if k:row[(k-1)*m+j]=-1
            offset=previous[j] if k==0 else 0.
            rows.extend([row,-row]);bounds.extend([slew[j]*dt[k]+offset,slew[j]*dt[k]-offset])
    lower=np.asarray(lower,float);upper=np.asarray(upper,float)
    if lower.shape!=(n+1,len(initial)) or upper.shape!=lower.shape:raise ValueError('corridor shape')
    if not np.isfinite(lower).all() or not np.isfinite(upper).all() or (lower>upper).any():raise ValueError('invalid corridor')
    # Initial node is fixed, so reject its corridor incompatibility explicitly.
    if (initial<lower[0]-tolerance).any() or (initial>upper[0]+tolerance).any():
        return {'status':'initial_node_outside_corridor','certificate':'fixed initial state violates node box beyond tolerance'}
    for k in range(1,n+1):
        prefix=np.zeros((len(initial),n*m));prefix[:,:k*m]=np.hstack([d*B for d in dt[:k]])
        rows.extend(prefix);bounds.extend(upper[k]-initial)
        rows.extend(-prefix);bounds.extend(initial-lower[k])
    result=linprog(np.zeros(n*m),A_ub=np.array(rows),b_ub=np.array(bounds),A_eq=Aeq,b_eq=rhs,
                   bounds=[(-limit[j],limit[j]) for k in range(n) for j in range(m)],method='highs')
    if result.status==2:return {'status':'solver_infeasible','solver_message':result.message,'certificate':'no independently verified dual certificate'}
    if not result.success:raise RuntimeError(result.message)
    u=result.x.reshape(n,m);trajectory=np.vstack([initial,initial+np.cumsum(dt[:,None]*(u@B.T),axis=0)])
    increments=np.diff(np.vstack([previous,u]),axis=0)
    residuals={'terminal_max_abs':float(np.max(np.abs(trajectory[-1]-target))),
               'actuator_bound_violation':float(max(0,np.max(np.abs(u)-limit))),
               'slew_bound_violation':float(max(0,np.max(np.abs(increments)-dt[:,None]*slew)))}
    residuals['node_corridor_violation']=float(max(0,np.max(lower-trajectory),np.max(trajectory-upper)))
    if not all(np.isfinite(a).all() for a in (u,trajectory)) or max(residuals.values())>tolerance:raise RuntimeError('primal readback failed')
    return {'status':'primal_checked','controls':u.tolist(),'trajectory':trajectory.tolist(),'residuals':residuals,
            'scope':'discrete node-box constrained linear integrator; not continuous safety, anatomy, or hardware validation'}
