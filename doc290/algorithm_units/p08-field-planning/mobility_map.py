"""Proposed local fixed-moment map assembly. Inputs must be externally calibrated."""
import numpy as np

def assemble(moment,gradient_per_current,mobility):
    """G[a,b,j] = partial(field component b)/partial(position a)/current j.
    Force[a,j] = sum_b moment[b]*G[a,b,j]; velocity_map = mobility @ force.
    SI inputs: moment A*m^2, G T/(m*A), mobility m/(N*s).
    Fixed dipole, local constant gradient and linear mobility assumptions only.
    """
    m=np.asarray(moment,float);G=np.asarray(gradient_per_current,float);L=np.asarray(mobility,float)
    if m.shape!=(3,) or G.ndim!=3 or G.shape[:2]!=(3,3) or G.shape[2]<1 or L.shape!=(3,3):raise ValueError('map shape')
    if not all(np.isfinite(x).all() for x in (m,G,L)):raise ValueError('nonfinite map input')
    if not np.allclose(L,L.T,rtol=0,atol=1e-12) or (np.linalg.eigvalsh(L)<=0).any():raise ValueError('mobility must be symmetric positive definite')
    with np.errstate(over='raise',invalid='raise'):
        force=np.einsum('b,abj->aj',m,G);velocity=L@force
    if not np.isfinite(force).all() or not np.isfinite(velocity).all():raise ValueError('map arithmetic overflow')
    return {'force_per_current':force.tolist(),'velocity_per_current':velocity.tolist(),
            'scope':'proposed local fixed-moment mobility-gradient map; no device calibration, flow, wall or orientation dynamics'}
