"""Pinned synthetic algebra map-to-schedule fixture, not hardware instance."""
import numpy as np
from gradient_structure import construct,check
from mobility_map import assemble
from feasibility import solve

def run():
    # Each matrix symmetric trace-free, with first field-component column
    # aligned to a distinct force axis for moment [1,0,0]. All arbitrary units.
    G=construct([[1,0,0,0,0],[0,0,1,0,0],[0,0,0,1,0]])
    if not check(G)['passes_local_structure']:raise RuntimeError('synthetic gradient structure failure')
    mapping=assemble([1,0,0],G,np.diag([1.,2.,3.]))
    B=np.array(mapping['velocity_per_current'])
    target=np.array([1.,2.,3.]);dt=np.array([1.,1.])
    schedule=solve([0,0,0],target,dt,B,[.5,.5,.5],[1,1,1],[0,0,0])
    if schedule['status']!='primal_checked':raise RuntimeError('synthetic schedule failed')
    # Replay force and mobility separately from the planner velocity map.
    position=np.zeros(3);u=np.array(schedule['controls']);L=np.diag([1.,2.,3.]);m=np.array([1.,0,0])
    for t,current in zip(dt,u):
        field_gradient=G@current;force=field_gradient@m;position+=t*(L@force)
    residual=float(np.max(abs(position-target)))
    if not np.isfinite(residual) or residual>1e-8:raise RuntimeError('separate force replay failed')
    return {'scope':'synthetic integration fixture with arbitrary units; no hardware admission',
            'gradient_coefficients':[[1,0,0,0,0],[0,0,1,0,0],[0,0,0,1,0]],
            'moment':[1,0,0],'mobility_diagonal':[1,2,3],'target':target.tolist(),'dt':dt.tolist(),
            'schedule':schedule,'independent_force_replay_terminal':position.tolist(),'replay_max_abs_error':residual}

if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2,allow_nan=False))
