# 31 - GO semantic similarity for predicting physical PPIs (headline FAIL; post-hoc pivot PASS)

Question: does simGIC (Pesquita 2008) beat Resnik best-match-average (Resnik 1995) at separating STRING v12 high-confidence physical interactions (experimental >= 700) from degree-matched non-interacting pairs? 10k positives, 10k negatives. IPI annotations and "protein binding" removed to limit leakage. Gates locked before scoring (commit 626125cc).

| Gate | Result | Value (95% CI, 1000 stratified bootstraps) |
|---|---|---|
| G1 AUROC simGIC-BP - Resnik-BMA-BP >= 0.01 | FAIL | -0.014 (-0.017, -0.012) |
| G2 simGIC over all 3 ontologies - best single-ontology Resnik-BMA >= 0.02 | PASS | +0.021 (0.017, 0.025) |
| G3 simGIC-BP - Resnik-max-BP > 0 | FAIL | -0.023 (-0.026, -0.020) |

AUROC, BP: Resnik-BMA 0.885, Resnik-max 0.893, Lin-BMA 0.887, simGIC 0.870. CC: simGIC 0.887 (best in CC). MF: all about 0.70. simGIC-ALL 0.906.

Post-hoc pivot (Amendment 1, locked and pushed before scoring, commit 6596432a; chosen after seeing the per-measure AUROCs, so treat it as exploratory): 5-fold out-of-fold logistic regression over all 13 pre-registered scores.
- P1 vs Resnik-BMA-BP >= 0.03: PASS, AUROC 0.938, +0.054 (0.051, 0.057)
- P2 vs simGIC-ALL >= 0.005: PASS, +0.033 (0.030, 0.035)

Takeaway: in biological process, simGIC is not better than Resnik; it is worse. The gain comes from combining ontologies: CC and MF carry signal that BP measures miss. A 13-weight combination adds about 0.05 AUROC over the standard single measure.

Caveats: the pivot is post hoc. CV splits by pair, not protein (low capacity limits the leak risk, but it isn't zero). Well-studied proteins have more annotations and more reported interactions. Degree-matched negatives reduce this but don't remove it. CC similarity partly restates co-localization, which experimental PPI detection also depends on. STRING "experimental" includes curated databases.
