"""Established offline RTS Gaussian smoother. No causal control claim."""
import numpy as np
from kalman import matrix


def smooth(filtered_means,filtered_covariances,predicted_means,predicted_covariances,transitions):
    """Prediction arrays/transition k map filtered time k to time k+1.

    All means are 4-vectors. Prediction covariances must be positive definite
    for linear solve. Singular predictions are explicitly unsupported. This
    function does not infer or certify consistency of supplied filter records.
    Returns independent arrays, leaving all input buffers unchanged.
    """
    means=np.asarray(filtered_means,dtype=float)
    if means.ndim!=2 or means.shape[1]!=4 or len(means)<1 or not np.isfinite(means).all():
        raise ValueError('filtered means must be nonempty finite Nx4')
    n=len(means)
    covs=np.asarray(filtered_covariances,dtype=float)
    predictions=np.asarray(predicted_means,dtype=float)
    pcs=np.asarray(predicted_covariances,dtype=float)
    Fs=np.asarray(transitions,dtype=float)
    if covs.shape!=(n,4,4):raise ValueError('filtered covariance shape')
    if predictions.shape!=(n-1,4) or not np.isfinite(predictions).all():raise ValueError('predicted mean shape/finite check')
    if pcs.shape!=(n-1,4,4):raise ValueError('predicted covariance shape')
    if Fs.shape!=(n-1,4,4) or not np.isfinite(Fs).all():raise ValueError('transition shape/finite check')
    covs=np.array([matrix(p,(4,4),'filtered P') for p in covs])
    for p in pcs:matrix(p,(4,4),'predicted P',True)
    sm=means.copy();sc=covs.copy()
    with np.errstate(over='raise',invalid='raise'):
        for k in range(n-2,-1,-1):
            gain=np.linalg.solve(pcs[k],(covs[k]@Fs[k].T).T).T
            sm[k]=means[k]+gain@(sm[k+1]-predictions[k])
            sc[k]=covs[k]+gain@(sc[k+1]-pcs[k])@gain.T
            sc[k]=(sc[k]+sc[k].T)/2
            if not np.isfinite(sm[k]).all() or not np.isfinite(sc[k]).all():raise ValueError('smoothing overflow')
            # Inconsistent externally supplied records are not silently repaired.
            matrix(sc[k],(4,4),'smoothed P')
    return sm,sc
