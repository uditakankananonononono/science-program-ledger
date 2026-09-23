# 29 - Splice donor recognition: PWM vs WAM vs MaxEnt-style pairwise model (PASS, reproduction)

Train hg38 chr1-3, test chr21+22 (chromosome held out). GENCODE v44 canonical GT donors (9-mer) vs random genomic GT decoys. Test: 8582 donors, 1.22M decoys. Gates locked before scoring (commit 40926d1; Amendment 1 = memory fix, equivalent math, before any score).

| Gate | Result | Value (95% CI, 1000 stratified bootstraps) |
|---|---|---|
| G1 auPRC MaxEnt-style - PWM >= 0.03 | PASS | +0.045 (0.040, 0.050) |
| G2 auPRC WAM - PWM > 0 | PASS | +0.030 (0.027, 0.033) |
| G3 FPR@90% sens MaxEnt <= 0.8 x PWM | PASS | 0.053 vs 0.085 (diff 0.032, CI 0.029-0.035) |

auPRC: PWM 0.241, WAM 0.271, MaxEnt-style pairwise LR 0.285.

This reproduces a known result (Zhang & Marr 1993; Yeo & Burge 2004): modelling dependencies between donor positions beats a position-independent matrix. Not state of the art; deep models using wider context do much better. Caveats: decoys are random GT sites, not cryptic splice sites; 9-mer window only; the pairwise model is a logistic-regression stand-in for MaxEntScan, not MaxEntScan itself; low absolute auPRC reflects the 1:142 class ratio.
