# METENG-insert — Blind Knockout-Priority Scan: RESULTS

**Outcome: GATE FAIL (1 of 5 products pass; locked bar was >=3) -> DOCUMENTED BOUNDARY per R9.
Not submitted for counting. The calibration case (succinate) PASSED cleanly, so the boundary is
informative: the method is product-class-specific, not generally predictive.**

## Gate result (statistic frozen in GATES.md R3/R4 before scoring)

| product | target score (mean percentile) | null max (200 seeded) | verdict |
|---|---|---|---|
| succinate (CALIBRATION, excluded) | 0.998 | 0.894 | PASS (method sanity confirmed) |
| fumarate | 0.9995 (FUM1 = rank 1 / 949) | 0.9874 | **PASS** |
| pyruvate | 0.513 (PDC1/PDC5/PDC6) | 0.826 | FAIL |
| L-lactate | 0.464 (PDC1, ADH1) | 0.949 | FAIL |
| ethanol | 0.610 (GPD2 0.88; GPD1/FPS1/DLD3 0.45; ADH2 0.82) | 0.847 | FAIL |
| 2,3-butanediol | 0.361 (PDC1, PDC5) | 0.917 | FAIL |

Evaluated: 1/5 pass (< 3) -> GATE FAIL. Fumarate-sensitivity: without fumarate 0/4 - same verdict.

## Interpretation (honest)
The blind gc90 scan recovers knockouts that DISABLE A REACTION DIRECTLY CONSUMING THE PRODUCT
(direct stoichiometric coupling): FUM1 for fumarate (and succinate), SDH2/SDH3 for succinate -
exactly the targets the literature validated for TCA organic acids. It does NOT recover the
redox/regulatory target class: PDC deletions (pyruvate/lactate/BDO) and GPD/FPS1/ADH/DLD deletions
(ethanol) succeed in vivo through cofactor/redox rebalancing and regulation, which a growth-coupling
objective at fixed biomass does not see - in the model these KOs leave the product's gc90 export
inside the large WT-level tie block. The 008 succinate rediscovery was real but class-specific:
blind target rediscovery works for direct-consumption organic-acid designs, not genome-wide.

## Named-baseline arm (R5, beat-or-document)
- Fumarate (PLoS ONE 2012 7:e52086, PMC3530589): published in-silico workflow (iND750 FBA) tested
  ONE literature-chosen target (FUM1). Our blind genome-wide scan ranks FUM1 #1 of 949 - reproduces
  their prediction without the literature prior. AGREEMENT; arguably stronger (ranked, blind).
- Succinate, calibration context (OptGene, Otero 2012 PLoS ONE 7:e54144): published targets
  sdh3+ser3+ser33 (combination). Our single-KO top-3: FUM1, SDH3, SDH2 - overlap on SDH3; we also
  surface FUM1 (independently validated, Arikawa 1999). PARTIAL OVERLAP, complementary (they needed
  combinations + evolution for titer; single-KO growth coupling is necessarily partial).

## Ablation (R6)
The 008 G2-style scan (max product at a flat 10%-of-WT biomass floor) is degenerate - all 949 KOs
tie at theoretical max - confirming the strain-relative 90% growth coupling is what carries signal.

## Tool + nomination (R7/R8)
meteng_cli.py smoke-tested: WT succinate gc90 0.1438 (= 008 reference); FUM1Δ fumarate 0.1818
(+0.0224 vs WT); YJL121CΔ fumarate 0.1617.
**Wet-lab nomination:** RPE1Δ (YJL121C) for fumarate overproduction - top-ranked gene NOT in any
literature target set (gc90 +2.2% at 99%+ growth); also ranked #4-5 for succinate in 008. PPP/NADPH
rebalance hypothesis; test in CEN.PK, aerobic glucose batch, fumarate titer by HPLC, vs FUM1Δ control.

## Errata
E1: scoring-script percentile formula initially inverted; caught because the succinate calibration
failed against the known 008 result; fixed before any result was used; corrected run is of record.
E2: scan orchestration: background processes die in this environment; all scans run foreground with
checkpoint resume (deterministic values; resume-by-skip verified).

## Data & reproducibility
PROVENANCE.md: locked gates SHA, model SHA, citations, code SHAs, score artifact SHA.
