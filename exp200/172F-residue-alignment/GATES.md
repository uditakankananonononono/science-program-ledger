# 172F - follow-up to 172 (DOC-2-072): per-residue ESM-2 soft alignment
Approved by the parent at 11:17 as a fresh experiment on 172's failure mechanism. Locked 2026-09-24 ~11:57 IST, before any per-residue scores were computed.
Failure being attacked: mean-pooling throws away residue order and local motifs (172: mean-pool fold accuracy 0.143, gate 0.40).

## Data and splits
- SCOPe 2.08 40% (the same FASTA and checksum as 172).
- Split 1: exactly 172's pivot1 query and reference IDs (300 queries, held-out superfamily, 1,500 references).
- Split 2 (frozen external): the same construction procedure with seed 7. The query superfamily is chosen from those not used as the split-1 query superfamily where a fold has an alternative. Generated and frozen before scoring.

## Method (fixed; one primary score, no alternatives)
- Frozen ESM-2 8M (facebook/esm2_t6_8M_UR50D) per-residue last-layer embeddings, L2-normalized per residue.
- Soft-alignment score (BERTScore-style bidirectional max): S(q,r) = 0.5 x (mean over q residues of max cosine to r + mean over r residues of max cosine to q).
- Nearest reference by S gives the predicted fold.

## Baselines
- Mean-pooled ESM-2 cosine: the standard embedding-search baseline, as in 172.
- Smith-Waterman BLOSUM62 (named classical baseline): 0.03 on split 1 in 172.

## Gates
- G1: split-1 fold accuracy >= 0.40, AND >= mean-pool + 0.10, AND McNemar p < 0.01 vs mean-pool.
- G2 (frozen external, split 2): accuracy >= 0.30 AND >= mean-pool + 0.08.
- G3 (mechanism; the prediction is that order and local motifs matter most in mixed topology): the soft-alignment gain over mean-pool in class c (alpha/beta) is >= +0.10 on split 1.
- G4: a CLI fold-search tool, plus one prospective nomination (the split-2 query with the largest soft-alignment margin whose Smith-Waterman hit is the wrong fold).
- PASS = G1-G4. Otherwise a boundary. No change of model, score or splits after results.
