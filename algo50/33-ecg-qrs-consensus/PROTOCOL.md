# 33 - QRS detection: multi-detector consensus vs Pan-Tompkins on MIT-BIH

Locked before any detector is run.

Data: MIT-BIH Arrhythmia Database (PhysioNet mitdb, 48 half-hour records, 360 Hz), lead MLII (channel 0). Paced records 102, 104, 107, 217 excluded. Split per de Chazal et al. 2004: DS1 (22 records: 101,106,108,109,112,114,115,116,118,119,122,124,201,203,205,207,208,209,215,220,223,230) for choosing the one free parameter; DS2 (22 records: 100,103,105,111,113,117,121,123,200,202,210,212,213,214,219,221,222,228,231,232,233,234) for scoring.
Reference: beat annotations (symbols N L R B A a J S V r F e j n E / f Q ?). Match: greedy one-to-one, tolerance 150 ms (54 samples). Whole record.

Detectors (independent implementations in neurokit2 0.2.13, each with its paired cleaning filter where one exists, else "neurokit"):
- Baseline: Pan & Tompkins 1985 (pantompkins1985).
- Others: hamilton2002, elgendi2010, christov2004, neurokit.
Method: consensus voting. Pool all 5 detectors' peaks, greedily cluster sorted peaks within 75 ms, keep clusters supported by >= k distinct detectors, place the beat at the median sample. k in {1..5} chosen on DS1 by pooled F1.

Metrics on DS2: pooled sensitivity, PPV, F1 (summed TP/FP/FN). 95% CI from 2000 bootstraps over DS2 records (seed 33).
Gates:
- G1 (headline): F1(consensus) - F1(Pan-Tompkins) >= 0.003, CI lower bound > 0.
- G2: F1(consensus) - F1(best single detector chosen on DS1) > 0, CI lower bound > 0.
- G3: number of DS2 records with F1 < 0.99 is lower for consensus than for Pan-Tompkins.
If G1 fails: one post-hoc pivot, locked and pushed before scoring.
Caveats declared: neurokit2's Pan-Tompkins is one implementation; published PT figures on MIT-BIH (99.3% sens, 99.5% PPV) are higher than many reimplementations reach, so both are reported. Consensus of existing detectors is an engineering method, not a new detector.

## Amendment 1 - pivot (POST HOC, locked before the pivot was scored)
Original result preserved (results/metrics_original.json): G1-G3 FAIL. Pan-Tompkins (neurokit2) reached DS2 F1 0.998, near published figures; 5-detector consensus (k=3 chosen on DS1) got 0.9945. christov2004 over-detected badly (DS1 F1 0.67). Chosen after seeing DS2 results, so disclosed as post hoc. Pivot keeps the method family but moves all choices to DS1 by a generic search rather than hand-dropping detectors:
- Consensus over a detector subset S (all subsets of size >= 3 of the 5 detectors) with vote threshold k in {2..|S|}; (S, k) chosen jointly by DS1 pooled F1 (ties: smaller S, then larger k). Scored once on DS2.
- P1: F1(pivot) - F1(Pan-Tompkins) > 0, CI lower bound > 0 (2000 DS2 record bootstraps, seed 33).
- P2: DS2 records with F1 < 0.99 for pivot <= Pan-Tompkins (0).
No further pivots.
