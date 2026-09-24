# algo50/47 - Atrial fibrillation from RR irregularity: boosted windows vs Poincare baseline

Lane RES-1.

## Question
AF detection from the RR tachogram alone (no ECG morphology) is the classic
ambulatory/wearable screening problem. With the same from-scratch QRS front
end as algo50/45: does a boosted model on an extended irregularity feature
set beat the classic Poincare/RMSSD-style linear model, record-held-out, and
can window-level scores recover each record's AF burden?

## Data
MIT-BIH Atrial Fibrillation Database v1.0.0 (physionet-open S3 mirror,
afdb/1.0.0). The 23 records with ECG signal files (04015 ... 08455; 00735 and
03665 excluded as in the database notes). Rhythm labels from the `.atr`
reference annotations (`(AFIB`, `(AFL`, `(N`, etc. in aux_note). ECG 250 Hz,
decimated to 100 Hz before QRS detection. Raw files not committed; sha256 +
retrieval time in `data/`.

## Pipeline
- QRS: the algo50/45 segment-adaptive Pan-Tompkins detector (code reused,
  decimated fs=100). RR outside 0.3-2.0 s dropped.
- Windows: 60 consecutive clean beats, stride 30. A window is AF-positive if
  its center beat falls inside an `(AFIB` rhythm region; inside `(AFL` or
  other non-AFIB regions it counts as negative (AFL folded into negative is
  the harder, declared choice).
- Features per window:
  - B0: RMSSD only.
  - B1 (classic): RMSSD, pNN50, coefficient of variation, Poincare SD1, SD2,
    SD1/SD2 ratio.
  - M1: B1 + sample entropy (m=2, r=0.2sd) + turning point ratio + mean
    absolute successive difference + histogram spread (IQR) + median RR.

## Models
- B0/B1: logistic regression (L2, C in {0.1,1,10} by inner record-held-out CV
  on training records only; B0 fixed C=1.0), standardized per fold.
- M1: HistGradientBoostingClassifier (max_iter 300, lr 0.06, 31 leaves,
  min_samples_leaf 20, L2 1.0, fixed before results).

## Evaluation
Leave-one-record-out over 23 records. Primary metric: pooled AUROC over
held-out windows. Thresholded metrics use the per-fold training Youden-optimal
threshold (training records only). AF burden per record = fraction of the
record's windows labeled AF; predicted burden = mean predicted probability.

## Gates (declared before any model is run)
- G1: pooled record-held-out AUROC(M1) >= AUROC(B1) + 0.02.
- G2: AUROC(B1) >= AUROC(B0) + 0.05.
- G3: at the per-fold training Youden threshold, held-out sensitivity >= 0.90
  AND specificity >= 0.90.
- G4: across the 23 records, Spearman(predicted AF burden, true AF burden)
  >= 0.90.

## Pivot plan (only if gates fail, pre-registered as amendments before results)
- P1: if G3 fails on AFL contamination, rerun with AFL windows EXCLUDED from
  both training and evaluation: gate P1 = sensitivity >= 0.90 and
  specificity >= 0.90 on AFIB-vs-clean-negative windows.
- P2: if G1 fails, window-length ablation (120-beat windows): gate P2 =
  AUROC(M1) >= AUROC(B1) + 0.02 at 120 beats.

## Honest-negatives policy
Every gate outcome is reported PASS/FAIL as declared. Failed gates stay in the
README with their numbers.
