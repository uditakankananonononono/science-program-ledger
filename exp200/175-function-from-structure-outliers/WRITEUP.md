# DOC-2-075 Function From Structure's Outliers - sandbox slice (exp200/175)

**Outcome: PASS on locked gates, flagged fragile.**

## Setup
Structure comparison (PDB/AlphaFold) did not fit the sandbox. Proxy: members of one Pfam family are fold "twins". The local feature is whether a member keeps the family's conserved 4-mer motif set, frozen label-free in exp200/180. "Different job" = no EC number, or a different EC 3-level class than the family's modal class. Data: 20 families of reviewed UniProt members. 16 were eligible; 4 were excluded because fewer than 50% of members carry an EC.

## Results
- Mantel-Haenszel OR for motif-lost vs motif-kept = 3.24, p < 1e-10 (gate >= 3, p < 0.001).
- 13/16 families have OR > 1 (gate >= 70%). 16 families (gate >= 8).
- Post hoc: very heterogeneous (Breslow-Day p < 1e-10). Leave-one-family-out OR ranges 2.6-4.2, so the pass depends on which families are included.

## What it found
Two different kinds of "outlier twin" show up:
1. **Pseudo-enzymes (the intended target).** Trypsin-fold members that lost the motifs include haptoglobin, haptoglobin-related protein, azurocidin, HGF, protein Z and "probable inactive serine protease 37". These are textbook catalytically dead proteases. Kinase-fold ones: STRADA (STE20-related adapter), PEAK1 ("inactive tyrosine kinase"), SCYL1 (N-terminal kinase-like), CaMK-like vesicle protein, RNase L. In Ras-fold proteins the atypical RGK GTPases (REM1, RAD) and AGAPs were flagged.
2. **Subfamily splits (a confound).** In aminotransferase class I (PF00155) and histidine phosphatase (PF00300) families, motif loss just marks a different active enzyme subfamily (aspartate/tyrosine aminotransferases vs the modal 2.3.1 class; PFKFB/TIGAR/PGAM5). These are real functional differences, but not dead enzymes.
3. Reverse direction in 3 families (papain, AMP-binding, aminotransferase III). There, the motif set came from a subfamily other than the modal-EC one.

## Useful result
Losing a family's label-free conserved motifs is a cheap flag for "same fold, different job" members, at about 3x odds. In protease and kinase families it pulls out known pseudo-enzymes. The confound is also informative: a naive motif-loss screen will mix pseudo-enzymes with subfamily switches. A usable tool has to separate them, e.g. by checking the annotated catalytic residue position rather than whole motifs.

## Limits
- Sequence proxy, not structure.
- EC absence is an imperfect "different job" label: missing annotation is not the same as non-catalytic.
- UniProt first-400 sampling.
- The motifs come from the same member sets (label-free, but not independent samples).

## Reproduce
python3 code/fetch.py; python3 code/run.py (needs data/motifs_from_180.json).
