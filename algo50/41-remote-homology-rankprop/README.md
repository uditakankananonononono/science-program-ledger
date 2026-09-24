# 41 - Remote homology: RankProp network diffusion vs Smith-Waterman on SCOPe 2.08 (NEGATIVE)

SCOPe 2.08 ASTRAL <40% domains, classes a-d, 4,000-domain random sample; 2,826 queries with >= 2 remote homologs (same superfamily, different family); negatives = different fold. All-vs-all Smith-Waterman (BLOSUM62, 11/1, parasail). Gates locked before any alignment (commit fa2000aa; Amendment 1 = batched iteration, identical math).

| Gate | Result | Value (95% CI, 2000 bootstraps over queries) |
|---|---|---|
| G1 mean AUROC RankProp - SW E-value >= 0.03 | FAIL | -0.048 (-0.053, -0.043) |
| G2 mean ROC50 RankProp - SW E-value > 0 | FAIL | -0.022 (-0.024, -0.019) |
| G3 RankProp >= SW on >= 60% of queries | FAIL | 37% |

Mean AUROC: raw SW 0.744, SW E-value 0.745, RankProp 0.697. ROC50: 0.272 / 0.278 / 0.257.

Post-hoc pivot (Amendment 2, locked and pushed before scoring, commit f16a25c1): sparsify the graph to edges with E <= 10. AUROC -0.046 (-0.052, -0.041) FAIL; ROC50 -0.004 (-0.008, +0.001) FAIL (now level with SW, not better).

Why it fails here: exp(-E/100) is exactly zero for most unrelated and many remote pairs, so RankProp scores the long tail as ties at zero while the E-value ranking still orders it; full-list AUROC punishes that. At the top of the list (ROC50) the sparse version ties SW but does not beat it. The published RankProp gain used PSI-BLAST E-values (more sensitive) on a much larger database, which gives the walk more real edges; a 4,000-domain sample with plain SW is too sparse for diffusion to find new remote homologs.

Caveats: not a replication of the paper's setup (PSI-BLAST, full SCOP database); sigma and alpha were the paper's values, not tuned.
