# algo50/49 - Inter-patient heartbeat classification (AAMI 5-class) from morphology + RR

Lane RES-1. Protocol hashed and locked before any model ran; Amendment 1 locked before its pivots ran (`results/lock.txt`).

## Bottom line
- Documented negative on the headline hypothesis: the boosted morphology+RR model does NOT clear the +0.02 accuracy bar over the linear model in both inter-patient directions (G1 FAIL: +0.009 DS1->DS2, +0.015 DS2->DS1), and the N/V/F/Q-only pivot P2 also fails (+0.012, +0.014).
- G2 FAIL with a sign reversal worth remembering: RR-only logistic (B0) beats morphology+RR logistic (B1) in the DS2->DS1 direction (0.929 vs 0.869). Linear morphology weights do not transfer across patients; the boosted model recovers the damage (0.885) but only because it is nonlinear.
- G3 PASS: V(entricular) sensitivity 0.946 / 0.917 in the two directions (gate 0.75) - consistent with the de Chazal-era literature.
- G4 FAIL and P1 FAIL: S(upraventricular) sensitivity is 0.100 / 0.175, and oversampling S to 50% of N only reaches 0.154 / 0.275. S is essentially unlearnable inter-patient from single-lead fixed-window morphology + RR with these features. This reproduces the field's known weak point honestly.
- Practical read: inter-patient, RR intervals are the robust signal; raw fixed-window morphology helps a nonlinear model modestly and actively hurts a linear one.

## Data
MIT-BIH Arrhythmia DB v1.0.0 (physionet-open S3), 44 non-paced records in the de Chazal DS1/DS2 split, reference beat positions and AAMI-mapped labels (N/S/V/F/Q; Q has 7-8 beats per split and is reported but meaningless). Test sizes: DS2 51011 beats... (per-class counts in `results/results.json`). MLII channel chosen from the `.hea` description, record 114 negated. Raw not committed; `code/prep.py` re-downloads.

## Methods
Per beat at reference position: RR features (pre, post, pre/local-20-beat mean, pre/record mean), morphology (MLII window -200..+300 ms decimated to 25 z-scored points, window max/min, QRS width at 20% of peak), M1 adds the 25-point first-difference window and relative argmax position. B0 = 4 RR features; B1 = RR + morphology (32 features) logistic with C from 5-fold CV on the training split; M1 = HistGradientBoosting (fixed hyperparameters) on all 58. Both directions evaluated.

## Results
| Direction | B0 acc | B1 acc | M1 acc | M1 V sens | M1 S sens |
|---|---|---|---|---|---|
| DS1->DS2 | 0.917 | 0.925 | 0.934 | 0.946 | 0.100 |
| DS2->DS1 | 0.929 | 0.869 | 0.885 | 0.917 | 0.175 |

P1 (S oversampled): S sens 0.154 / 0.275. P2 (N/V/F/Q only): M1 0.966 vs B1 0.954; 0.898 vs 0.883.

Gate outcomes: G1 FAIL, G2 FAIL, G3 PASS, G4 FAIL; P1 FAIL, P2 FAIL. Figure: `results/fig_interpatient.png`.

## Caveats
- Reference beat positions are used (declared); detector error is out of scope (algo50/45 owns detection quality).
- F and Q classes are too small (a few hundred / <10 beats) for meaningful sensitivity; reported but not gated.
- The linear C search uses accuracy on stratified folds of the training split, which favors the majority class; a balanced-C search might narrow but not reverse the G2 gap.
- Single lead (MLII); the literature's best inter-patient numbers use two leads and patient-adaptive schemes, which by definition break the pure inter-patient frame.

## Next steps
Patient-adaptive hybrid (small per-patient calibration set) as a separate declared study; learnable morphology (small CNN) under the same split to test whether the G2 reversal is linearity-specific; two-lead features.

## Reproduce
`python3 code/prep.py && python3 code/run49.py && python3 code/amend1.py && python3 code/figure.py` (needs wfdb, numpy, scipy, pandas, scikit-learn, matplotlib).
