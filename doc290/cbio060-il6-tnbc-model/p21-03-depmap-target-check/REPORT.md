# P21-03 Build Report: Do Model-Ranked IL-6 Targets Matter in IL-6-high TNBC Lines? (DepMap check)

**Parent:** CBIO060 IL-6 TNBC Model | **Spec:** doc290/cbio060-il6-tnbc-model/03-depmap-target-check.md
**Built:** 2026-09-24 (lane D) | **Status:** BOUNDARY RESULT. G1 FAIL (0/5 targets IL-6-context-specific),
G2 reported (null: rho -0.54, CI [-1.0, 0.70], n = 7 genes), G3 PASS (12 vs 12 lines). Protocol locked in
`PROTOCOL_LOCK.md` (17a126e5) before any dependency value was read.

## What was built
`tool/depmap_check.py` uses DepMap 24Q2 Public (figshare article 25880521: CRISPRGeneEffect.csv,
OmicsExpressionProteinCodingGenesTPMLogp1.csv, Model.csv). The P21-01 top-5 model targets are mapped to genes.
The 24 annotated basal/TNBC breast lines with CRISPR and expression data are split at the median IL6
expression. Each gene is tested for stronger dependency (more negative Chronos) in IL-6-high lines
(one-sided Mann-Whitney, BH-FDR). Model score is then correlated with context dependency across 7 mapped genes.
Run: `python3 tool/depmap_check.py <depmap_dir> results/results.json doc290/cbio060-il6-tnbc-model/p21-01-identifiability/results/results.json`.
The raw DepMap files (~0.9 GB) are not committed. Fetch them with figshare API article 25880521.

## Results vs locked gates
| gene (model parameter) | Chronos IL-6-high / low | diff | FDR q | counts |
|------|------|------|------|------|
| JAK1 (kcatSTATPhos) | +0.074 / -0.031 | +0.105 (wrong direction) | 0.96 | no |
| IL6 (ksynthIL6Gut) | +0.005 / +0.028 | -0.023 | 0.74 | no |
| IL6R (kRLOn) | -0.065 / -0.062 | -0.003 | 0.75 | no |
| ADAM17 (kRShedding) | +0.015 / +0.024 | -0.009 | 0.74 | no |
| CRP (kCRPSecretion) | -0.054 / -0.030 | -0.025 | 0.74 | no |
| JAK2 (reported only) | +0.131 / +0.156 | -0.025 | - | - |

| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1 | >= 2 of top-5 context-specific (diff <= -0.1, q < 0.05) | 0/5; the expression-defined TNBC sensitivity set (17 lines, 8 vs 9) also gives 0/5 | **FAIL** |
| G2 | model-score vs dependency rank correlation with CI | rho = -0.54, bootstrap 95% CI [-1.00, 0.70], 7 genes | **REPORTED (null)** |
| G3 | line counts; < 5 per group exploratory | 12 IL-6-high vs 12 IL-6-low; not exploratory | **PASS** |

## What this means
1. **None of the model's top targets is a dependency in TNBC lines at all, in either IL-6 group.** All mean
   Chronos values are within about 0.15 of zero (about -1 marks a common essential gene). In 2D culture, TNBC
   lines do not need autocrine IL-6/JAK1/IL-6R signalling to proliferate. So CRISPR dependency is the wrong readout
   for a pathway whose model output is pSTAT3, not growth.
2. **Some of the "targets" are artefacts of the model class.** CRP secretion and receptor shedding rank highly
   because the surrogate model (Dwivedi 2014) is a liver/gut multiscale model with inter-compartment loops. They
   are not tumour-cell dependencies. This supports treating P21-01's ranking as model-internal.
3. JAK1 points the wrong way: IL-6-high lines are slightly less JAK1-dependent. That is consistent with no
   IL-6 addiction in vitro.

## Honesty notes
- "TNBC" is the DepMap legacy basal annotation (basal_A/basal_B/basal). The expression-defined alternative
  gives the same 0/5 result.
- The G2 CI is very wide because n = 7 genes. The correlation is uninformative in either direction.
- PRISM JAK/STAT3 inhibitor sensitivity was not used (needs next). It would test drug response, not genetic
  dependency, and might be the better readout.
- Same scope caveat: the surrogate model, not the unpublished CBIO060 model.
