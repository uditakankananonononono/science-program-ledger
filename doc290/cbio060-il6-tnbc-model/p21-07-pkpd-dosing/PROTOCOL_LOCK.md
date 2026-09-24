# P21-07 Protocol and Gates - LOCKED BEFORE RESULTS (lane D, 2026-09-24 ~12:12 IST)

Spec: doc290/cbio060-il6-tnbc-model/07-pkpd-dosing.md. Spec gates kept; amendments locked before any PK/PD
simulation is run.

## Sources (fetched 2026-09-24)
- Jakafi label (accessdata.fda.gov/drugsatfda_docs/label/2017/202192s015lbl.pdf): MF dose 20 mg BID (platelets
  >200x10^9/L); Cmax dose-proportional, 205-7100 nM over 5-200 mg; tmax 1-2 h; F >= 95%; Vss 72 L; protein
  binding ~97%; t1/2 ~3 h; CL 17.7 L/h (women) / 22.1 L/h (men).
- Actemra label (.../label/2025/125276s147lbl.pdf): 8 mg/kg IV q4w; steady-state median Cmax 176 ug/mL,
  Ctrough 13.4 ug/mL; terminal t1/2 ~21.5 d at high concentration (linear phase); nonlinear (MM) elimination;
  MW ~148 kDa.
- Sylvant label (.../label/2019/125496s018lbl.pdf): 11 mg/kg IV q3w; steady-state mean Cmax 332 ug/mL, trough
  84 ug/mL; Vc 4.5 L (70 kg male); CL 0.23 L/day; t1/2 after first dose 20.6 d; accumulation ~1.7x.
- Potency: ruxolitinib JAK1 IC50 3.3 nM (Quintas-Cardama 2010, doi.org/10.1182/blood-2009-04-214957, as
  quoted in PMC5147419); tocilizumab-IL-6R Kd 2.54 nM (PubMed 16102523). Siltuximab: no verified public Kd
  found in this run -> use the host model's own anti-IL-6 antibody affinity (kIL6AbUnbind/kIL6AbBind =
  2.5e-3 nM, Dwivedi 2014 calibration), flagged as model-internal.

## Pre-locked amendments
- A1 host model: P21-01 surrogate (BIOMD0000000535, nominal parameters), native antibody dosing OFF.
- A2 PK (70 kg): ruxolitinib 1-compartment oral, F 0.95, ka 2.0 /h (fixed a priori), V 72 L,
  CL 19.9 L/h (mean of label sexes), MW 306.4, free fraction 0.03. Tocilizumab 1-compartment IV bolus,
  V = 3.2 L (= 560 mg / 176 ug/mL; so its Cmax check is partly circular - disclosed), two elimination arms:
  arm A t1/2 21.5 d (label linear phase), arm B t1/2 7.6 d (derived from label Ctrough/Cmax over 28 d).
  Siltuximab 1-compartment IV bolus, V 4.5 L, CL 0.23 L/d (label values, no tuning).
- A3 PD link (quasi-equilibrium, no target-mediated disposition): ruxolitinib multiplies kcatSTATPhos by
  (1 - Cf/(Cf+3.3 nM)); tocilizumab multiplies kRLOn by (1 - C/(C+2.54 nM)); siltuximab multiplies kRLOn by
  (1 - C/(C+0.0025 nM)). Multipliers piecewise constant, updated every 0.5 h (rux) / 6 h (mAbs) at the
  step midpoint.
- A4 schedules: 4 weeks (0-672 h) from untreated steady state; rux 20 mg q12h; toc 8 mg/kg at 0 h (next at
  672 h, outside the window); sil 11 mg/kg at 0 and 504 h.
- A5 metrics (tissue pSTAT3, relative to untreated steady state): dynamic = time-averaged suppression 0-672 h
  (primary); static = steady-state suppression at constant concentration equal to the first-dose Cmax.
  Sustained = over the last dosing interval inside the window, trough suppression >= 80% of peak suppression;
  rebound = trough < 50% of peak.
- A6 G1: each drug's model Cmax and t1/2 within 20% of label: rux single 20 mg Cmax vs 710 nM (label 7100 nM /
  200 mg, dose-proportional) and t1/2 vs 3 h; toc (arm A) steady-state Cmax vs 176 ug/mL and t1/2 vs 21.5 d;
  sil steady-state Cmax vs 332 ug/mL and t1/2 vs 20.6 d. Pass only if all checks pass; each check reported.
  Toc arm B reported (trough vs 13.4 ug/mL), not gated.
- A7 G2: static vs dynamic ranking (3 drugs, arm A) reported for all 3 pairs, with arm B as a sensitivity.
- A8 G3: 100 P21-01 ensemble members (every 3rd of the 300 regenerated with the identical seed-2101 sampler;
  regeneration checked by matching the member count and nominal chi2 26.525). Pass iff the nominal dynamic
  ranking order AND the nominal verdicts (sustained/rebound per drug, any-pair reversal) hold in >= 80%.
- Spec failure rule: if PK changes no ranking, report that static screens are enough for this pathway.
