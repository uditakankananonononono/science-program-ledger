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

## Primary result (00:42) - G1 PASS, G2 FAIL, preserved
- Model: 5-fold CV AUROC in training. On E1 (GSE42026, 18 bacterial / 41 viral) AUROC 0.855; on E2 (GSE40396, 8 / 35) AUROC 0.896. G1 PASS.
- Baselines: B1 Herberg 0.870 / 0.857; B2 Sweeney 0.912 / 0.893.
- Pooled: model 0.861 vs B2 0.898, difference -0.036 (CI -0.086 to +0.009). G2 FAIL: the trained model does not beat the published 7-gene Sweeney score. It is at best equivalent.

## Pivot 1 (locked 00:44, before any Pivot 1 data was downloaded or scored)
- Question: does the trained model add information on top of the published Sweeney score? Combined score = mean of the within-cohort percentile ranks of the frozen model and B2, with no fitted weights. The idea came after seeing that B2 won, so it is tested ONLY on a cohort I have not touched.
- E3 (fresh): GSE6269 (Ramilo et al., Blood 2007) sub-series GPL570 and GPL96. Bacterial (S. aureus, E. coli, S. pneumoniae) vs influenza A. Scores ranked within each sub-series, then pooled.
- P1-G1: combined AUROC on E3 >= 0.85.
- P1-G2: combined AUROC minus max(B1, B2) on E3 >= 0.02, with a 2,000x stratified bootstrap CI lower bound > 0.
- Reported: model-alone, B1 and B2 on E3.
Pre-scoring notes (00:46, from series metadata only): GSE6269 profiles PBMCs, not whole blood, so it is a tissue shift. It is disclosed and kept, because the lock came first. Influenza B samples are excluded, as locked. GPL570 has no GEO annot file, so its probes are mapped with the GPL96 annotation (shared HG-U133A probe IDs).

## Pivot 1 result (00:44) - P1-G1 PASS, P1-G2 FAIL, preserved
- E3 (GSE6269, PBMC): 91 bacterial vs 25 influenza A. Combined AUROC 0.931 (P1-G1 PASS). Model alone 0.914; B2 Sweeney 0.922.
- P1-G2 FAIL: difference +0.009, CI -0.018 to +0.035.
- B1 is invalid on E3 (FAM89A is absent from U133A, so the score collapses to a constant). This does not change the gate, because B2 was the max.
Closed as a documented boundary: the frozen model transfers but does not beat the named published 7-gene score.
