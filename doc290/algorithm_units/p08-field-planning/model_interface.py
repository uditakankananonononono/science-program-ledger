"""Explicit source-described gradient packing and caller workspace checks."""
import numpy as np
from gradient_structure import construct

def unpack_upstream(packed):
    """Input Nx5 rows [xx,xy,xz,yy,yz]; output G[derivative,field,actuator].
    Symmetric trace-free local convention only, not calibration admission.
    """
    p=np.asarray(packed,float)
    if p.ndim!=2 or p.shape[1]!=5 or not len(p) or not np.isfinite(p).all():raise ValueError('finite Nx5 upstream rows required')
    return construct(p[:,[0,3,1,2,4]])

def require_workspace(position,bounds):
    """Inclusive finite coordinate range, no tolerance or unit conversion.
    Checks only supplied point against declared bounds, not fit accuracy.
    """
    x=np.asarray(position,float);b=np.asarray(bounds,float)
    if x.shape!=(3,) or b.shape!=(3,2) or not np.isfinite(x).all() or not np.isfinite(b).all():raise ValueError('finite position/bounds required')
    if (b[:,0]>b[:,1]).any():raise ValueError('reversed workspace bounds')
    if (x<b[:,0]).any() or (x>b[:,1]).any():raise ValueError('outside declared workspace')
    return x.copy()
