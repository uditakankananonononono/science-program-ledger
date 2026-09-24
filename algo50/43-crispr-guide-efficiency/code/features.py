"""Feature builders shared by all models. ext34 = NNNN[20nt spacer]NGGNNNNNNN."""
import numpy as np

BASES = 'ACGT'
DI = [a + b for a in BASES for b in BASES]

def _tm_wallace(s):
    return 2 * sum(c in 'AT' for c in s) + 4 * sum(c in 'GC' for c in s)

def _gc(s):
    return sum(c in 'GC' for c in s) / max(len(s), 1)

def _longest_run(s):
    best = cur = 1
    for i in range(1, len(s)):
        cur = cur + 1 if s[i] == s[i-1] else 1
        best = max(best, cur)
    return best

def build(df, extended=False):
    """Returns X, names. B1 set = Rule Set 1-style; extended adds M1 extras."""
    ext = df['ext34'].values
    n = len(ext)
    cols, names = [], []
    # position-specific mono
    mono = np.zeros((n, 34 * 4), dtype=np.float32)
    for p in range(34):
        for bi, b in enumerate(BASES):
            mono[:, p * 4 + bi] = [1.0 if s[p] == b else 0.0 for s in ext]
    cols.append(mono); names += [f'mono{p}{b}' for p in range(34) for b in BASES]
    # position-specific dinucleotide
    di = np.zeros((n, 33 * 16), dtype=np.float32)
    for p in range(33):
        for dii, d in enumerate(DI):
            di[:, p * 16 + dii] = [1.0 if s[p:p+2] == d else 0.0 for s in ext]
    cols.append(di); names += [f'di{p}{d}' for p in range(33) for d in DI]
    # position-independent dinuc counts (over spacer)
    pic = np.zeros((n, 16), dtype=np.float32)
    for dii, d in enumerate(DI):
        pic[:, dii] = [sum(1 for i in range(19) if s[4+i:4+i+2] == d) for s in ext]
    cols.append(pic); names += [f'pic{d}' for d in DI]
    num = np.zeros((n, 6), dtype=np.float32)
    for i, s in enumerate(ext):
        sp = s[4:24]
        num[i] = [_gc(sp), _gc(s[4:9]), _tm_wallace(sp),
                  _tm_wallace(sp[:7]), _tm_wallace(sp[13:]),
                  _gc(s[19:24])]
    cols.append(num)
    names += ['gc_spacer', 'gc_distal5', 'tm_spacer', 'tm_5p', 'tm_3p', 'gc_prox5']
    ann = df[['aa_pos', 'pct_peptide']].to_numpy(dtype=np.float32)
    cols.append(ann); names += ['aa_pos', 'pct_peptide']
    if extended:
        gg = np.zeros((n, 20), dtype=np.float32)
        lr = np.zeros((n, 1), dtype=np.float32)
        for i, s in enumerate(ext):
            sp = s[4:24]
            hit = False
            for p in range(19):
                if sp[p:p+2] == 'GG':
                    gg[i, p] = 1.0; hit = True
            gg[i, 19] = 0.0 if hit else 1.0
            lr[i, 0] = _longest_run(sp)
        cols += [gg, lr]
        names += [f'gg{p}' for p in range(19)] + ['gg_absent', 'homopolymer']
    return np.hstack(cols), names
