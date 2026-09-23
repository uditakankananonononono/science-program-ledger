# algo50/15 - Tissue-specificity indices: does collapsing redundant GTEx tissues help tau predict protein-level restriction?

Protocol and gates locked before scoring (PROTOCOL.md, results/lock.txt). RNA: GTEx v8 median TPM, 52 tissues (cell lines dropped) collapsed to 30 organs for tau_organ. Independent truth: HPA normal-tissue immunohistochemistry (antibody staining). 8643 genes: 1147 protein-restricted (<= 3 tissues), 7496 broad (>= 20), and 2047 intermediate (used in the pivot).

## Original gates (results/metrics_original.json)
| index | AUROC restricted vs broad |
|---|---|
| tau_raw (= TSI, same ranking) | 0.964 |
| tau_organ | 0.964 |
| entropy | 0.954 |
| Gini | 0.950 |
| max z | 0.921 |
- G1 FAIL: tau_organ - tau_raw = +0.0002 (CI -0.0012 to 0.0016).
- G2 FAIL: the best other index was TSI, which ranks genes the same way as tau. That's a design flaw, disclosed in Amendment 1.
- G3 PASS after a disclosed NaN bug fix (Amendment 1): tau_organ on half the organs vs all organs, mean Spearman 0.944 (min 0.895).

## Post-hoc pivot (Amendment 1, locked before scoring; results/pivot_metrics.json)
Restricted vs broad is saturated, so the pivot used the harder contrast restricted vs intermediate (4-19 tissues):
| index | AUROC |
|---|---|
| max z | 0.776 |
| tau_raw | 0.759 |
| tau_organ | 0.749 |
| entropy | 0.711 |
| Gini | 0.695 |
- P1 FAIL: tau_organ is slightly WORSE than raw tau (-0.0097, CI -0.015 to -0.005).
- P2 FAIL: max z beats tau_organ.

## What this means
Collapsing GTEx's over-sampled organs does not make tau a better predictor of where a protein is actually found. On the harder contrast it is a bit worse, perhaps because sub-regions (e.g. brain areas) carry real specificity signal that the median throws away. Plain tau is already robust, and on the hard contrast max z edges it out. 15 closes as a documented negative, with G3 (robustness) passing.

## Caveats
HPA IHC tissues and GTEx tissues are not the same panel; antibody detection has its own sensitivity limits; the restricted/broad cut-offs were chosen upfront, not tuned.

## Reproduce
Download the two URLs in data/source_url.txt into data/ (unzip the HPA file), check SHA256_raw.txt, then python3 code/run.py && python3 code/pivot.py (about 1 min).
