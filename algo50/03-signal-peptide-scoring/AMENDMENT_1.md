# Amendment 1 - label-free operating-point transfer (locked before these results were computed)

## Outcome of the original protocol (not re-scored)
G1 PASS (pooled external MCC P 0.317 vs B2 0.261, diff +0.056, bootstrap 95% CI 0.009-0.105). G2 PASS (hard-negative FPR P 0.288 vs 0.5 x B1 0.346). G3 FAIL (MCC 0.31 yeast, 0.30 E. coli; needed >= 0.6 each). Project PASSES by its primary definition, but the transfer component failed.
Diagnosis prompting the pivot: ranking transfers (pooled AUROC 0.94) but the operating point does not. SP prevalence among experimentally-annotated proteins is about 4.7% in human training data, 0.6% in yeast and 4.6% in E. coli here, so a threshold picked on human does not carry over.

## New direction
Adjust P's posteriors to each target organism's unknown SP prevalence using the label-free EM prior-shift correction (Saerens, Latinne & Decaestecker 2002), run on the unlabeled target scores only, then threshold the adjusted posterior at the human-CV-optimal threshold rescaled by the same odds ratio. No target labels are used to set anything.

## Gates
- A1: after correction, P's pooled external MCC >= 0.40.
- A2: correction improves MCC on both yeast and E. coli separately (each strictly higher than the uncorrected value).
- A3: EM-estimated prevalence within a factor of 2 of the true prevalence in each organism.
