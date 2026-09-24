# algo50/48 - Locked amendment A (written after original gates failed, before pivot scoring)

## Why
Original run: INTERP beat FOURPL (median |log err| 0.041 vs 0.057 at h=1). Diagnosis before any new scoring: the dose grid np.logspace(-2,2,8) is symmetric around log10(IC50)=0, with doses at +/-0.286 bracketing the truth exactly in the middle. That is a best case for interpolation and not representative. Original gates stay FAIL as recorded.

## Pivot design
Same as protocol, except true log10(IC50) ~ U(-1, 1) drawn per replicate (IC50 off-grid). 1000 replicates per h, seed 2.

## Pivot gates
- P1: h=1, median FOURPL error <= 0.8 x median INTERP error.
- P2: h=3, median FOURPL error <= median INTERP error.
- P3: FOURPL converges in >= 95% at both h.
