# P21-02 Protocol and Gates - LOCKED BEFORE RESULTS (lane D, 2026-09-24 ~11:42 IST)

Spec: doc290/cbio060-il6-tnbc-model/02-model-reduction.md. Spec gates kept; amendments locked now, before
any reduced model is built or scored.

## Pre-locked amendments
- A1 (full model). Same surrogate as P21-01: Dwivedi 2014 IL-6 model, BIOMD0000000535 (39 floating ODEs,
  33 kinetic parameters; P21-01 commit 97dc7cf1). The CBIO060 48-ODE model is not public.
- A2 (reduction family). Species freezing: a floating species is replaced by a constant at its nominal
  untreated steady-state value (SBML boundaryCondition=true). Greedy backward elimination from 39 ODEs: at each
  step freeze the species whose removal gives the smallest selection error, until 12 ODEs remain; the whole
  error path is reported. QSSA/lumping are not attempted in this build (disclosed limitation; if G1 fails it is
  a boundary for the freezing family, not for reduction in general).
- A3 (selection vs evaluation, disjoint). Selection error = max nRMSE over outputs {tissue (gut) IL-6,
  tissue pSTAT3} on 3 selection conditions: antibody 100 / 300 / 600 mg at nominal parameters, 0-2016 h.
  Gate conditions (20) = 300 mg antibody experiment with 50% inhibition of each parameter ranked 1-20 in the
  P21-01 nominal pSTAT3 screen.
- A4 (G1 metric). nRMSE per condition x output = RMSE(reduced - full) / (max - min of the full trajectory),
  201 points over 0-2016 h. G1 passes only if the reduced model has <= 12 ODEs AND every one of the 40
  condition x output values is <= 0.1 (mean also reported).
- A5 (G2). Target screen as P21-01 A7 (50% inhibition, drop in untreated steady-state tissue pSTAT3) run on the
  reduced model over all 33 parameters; pass iff reduced top-5 set equals full-model top-5 set
  {kcatSTATPhos, ksynthIL6Gut, kRLOn, kRShedding, kCRPSecretion}. Pre-declared tie rule: kCRPSecretion and
  VmProtSynth tie exactly in the full model, so either one counts for the fifth slot.
- A6 (G3). No public pSTAT3 series in-sandbox: use the P21-01 synthetic training data (seed 2101, days
  0,1,3,7,21,28,56,84; serum IL-6, serum CRP, tissue pSTAT3). Both models refit with scipy least_squares on
  log10 parameters from nominal, bounds +/-2 decades. AIC = n ln(RSS_w/n) + 2k, k = parameters with nonzero
  sensitivity on that model's observables. Pass iff AIC_reduced <= AIC_full. If a frozen species makes an
  observable constant, that counts against the reduced model (no special-casing).
- Failure rule (spec): if G2 fails, report which modules' species cannot be frozen without changing the top-5.
