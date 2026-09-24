# algo50/45 - Sleep apnea from RR intervals alone: boosted HRV features vs linear baseline

Lane RES-1.

## Question
Per-minute obstructive apnea detection from nothing but the RR tachogram is a
classic PhysioNet/CinC 2000 challenge problem. This study asks: with
QRS detection and every feature computed from scratch, does a boosted model
on an extended heart-rate-variability feature set beat a linear model on the
classic time-domain set, record-held-out, and are the published performance
levels (~80%+ per-minute accuracy, near-perfect apnea-vs-control record
separation) reproducible?

## Data
PhysioNet Apnea-ECG database v1.0.0 (physionet.org/files/apnea-ecg/1.0.0/,
free, no auth). The 35 annotated learning-set records (a01-a20 apnea,
b01-b05 borderline, c01-c10 control), per-minute labels from the `.apn`
annotations (A = apnea minute, N = normal). ECG sampled at 100 Hz, 16-bit,
read directly from the `.dat`/`.hea` files. The 35 record challenge test set
(x01-x35) has no public per-minute labels and is not used. Raw files are not
committed; sha256 + retrieval time in `data/`.

## Pipeline
- QRS detection: a from-scratch Pan-Tompkins-style detector (bandpass 5-15 Hz
  via cascaded low/high-pass, derivative, squaring, 150 ms moving-window
  integration, adaptive threshold with 250 ms refractory) implemented in
  code/qrs.py. Detected beats give the RR tachogram; RR outside 0.3-2.0 s
  dropped as artifacts.
- Per-minute windows aligned to the annotation minutes. Features per minute:
  - B0 set: mean RR only.
  - B1 set (classic time domain): mean, std, RMSSD, pNN50, coefficient of
    variation, median absolute deviation of RR.
  - M1 set: B1 + frequency domain (Lomb-Scargle power in VLF 0.003-0.04,
    LF 0.04-0.15, HF 0.15-0.4, LF/HF, on the artifact-cleaned tachogram) +
    distribution features (skew, kurtosis, RR range, detrended std via
    first-difference std) + sample entropy (m=2, r=0.2*std) approximated on
    the minute's tachogram.

## Models
- B0/B1: logistic regression (L2, C in {0.1,1,10} by inner record-held-out CV
  on training records only), features standardized per fold.
- M1: HistGradientBoostingClassifier (max_iter 300, lr 0.06, 31 leaves,
  min_samples_leaf 20, L2 1.0, fixed before results).

## Evaluation
Leave-one-record-out over the 35 annotated records (minutes of one record are
never in training). Primary metric: AUROC over held-out minutes; also
per-minute accuracy at threshold 0.5. Record-level score: mean predicted
apnea probability over a record's minutes.

## Gates (declared before any model is run)
- G1: mean record-held-out AUROC(M1) >= AUROC(B1) + 0.02.
- G2 (reproduction sanity): AUROC(B1) >= AUROC(B0) + 0.05.
- G3: per-minute accuracy(M1) >= 0.80, record-held-out.
- G4: record-level separation of apnea (a-records, n=20) vs control
  (c-records, n=10) using mean predicted probability: AUROC >= 0.90.

## Pivot plan (only if gates fail, pre-registered as amendments before results)
- P1: if G3 fails on threshold 0.5, evaluate accuracy at the
  training-fold-optimal threshold (picked on training records only per fold):
  gate P1 = accuracy >= 0.80 at that threshold.
- P2: if G1 fails, feature ablation: gate P2 = M1 restricted to
  time-domain + LF/HF only still >= B1 + 0.02.

## Honest-negatives policy
Every gate outcome is reported PASS/FAIL as declared. Failed gates stay in the
README with their numbers.
