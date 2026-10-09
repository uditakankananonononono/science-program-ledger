# PREREG unit 193 - label-shift-weighted conformal abstention on PTB-XL (locked before any PTB-XL data is downloaded or opened)
Date: 2026-10-10 IST. No PTB-XL waveform, label or metadata file has been opened by the author before this lock.

## Question
Under a pre-specified class-prevalence shift, does a label-shift-weighted split-conformal rule (prevalence estimated from unlabeled data) keep marginal coverage closer to the 90% target than the best of two standard conformal baselines, without raising selective risk?

## Novelty disclosure (verbatim)
Weighted conformal prediction under label shift exists in the literature (e.g. Podkopaev and Ramdas 2021, label-shift-weighted conformal; BBSE prevalence estimation by Lipton et al. 2018). This unit is an incremental, application-level test on ECG diagnostic superclasses. It is not a new method class and will not be claimed as one.

## Data
PTB-XL v1.0.3, PhysioNet, CC BY 4.0, https://physionet.org/content/ptb-xl/1.0.3/ (21,799 records, 18,869 patients). 100 Hz records only (records100). Provided strat_fold 1-10 are used unchanged; folds are patient-disjoint as provided.
Labels: diagnostic superclass (NORM, MI, STTC, CD, HYP) from scp_codes via scp_statements.csv (diagnostic==1, diagnostic_class). A superclass counts as present if any of its SCP codes has likelihood >= 50. Only records with EXACTLY ONE superclass present are used (single-label subset); all others are excluded from every stage. The exclusion count is reported.

## Splits (fixed)
Train: folds 1-6. Calibration: folds 7-8. DEV-check: fold 9. TEST: fold 10 (opened once, only after DEV gates pass).

## Base classifier (frozen, no tuning)
Features per record, per lead (12 leads): mean, std, min, max, skewness, excess kurtosis, and Welch power in bands 0.5-4, 4-10, 10-20, 20-40 Hz (log10 of power + 1e-12). 12 x 10 = 120 features. Classifier: sklearn HistGradientBoostingClassifier(max_iter=200, learning_rate=0.1, max_depth=4, l2_regularization=1.0, random_state=193), trained on Train only. Nothing else is tuned anywhere in this unit.

## Conformal rules, alpha = 0.10 (target coverage 0.90)
Score s(x,y) = 1 - p_hat(y|x). Prediction set C(x) = {k : 1 - p_hat(k|x) <= q}.
B1 split conformal: q = the ceil((n+1)(0.9))/n empirical quantile of calibration scores (true-label scores), n = calibration size.
B2 Mondrian (class-conditional) conformal: one q_k per true class from that class's calibration scores, same quantile rule within class; C(x) = {k : 1 - p_hat(k|x) <= q_k}.
Candidate C: label-shift-weighted split conformal. Weight for calibration record i with true class y_i is w(y_i) = pi_test_hat(y_i)/pi_cal(y_i), pi_cal = class frequencies in the calibration set. q = smallest score value s such that (sum over i with s_i <= s of w_i) / (sum_i w_i + max_k w(k)) >= 0.90. pi_test_hat is estimated WITHOUT test labels by BBSE: solve C pi = mu for pi >= 0 (NNLS, normalized), where C[j,k] = calibration frequency of (predicted class j, true class k) using argmax predictions, and mu = the (weighted, see Shift) predicted-class histogram on the target population.
Reference only (not part of any gate): oracle-weight conformal using the true shift prevalence.

## Shift (pre-specified, label shift only)
Target class prevalence pi_shift = NORM 0.15, MI 0.30, STTC 0.25, CD 0.20, HYP 0.10. On a evaluation fold, each record of class k gets weight pi_shift(k) / (natural fold frequency of k); all shifted metrics are weighted averages with these weights (no resampling). mu for BBSE is the same weighted predicted-class histogram.

## Metrics (on the shifted fold)
Coverage = weighted fraction of records with true class in C(x). Coverage gap = |coverage - 0.90|. Selective risk = weighted error rate among records with |C(x)| = 1, error = the single member is not the true class (records with empty or multi-class sets are abstained). Also reported: weighted singleton rate, mean set size.

## Gates
G0 (base classifier headroom, DEV fold 9, natural prevalence): argmax accuracy >= 0.60, else DROP, TEST unopened.
G1 (DEV fold 9, shifted): primary baseline = whichever of B1/B2 has the smaller DEV coverage gap. Candidate must reduce the DEV coverage gap by >= 25% relative to that baseline (point estimate), else DROP, TEST unopened, recorded as a DEV-gate failure.
Only if G0 and G1 pass is fold 10 opened, once.

## TEST decision rule (fold 10, shifted, run once)
The primary baseline is the one fixed by DEV (not re-picked on TEST). WIN iff all hold: (1) coverage gap reduced by >= 25% relative to that baseline; (2) selective risk of C <= baseline selective risk + 0.005 absolute; (3) the paired patient-cluster bootstrap 95% CI of the coverage-gap reduction (baseline gap minus candidate gap) excludes 0 (B = 2000 resamples of patients with all their fold-10 records, seed 193; weights, BBSE and q recomputed inside each resample on a fixed calibration set); (4) singleton rate of C >= 0.9 x baseline singleton rate. Otherwise the outcome is reported as NULL (gap reduction not shown) or LOSS (candidate gap larger). Natural-prevalence results are reported for context only.

## Disclosures fixed in advance
Single-label subset only. Features are hand-crafted summaries, not a deep model; the base classifier will be modest and the result says nothing about stronger models. PTB-XL labels are cardiologist/automatic mixed annotations. Shift is simulated by reweighting, not a naturally shifted cohort. Any deviation from this file will be documented as a deviation and will void WIN eligibility.
