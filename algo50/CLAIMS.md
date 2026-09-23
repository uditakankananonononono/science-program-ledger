# algo50 - project number claims

Algorithm studies in bio/medicine (not counted toward the flagship 100). Lane split: RES-1 takes ODD numbers, RES-2 takes EVEN. Claim a number here before starting; pull --rebase before editing.

| # | slug | lane | status | claimed (UTC) |
|---|------|------|--------|---------------|
| 01 | spaced-seed-minhash | RES-1 | done - original gates FAIL, pivot 2 PASS | 2026-09-23T16:18Z |
| 03 | signal-peptide-scoring | RES-1 | done - G1+G2 PASS, transfer G3 + pivot FAIL | 2026-09-23T16:27Z |
| 05 | codon-adaptation-expression | RES-1 | done - G1+G2 PASS, G3 FAIL, pivot PASS | 2026-09-23T17:33Z |
| 07 | disorder-segmentation-hmm | RES-1 | done - G1-G3 PASS, G4 transfer narrow FAIL | 2026-09-23T17:37Z |
| 09 | docking-ifp-rescoring | RES-1 | done - G1+G2 PASS, G0 redock FAIL, G3 FAIL (2D similarity beats all) | 2026-09-23T18:28Z |
| 11 | nls-motif-scanner | RES-1 | done - G1+G3 PASS, G2 FAIL; pivot P1+P2 FAIL (documented negative) | 2026-09-23T21:11Z |
| 13 | amp-rule-vs-learned | RES-1 | done - G1-G3 FAIL, pivot P1+P2 FAIL (documented negative: rule beats learned) | 2026-09-23T21:28Z |
| 15 | tissue-specificity-index | RES-1 | done - G1+G2 FAIL, G3 PASS; pivot P1+P2 FAIL (documented negative) | 2026-09-23T21:51Z |
| 17 | thermo-composition | RES-1 | done - G1 PASS (marginal, +1.01C vs 1.0 gate), G2 PASS, G3 transfer FAIL | 2026-09-23T21:56Z |
| 19 | tm-helix-scanner | RES-1 | done - G1+G3 PASS, G2 FAIL; gain mostly from threshold (tuned KD F1 0.879 vs M1 0.911) | 2026-09-23T22:36Z |
| 21 | ss-gor-vs-mlp | RES-1 | done - G1-G3 PASS (reproduction of known direction, not SOTA) | 2026-09-23T22:41Z |
| 23 | disease-gene-rwr | RES-1 | done - G1 PASS (RWR>DN AUROC), G2 FAIL, G3 FAIL (degree correction hurts); small n=23 diseases | 2026-09-23T22:44Z |
| 25 | missense-substitution-score | RES-1 | done - G1-G3 PASS (learned swap score beats BLOSUM62/PAM250, gene-held-out) | 2026-09-23T22:49Z |
