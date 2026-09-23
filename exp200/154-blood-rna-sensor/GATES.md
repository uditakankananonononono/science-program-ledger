# DOC-2-054 RNA in Blood as a "Systemic State Sensor" - GATES (locked 2026-09-24 00:45 IST; only series-matrix headers and label fields inspected so far, no expression analysis)

## Experiment
A trained cross-platform blood-RNA classifier for bacterial vs viral infection, validated frozen on two independent pediatric cohorts and benchmarked against two published signatures.
- Training: GSE63990 (Tsalik et al., Sci Transl Med 2016; GPL571; adults, emergency department). Only the bacterial and viral samples are used. The model is L1 logistic regression on within-sample gene ranks. Genes are those present in all three platforms, collapsed to the max-mean probe per gene. C is picked by 5-fold CV on training only.
- External cohorts, frozen:
  - E1: GSE42026 (Herberg et al., J Infect Dis 2013; GPL6947). Gram-positive bacterial vs viral (H1N1 + RSV). Controls excluded.
  - E2: GSE40396 (Hu et al., PNAS 2013; GPL10558). Bacterial vs viral (adenovirus, enterovirus, HHV-6, rhinovirus). Controls excluded.
- Named published baselines, applied to the same samples without training:
  - B1: Herberg et al., JAMA 2016, 2-transcript disease risk score, IFI44L - FAM89A (within-cohort z-scores).
  - B2: Sweeney et al., Sci Transl Med 2016, 7-gene bacterial/viral score: mean z of HK3, TNIP1, GPAA1, CTSB minus mean z of IFI27, JUP, LAX1. A gene missing on a platform is dropped and the drop is disclosed.
  - Disclosure: GSE42026 was among the Herberg 2016 validation data, which favors B1 on E1.

## Gates (all must pass)
- G1 (frozen external performance): AUROC >= 0.85 on both E1 and E2.
- G2 (beats named baselines): pooled E1+E2 AUROC (scores ranked within cohort, i.e. cohort-wise percentile) of the model minus max(B1, B2) >= 0.02, with a 2,000x stratified bootstrap 95% CI lower bound > 0.

## Reported (not gated)
- Mechanism: I expect interferon-stimulated genes (IFI44L, IFI27, RSAD2, ISG15 family) in the model to point viral, and neutrophil/innate genes to point bacterial. Checked against the literature signatures.
- Tool: predict.py (expression table in, probability of bacterial out).
- Prospective nomination: the highest-|weight| model gene that appears in neither B1 nor B2, proposed as an added qPCR target for a febrile-infant cohort.

## Pivot rule
If a gate fails, keep the negative result, amend and lock here before new results, and never re-fish.
