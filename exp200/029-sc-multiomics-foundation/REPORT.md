# DOC-1-029: A Foundation Model for Single-Cell Multi-Omics
**Claim** (locked pre-outcomes): the foundation-model protocol (masked self-supervised pretraining +
linear probe) beats direct supervised ridge at RNA->surface-protein prediction, on held-out cells
and zero-shot on an independent donor. **Verdict: DOCUMENTED BOUNDARY** (G2 fail, P1 fail, tree exhausted).

## Scores (mean per-protein Pearson r, 14 TotalSeqB markers)
| arm | dev-test (held-out cells) | frozen (5k donor, zero-shot) |
|---|---|---|
| ridge baseline | 0.727 | 0.644 |
| FM linear probe | 0.670 | 0.587 |
| P1 end-to-end fine-tune | 0.394 | 0.354 |

G1 sanity: ridge 0.727 >= 0.50 - pass. G2: 0.670 < 0.727+0.02 - FAIL. P1: 0.394 - FAIL
(catastrophic overfit at n=5.5k). G3 moot. Boundary per the locked tree.

## Mechanism (G4) - the payload
1. Bottleneck information loss: masked reconstruction R^2 = 0.117 - the 256-dim encoder retains
   ~12% of masked-gene variance. Ridge uses all 2000 genes directly; the probe sees a lossy
   compression and loses on 12/14 proteins.
2. Yet the embedding is not useless: unlabeled k-means on the embedding segregates T (CD3-high
   clusters 0/3), monocyte (CD14-high cluster 1) and B (CD19-high cluster 4) compartments - coarse
   lineage structure transfers, fine quantitative variation does not.
3. Fine-tuning collapses: end-to-end training overfits (dev 0.394) - 0.5M params vs 5.5k cells
   with full-batch training. The pretrain-and-transfer protocol needs scale this envelope lacks.
4. Transfer gaps are equal for both arms (~-0.084): donor shift costs the same whether or not
   representations are pretrained - pretraining bought no robustness.
Map entry candidate: at sub-atlas scale, the foundation-model protocol is strictly dominated by
direct supervised mapping - pretraining's value is scale-dependent, not protocol-inherent.
CD15 is unpredictable from RNA in every arm (0.25 dev, -0.09 frozen): ADT noise floor, disclosed.

## Tool (G5)
code/fm_embed.py (pretrained encoder embedder) + ridge as the recommended prediction path;
smoke-tested, bit-exact reproduction of pipeline embeddings. Honest scope in docstring.
## Prospective lab nomination (locked)
Single-cell cores running CITE-seq vaccine/immune-monitoring PBMC cohorts: ridge RNA->protein
predictor for QC; embedding for visualization only.
