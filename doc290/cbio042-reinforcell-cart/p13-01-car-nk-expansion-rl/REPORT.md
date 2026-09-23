# P13-01 Build Report: NK-Expand (CAR-NK Bioreactor RL)

**Parent:** CBIO042 ReinforCell | **Spec:** doc290/cbio042-reinforcell-cart/01-car-nk-expansion-rl.md
**Built:** 2026-09-23 | **Status:** BOUNDARY RESULT (1 of 4 gates failed - documented, not re-fished)

## What was built
`tool/nkexpand.py` - a complete, runnable pipeline: a literature-parameterized CAR-NK
expansion simulator (total-cells dynamics with density-managed splitting, nutrient
depletion, exhaustion and persistence state), three static published-style baseline
protocols plus one human-heuristic schedule, a tabular Q-learning agent (two
pre-committed configurations, both reported), and a locked-gate evaluation harness.
Run: `python3 tool/nkexpand.py results/results.json` (seconds, numpy only).

## Gate amendment (locked before results, per pivot rule)
Spec G1 required fitting to real held-out NK expansion time series. No public NK
expansion time-series dataset is retrievable in this environment; publishing
curve-fit claims without the data would be fabrication. G1 was therefore re-locked
as **G1' (calibration validity)**: static protocols simulated by the model must
reproduce the published feeder-free fold-expansion range (50-500x, +25% tolerance).
This re-lock happened before any gate evaluation. The original G1 remains open and
is the first item in "what this build needs next" - the tool's calibration mode is
built for it.

## Results vs locked gates
| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1' | static IL-2 fold within 50-625x | 507x mean | **PASS** |
| G2 | RL composite >= 1.20x best static | 1.174x (coarse cfg); 0.759x (fine cfg) | **FAIL** |
| G3 | RL viability >= 0.9x baseline floor | 0.906 vs 0.817 floor | **PASS** |
| G4 | persistence-reward ablation >= 5% | 37.1% delta | **PASS** |

Two RL configurations were pre-committed (coarse bins/4k episodes, fine bins/12k
episodes). Both were evaluated once and are reported. G2 failed on both; no further
hyperparameter iteration was attempted - continuing would be gate-fishing.

## The useful results inside the failed gate
1. **Density management dominates.** The best static protocol (IL-15, full exchange,
   split-to-density) reaches composite 1.238 of the RL best's 1.453 scale; the
   achievable objective is mostly captured by good density practice, not scheduling
   cleverness. Labs should fix splitting discipline before buying optimization.
2. **RL's edge is real but bounded (~17%) and sits in persistence, not yield.**
   The RL policy produces *lower* fold expansion (225x vs 346x) but higher
   persistence (0.53 vs 0.48 mean) - it learns to trade raw expansion for
   memory-like phenotype preservation, exactly the parent's CAR-NK thesis. The
   trade exists; its size over a disciplined static protocol is under 20%.
3. **Tabular RL is fragile to state discretization.** A 3x finer binning swung
   policy performance by 24 points of composite ratio (1.174 -> 0.759) at 3x the
   training budget. For ReinforCell-class projects: the state representation is
   load-bearing; report discretization sensitivity or the RL claim is not credible.
4. **Persistence reward is a verified driver (G4).** Removing it collapses the
   composite by 37% - the objective design, not the optimizer, is where the
   CAR-NK persistence thesis lives.

## What this build needs next
- Real NK expansion time series (the open G1): the tool's calibration mode accepts
  per-lab growth curves to refit r0/K/nutrient constants; the gates can then be
  re-run against lab-true dynamics.
- Function approximation instead of tabular Q (the discretization fragility).

## Honesty notes
In silico throughout; every dynamic parameter carries a literature anchor in the
tool's header. No real patient or donor data exists here. The G2 miss is reported
with both configurations; the boundary claim is the deliverable, per program
standing rules (pivot rule: documented boundary, mechanism extracted, no re-fish).
