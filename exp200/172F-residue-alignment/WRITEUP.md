# 172F - per-residue ESM-2 soft alignment (follow-up to 172): BOUNDARY, clean negative (not counted)

Gates were locked before scoring (commit be92a9ab, which includes the frozen split 2).

| split | soft alignment | mean-pool | McNemar (soft-only / mean-only hits) |
|---|---|---|---|
| split 1 (172 queries) | 0.100 | 0.143 | 8 / 20, p = 0.036 (worse) |
| split 2 (frozen, new query superfamilies) | 0.123 | 0.180 | 11 / 28, p = 0.009 (worse) |

- G1 FAIL, G2 FAIL, G3 FAIL. Class c: 0.06 vs 0.09 on split 1.
- Soft alignment loses in every class except class d, where both are near zero.
- G4: no tool is released. The method is worse than its own baseline.

## Why (mechanism)
- The locked score is a bidirectional max-match: every residue takes its best partner anywhere in the other protein. That keeps local detail but still ignores order, and it adds noise.
- In a small 8M model, residue embeddings are generic enough that almost every residue finds a close match in any protein. The score then drifts toward composition and length, and fold identity gets diluted.
- Mean-pooling averages that noise away, which is why it does better.
- Lesson: residue-level detail helps only with an order-preserving alignment (dynamic programming over a denoised similarity matrix, as in EBA, Pantolini et al.). Unordered max-matching does not help. The 172 boundary stands. An EBA-style ordered alignment would be the next distinct attack, not a retry of this gate.

## Reproduce
code/splits.py (frozen split 2), then code/run.py. Results are in results/results.json. Data is the same SCOPe FASTA as 172 (checksum in 172/data/SHA256SUMS).
