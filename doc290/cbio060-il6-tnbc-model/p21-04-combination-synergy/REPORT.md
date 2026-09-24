# P21-04 Build Report: IL-6 Pathway Combination Synergy Atlas

**Parent:** CBIO060 IL-6 TNBC Model | **Spec:** doc290/cbio060-il6-tnbc-model/04-combination-synergy-screen.md
**Built:** 2026-09-24 (lane D) | **Status:** BOUNDARY RESULT. Validation is UNDERPOWERED (G1: 0 matched
pairs), so G2 cannot be evaluated. G3 PASS for the model-internal atlas. Protocol locked in
`PROTOCOL_LOCK.md` (a9f2513c) before any simulation or data matching.

## What was built
`tool/synergy.py` runs on the P21-01 surrogate IL-6 model (BIOMD0000000535):
(a) the NCI-ALMANAC matching step;
(b) Bliss excess on steady-state tissue pSTAT3 for the three druggable mechanisms the model has (JAK/STAT3
node, IL-6/IL-6R binding, gp130), each on a 3x3 grid of fractional inhibition;
(c) a full virtual atlas of all 528 pairs of the 33 kinetic parameters at 50%+50% inhibition;
(d) robustness of the top-5 pairs across 50 P21-01 ensemble members, taken from the saved P21-07 ensemble.
Run from repo root: `python3 doc290/cbio060-il6-tnbc-model/p21-04-combination-synergy/tool/synergy.py <out.json> <almanac_rux.csv>`.
The CSV holds the ruxolitinib rows (NSC 763371) extracted from ComboDrugGrowth_Nov2017.zip on the NCI-ALMANAC
wiki page (https://wiki.nci.nih.gov/spaces/NCIDTPdata/pages/338237347/NCI-ALMANAC).

## Results vs locked gates
| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | >= 10 matched drug pairs with TNBC data | 0. In NCI-ALMANAC's 104-drug set only ruxolitinib maps to a model node. It has 3,945 combination rows in the 4 NCI-60 TNBC lines, against 102 partners, all unmodeled (chemo, kinase inhibitors etc.). DrugComb API timed out from the sandbox. | **UNDERPOWERED** |
| G2 | Spearman rho >= 0.3 | no matched pairs | **NOT EVALUABLE** (null not testable) |
| G3 | top untested combos robust in >= 80% of parameter sets | top-5 pairs stay in the member top-20 in 100%, 100%, 96%, 98%, 100% of 50 members; 0 solver failures | **PASS** |

Atlas top 5 (Bliss excess on tissue pSTAT3, 50%+50%): kcatSTATPhos+ksynthIL6Gut 0.062;
kRLOn+kcatSTATPhos 0.034; kRLOn+ksynthIL6Gut 0.032; kRLOn+kdistSerumToTissue 0.029;
kcatSTATPhos+kRShedding 0.029. 34% of the 528 pairs have positive Bliss excess. The most antagonistic pairs
(about -0.03) combine two steps of the same phosphorylation cycle (kcatSTATPhos with KmSTATPhos,
VmSTATDephos or kintActiveR).

## What this means
1. **The spec's validation cannot be done with public screens.** They test viability drugs (chemo, targeted
   agents) that this IL-6 model does not contain. The only overlap is one JAK inhibitor, and a pair needs two
   modelled drugs. This is a structural mismatch, not a data-access problem, and DrugComb would not change it:
   IL-6/IL-6R antibodies are not used in cell-line screens.
2. **Most of the model's Bliss "synergy" comes from saturation, not from network interaction.** A sham
   combination (the JAK/STAT3 node combined with itself) scores Bliss excess 0.123 on the 3x3 grid. That is
   higher than every true cross-mechanism pair: JAK+IL-6R 0.081, JAK+gp130 0.020, IL-6R+gp130 0.014. In a
   saturated pathway, the Bliss null counts any dose response steeper than independence as synergy. Positive
   Bliss here should not be read as real synergy. Needs next: a Loewe/HSA or same-target-sham-normalised score.
3. **The ranking of the virtual atlas is robust** (G3), but it inherits the caveat above. The top pair
   (STAT3 phosphorylation + local IL-6 synthesis) is simply the combination of the two strongest single levers
   from P21-01.

## Honesty notes
- Loewe was dropped (locked A4) because mapped drugs have no defined dose-response in the host model.
- Same scope caveats as P21-01: surrogate public model, not the unpublished CBIO060 model.
- The viability-module pivot (spec failure rule) is a "needs next" item and was not built in this run.
- G1 counts only ALMANAC. DrugComb was unreachable (curl timeouts on api.drugcomb.org and drugcomb.org), and the
  mapping rule would still leave its pairs unscorable unless it holds two modelled drugs in TNBC lines.
