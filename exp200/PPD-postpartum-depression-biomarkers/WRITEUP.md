# PPD-BIOMARKERS — postpartum-depression blood biomarkers: a five-version verification study
**Verdict: DOCUMENTED BOUNDARY (candidate "useful negative" - adjudication requested).**

## The question and the design
User-steered insert: identify AND verify PPD biomarkers from public patient data. Run as a
verification study, not a fishing exercise: locked gates v1, then every pivot pre-registered
before new outcomes (v2: ISEF checklist + named baseline; v3: broadened discovery; v4:
second discovery cohort; v5: frozen external test of the locked v3 panel).

- Discovery A (v1-v3): GSE45603 (Mehta 2014 prospective cohort, HT-12 microarray, whole
  blood). v1 design (3rd trimester only, n=43): repeated-CV AUROC 0.516 - no signal.
  v3 (1st+3rd trimester, n=80, ElasticNet): CV AUROC 0.705 +/- 0.036 BUT failed the locked
  permutation criterion (observed 0.683 < null max 0.718 over 200 full-pipeline shuffles).
- Discovery B (v4): GSE290797 PRAM-D (antenatal depression, n=69): CV 0.600, perm p=0.41 -
  no signal.
- External verification (v5): the FROZEN v3 200-gene panel applied ONCE to GSE290313
  (RNA-seq, pregnancy blood of women later PPD-symptomatic vs controls, n=74: 14 cases).

## Results
| gate | result | verdict |
|---|---|---|
| G1 v1 | CV AUROC 0.516 | FAIL |
| G1 v3 | CV 0.705, perm criterion missed (null max 0.718) | FAIL |
| G1 v4 | CV 0.600, p=0.41 | FAIL |
| G2 v5 external AUROC | **0.429 (95% CI 0.273-0.591) - below chance** | FAIL |
| G2b single-feature gate | panel 0.429 vs best single gene 0.717 | FAIL (diff -0.288) |
| sign concordance | 79/185 (42.7%), binom p=0.056 | trend BELOW chance |

## What is genuinely learned (the useful negative)
1. **Single-cohort CV optimism quantified:** a panel showing 0.705 internal CV scored
   0.429 - worse than a coin flip - on an independent cohort. Cross-platform blood-
   transcriptome PPD biomarkers did not transport at n~100 scale with standard models,
   in either discovery direction.
2. **Permutation discipline caught a false positive:** the v3 panel "passed" CV (0.705)
   but the full-pipeline permutation null reached 0.718 - selection-on-80-samples
   inflates CV by exactly the margin that looked like signal.
3. **Mechanism check vs literature:** top-weighted panel genes (PAM, IL18RAP, LRRC25) are
   innate-immune/inflammation-linked, partially consistent with the immune-landscape PPD
   literature (Trans Psychiatry 2021 doi:10.1038/s41398-021-01270-5), but the panel did
   NOT recover Mehta 2014's estrogen-receptor-signaling axis, and 57% of panel genes
   flipped effect sign externally - the signal was cohort-specific, not biological.
4. Named-baseline gate (G2c vs Mehta 2014 panel): not reached - the panel failed the
   primary external gates; their full gene list was also not extractable from open
   sources (documented).

## Shipped (labeled honestly)
- results/panel_200genes.csv + results/ppd_panel_model.joblib (frozen v3 panel)
- code/ppd_score.py (scoring CLI, smoke-tested; header carries the FAILED-verification
  warning), code/analysis scripts per version
- results/*.json (all gate metrics), GATES.md + v2/v3/v4/v5 + addenda (all SHA-256'd)
- Prospective nomination: none made - nominating a lab target from a non-transporting
  panel would be dishonest. ATG10's external single-gene AUROC (0.717) is reported as
  post-hoc-selected-on-test and explicitly NOT a validated biomarker.
