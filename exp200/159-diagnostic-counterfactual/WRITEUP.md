# 159 / DOC-2-059 - The diagnostic counterfactual: BOUNDARY (not counted)

Gates were locked before results (commits bfc1b20d and 3d90a105).
- Model: L1 logistic regression on UC vs normal colon (GSE87466).
- Counterfactual (CF) test: before/after infliximab biopsies (GSE16879; 42 colonic pairs, 19 responders).

## Results
- G1 PASS: frozen external GSE38713 AUROC 0.997. The calprotectin genes S100A8/9 score 1.000, inside the locked -0.02 tolerance.
- G2 FAIL. In responders, the patient's CF genes moved in the predicted direction 0.88 of the time. Global feature importance scored 0.82. The +0.06 margin misses the locked +0.10. The pairing-shuffle null averages 0.85 (p = 0.26), so per-patient CFs carry no patient-specific information.
- G3 FAIL: the CF gene union is only SLC6A14, DPP10-AS1 and TIMP1. TNFA enrichment p = 1.0; inflammatory p = 0.03 (above the 0.01 bar).
- G4 done: the tool is code/cf_test.py (diagnosis plus "flip-if" genes). Nomination below.
- Not gated: in non-responders CF precision is 0.59 vs 0.88 in responders. CF genes move toward healthy only when the patient heals, so the test behaves as a falsifiable response read-out.

## Why it failed (mechanism)
- The L1 model keeps 9 genes. A CF flips the call after 2.0 genes on average (max 3), not the 10 planned, and 16 of 19 responders get the same pair (SLC6A14, DPP10-AS1).
- A sparse, near-perfect diagnostic has one dominant axis, so its counterfactual collapses to global importance. Counterfactuals only become patient-specific when the model has several competing routes to the call.
- The failure is sparsity, not the counterfactual idea.

## Prospective nomination
A one-gene falsification test for anti-TNF response: if mucosal SLC6A14 does not fall after the first infliximab dose, the model predicts the UC call persists. Of the 3 non-responders whose CF genes did not move (precision 0.0), all stay at P(UC) >= 0.77 after treatment (UC_NR_8, UC_NR_14, CDc_NR_1). SLC6A14 is already a known UC-inflamed-mucosa gene (it was the single-gene baseline in exp200/156), so this repackages a known marker as a falsification test. It is not a new marker.

## Follow-up that attacks the mechanism (not a gate retry)
- Use a dense or grouped model (elastic-net or group-lasso over pathways) so counterfactuals have several routes.
- Score per-patient CFs against the global-importance baseline on the same GSE16879 pairs, under new locked gates.

## Data
GEO series matrices for GSE87466, GSE38713 and GSE16879, plus GPL annotations. Checksums are in SHA256SUMS.
