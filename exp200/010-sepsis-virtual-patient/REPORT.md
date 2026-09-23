# DOC-1-010 REPORT - A Virtual Patient for Sepsis Prediction
EXP-1, 2026-09-24. Gates locked BEFORE outcomes (GATES.md, commit dcc7c50). All gate criteria below are the locked ones, unchanged.

## Data (PROVENANCE.md)
PhysioNet/CinC Challenge 2019 v1.0.0, AWS Open Data mirror, integrity-verified (0 size mismatches, 0/600 MD5 spot-check mismatches vs S3 ETags; aggregate manifest SHA-256s recorded). Patient-level features from hourly vitals+labs; septic records truncated strictly before the first label hour (labels are shifted 6h pre-onset by the organizers, so all features are >=6h pre-onset). Excluded: 250 (A) / 252 (B) patients with no pre-label window (already septic at admission).

## Cohorts
- Train/tune: set A only, 20,086 patients (7.67% sepsis), internal 80/20 stratified split; ALL tuning on A.
- Frozen external validation: set B, 19,748 patients (4.51% sepsis), different hospital systems, touched exactly once for final scoring.

## Results vs locked gates
- Model: HistGradientBoostingClassifier, 194 aggregate features. Set-A internal validation: AUROC 0.9548, AUPRC 0.8396.
- G2 (frozen cross-hospital): set-B AUROC 0.8813 (locked bar >= 0.75: PASS); transport drop 0.0735 (locked bound <= 0.08: PASS). AUPRC on B 0.4618 vs prevalence 4.51% (10.2x baseline).
- G1 (named published baselines, computed by us from the same set-B patients at the same truncation points): SIRS 0.6378, qSOFA 0.5771, NEWS 0.7022, partial SOFA 0.5753. Model 0.8813 STRICTLY EXCEEDS the best (NEWS) by +0.179 AUROC: PASS. Baseline limitations per locked gates: qSOFA is the 2-criterion variant (no mentation data); NEWS lacks consciousness; SOFA is 4-organ partial (no PaO2/GCS).
- G3 (interpretation): top importances mix physiology and care process. Physiological signals are coherent with SIRS/Sepsis-3: Temp_last, Resp_min (fever/tachypnea), FiO2 recency (recent oxygen therapy -> hypoxemia proxy). Care-process signals (window_hours, SBP_n measurement frequency, *_hrs_since recency, Unit1 MICU/SICU) are documented EHR monitoring-intensity confounders (sicker patients are measured more); their presence is expected and documented rather than hidden. No incoherent dominant signal found: PASS with caveat.
- G4 (tool + nomination): code/sepsis_risk.py CLI scores any patient .psv with risk + top contributing features; smoke-tested on 4 patients across both sets (septic 0.962/0.993, non-septic 0.008/0.013). Prospective nomination: Prof. Matthew Churpek's lab (University of Wisconsin; eCART deterioration-prediction program) for silent-mode prospective validation on a live ICU stream.

## Honest limits
- The known A->B prevalence shift (7.67% -> 4.51%) costs AUPRC (0.84 -> 0.46) while AUROC holds; threshold deployment would need recalibration per site.
- qSOFA/NEWS/SOFA comparisons are limited by missing mentation/PaO2 fields (stated in locked gates).
- 502 patients already septic at ICU entry are out of scope for early prediction.

## Verdict
G1 PASS, G2 PASS, G3 PASS (documented caveat), G4 PASS. Submitted for adjudication as a counted experiment.
