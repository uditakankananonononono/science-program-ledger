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
| 18 | pileup-variant-calling | RES-2 | done - G1 FAIL (30x ceiling, both ~0.999), G2+G3+G4 PASS; 4x pivot P1-P3 PASS (BB het F1 0.513 vs 0.175) | 2026-09-24T07:56Z |
| 20 | hwe-exact-vs-chi2 | RES-2 | done - G1-G4 all PASS (chi2 type-I 4.4x exact at MAF 0.05; power cost 0.034) | 2026-09-24T08:03Z |
| 22 | ld-decay-r2 | RES-2 | done - G1+G4 FAIL (naive exp fit recovers 8.8kb of 50kb), G2+G3 PASS; pivot P1-P3 PASS (A+c fit recovers l=18.8kb ~ lambda/2) | 2026-09-24T08:04Z |
| 24 | pwm-vs-consensus-scan | RES-2 | done - G1+G4 PASS (PWM +0.053 AUROC), G2+G3 FAIL; pivot P1+P2 FAIL (PWM edge real but small, ~+0.02) | 2026-09-24T08:05Z |
| 26 | orf-length-gc | RES-2 | done - G1 FAIL (mtb 1.27>1.25), G2 PASS, G3 void-by-construction FAIL; pivot P1+P2 PASS (dinuc correction), P3 FAIL (shadows 2.3-4.5x random) | 2026-09-24T08:06Z |
| 28 | palindrome-depletion | RES-2 | DONE - order-1 null G1+G3+G4 FAIL (incl. artifactual mtb reversal); order-2 pivot P1-P3 PASS (RS depleted beyond palindromes 3/4, ecoli 0.45 vs 0.67) | 2026-09-24T08:25Z |
| 30 | banded-edit-distance | RES-2 | DONE - oracle band exact 100%, 5-6x faster; stable-doubling rule unsound (silent wrong answer); k>=d termination provably exact 300/300 | 2026-09-24T08:12Z |
| 32 | fmindex-exact-match | RES-2 | DONE - G1+G2 PASS (500/500 agreement, byte-exact BWT inversion); G3+G4 FAIL (FM 7x slower than SA binary search at 4.6Mbp in pure Python) | 2026-09-24T08:15Z |
| 34 | quality-weighted-consensus | RES-2 | DONE - PASS all gates: QW strictly dominates, 2.5x lower error at cov=3; cov>=5 both at 0-error floor (G4 vacuous, documented) | 2026-09-24T08:17Z |
| 36 | dust-masking | RES-2 | DONE - masker: 100% region recall, 0.96% false-mask, 100% spurious removal; retention 48/50 misses 98% gate (Q2 FAIL); two earlier FAILs were diagnosed harness artifacts | 2026-09-24T08:20Z |
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
| 55 | molnet-task-pattern | RES-1 | done - G1-G4 ALL PASS (ClinTox gap +0.032, HIV +0.069; 4/4 sign-consistent with 51/53: bulk=descriptor, pocket=substructure) | 2026-09-24T02:16Z |
| 56 | debruijn-contig-vs-k | RES-2 | DONE - original G3+G4 FAIL (gate miscalibration, documented); Amd2 pivot P1-P3 PASS: unresolved = #{R>=k} exactly, N50 3.8k->120kb single contig at k=7000 | 2026-09-24T08:23Z |
| 57 | bioplex-ppi-validation | RES-1 | claimed - user-directed BioPlex follow-up to 31 | 2026-09-24T08:12Z |
| 58 | hmm-viterbi-vs-posterior | RES-2 | DONE - G1-G3 PASS (36% disagreement in hard regime, MPM strictly >= Viterbi); G4 FAIL documented: 98% unreachable at stay=0.90, information-theoretic boundary limit | 2026-09-24T08:26Z |
| 60 | wahlund-heterozygosity | RES-2 | DONE - PASS all gates: F_IS sim matches theory within 0.006 all cells; Ho/He 0.51-0.99 across d; control clean | 2026-09-24T08:28Z |
| 62 | local-vs-global-alignment | RES-2 | DONE - G2+G3 FAIL (detection premise false: SW=NW power vs length-matched null); localization pivot PASS (SW recovers domain 30/30, NW precision 2.9%) | 2026-09-24T08:31Z |
| 64 | rnaseq-gc-bias | RES-2 | claimed - protocol in prep | 2026-09-24T08:32Z |
| 38 | multitest-bh-vs-bonferroni | RES-3 | done - G1-G4 all PASS (BH power 0.612 vs Bonferroni 0.182, FDR 0.043; rho=0.5 FDR 0.039; reproduction) | 2026-09-24T08:05Z |
| 40 | km-vs-naive-censoring | RES-3 | done - G1-G4 all PASS (KM bias +0.00002 at 32% cens, +0.008 at 63%; drop-censored -34%, as-death -27%; reproduction) | 2026-09-24T08:05Z |
| 42 | bootstrap-ci-coverage-skewed | RES-3 | done - NEGATIVE: G1+G4 PASS, G2+G3 FAIL (percentile bootstrap 0.810 cov vs t 0.831 at n=15; not a fix) | 2026-09-24T08:07Z |
| 44 | mr-ivw-vs-egger-pleiotropy | RES-3 | done - G1-G4 all PASS (pleiotropy biases IVW +0.141; Egger -0.010 but 2.9x SD; reproduction) | 2026-09-24T08:07Z |
| 46 | wilcoxon-vs-t-heavy-tails | RES-3 | done - G1-G4 all PASS (t3 tails: Wilcoxon power 0.500 vs Welch 0.387; normal cost 0.026; reproduction) | 2026-09-24T08:08Z |
| 48 | ic50-4pl-vs-interpolation | RES-3 | done - NEGATIVE: G1+G3 FAIL (interp beats free 4PL at Hill 1), G2+G4 PASS; amendment A off-grid P1 FAIL, P2+P3 PASS | 2026-09-24T08:08Z |
| 50 | trial-peeking-pocock | RES-3 | done - G1-G3 PASS (peeking type-I 0.195 -> Pocock 0.050), G4 FAIL narrow (power 0.743 vs 0.750 floor) | 2026-09-24T08:09Z |
| 52 | missing-mar-cc-vs-imputation | RES-3 | done - G1-G4 all PASS (CC bias -0.35; reg-imp +0.002; IPW -0.001; mean-imp SD 0.70; reproduction) | 2026-09-24T08:09Z |
| 54 | epi-growth-rate-poisson-vs-loglinear | RES-3 | done - G1 FAIL narrow (log-linear bias -0.008 < 0.01 gate), G2-G4 PASS (Poisson GLM bias +0.0003, RMSE 0.67x) | 2026-09-24T08:10Z |
