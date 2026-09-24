# algo50/47 - Atrial fibrillation from RR irregularity: boosted windows vs Poincare baseline

Lane RES-1. Protocol hashed and locked before any model ran; Amendment 1 locked before its pivot ran (`results/lock.txt`).

## Bottom line
- The classic feature set nearly saturates this problem, and that is the finding.
- G1 FAIL (honest negative): boosted trees on the extended set reach pooled record-held-out AUROC 0.9872 vs 0.9742 for logistic regression on the 6 classic features - a +0.013 edge, below the declared +0.02. P2 FAIL too: at 120-beat windows the edge shrinks to +0.010 (B1 0.9771, M1 0.9874); longer windows saturate the classic features further instead of helping the boosted model.
- G2 PASS: the classic set beats RMSSD alone by +0.101 AUROC (>= 0.05; B0 0.873).
- G3 PASS: at per-fold training-chosen Youden thresholds, held-out sensitivity 0.916 and specificity 0.957 (both >= 0.90).
- G4 PASS: predicted AF burden (mean window probability) tracks true burden across the 23 records at Spearman 0.958 (>= 0.90), with no per-record calibration.
- Practical read: for RR-only AF screening, a 6-feature logistic model is within ~1 AUROC point of a boosted model; spend complexity on sensor quality and longer recordings, not on the classifier.

## Data
MIT-BIH AFDB v1.0.0 (physionet-open S3 mirror), the 23 records with ECG files; 35,922 windows of 60 clean beats (stride 30), 42.9% AF-positive. Rhythm labels from `.atr` aux_note markers; window positive iff its center beat is inside an `(AFIB` region; `(AFL` counts as negative (declared harder choice). ECG 250 Hz resampled 2/5 to 100 Hz. Raw not committed; `code/prep.py` re-downloads with provenance.

## Methods
Same from-scratch segment-adaptive Pan-Tompkins QRS detector as algo50/45. RR outside 0.3-2.0 s dropped. Features per window: B0 RMSSD; B1 = RMSSD, pNN50, CV, Poincare SD1/SD2/ratio; M1 = B1 + sample entropy, turning-point ratio, mean |successive diff|, IQR, median RR. B0 C=1.0; B1 logistic C in {0.1,1,10} by inner record-held-out CV; M1 HistGradientBoosting fixed hyperparameters. Leave-one-record-out over all 23 records.

## Results
| Metric | B0 | B1 | M1 |
|---|---|---|---|
| Pooled LORO AUROC (60-beat) | 0.8731 | 0.9742 | 0.9872 |
| Pooled LORO AUROC (120-beat, P2) | - | 0.9771 | 0.9874 |

G3: sens 0.916, spec 0.957. G4: burden Spearman 0.958.

Gate outcomes: G1 FAIL, G2 PASS, G3 PASS, G4 PASS; P2 FAIL. Figure: `results/fig_auroc_burden.png`. Full numbers: `results/results.json`, `results/amend1.json`, `results/window_predictions.csv`.

## Caveats
- AFL windows count as negatives; some contain AF-like irregularity, which caps every model's achievable AUROC. The declared P1 path (exclude AFL) was not needed since G3 passed.
- Window center labeling mislabels windows straddling rhythm transitions (bounded by the 60-beat span).
- QRS detection is from scratch and unvalidated against the database's own `.qrs` files; detector error is part of the measured pipeline.
- AUROC is pooled across records; per-record operating points vary.

## Next steps
Onset/offset localization error (detect transitions, not just windows); per-record adaptive thresholds; test on the Long-Term AF Database for transfer; compare against the database's own `.qrs` detections to isolate detector error.

## Reproduce
`python3 code/prep.py && python3 code/run47.py && python3 code/amend1.py && python3 code/figure.py` (needs wfdb, numpy, scipy, pandas, scikit-learn, matplotlib).
