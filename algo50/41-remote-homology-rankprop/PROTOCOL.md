# 41 - Remote homology detection: RankProp network diffusion vs Smith-Waterman (SCOPe 2.08)

Locked before any alignment is computed.

Data: SCOPe 2.08 ASTRAL genetic-domain sequences, <40% identity subset, classes a-d (13,819 domains). Random sample of 4,000 domains (seed 41) = database. Queries: every sampled domain with >= 2 remote homologs in the sample (same superfamily, different family): 2,826 queries.
Labels per query: positive = same superfamily, different family; negative = different fold; ignored = same family, or same fold but different superfamily.

Scores: Smith-Waterman local alignment (Smith & Waterman 1981), BLOSUM62, gap open 11 / extend 1 (parasail 2.6.1), all-vs-all over the 4,000 database domains.
- Baseline B1: SW E-value ranking, E = K m n N exp(-lambda S), lambda 0.267, K 0.041 (BLOSUM62 11/1 gapped Karlin-Altschul), N = 4,000. Length-corrected; the main baseline.
- Baseline B0 (reported): raw SW score.
- Method: RankProp (Weston et al. 2004, PNAS): database graph K_ij = exp(-E_ij / sigma), sigma = 100, diagonal zero, columns normalized to sum 1; query vector y0_i = exp(-E_qi / sigma); iterate y <- y0 + alpha K y, alpha = 0.95, 20 iterations; rank by y. Query excluded from its own ranking and from the graph walk start. Paper settings, not tuned.

Metrics per query: AUROC (positives vs negatives) and ROC50 (normalized area up to 50 false positives), averaged over queries. 95% CI from 2000 bootstraps over queries (seed 41).
Gates:
- G1 (headline): mean AUROC (RankProp - B1) >= 0.03, CI lower bound > 0.
- G2: mean ROC50 (RankProp - B1) > 0, CI lower bound > 0.
- G3: RankProp AUROC >= B1 on >= 60% of queries.
If G1 fails: one post-hoc pivot, locked and pushed before scoring.
Caveats declared: RankProp's original used PSI-BLAST E-values on a larger database; this uses plain SW on a 4,000-domain sample; transductive: the query ranking uses the unlabeled database graph (as in the paper), labels never used.

## Amendment 1 (engineering, before any score)
evaluate.py: the RankProp iteration is run for all queries at once as a matrix product (identical math, same 20 iterations) instead of one query at a time, for runtime.
