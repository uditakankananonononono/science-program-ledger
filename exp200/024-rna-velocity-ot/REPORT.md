# DOC-1-024: Reconstructing Developmental Trajectories with RNA Velocity + Optimal Transport
Status: DOCUMENTED BOUNDARY - reported to main for adjudication (never self-counted). 2026-09-24.

## Question
Does adding optimal-transport coupling to RNA velocity beat the velocity graph alone (scVelo, named
published baseline; Bergen 2020 Nat Biotechnol 38:1408) at reconstructing a developmental trajectory?

## Design (GATES.md + Addendum B locked pre-outcome)
DEV: pancreas endocrinogenesis E15.5 (Bastidas-Ponce 2019 Development 146:dev173849; scvelo datasets;
sha256_16 9e3e459eca00ba06), 7 canonical lineage edges. FROZEN: dentate gyrus neurogenesis (Hochgerner
2018), 5 canonical edges. Arms: scVelo stochastic velocity graph (baseline) vs OT-refined trajectory
(DPT bins + Sinkhorn couplings, cost = distance - lambda*velocity-agreement). Score: cluster-level net
flow forward > backward per canonical edge.

## Results
| arm | dev (7 edges) | spurious | frozen (5 edges) | spurious |
|---|---|---|---|---|
| scVelo baseline | 7/7, wrong 0 | 0.223 | 4/5, wrong 1 | 0.261 |
| OT lam=1.0 | 6/7, wrong 1 | 0.367 | 4/5, wrong 1 | 0.619 |
| OT P1 lam=0.5 / 2.0 | 6/7 (identical) | 0.367 | - | - |
| OT ablation lam=0 | 6/7 (identical) | 0.367 | - | - |

- G1: baseline reproduces scVelo's published-quality behavior (7/7 dev). PASS (sanity: >=4/7).
- G2: FAIL - OT 6/7 < 7/7. P1 lambda sweep: identical 6/7. 
- G3: baseline frozen 4/5 (Granule immature->mature reverses - maturation is a transcriptionally quiet
  gradient velocity cannot see); winner-stability vs locked margin (>= dev-2 = 5): 4 < 5, FAIL - even
  the named baseline degrades on the harder cohort. Frozen OT ties baseline edges (4/5) with 2.4x the
  spurious mass - no advantage anywhere.
- G4 (the payload): OT results are BIT-IDENTICAL across lambda in {0, 0.5, 1.0, 2.0} - the velocity
  term in the OT cost is INERT; the DPT-bin coupling scaffold determines everything, and its single
  dev error (Ductal->Ngn3 low EP, the root region) is a scaffold artifact. Velocity information does
  not survive aggregation into bin-level couplings.
- G5: trajectory_ot.py CLI (winning scVelo arm, honest banner) smoke PASS: 6/7 on an 800-cell
  subsample. Theis lab nomination.

## Boundary statement (program summary)
OT coupling adds nothing over the raw velocity graph at single-timepoint scale: the velocity signal
lives at cell resolution and is destroyed by bin-level OT aggregation (lambda-invariance proves the
channel carries nothing), while the velocity graph itself already achieves ceiling (7/7) on a clean
dataset. Velocity's real limit is elsewhere: transcriptionally QUIET transitions (granule maturation,
frozen cohort) reverse even in scVelo. Task-type map, fifth entry: post-hoc coupling of two methods
fails when the second method's aggregation scale destroys what the first captures (024); vs
augmentation priors fighting the signal (023), generation where a reference carries it (021),
cross-library-design correction (020), alignment of an existing signal (022 - the one win).

## Implementation notes (sanity-halt worked as designed)
First baseline run scored 0/7 - the locked G1 sanity halt fired; cause was my transpose of scvelo's
velocity_graph (pi_ij = cos(x_j - x_i, v_i) is source-rows per scvelo docs). Fixed, rerun, 7/7.
The flawed-cohort file is preserved (results/local/base.log); no outcome was used before the fix.

## Reproduce
code/score_baseline.py, code/score_ot.py [lambda] [dev|frozen], code/score_frozen.py,
code/trajectory_ot.py, code/flows.py. Data via scvelo.datasets (hashes above + results/baseline_*.json).
