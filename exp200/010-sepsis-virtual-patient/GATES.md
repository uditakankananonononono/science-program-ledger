# DOC-1-010 GATES - A Virtual Patient for Sepsis Prediction
Locked 2026-09-24 04:41 IST by EXP-1 BEFORE any model training, scoring, or outcome evaluation.
Dataset: PhysioNet/CinC Challenge 2019 "Early Prediction of Sepsis from Clinical Data" v1.0.0 (public).
Source of truth: https://physionet.org/content/challenge-2019/1.0.0/ via AWS Open Data mirror s3://physionet-open/challenge-2019/1.0.0/ (manifest + per-file MD5 ETags recorded in PROVENANCE.md at download time).

## Task definition (locked)
Patient-level early sepsis prediction. For septic patients, the record is TRUNCATED at the first hour with SepsisLabel=1 (the organizers shift labels 6h before clinical onset, so this cutoff is >=6h pre-onset; features use only data strictly before that hour). For non-septic patients the full record is used. Label: patient ever labeled septic. Features: per-patient aggregates over the retained window (last/min/max/mean/slope of vitals+labs, measurement recency, missingness, demographics). No information from after the truncation point is used. This is the "virtual patient" risk model: given an ICU patient's early course, will this patient become septic?

## G1 - Named published baseline benchmark (beat or document loss)
Baselines computed by us from the SAME frozen set B patients at the SAME truncation points, per published definitions:
- SIRS criteria count (Bone et al., ACCP/SCCM 1992): Temp>38 or <36, HR>90, Resp>20, WBC>12k or <4k.
- qSOFA (Seymour et al., JAMA 2016): Resp>=22, SBP<=100; altered mentation unavailable in this dataset -> 2-criterion variant, limitation documented in report.
- NEWS (Royal College of Physicians, 2012): Resp, O2Sat, Temp, SBP, HR, supplemental-O2 proxy (FiO2>0.21), consciousness unavailable -> documented.
- Partial SOFA (Vincent et al., Intensive Care Med 1996): platelets, bilirubin, MAP, creatinine subscores (PaO2/GCS unavailable -> 4-organ partial, documented).
Gate G1 PASS iff trained-model AUROC on frozen set B STRICTLY EXCEEDS the best clinical-score AUROC on set B. A loss is reported as a documented boundary, not hidden.

## G2 - Frozen cross-hospital external validation
Training and all tuning (including threshold/hyperparameter choices) use set A ONLY (20,336 patients, hospital system A) with an internal A split. Set B (20,000 patients, different hospital systems) remains untouched until exactly ONE final scoring pass. Gate G2 PASS iff set-B AUROC >= 0.75 AND set-B AUROC drop vs set-A internal validation <= 0.08 (cross-hospital transport bound).

## G3 - Mechanistic interpretation vs sepsis literature
Top-10 model features by importance must be interpreted against sepsis pathophysiology (lactate/hypoperfusion, MAP, SIRS vitals, WBC) per Surviving Sepsis Campaign (Evans et al. 2021) and Sepsis-3 (Singer et al. JAMA 2016). PASS iff the dominant signals are physiologically coherent or any incoherence is specifically explained.

## G4 - Working tool + prospective nomination
sepsis_risk.py CLI: takes a patient .psv (challenge format), outputs risk score + top contributing features. Smoke-tested. One prospective validation nomination: an ICU early-warning / sepsis research group (named in REPORT.md).

## Failure tree (locked, per no-re-fishing rule)
If G1 or G2 FAILS on the single frozen set-B scoring pass: NO new arms, NO threshold changes, NO reformulation. The result is reported as a documented boundary with the failure analysis. Published challenge-reference numbers (Reyna et al., Critical Care Medicine 2020; winner normalized utility 0.360) are context only, not gates.
