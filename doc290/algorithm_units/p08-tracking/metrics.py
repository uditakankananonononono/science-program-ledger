"""Tracking error metrics with explicit truth availability; no calibration claim."""
import numpy as np
from kalman import matrix


def evaluate(truth,estimated,covariances,truth_available):
    truth=np.asarray(truth,dtype=float);estimated=np.asarray(estimated,dtype=float)
    covariance=np.asarray(covariances,dtype=float);available=np.asarray(truth_available)
    if truth.ndim!=2 or truth.shape[1]!=4 or len(truth)==0:raise ValueError('truth must be nonempty Nx4')
    n=len(truth)
    if estimated.shape!=truth.shape or not np.isfinite(estimated).all():raise ValueError('estimate shape/finite check')
    if covariance.shape!=(n,4,4):raise ValueError('covariance shape')
    if available.shape!=(n,) or available.dtype!=np.bool_:raise ValueError('truth availability must be boolean N-vector')
    if not np.isfinite(truth[available]).all():raise ValueError('available truth must be finite')
    # Validate uncertainty for all records, not only scored truth rows.
    for p in covariance:matrix(p,(4,4),'evaluation P',True)
    errors=estimated[available]-truth[available]
    nees=[]
    with np.errstate(over='raise',invalid='raise'):
        for error,p in zip(errors,covariance[available]):nees.append(float(error@np.linalg.solve(p,error)))
        if len(errors):
            position=float(np.sqrt(np.mean(np.sum(errors[:,:2]**2,axis=1))))
            velocity=float(np.sqrt(np.mean(np.sum(errors[:,2:]**2,axis=1))))
            mean_nees=float(np.mean(nees))
            if not np.isfinite([position,velocity,mean_nees]).all():raise ValueError('metric overflow')
        else:position=velocity=mean_nees=None
    return {'total_records':n,'scored_records':int(available.sum()),'excluded_missing_truth':int((~available).sum()),
            'position_rmse':position,'velocity_rmse':velocity,'nees':nees,'mean_nees':mean_nees,
            'scope':'error metrics only; no chi-square/calibration guarantee without model and independence assumptions'}
