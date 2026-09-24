# P21-04 Protocol and Gates - LOCKED BEFORE RESULTS (lane D, 2026-09-24 ~12:22 IST)

Spec: doc290/cbio060-il6-tnbc-model/04-combination-synergy-screen.md. Spec gates kept; amendments locked
before any combination is simulated or any screen data is matched.

## Pre-locked amendments
- A1 host model: P21-01 surrogate (BIOMD0000000535, 33 kinetic parameters), untreated steady state; output =
  steady-state tissue pSTAT3 (IL-6 output also reported). Not the unpublished CBIO060 model.
- A2 drug -> model mapping (primary target from the screen's own annotation, else ChEMBL): JAK1/JAK2 inhibitors
  and STAT3 inhibitors -> kcatSTATPhos; IL-6 or IL-6R antibodies -> kRLOn; gp130 inhibitors -> kgp130On. All
  other drugs (chemotherapy, MEK, PI3K, ...) are unmodeled: the model has no NF-kB/MEK/PI3K or viability
  nodes, so a pair with an unmodeled drug has model Bliss excess 0 by construction and cannot be scored.
  A matched pair = both drugs mapped, measured in a TNBC line (MDA-MB-231, MDA-MB-468, HS 578T, BT-549,
  HCC1937, HCC1806, HCC38, HCC70, BT-20, MDA-MB-436, CAL-51, SUM149PT, SUM159PT).
- A3 data: DrugComb (drugcomb.org) summary Bliss scores, else NCI-ALMANAC ComboScore, for matched pairs;
  measured synergy = mean over replicates and TNBC lines per drug pair. If neither source can be fetched in the
  sandbox, G1 is recorded as UNDERPOWERED (data unavailable) and G2 as not evaluable - no substitution.
- A4 model synergy: drugs as fractional inhibition of the mapped parameter at 25/50/75%; Bliss excess =
  observed combined suppression - (sA + sB - sA*sB), averaged over the 3x3 grid. Loewe is not computed
  (dropped: it needs full dose-response curves the host model does not define for mapped drugs).
- A5 G3 (untested combos): all 528 pairs of the 33 parameters as virtual targets at 50%+50% inhibition, ranked
  by Bliss excess on tissue pSTAT3; top-5 nominal pairs robust iff each stays in the member top-20 in >= 80% of
  50 P21-01 ensemble members (every 6th of the 300 regenerated with the P21-07 sampler; saved ensemble
  p21-07-pkpd-dosing/results/results_ensemble.npy is used directly). Solver failures: fresh instance and one
  retry (infrastructure, per parent's P21-07 ruling); remaining failures count against robustness.
- Failure rule (spec): if G2 fails or is not evaluable, report the gap; the viability-module pivot is a
  "needs next" item, not built in this run.
