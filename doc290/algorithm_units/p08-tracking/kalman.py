"""Established 2D constant-velocity Kalman baseline, not microrobot validation."""
import numpy as np


def matrix(value,shape,name,strict=False):
    a=np.asarray(value,dtype=float)
    if a.shape!=shape or not np.isfinite(a).all():raise ValueError(name+' shape/finite check failed')
    if not np.allclose(a,a.T,rtol=0,atol=1e-12):raise ValueError(name+' must be symmetric')
    eigen=np.linalg.eigvalsh(a)
    if (eigen<=0).any() if strict else (eigen < -1e-12).any():
        raise ValueError(name+' must be positive '+('definite' if strict else 'semidefinite'))
    return a.copy()


def scalar(value,name,positive=False):
    if isinstance(value,(bool,str)) or not np.isscalar(value):raise ValueError(name+' must be numeric scalar')
    value=float(value)
    if not np.isfinite(value) or (value<=0 if positive else value<0):raise ValueError(name+' invalid')
    return value


class ConstantVelocity:
    """State [x,y,vx,vy]; white-acceleration spectral density q.
    Exact dt-dependent integrated process covariance for this ASSUMED model.
    Missing observations are prediction-only. No noise calibration inferred.
    """
    def __init__(self,state,covariance,q):
        self.state=np.asarray(state,dtype=float).copy()
        if self.state.shape!=(4,) or not np.isfinite(self.state).all():raise ValueError('state must be finite 4-vector')
        self.covariance=matrix(covariance,(4,4),'P')
        self.q=scalar(q,'q')

    def step(self,dt,measurement=None,measurement_covariance=None):
        dt=scalar(dt,'dt',True)
        if measurement is None:
            if measurement_covariance is not None:raise ValueError('R supplied without observation')
            z=R=None
        else:
            z=np.asarray(measurement,dtype=float)
            if z.shape!=(2,) or not np.isfinite(z).all():raise ValueError('measurement must be finite 2-vector')
            R=matrix(measurement_covariance,(2,2),'R',True)
        F=np.eye(4);F[0,2]=F[1,3]=dt
        Q=np.zeros((4,4))
        for a,b in ((0,2),(1,3)):
            Q[a,a]=self.q*dt**3/3;Q[a,b]=Q[b,a]=self.q*dt**2/2;Q[b,b]=self.q*dt
        with np.errstate(over='raise',invalid='raise'):
            predicted=F@self.state
            P=F@self.covariance@F.T+Q
            if not np.isfinite(P).all():raise ValueError('prediction overflow')
            innovation=nis=None
            if z is not None:
                H=np.array([[1.,0,0,0],[0,1.,0,0]])
                innovation=z-H@predicted;S=H@P@H.T+R
                K=np.linalg.solve(S,(P@H.T).T).T
                predicted=predicted+K@innovation
                # Joseph form, preserving covariance symmetry under roundoff.
                A=np.eye(4)-K@H
                P=A@P@A.T+K@R@K.T
                nis=float(innovation@np.linalg.solve(S,innovation))
            P=(P+P.T)/2
            if not np.isfinite(predicted).all() or not np.isfinite(P).all():raise ValueError('update overflow')
        # Commit only after all calculations succeed.
        self.state=predicted;self.covariance=P
        return {'state':predicted.copy(),'covariance':P.copy(),'innovation':None if innovation is None else innovation.copy(),
                'nis':nis,'observed':z is not None}
