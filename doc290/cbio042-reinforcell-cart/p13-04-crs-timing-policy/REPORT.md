# P13-04 Build Report: CRS Timing Policy

**Parent:** CBIO042 ReinforCell | **Spec:** doc290/cbio042-reinforcell-cart/04-crs-timing-policy.md
**Built:** 2026-09-23 | **Status:** 3/3 evaluable gates pass; off-policy arm documented as data boundary

## What was built
`tool/crs_policy.py` - literature-anchored stochastic CRS deterioration model
(ASTCT grades 0-4, patient frailty heterogeneity, tocilizumab/steroid response
arms), a parameterized conservative policy family with an honest train/eval
policy search (selection on 1500 training runs, single evaluation on 4000 fresh
runs), a safety-invariant checker, and an efficacy-penalty sensitivity sweep.
Run: `python3 tool/crs_policy.py results/results.json` (~30s).

## Results vs locked gates
| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1' | untreated grade>=3 rate in published 10-45% band | 12.7% | **PASS** |
| G2' | learned policy >=10% better than BOTH fixed heuristics | selected policy 1.97 vs treat-at-2 3.48, treat-at-3 5.73 (-43%) | **PASS** |
| G3' | 0 runs leave grade>=3 untreated with treatment available | 0/2000 | **PASS** |
| G4 | off-policy evaluation vs physician policy | needs real serial trajectories | **BOUNDARY documented** |

## The useful results
1. **Early tocilizumab dominates in the calibrated model** - treat-at-grade-1
   beats treat-at-grade-2 (-43% composite) and treat-at-grade-3 (-66%), matching
   the clinical drift toward pre-emptive toci.
2. **The ranking is robust, the margin is not.** Across efficacy-penalty values
   0.05-0.60 the winner never changes, but the advantage over treat-at-2 shrinks
   from 44% to 2%. The entire clinical question collapses to one measurement:
   the true efficacy cost of early tocilizumab. That is the trial worth running,
   and the tool says so quantitatively.
3. **Honest-search machinery**: the policy family is searched on training seeds
   and evaluated once on fresh seeds - no selection-on-evaluation. First
   hardcoded-candidate version of this build exposed the risk (candidate was
   identical to a heuristic); the search framework is the fix.

## Boundary (spec's off-policy arm)
Doubly-robust evaluation against observed physician policy needs real serial
cytokine/grade trajectories with recorded interventions. Published CAR-T cohorts
report figures/text, not bulk trajectories; MIMIC-IV is credential-gated.
Exact requirements: >= 3 cohorts, daily (or better) grade + intervention
timestamps, >= 200 patients. The simulator/policy machinery is ready to receive
that data unchanged.

## Honesty notes
In silico throughout; every anchor cited in the tool header; the efficacy-penalty
is an assumption whose sensitivity is the reported result, not a hidden knob.
Gates locked before evaluation; the one structural rewrite (real search vs
hardcoded candidate) happened before final gate evaluation and is disclosed.
