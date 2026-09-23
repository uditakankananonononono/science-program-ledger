# PPD-BIOMARKERS GATES v5 — locked 2026-09-24 ~00:18 IST, BEFORE touching external data.
# v3 and v4 discovery both FAILED G1 (v3: CV 0.705 but perm criterion not met; v4: CV
# 0.600, obs 0.518, perm p=0.41). No further discovery-cohort fishing (locked in v4).
# The single decisive pre-registered experiment remains: apply the FROZEN v3 panel
# (200 genes + ElasticNet coefficients, locked 00:14, /tmp/v3_model.joblib, panel CSV
# in results/) ONCE to the untouched external cohort GSE290313.
#
# External evaluation (frozen):
# - Samples: GSE290313 "pregnancy sample" timepoint only; groups "Depressive symptomes
#   only postpartum" (postpartum-onset cases) vs "Control". Other groups excluded.
# - Features: gene-symbol intersection with the 200-gene panel; RNA-seq CPM+log1p;
#   per-cohort z-score per gene (external cohort z-scored within itself; discovery
#   z-parameters NOT reused - document both choices; model coefficients applied to
#   externally z-scored values).
# - Metrics: AUROC with 10k-bootstrap 95% CI; single-feature gate G2b (panel must beat
#   best single panel gene by >=0.03); named-baseline gate G2c (Mehta 2014 panel if its
#   gene list is extractable from open sources, else documented as unavailable);
#   sign-concordance (fraction of panel genes with matching effect direction, binomial
#   vs 50%).
# - Verdict rule: TRANSPORTED (useful) iff AUROC >= 0.65 AND CI lower > 0.5 AND G2b
#   passes. Otherwise DOCUMENTED BOUNDARY for blood-transcriptome PPD biomarker
#   transport under this program's compute/data envelope - with the full evidence chain
#   (v1-v4 negatives, external result, mechanism analysis vs literature) in the writeup.
#   Either way the scoring CLI + panel ship, labeled with its verified or failed status.
