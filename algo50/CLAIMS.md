# algo50 - project number claims

Algorithm studies in bio/medicine (not counted toward the flagship 100). Lane split: RES-1 takes ODD numbers, RES-2 takes EVEN. Claim a number here before starting; pull --rebase before editing.

| # | slug | lane | status | claimed (UTC) |
|---|------|------|--------|---------------|
| 02 | minimizer-read-overlap | RES-2 | done - G1+G2+G4 PASS, G3 speed FAIL (sketch 5.5x smaller, only ~2x wall-time in pure Python) | 2026-09-24T07:34Z |
| 04 | cds-hexamer-discrimination | RES-2 | done - G1 PASS, G2-G4 FAIL (hexamer Markov loses to aa-usage); pivot P1-P3 PASS | 2026-09-24T07:38Z |
| 06 | rna-fold-energy-vs-nussinov | RES-2 | done - G1+G2+G4 PASS, G3 sanity FAIL (Nussinov recall 0.336 < textbook 0.40) | 2026-09-24T07:43Z |
| 08 | nj-vs-upgma-clock | RES-2 | done - G1-G4 all PASS (rate variation: UPGMA nRF 0.228 vs NJ 0.067) | 2026-09-24T07:45Z |
| 10 | tetranuc-contig-binning | RES-2 | done - G1+G2 FAIL (ceiling), G3+G4 PASS; pivot P1 PASS, P2+P3 FAIL (K4 0.768 on close relatives) | 2026-09-24T07:46Z |
| 12 | cpg-hmm-vs-rule | RES-2 | done - G1+G3+G4 FAIL (margin miss, LLR ties rule, over-segments), G2 PASS; pivot P1-P3 PASS | 2026-09-24T07:50Z |
| 14 | shine-dalgarno-scanner | RES-2 | done - G1+G2+G4 PASS (ecoli AUROC 0.79, bsub 0.92, mtb 0.66 boundary), G3 FAIL (position ratio 1.37<1.5) | 2026-09-24T07:52Z |
| 16 | kmer-spectrum-genomesize | RES-2 | done - G1+G4 FAIL (naive area estimator -13%/-30%), G2+G3 PASS; pivot P1+P3 PASS (Poisson fit fixes 30x), P2 FAIL (5x unrecoverable) | 2026-09-24T07:53Z |
| 18 | pileup-variant-calling | RES-2 | claimed - protocol in prep | 2026-09-24T07:56Z |
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
| 53 | bace-scaffold-transfer | RES-1 | done - G1+G2+G4 PASS (BACE substructure-dominated, contrast to BBBP); G3+P1 FAIL (cross-task transfer anti-predictive 0.368/0.378) | 2026-09-24T02:07Z |
| 55 | molnet-task-pattern | RES-1 | claimed - protocol in prep | 2026-09-24T02:16Z |
