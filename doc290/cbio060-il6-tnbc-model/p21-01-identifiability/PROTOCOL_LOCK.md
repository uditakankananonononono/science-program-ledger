# P21-01 Protocol and Gates - LOCKED BEFORE RESULTS (lane D, 2026-09-24 ~11:26 IST)

Spec: doc290/cbio060-il6-tnbc-model/01-identifiability-uncertainty.md. Spec gates G1-G3 kept verbatim;
amendments below are locked now, before any identifiability, ensemble, or fit result is computed.

## Pre-locked amendments
- A1 (model substitution). The CBIO060 48-ODE TNBC model has no public SBML (BioModels/GitHub search, 2026-09-24).
  Structural surrogate: Dwivedi et al. 2014 IL-6 multiscale model, BioModels BIOMD0000000535 (PMID 24402116;
  fetched from the sys-bio/temp-biomodels GitHub mirror because the EBI endpoint returns 403 from the sandbox).
  42 species (39 floating ODEs), 71 reactions: IL-6/sIL-6R/gp130 receptor module, JAK/receptor activation,
  STAT3 phosphorylation/dephosphorylation, pSTAT3-driven protein synthesis (CRP), sgp130 buffering,
  serum/liver/gut compartments, anti-IL-6 antibody PK. Conclusions are about this IL-6/JAK/STAT3 model class,
  NOT a claim about the unpublished CBIO060 model.
- A2 (data). No digitizable public TNBC pSTAT3 time course is usable in-sandbox (no WebPlotDigitizer). Data are
  realistic synthetic: a single anti-IL-6 antibody experiment (300 mg at t=0.1 h, monthly repeats per the model's
  events), observables = serum free IL-6, serum CRP, tissue (gut compartment = tumor analog) pSTAT3, sampled at
  days 0,1,3,7,14,21,28,42,56,70,84; lognormal noise CV 10% (IL-6, CRP), 15% (pSTAT3); RNG seed 2101.
  Held-out time points for G3: days 14, 42, 70. G3 is therefore a model self-consistency test, disclosed as such.
- A3 (estimated set). 33 kinetic parameters are estimated (receptor, signaling, synthesis/degradation,
  distribution, antibody binding). Physiological volumes, flows, antibody PK transfer/degradation, dose and
  infusion time are fixed as known (they are measured, not fitted, in practice).
- A4 (structural identifiability). StructuralIdentifiability.jl is unavailable. Local structural identifiability
  is assessed numerically: SVD of the noise-free log-parametrised sensitivity matrix on a dense grid (200 points)
  of all three observables; a parameter is structurally non-identifiable if it loads >0.1 (|v_i|) on any singular
  direction with s/s_max < 1e-6.
- A5 (practical identifiability). Fisher-information approximation to profile likelihood under the A2 design and
  noise (no prior): practically identifiable iff 1.96*SE(log10 p) <= 0.5 (95% CI within ~3.2-fold).
  Spec hypothesis part 1 ("fewer than half identifiable") is evaluated on this criterion.
- A6 (ensemble). Plausible parameter sets: draw log10 p ~ N(nominal, (FIM + prior)^-1), prior sd 1 decade per
  parameter; accept iff chi2(theta) - chi2(theta_nominal) <= chi2_0.95(df=33) = 47.40 on the training data.
  Target: 300 accepted members (max 20,000 draws). Nominal = data-generating values (near-MLE; disclosed).
- A7 (target ranking). Virtual drug-target screen: for each of the 33 parameters, 50% inhibition (p -> 0.5p);
  score = relative drop in untreated steady-state tissue pSTAT3 (500 h settle from the nominal steady state).
  Top-5 = the five largest drops at nominal. G2 evaluated over accepted ensemble members.
- A8 (G3 metric). Ensemble-median prediction at held-out points; nRMSE per observable = RMSE / (max - min of
  that observable's observed values); G3 passes only if all three observables are <= 0.2.
- Failure rule (spec): if G2 fails, run a greedy D-optimal-style search over candidate added measurements
  (extra time points / extra observables) for the one that most reduces top-5 rank uncertainty.
