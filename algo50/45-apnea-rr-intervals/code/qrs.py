"""From-scratch QRS detector: Pan-Tompkins integer-filter front end plus
segment-adaptive thresholding (robust to the clipped / high-artifact records
in Apnea-ECG)."""
import numpy as np
from scipy.signal import lfilter

def detect_qrs(ecg, fs=100):
    ecg = np.asarray(ecg, dtype=np.float64)
    ecg = ecg - np.median(ecg)
    # Pan-Tompkins low-pass: y[n]=2y[n-1]-y[n-2]+x[n]-2x[n-6]+x[n-12]
    b_lp = np.zeros(13); b_lp[0] = 1; b_lp[6] = -2; b_lp[12] = 1
    lp = lfilter(b_lp, [1, -2, 1], ecg)
    # Pan-Tompkins high-pass: y[n]=y[n-1]-x[n]/32+x[n-16]-x[n-17]+x[n-32]/32
    b_hp = np.zeros(33); b_hp[0] = -1/32; b_hp[16] = 1; b_hp[17] = -1; b_hp[32] = 1/32
    hp = lfilter(b_hp, [1, -1], lp)
    d = np.convolve(hp, np.array([1, 2, 0, -2, -1]) * fs / 8.0, mode='same')
    sq = d ** 2
    w = max(1, int(0.150 * fs))
    mwi = np.convolve(sq, np.ones(w) / w, mode='same')
    refr = int(0.250 * fs)
    peaks = []
    seg = 10 * fs
    for s0 in range(0, len(mwi), seg):
        s = mwi[s0:s0 + seg]
        if len(s) < w:
            continue
        med = np.median(s)
        hi = np.percentile(s, 97)
        if hi <= med:
            continue
        thr = med + 0.35 * (hi - med)
        i = 0
        while i < len(s):
            if s[i] > thr:
                j = i + int(np.argmax(s[i:i + w]))
                g = s0 + j
                if not peaks or g - peaks[-1] > refr:
                    peaks.append(g)
                i = j + refr
            else:
                i += 1
    peaks = np.array(peaks, dtype=np.int64)
    # dedup: merge peaks closer than 350 ms, keeping the stronger MWI peak
    if len(peaks) > 1:
        keep = [peaks[0]]
        for p in peaks[1:]:
            if p - keep[-1] < int(0.350 * fs):
                if mwi[p] > mwi[keep[-1]]:
                    keep[-1] = p
            else:
                keep.append(p)
        peaks = np.array(keep, dtype=np.int64)
    return peaks
