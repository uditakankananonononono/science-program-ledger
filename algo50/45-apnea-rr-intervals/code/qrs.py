"""From-scratch Pan-Tompkins QRS detector (integer filters via lfilter)."""
import numpy as np
from scipy.signal import lfilter

def detect_qrs(ecg, fs=100):
    ecg = np.asarray(ecg, dtype=np.float64)
    ecg = ecg - np.mean(ecg)
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
    thresh = float(np.mean(mwi) * 0.35)
    sig_lev, noise_lev = 2 * thresh, thresh / 2
    peaks = []
    i = w
    n = len(mwi) - w
    while i < n:
        if mwi[i] > thresh:
            j = i + int(np.argmax(mwi[i:i+w]))
            if not peaks or j - peaks[-1] > refr:
                peaks.append(j)
                sig_lev = 0.125 * mwi[j] + 0.875 * sig_lev
                i = j + refr
                thresh = noise_lev + 0.25 * (sig_lev - noise_lev)
                continue
        noise_lev = 0.1 * mwi[i] + 0.9 * noise_lev
        thresh = noise_lev + 0.25 * (sig_lev - noise_lev)
        i += 1
    return np.array(peaks, dtype=np.int64)
