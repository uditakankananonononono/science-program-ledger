# 014F GATES ADDENDUM A — AMPlify cutoff correction (locked 2026-09-24 13:26 IST, before any gate scoring)

Mechanics correction only; all gate thresholds unchanged.
GATES.md locked AMPlify's threshold as "its published score cutoff 5.0". The cloned BCGSC
repo README states the published default: sequences with AMPlify log-scaled score > 3.01
(probability > 0.5) are predicted AMPs. The AMPlify judge threshold is therefore the
PUBLISHED 3.01 (log-scaled), i.e. probability > 0.5 - this corrects a transcription error
in GATES.md before any scoring. amPEPpy threshold (probability >= 0.5) stands as locked.
Judge independence note: amPEPpy (RF on physicochemical features) and AMPlify (deep
attention model) are independently trained published predictors, both independent of the
Macrel guide.
