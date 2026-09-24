# P21-09 Protocol and Gates - LOCKED BEFORE RESULTS (lane D, 2026-09-24 ~12:54 IST)

Spec: doc290/cbio060-il6-tnbc-model/09-csc-population-dynamics.md. Spec gates kept; amendments locked before
any treatment simulation. (One untreated smoke run of the host model was done to check it loads: day-400
stem fraction ~2%. It is disclosed here and does not touch any gate quantity except G3, which is declared not
evaluable below.)

## Pre-locked amendments
- A1 population module: Nazari et al. 2018 (PMID 29351275), BioModels BIOMD0000000819, from the
  sys-bio/temp-biomodels GitHub mirror. Three populations: cancer stem S, progenitor E, differentiated D.
  IL-6 is produced by tumour cells and binds IL-6R on each population. Occupancy phi raises S self-renewal
  (P_Smin) and lowers death on all populations (gamma terms). The model has no explicit dedifferentiation
  (E/D -> S). IL-6 acts on self-renewal/survival instead. This is a structural difference from spec step 1,
  and dedifferentiation is not added (it has no parameter source without the digitised data).
  Published for head-and-neck cancer, not TNBC: disclosed.
- A2 coupling to the signaling layer: IL-6 blockade = K_f (IL-6/IL-6R binding) x (1 - b). Primary b = 0.98,
  the tocilizumab steady-state pSTAT3 suppression from P21-07. b = 0.5 and 0.9 are reported as a sensitivity
  analysis only.
- A3 chemotherapy (spec: kills non-stem faster): extra first-order death k_c = 0.3/day on E and D and
  0.03/day on S (10x stem resistance, an assumption), days 100-121 after seeding from the model's initial
  state. IL-6 blockade runs over the same window.
- A4 readout: stem fraction SF = S/(S+E+D) at day 121 (end of treatment, primary) and day 142. Combination
  benefit = 1 - SF(chemo + blockade) / SF(chemo alone).
- A5 G1: Iliopoulos 2011 figures cannot be digitised in the sandbox and no tabulated conversion data were
  found. G1 is recorded as NOT MET (data too sparse to fit). The spec failure rule then applies: qualitative
  (sign-level) predictions plus a list of the specific measurements needed.
- A6 G2: 200 parameter sets. Each of alpha_S, Pstar_Smin, P_Smax, myu, gamma_S, gamma_E, gamma_D, K_f, K_r,
  rho, lambda, K_p is multiplied by 10^N(0, 0.3), and the stem resistance ratio is drawn as 10^U(0.5, 1.5),
  seed 2109. Pass iff nominal benefit >= 30% AND benefit >= 30% in >= 80% of sets. Otherwise the null (or
  the sign-level result) is reported. Solver failure: fresh instance, one retry; still failing counts as not
  meeting the criterion.
- A7 G3: GSE176078 needs single-cell processing that is not feasible in-sandbox, and there is no validated
  stem-state annotation. G3 is NOT EVALUABLE in this build. The model's baseline SF is reported for a
  future check.
