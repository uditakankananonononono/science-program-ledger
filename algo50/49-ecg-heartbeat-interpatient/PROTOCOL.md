# algo50/49 - Inter-patient heartbeat classification (AAMI 5-class) from morphology + RR

Lane RES-1.

## Question
Heartbeat classification is easy intra-patient and hard inter-patient - the
de Chazal (2004) result. With from-scratch morphology features (no learned
embeddings), does a boosted model beat the classic linear model under a true
inter-patient split, and are published inter-patient sensitivities for the
ectopic classes (S, V) reproducible?

## Data
MIT-BIH Arrhythmia Database v1.0.0 (physionet-open S3 mirror, mitdb/1.0.0),
the 44 non-paced records in the standard de Chazal split:
- DS1: 101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230
- DS2: 100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234
Beat positions and labels from the reference `.atr` annotations (declared:
we classify at reference positions; detector error is out of scope here -
algo50/45 owns the detector). AAMI mapping: N,L,R,e,j -> N; A,a,J,S -> S;
V,E -> V; F -> F; /,f,Q,p -> Q. Modified limb lead II (channel 0; record 114
is inverted - negated per the database notes; records 102/104 use channel 1
as MLII - handled by using the channel whose `.hea` description contains
"MLII" when present, else channel 0). ECG 360 Hz, raw files not committed.

## Features per beat
- RR: pre-RR, post-RR, pre-RR/local-mean-RR (20 beats), pre-RR/record-mean-RR.
- Morphology: MLII samples from -200 ms to +300 ms around the R peak,
  decimated to 25 points, amplitude-normalized per beat (z-score of the
  window), plus window max amplitude, min amplitude, and QRS width estimate
  (span where |signal| > 20% of window peak around the R).
- B0: the 4 RR features only.
- B1: RR + morphology summary (max, min, width, and the 25-point window).
- M1: B1 + the same window of the first difference of the signal (25 points)
  + position of window max relative to R.

## Models
- B0/B1: logistic regression (L2, C in {0.1,1,10} by 5-fold CV on the
  training split only), standardized.
- M1: HistGradientBoostingClassifier (max_iter 300, lr 0.06, 31 leaves,
  min_samples_leaf 20, L2 1.0, fixed before results).
- Multiclass, one model, 5 classes; evaluation both directions
  (train DS1/test DS2 and train DS2/test DS1).

## Gates (declared before any model is run)
- G1: overall accuracy(M1) >= accuracy(B1) + 0.02 in BOTH directions.
- G2: accuracy(B1) >= accuracy(B0) + 0.05 in both directions.
- G3: V-class sensitivity(M1) >= 0.75 in both directions.
- G4: S-class sensitivity(M1) >= 0.55 in both directions (S is the class the
  literature loses most often inter-patient).

## Pivot plan (only if gates fail, pre-registered as amendments before results)
- P1: if G4 fails, class-conditional sampling (oversample S in training to
  50% of N count): gate P1 = S sensitivity(M1) >= 0.55 in both directions.
- P2: if G1 fails, report per-class breakdown and test whether the failure is
  S-specific: gate P2 = accuracy(M1) >= accuracy(B1) + 0.02 on N/V/F/Q only.

## Honest-negatives policy
Every gate outcome is reported PASS/FAIL as declared. Failed gates stay in the
README with their numbers.
