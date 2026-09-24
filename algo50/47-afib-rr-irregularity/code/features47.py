"""Window-level RR-irregularity features (60 clean beats per window)."""
import numpy as np

def _sampen(rr, m=2, r=None):
    n = len(rr)
    if n < m + 2:
        return 0.0
    sd = rr.std()
    r = 0.2 * sd if r is None and sd > 0 else (r or 1e-9)
    # vectorized Chebyshev distance between all length-m and length-(m+1) windows
    def cheb(mm):
        W = np.lib.stride_tricks.sliding_window_view(rr, mm)  # (n-mm+1, mm)
        d = np.abs(W[:, None, :] - W[None, :, :]).max(axis=2)
        iu = np.triu_indices(d.shape[0], k=1)
        return int(((d[iu] < r)).sum())
    b, a = cheb(m), cheb(m + 1)
    return float(-np.log(a / b)) if a > 0 and b > 0 else 0.0

def _tpr(d):
    if len(d) < 3:
        return 0.0
    tp = int(np.sum((d[1:-1] > 0) & (d[2:] < 0)) + np.sum((d[1:-1] < 0) & (d[2:] > 0)))
    return tp / max(len(d) - 2, 1)

def window_features(rr_series, win=60, stride=30):
    """rr_series: clean RR (s). Windows of `win` beats, `stride` step."""
    feats = []
    for s in range(0, len(rr_series) - win + 1, stride):
        rr = rr_series[s:s + win]
        d = np.diff(rr)
        sd = rr.std()
        sd1 = float(np.std(d) / np.sqrt(2))
        sd2 = float(np.sqrt(max(2 * sd**2 - 0.5 * np.std(d)**2, 0)))
        feats.append([
            float(np.sqrt(np.mean(d**2))),                       # RMSSD
            float(np.mean(np.abs(d) > 0.05)),                    # pNN50
            float(sd / rr.mean()),                               # CV
            sd1, sd2, sd1 / sd2 if sd2 > 0 else 0.0,             # Poincare
            _sampen(rr), _tpr(d),                                # SampEn, TPR
            float(np.mean(np.abs(d))),                           # MAD successive
            float(np.percentile(rr, 75) - np.percentile(rr, 25)),  # IQR
            float(np.median(rr)),
        ])
    return np.array(feats, dtype=np.float32)

B1_IDX = [0, 1, 2, 3, 4, 5]
B0_IDX = [0]
