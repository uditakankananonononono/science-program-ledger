# algo50/45 - Sleep apnea from RR intervals alone: boosted HRV features vs linear baseline

Lane RES-1. Protocol hashed and locked before any model ran; Amendment 1 locked before its pivot ran (`results/lock.txt`).

## Bottom line
- Mixed outcome: the ranking gates passed, the deployment-style gates failed.
- G1 PASS: boosted trees on the extended HRV set reach pooled record-held-out AUROC **0.764** vs 0.695 for logistic regression on the classic time-domain set (+0.069 >= 0.02).
- G2 PASS: B1 beats the mean-RR-only baseline by 0.528 AUROC (>= 0.05). B0's pooled AUROC is 0.167 - far below chance - because the sign of the mean-RR/apnea relationship flips across records: apnea minutes have longer mean RR in 20 records (mostly severe a-records, bradycardia during events) and shorter in 11 (mostly b/c, arousal tachycardia). A single linear coefficient cannot survive record-held-out pooling.
- G3 FAIL: per-minute accuracy at threshold 0.5 is 0.712 (< 0.80). P1 FAIL too: choosing the threshold on training records per fold gives 0.713 (< 0.80) - the chosen threshold's median is 0.50, so threshold tuning buys nothing. The 0.80 bar came from literature using expert-annotated QRS complexes; with a from-scratch detector on the raw ECG, ~0.71 is what RR-only features deliver here.
- G4 FAIL (honest negative): record-level apnea-vs-control separation (mean predicted probability, 20 a- vs 10 c-records) reaches AUROC 0.835 (< 0.90). Borderline b-records score between, as they should; the miss is overlap between the mildest a-records and the noisiest c-records.

## Data
PhysioNet Apnea-ECG v1.0.0, 35 annotated learning-set records (a01-a20, b01-b05, c01-c10), 17,012 labeled minutes (38.3% apnea). ECG 100 Hz 16-bit read from `.dat`/`.hea`; per-minute labels from `.apn`. Downloaded from the physionet-open S3 mirror (physionet.org direct was throttled to ~10 KB/s mid-transfer); provenance + sha256 via `code/prep.py` (`data/`, raw not committed).

## Methods
QRS: from-scratch Pan-Tompkins integer-filter front end (lfilter low/high-pass, derivative, squaring, 150 ms integration) with segment-adaptive thresholding (10 s segments, median + 0.35x(97th-median) percentile threshold, 250 ms refractory, <350 ms peak dedup by MWI amplitude) - the plain adaptive-threshold loop failed on the clipped high-artifact records (a03 yielded 7 beats before the fix). Detector output sanity: 61-79 bpm and >= 99.6% clean RR on the five early-downloaded records. RR outside 0.3-2.0 s dropped. Per-minute features: B0 mean RR; B1 classic time domain (mean, std, RMSSD, pNN50, CV, MAD); M1 adds Lomb-Scargle VLF/LF/HF + LF/HF, skew, kurtosis, range, first-difference std, sample entropy (m=2, r=0.2sd). B0 C=1.0 fixed (single feature); B1 logistic C in {0.1,1,10} by inner record-held-out CV (training minutes subsampled to 6,000 per inner fit); M1 HistGradientBoosting fixed hyperparameters. Leave-one-record-out over all 35 records.

## Results
| Metric | B0 | B1 | M1 |
|---|---|---|---|
| Pooled LORO AUROC | 0.167 | 0.695 | 0.764 |
| Per-minute accuracy @0.5 | - | 0.686 | 0.712 |

P1 (training-chosen threshold): 0.713. Record-level a-vs-c AUROC (M1): 0.835.

Gate outcomes: G1 PASS, G2 PASS, G3 FAIL, G4 FAIL; P1 FAIL. Figure: `results/fig_scores.png`. Full numbers: `results/results.json`, `results/amend1.json`, `results/minute_predictions.csv`.

## Caveats
- Pooled AUROC mixes within-record and across-record discrimination; per-record calibration differs, which is exactly why G3/G4 fail while G1/G2 pass.
- The QRS detector is from scratch and unvalidated against the challenge's expert annotations on these records; detector noise is part of the measured pipeline cost.
- Sample entropy is computed on raw per-minute tachograms (short, irregular); it is a weak feature here, kept for completeness.
- The b-records (borderline) are in the training pool; some literature drops them.

## Next steps
Per-record z-scored features (calibrate to the record's own night) as a declared amendment - the sign-flip finding says record-relative features should fix G4; evaluate against the expert QRS annotations to isolate detector error; add cyclical HR pattern features (Penzel's PSD approach).

## Reproduce
`python3 code/prep.py && python3 code/run45.py && python3 code/amend1.py && python3 code/figure.py` (needs wfdb, numpy, scipy, pandas, scikit-learn, matplotlib).
