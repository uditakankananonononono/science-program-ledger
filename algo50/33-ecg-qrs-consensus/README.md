# 33 - QRS detection: multi-detector consensus vs Pan-Tompkins on MIT-BIH (NEGATIVE)

MIT-BIH Arrhythmia DB, lead MLII, paced records excluded, de Chazal DS1 (tuning) / DS2 (scoring) split, 150 ms match tolerance. Detectors from neurokit2 0.2.13. Gates locked before any detector ran (commit d58ceda8).

| Gate | Result | Value (95% CI, 2000 DS2 record bootstraps) |
|---|---|---|
| G1 F1 consensus - Pan-Tompkins >= 0.003 | FAIL | -0.0036 (-0.0064, -0.0015) |
| G2 consensus - best single on DS1 (= Pan-Tompkins) > 0 | FAIL | same |
| G3 fewer DS2 records with F1 < 0.99 | FAIL | 4 vs 0 |

DS2 F1: Pan-Tompkins 0.9982 (sens 99.83%, PPV 99.80%, close to the published 99.3/99.5), Hamilton 0.9946, consensus (5 detectors, k=3) 0.9945, neurokit 0.9829, Elgendi 0.9753, Christov 0.7448 (this implementation/cleaner pairing over-detects badly).

Post-hoc pivot (Amendment 1, locked and pushed before scoring, commit 998a7be7): detector subset and vote threshold chosen jointly on DS1 by generic search (picked PT + Hamilton + Elgendi, k=2). DS2 F1 0.9958 vs 0.9982, -0.0024 (-0.0071, +0.0001). P1 FAIL, P2 FAIL (1 low record vs 0).

Takeaway: when one detector is already near ceiling, voting with weaker detectors trades its few errors for more missed beats. Consensus was below Pan-Tompkins even on the tuning set. Caveats: one library's implementations; a stronger or more diverse detector pool (e.g. learned detectors) might change this.
