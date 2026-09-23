# 29 - Splice donor recognition: PWM vs WAM vs MaxEnt-style pairwise model

Locked before any model is fit or scored.

Data: hg38 chr1,2,3,21,22 (UCSC) + GENCODE v44 basic GTF. Positives: annotated donor sites (last exonic 3 nt + first 6 intronic nt, 9-mer as in MaxEntScan), canonical GT only (non-canonical GC/AT excluded, ~2%). Decoys: random genomic GT dinucleotides on either strand that are not annotated donors, same 9-mer window (seed 29). Duplicates kept as observed.
Split: train chr1-3 (~60k pos, ~1.2M decoys); test chr21+22 (~8.6k pos, ~1.22M decoys). No test data used for any fitting or choice.

Models (all fit on train only):
- M0 PWM baseline: position-independent log-odds (Staden / Shapiro-Senapathy weight matrix; the "WMM" baseline in Yeo & Burge 2004), pseudocount 1.
- M1 WAM: first-order Markov log-odds (Zhang & Marr 1993), pseudocount 1.
- M2 MaxEnt-style: L2 logistic regression on single-position and all pairwise-position dinucleotide one-hot features (9 + 36 pairs), C=1.0 fixed, liblinear. Stands in for the pairwise dependencies MaxEntScan models (Yeo & Burge 2004); not a reimplementation of MaxEntScan.

Metrics on test: auPRC (average precision) at the natural decoy ratio; FPR at 90% sensitivity. 95% CI from 1000 stratified bootstrap resamples (positives and decoys resampled separately), seed 29.

Gates:
- G1 (headline): auPRC(M2) - auPRC(M0) >= 0.03, CI lower bound > 0.
- G2: auPRC(M1) - auPRC(M0) > 0, CI lower bound > 0.
- G3: FPR90(M2) <= 0.8 x FPR90(M0), and CI of FPR90(M0) - FPR90(M2) lower bound > 0.
If G1 fails: one post-hoc pivot, locked and pushed before scoring.
Caveats declared up front: decoys are random GT sites, not cryptic splice sites, so absolute numbers overstate real-genome accuracy; 9-mer only; known direction in the literature (this is a reproduction, not SOTA).

## Amendment 1 (engineering only, before any score was produced)
First run was killed for memory (2 GB sandbox) before fitting finished; no metric was computed. Changes, all mathematically equivalent: M2 is fit on unique 9-mers with duplicate counts as sample weights (identical L2 objective); bootstrap resampling is done as multinomial count weights with a weighted average-precision / FPR90 routine (sklearn AP also reported on the full test set as a check). Models, data, gates unchanged.
