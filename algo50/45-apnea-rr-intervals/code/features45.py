"""Per-minute HRV features from the RR tachogram."""
import numpy as np
from scipy import signal, stats

def minute_features(rr_t, rr_v, fs_ann=60):
    """rr_t: beat times (s), rr_v: RR intervals (s). Returns list of feature
    vectors per minute with >= 5 clean beats, plus the minute index."""
    feats, mins = [], []
    t_end = rr_t[-1] if len(rr_t) else 0
    for m in range(int(t_end // 60)):
        lo, hi = m * 60.0, (m + 1) * 60.0
        mask = (rr_t >= lo) & (rr_t < hi)
        rr = rr_v[mask]
        rr = rr[(rr >= 0.3) & (rr <= 2.0)]
        if len(rr) < 5:
            continue
        t = rr_t[mask][:len(rr)]
        d = np.diff(rr)
        mean, sd = rr.mean(), rr.std()
        rmssd = float(np.sqrt(np.mean(d**2))) if len(d) else 0.0
        pnn50 = float(np.mean(np.abs(d) > 0.05)) if len(d) else 0.0
        cv = sd / mean
        mad = float(np.median(np.abs(rr - np.median(rr))))
        skew = float(stats.skew(rr)); kurt = float(stats.kurtosis(rr))
        rng = float(rr.max() - rr.min())
        dstd = float(np.std(d)) if len(d) else 0.0
        # Lomb-Scargle on the irregular tachogram
        vlf = lf = hf = 0.0
        if len(rr) >= 10:
            tt = np.cumsum(rr) - rr[0]
            f = np.linspace(0.003, 0.4, 200)
            p = signal.lombscargle(tt, rr - rr.mean(), f * 2 * np.pi,
                                   normalize=True)
            vlf = float(np.trapezoid(p[(f >= 0.003) & (f < 0.04)]))
            lf = float(np.trapezoid(p[(f >= 0.04) & (f < 0.15)]))
            hf = float(np.trapezoid(p[(f >= 0.15) & (f <= 0.4)]))
        lfhfr = lf / hf if hf > 0 else 0.0
        # sample entropy m=2, r=0.2*sd (coarse)
        r = 0.2 * sd if sd > 0 else 1e-9
        n = len(rr)
        def count(mm):
            c = 0
            for i in range(n - mm):
                for j in range(i + 1, n - mm + 1):
                    if np.max(np.abs(rr[i:i+mm] - rr[j:j+mm])) < r:
                        c += 1
            return c
        a_, b_ = count(3), count(2)
        sampen = float(-np.log(a_ / b_)) if a_ > 0 and b_ > 0 else 0.0
        feats.append([mean, sd, rmssd, pnn50, cv, mad, skew, kurt, rng, dstd,
                      vlf, lf, hf, lfhfr, sampen])
        mins.append(m)
    return np.array(feats, dtype=np.float32), np.array(mins)

B1_IDX = [0, 1, 2, 3, 4, 5]          # mean, std, rmssd, pnn50, cv, mad
B0_IDX = [0]                          # mean RR only
