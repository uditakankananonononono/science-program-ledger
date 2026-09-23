# PPD-BIOMARKERS GATES v3 — locked 2026-09-24 ~00:13 IST, BEFORE any v3 results.
# Trigger: G1 FAILED on the v1/v2 discovery design (3rd-trimester-only, n=43:
# repeated-CV AUROC 0.516 +/- 0.042 - no signal). Documented negative preserved.
# Program pivot rule: steer direction, lock new gates first, keep honesty rules.
#
# v3 changes (everything else from v1/v2 stands):
# 1. Discovery cohort broadened to match the published Mehta 2014 design: 1st + 3rd
#    trimester samples, PPD vs euthymic (still fully prospective - pregnancy blood,
#    postpartum outcome label). Exact n recorded at parse. 2nd trimester excluded
#    (n=3, too sparse).
# 2. Classifier: ElasticNet logistic (l1_ratio=0.5, C=1.0, saga, max_iter 5000) for a
#    sparser, more stable panel at small n. Panel = genes with nonzero coefficient in
#    the final all-data fit (cap 200 by |coef| if more).
# 3. Specificity negative control (ISEF-worthy addition): the frozen panel is also
#    applied to 3rd-trimester "always depressed" samples (chronic depression, not PPD).
#    A PPD-SPECIFIC panel should score always-depressed closer to euthymic than to PPD;
#    reported as an AUROC with honest discussion either way (not a pass/fail gate).
# 4. G1 threshold unchanged (repeated-CV AUROC >= 0.70 AND permutation p<=0.01, 1000
#    shuffles). G2/G2b/G2c external gates unchanged and still FROZEN-untouched.
# 5. If G1 fails AGAIN under v3, next pivot = different discovery cohort (PRAM-D
#    GSE290797 antenatal depression as discovery, GSE290313 stays external), locked as
#    v4 before running. A boundary is declared only after that.
