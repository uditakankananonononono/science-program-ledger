# GATES v3 ADDENDUM — locked 2026-09-24 ~00:14 IST, BEFORE the permutation test is run.
# Implementation parameters for the v3 G1 permutation test (compute-envelope fit, declared
# before outcomes per standing rule 4):
# - 200 label shuffles (not 1000): each shuffle re-runs the FULL v3 pipeline
#   (in-shuffle selection + ElasticNet + one 5-fold CV). With 200 shuffles the minimum
#   achievable p is 1/201 ~= 0.005, which still satisfies the p<=0.01 gate; G1 permutation
#   criterion is met only if the observed AUROC exceeds ALL 200 null AUROCs.
# - saga tolerance set to tol=1e-2 (documented; AUROC impact negligible at 200 features,
#   verified by re-running the 20-rep CV under the same tolerance in the same job).
# Everything else from GATES.md/v2/v3 stands unchanged.
