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
| 27 | coexpression-mutual-rank | RES-1 | done - NEGATIVE (G1+G2 FAIL, G3 PASS; SNN pivot FAIL) | 2026-09-23T22:56Z |
| 29 | splice-donor-wam | RES-1 | done - G1-G3 PASS (pairwise LR and WAM beat PWM, chrom-held-out; reproduction) | 2026-09-23T23:02Z |
| 31 | go-semsim-ppi | RES-1 | done - G1+G3 FAIL, G2 PASS; post-hoc combination pivot P1+P2 PASS | 2026-09-23T23:29Z |
| 33 | ecg-qrs-consensus | RES-1 | done - NEGATIVE (G1-G3 FAIL; pivot P1+P2 FAIL; Pan-Tompkins F1 0.998 unbeaten) | 2026-09-23T23:33Z |
| 35 | survival-rsf-vs-cox | RES-1 | done - G1-G3 FAIL; post-hoc Cox+RSF rank-ensemble pivot P1+P2 PASS (small, +0.007 C) | 2026-09-23T23:50Z |
| 37 | nuclei-seg-otsu-vs-rf | RES-1 | done - G1 FAIL narrow (+0.024 < 0.03), G2+G3 PASS; pivot P1 FAIL (+0.026), P2 PASS | 2026-09-24T00:08Z |
| 39 | ili-forecast-gbm | RES-1 | done - G1-G3 PASS (GBM relMAE 0.79 vs persistence, 0.49 vs climatology; revised data) | 2026-09-24T00:21Z |
| 41 | remote-homology-rankprop | RES-1 | done - NEGATIVE (G1-G3 FAIL; sparse pivot FAIL; RankProp < SW E-value) | 2026-09-24T00:23Z |
| 43 | crispr-guide-efficiency | RES-1 | done - G1-G4 all PASS (GBM 0.468 vs RS1-ridge 0.293 LOGO; V2 transfer 0.352 vs 0.314; top-decile 0.53) | 2026-09-24T00:31Z |
| 45 | apnea-rr-intervals | RES-1 | done - G1+G2 PASS (M1 AUROC 0.764 vs B1 0.695), G3+G4 FAIL (acc 0.712, rec AUROC 0.835), P1 FAIL | 2026-09-24T00:55Z |
| 47 | afib-rr-irregularity | RES-1 | done - G2+G3+G4 PASS, G1 FAIL (+0.013<0.02), P2 FAIL (+0.010@120b; classic Poincare set saturates) | 2026-09-24T01:40Z |
| 49 | ecg-heartbeat-interpatient | RES-1 | done - G3 PASS (V sens 0.95/0.92); G1,G2,G4,P1,P2 FAIL (documented negative: S unlearnable, morphology hurts linear cross-patient) | 2026-09-24T01:48Z |
| 51 | bbbp-fingerprint-ecfp | RES-1 | done - G1+G3 PASS (M1 0.906 vs B1 0.844, 1-NN 0.779); G2 FAIL (3-desc 0.826); G4 FAIL mis-specified ceiling, documented | 2026-09-24T01:59Z |
| 53 | bace-scaffold-transfer | RES-1 | claimed - protocol in prep | 2026-09-24T02:07Z |
