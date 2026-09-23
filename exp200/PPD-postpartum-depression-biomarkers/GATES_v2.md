# PPD-BIOMARKERS GATES v2 — locked 2026-09-24 ~00:13 IST, BEFORE any model fitting.
# Reason: new program-wide "ISEF-worth" checklist (user steering via main 00:10).
# v1 (SHA fa42093a...) governed no results; v2 extends it. All v1 gates stand.
# Discovery cross-tab now parsed and FROZEN: GSE45603 3rd-trimester, PPD n=15, euthymic n=28.

## ISEF checklist amendments
1. NAMED PUBLISHED BASELINE: Mehta et al. 2014, Psychological Medicine, "Early predictive
   biomarkers for postpartum depression point to a role for estrogen receptor signaling"
   (doi:10.1017/s0033291713003231) - the study behind GSE45603. Their published predictor
   gene set (extracted from the open-access manuscript/supplement via QUT ePrints 197508)
   is the named baseline. Gate G2c: on the FROZEN external cohort, our panel AUROC must
   EXCEED the Mehta-panel AUROC (same scoring pipeline, gene-symbol intersection); if the
   full Mehta gene list is not extractable from open sources, that is documented and the
   baseline becomes their published top-gene direction check, clearly labeled as partial.
2. Frozen external validation: already G2/G2b (GSE290313 pregnancy samples, untouched
   until panel lock).
3. Biological interpretation: panel must be checked against known PPD mechanisms in the
   literature - estrogen receptor signaling (Mehta 2014), altered immune landscape
   (Trans Psychiatry 2021, doi:10.1038/s41398-021-01270-5), cytokine/chemokine patterns
   (PMC6676209), B-cell/insulin-resistance TWAS (Mol Psychiatry 2022). Overlap or
   contradiction reported honestly in the writeup; contradiction does not fail the gates
   but must be discussed.
4. Working tool + nomination: scoring CLI (gene-expression vector -> PPD risk score) plus
   ONE prospective nomination: the panel's top-weighted gene with an external-cohort-
   consistent effect direction, nominated for lab validation with a concrete assay idea.

## Frozen sample definitions (parsed, locked)
- Discovery: 43 samples (15 PPD / 28 euthymic), 3rd-trimester whole blood, GSE45603.
- External: GSE290313 pregnancy samples, "Depressive symptomes only postpartum" vs
  "Control" (exact n counted at parse; RNA-seq counts from RAW tar, 301 files).
