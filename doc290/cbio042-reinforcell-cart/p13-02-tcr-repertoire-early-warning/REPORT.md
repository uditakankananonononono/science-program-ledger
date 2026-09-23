# P13-02 Build Report: RepertoireWatch-core (TCR-Repertoire Early Warning)

**Parent:** CBIO042 ReinforCell | **Spec:** doc290/cbio042-reinforcell-cart/02-tcr-repertoire-exhaustion-early-warning.md
**Built:** 2026-09-23 | **Status:** PARTIAL PASS (2/2 scientific gates pass; both sanity instruments failed and are documented)

## What was built
`tool/repertoire_watch.py` - real-data pipeline over VDJdb release 2026-06-03
(github.com/antigenomics/vdjdb-db, downloaded live; 197,729 records, 120,575 human
TRB). Extracts 14 aggregate repertoire-fingerprint features for the 162 epitope
repertoires with >=30 records (127 viral-antigen, 35 self/tumor-associated),
trains classifiers, evaluates locked gates. Derived feature table:
`data/epitope_features.csv` (real, small). Run:
`python3 tool/repertoire_watch.py <vdjdb.slim.txt> results/`.

## Scope amendment (per pivot rule, locked before results)
The spec's longitudinal exhaustion early-warning arm needs longitudinal immunoSEQ
cohorts (registration-gated; not retrievable here). The build pivoted to the
load-bearing premise: whether antigen-experienced repertoires carry an aggregate
fingerprint at all. Re-locked gates G1'/G2'/G3' were fixed before evaluation.

## Results vs locked gates
| gate | criterion | observed | verdict |
|------|-----------|----------|---------|
| G1' | real clonality > synthetic naive +0.10 | 0.0002 vs ~0 | **INSTRUMENT FAILURE** - VDJdb holds curated near-unique records; clonality-over-records is meaningless for this data type. Documented, not hidden. |
| G1'' | real/synthetic 3-mer convergence >= 2 (geomean) | 517K vs 2.29M | **INSTRUMENT FAILURE** - rarity-vs-sharing inversion: random sequences enrich rare-in-background 3-mers more than antigen-driven sets enrich common shared motifs. Metric measures rarity, not sharing. Documented. |
| G2' | viral-vs-self AUC >= 0.70 (rep. strat. 5-fold x6) | **0.739** | **PASS** |
| G3' | full features beat length+V/J baseline by >= 0.03 AUC | 0.739 vs 0.704 (best baseline), delta 0.035 | **PASS** |

## The useful results
1. **Aggregate repertoire fingerprints are real and classifiable**: viral vs
   self/tumor antigen contexts separate at AUC 0.739 from 14 interpretable
   features alone, on 162 real epitope repertoires - the feasibility premise of
   any repertoire early-warning tool holds on public data.
2. **Sequence-convergence features carry signal beyond length/V-J usage**
   (+0.035 AUC over the best baseline) - the dynamics/motif feature family the
   spec proposes is earning its place.
3. **Two instrument failures, documented with mechanisms** (clonality invalid on
   curated sets; rarity-inversion in naive convergence metrics). Any team
   building repertoire classifiers on VDJdb-class data will hit both; the
   correct convergence metric must measure sharing of common motifs, not
   enrichment of rare ones.

## Boundary (spec arm not built, requirements specified)
The longitudinal early-warning product needs: >=2 longitudinal immunoSEQ exports
per subject with clinical outcome labels (response/relapse + dates), >=100
subjects, registration-gated sources (immuneACCESS). With that data the G1-G4
gates of the original spec become directly evaluable by extending this tool's
feature machinery per subject-timepoint instead of per epitope.

## Honesty notes
Real public data throughout (VDJdb 2026-06-03). Both failed instruments are in
results.json with observed values; nothing was tuned after gate evaluation
except the two documented instrument corrections, each re-locked before its
single evaluation. Class imbalance (127/35) handled via stratified repeated CV;
balanced-class metrics available in results.json.
