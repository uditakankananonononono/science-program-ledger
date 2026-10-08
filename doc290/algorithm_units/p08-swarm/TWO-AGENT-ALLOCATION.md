# Exact finite-menu robust allocation development unit

Established Frechet bounds for two Bernoulli variables, not a new algorithm.
Target-only model: each agent has caller-supplied exact target probability and
positive payload. One or two agents only. No off-target outcome or collateral
constraint, time/flow/crowding/interaction mechanics, calibration or measured data.
The non-target state collapses all failures; no collateral safety implication.

For two agents, joint target mass t ranges from max(0,p1+p2-1) to min(p1,p2).
All four joint-state masses are affine in t. Threshold success is affine, so its
minimum/maximum occurs at endpoints. The returned independent value uses t=p1*p2;
it is an assumed-model baseline, not a data-supported dependence choice.
Finite-menu selection ranks exact minimum success; retains all maximin ties and
all candidate results. It optimizes only the supplied menu, not continuous weights
or physical designs. Alternatives must have identical total payload. Probabilities
may differ across alternatives but must be supplied separately: allocation-invariant
physical p is not inferred. Energy/information/actuation/cost budgets not equalized.

Six development tests: endpoint algebra, finite-menu independence ranking reversal,
weight assignment, ties/deterministic cases, invalid inputs and denominator-4 joint
mass enumeration. 25 marginal pairs times two thresholds are analytic development
fixtures, not held-out validation. No scored experiment or physical gate passed.
Retained reversal: single p=0.7 beats split p=(0.5,0.5) under arbitrary-dependence
minimum (0.7 vs 0.5), while independence ranks split higher (0.75 vs 0.7) for a half-
payload threshold. This demonstrates fragility of assumption-driven rankings, not
single or swarm empirical superiority. Outputs are exact Fractions, not JSON-ready.

Sources for scientific calibration remain unadmitted; see EXPERIMENT-SCREEN.md.
This is a usable robust design-selection baseline under a sharply restricted model,
not the invention or equal-budget comparison promised by the broader P08-05 idea.
