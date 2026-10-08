"""Synthetic local source-free magnetostatic gradient structure, not coil calibration."""
import numpy as np

def construct(coefficients):
    """Five coefficients per actuator: xx, yy, xy, xz, yz; zz=-xx-yy."""
    c=np.asarray(coefficients,float)
    if c.ndim!=2 or c.shape[1]!=5 or not len(c) or not np.isfinite(c).all():raise ValueError('finite Nx5 coefficients required')
    G=np.zeros((3,3,len(c)))
    with np.errstate(over='raise',invalid='raise'):
        for j,(xx,yy,xy,xz,yz) in enumerate(c):G[:,:,j]=[[xx,xy,xz],[xy,yy,yz],[xz,yz,-xx-yy]]
    if not np.isfinite(G).all():raise ValueError('construction overflow')
    return G

def check(G,tolerance=1e-12):
    G=np.asarray(G,float)
    if G.ndim!=3 or G.shape[:2]!=(3,3) or not G.shape[2] or not np.isfinite(G).all():raise ValueError('finite 3x3xN required')
    if isinstance(tolerance,(bool,np.bool_,str)) or not np.isscalar(tolerance) or not np.isfinite(tolerance) or tolerance<=0:raise ValueError('positive finite tolerance required')
    with np.errstate(over='raise',invalid='raise'):
        symmetry=np.max(abs(G-G.swapaxes(0,1)),axis=(0,1));trace=abs(np.trace(G,axis1=0,axis2=1))
    if not np.isfinite(symmetry).all() or not np.isfinite(trace).all():raise ValueError('residual overflow')
    return {'passes_local_structure':bool((symmetry<=tolerance).all() and (trace<=tolerance).all()),
            'symmetry_residuals':symmetry.tolist(),'trace_residuals':trace.tolist(),
            'scope':'necessary local current-free magnetostatic structure only, not finite coils or global realizability'}
