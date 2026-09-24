# GATES ADDENDUM B - DOC-1-032 (locked 2026-09-24 09:01 IST, BEFORE any gate scoring)

## Provenance finding (eligibility coherence check, pre-gate)
Applying the shipped MelonnPan weight matrix to the PRISM training samples yields a positional
metabolite correspondence (the 80 weight-matrix output columns correspond positionally to the
80 compound columns: mean diagonal Spearman 0.621, 100% >= 0.3, vs off-diagonal mean 0.066) -
AND an in-sample-level fit. Combined with the MelonnPan-Train protocol (which retains only
well-predicted metabolites) and the ENVIM paper's PRISM->NLIBD MelonnPan testing fraction of
26%, this establishes that the shipped weight matrix was TRAINED ON PRISM's 157 samples.

## Consequence (arm redefinition)
- The shipped weights CANNOT baseline PRISM dev (in-sample leakage). They CAN and DO baseline
  the NLIBD frozen cohort (zero leakage; published PRISM->NLIBD MelonnPan testing = 26%,
  ENVIM paper Table 3).
- DEV baseline redefinition: ARM A (dev) = the MelonnPan-Train PROTOCOL (Mallick 2019, named
  published method) reimplemented in-envelope: per-metabolite elastic net (alpha by inner CV on
  training folds only, well-predicted selection per protocol), retrained per dev fold on PRISM.
  Published performance anchors for dev context: Mallick 53.8% (HMP2); ENVIM paper Mallick
  cohort DNA: MelonnPan 38% testing / ENVIM 48%.
- ARM A (frozen) = shipped published weight matrix (unchanged from the original lock).
- G1 redefined: ARM A (frozen, shipped weights on NLIBD) fraction well-predicted within
  [0.10, 0.50] (published 0.26 +/- tolerance) -> else frozen data incoherent, halt; AND dev-side
  coherence: the reimplemented protocol yields >= 20% well-predicted on PRISM CV.
- All other gates, margins, P1, G4, G5 unchanged.

No gate outcome has been computed at the time of this lock.
