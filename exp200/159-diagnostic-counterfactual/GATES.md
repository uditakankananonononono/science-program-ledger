# 159 / DOC-2-059 - The diagnostic counterfactual
Locked 2026-09-24 ~11:55 IST, before any model fitting.

Idea: a diagnostic model should say which measurements would have to change to flip its call. Those counterfactual predictions can then be falsified against real therapeutic perturbation.

## Data (GEO, checksums in data/SHA256SUMS)
- Train: GSE87466 (GPL13158), UC colon (87) vs normal (21).
- Frozen external diagnosis: GSE38713 (GPL570), active UC vs non-inflamed (normal + remission).
- Real perturbation: GSE16879 (GPL570), colonic UC + CD, paired biopsies before and after first infliximab. Responders (R) and non-responders (NR) are both included. The model never sees GSE16879 labels.

## Model (fixed)
- Features: within-sample percentile ranks of the shared genes.
- Diagnostic model: L1 logistic regression (C=0.1, standardized) on GSE87466.
- Counterfactual (CF) for an active sample: move features toward the healthy training mean, in order of largest |coef| x distance gain to the logit, until the predicted P(UC) < 0.5. The CF set is the genes moved, with their predicted direction.
- Per-patient CF top-10 = the first 10 genes moved.

## Baselines
- B-dx (named, clinical): calprotectin genes S100A8 + S100A9 mean rank (fecal calprotectin is the standard UC activity biomarker; Tibble et al. 2000; Mosli et al. 2015 meta-analysis).
- B-imp (explanation baseline): global feature importance. The same top-10 |coef| genes for every patient, direction = sign(coef). This is the standard "feature importance only" explanation the topic contrasts against.

## Gates
- G1 (diagnosis, frozen external): model AUROC on GSE38713 >= 0.90 and >= B-dx - 0.02 (the model must be clinically competitive, not necessarily better).
- G2 (counterfactual falsification, core): in GSE16879 responders (R), precision@10 = fraction of a patient's CF top-10 genes that move in the predicted direction after infliximab. Pass needs all of:
  - mean CF precision >= 0.70;
  - CF - B-imp >= +0.10;
  - a pairing-shuffle null (CF sets assigned to random other patients) gives p < 0.05.
- G3 (mechanism): the union of the CF genes is enriched for Hallmark INFLAMMATORY_RESPONSE or TNFA_SIGNALING_VIA_NFKB (hypergeometric p < 0.01). Infliximab is anti-TNF, so this is the expected mechanism.
- G4 (tool + nomination): a CLI that returns, for a sample, the diagnosis plus its "falsification test" (the genes whose change would flip it), plus one prospective nomination (the non-responder patient whose CF genes moved least, flagged as a predicted persistent-active case; or the gene most often in the CF sets but lacking UC literature).
- Also reported (not gated): the non-responder CF precision, expected lower than R.
- PASS = G1-G4. Otherwise a documented boundary. No retuning of C, K or the contrasts after results.

Clarification, committed before running: GSE38713 active = "active disease (involved mucosa)" (15); negatives = controls (13) + remission (8); non-involved mucosa from active patients (7) excluded as ambiguous. GSE16879 pairs are matched by sample-title prefix (e.g. UCR1_beforeT/afterT); colon only.
