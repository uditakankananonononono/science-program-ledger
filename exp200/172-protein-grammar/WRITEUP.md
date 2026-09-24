# DOC-2-072 Protein grammar across families (exp200/172)

**Outcome: documented boundary, not counted. The absolute gate failed; the comparison with alignment passed.**

## Experiment
- Question: can frozen ESM-2 8M embeddings (mean-pooled) recognize the same SCOP fold across unrelated superfamilies?
- Data: SCOPe 2.08 40% domains, 71 folds, 300 queries with their superfamily held out.
- Baseline: Smith-Waterman alignment (BLOSUM62).
- The first run was invalid because of a reference-cap defect. It was fixed and relocked before rerunning.

## Result
- ESM nearest-neighbour fold accuracy 0.14 vs alignment 0.03: about 4x better (McNemar p=1e-7), but below the 0.40 gate.
- By class: all-alpha 0.30 vs 0.04; all-beta 0.22 vs 0.04; alpha/beta 0.09 vs 0.05; alpha+beta 0 vs 0.

## Interpretation
- The embeddings carry cross-superfamily fold signal that alignment misses, mostly in all-alpha and all-beta folds.
- Mixed-topology folds are not recognized.
- Mean-pooled 8M embeddings are too coarse; larger or structure-aware models are the known next step.

## Limits
- Small model, CPU only.
- The 1,500-reference cap left 47 queries without a same-fold reference.
- No tool or nomination is released, because the gate failed.

## Reproduce
code/run.py (primary, defective) and code/pivot1.py. SCOPe FASTA checksum is in data/SHA256SUMS.
