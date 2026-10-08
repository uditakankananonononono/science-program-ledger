# Solver candidate to exact outer certificate

Established LP duality workflow, not invention. Floating LP supplies equality dual
multipliers for min(event) and min(-event). Upper candidate explicitly sign-negated.
Variables only nonnegative: normalization implies <=1, so no unaccounted upper-bound
dual multipliers. Finite/shape checked candidates converted exactly from binary
floats to Fractions, not approximate denominator rationals. Existing exact verifier
repairs normalization coordinate and checks every outcome inequality against exact
rational marginals/events. Its bounds remain valid even if candidate rounded/poor.

28 dev methods pass (24+4): AND/OR analytic lower/upper signs, exact nonbinary 1/3
single-agent marginal, injected successful NaN multiplier rejection. Floating
estimates reported separately; NOT exact extrema. No independently exact primal
optimizer or general optimality gap closure. Bounds may be loose. Product witness
inside certificate is not a witness for both extrema. Previous modules unchanged.

N<=5 guard, rational-to-float solver input can round; exact verifier uses original
rationals. Nonfinite conversion/solver failure rejects. Fractions not JSON-ready,
bit/CPU growth unprofiled; no physical marginals/correlations, energy/info/cost/time
budget or biological cap validation. No scored comparison/novelty/scientific gate.
Independent review pending. Caller must keep certificate/solver estimate distinction.
