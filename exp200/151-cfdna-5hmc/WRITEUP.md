# DOC-2-051 Liquid biopsy: cfDNA 5hmC cancer detection across labs (exp200/151)

**Outcome: documented boundary, not counted.**

## Experiment
Classifiers trained on plasma cfDNA 5hmC gene-body profiles from one lab (GSE89570, Li 2017: 245 cancers vs 96 healthy) and frozen-tested on another lab (GSE81314, Song 2017: 49 cancers vs 15 non-cancer).

| model | training CV | external |
|---|---|---|
| 50 co-variation modules (tested idea) | 0.76 | 0.61 |
| one gene (SNCAIP) | 0.79 (train) | 0.73 |
| elastic-net on genes (Li 2017 approach) | 0.78 | 0.64 |

## Takeaway
- Within one lab the signal is moderate (0.76-0.79). Across labs it mostly does not survive.
- The multi-gene models transferred worse than one gene, the opposite of the hypothesis. The likely cause is lab and normalization batch effects that multi-gene models absorb.
- Cross-study harmonization, not model complexity, is the bottleneck for 5hmC liquid biopsy.

## Limits
- The external set has only 15 controls, 7 of them HBV.
- Cancer types differ between cohorts.
- Processed gene-level data only.
- B2 was restricted to 2,000 genes for compute (amendment A, locked before results).
