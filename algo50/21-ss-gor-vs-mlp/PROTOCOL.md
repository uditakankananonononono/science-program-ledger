# algo50/21 - Protein secondary structure from single sequence: GOR-style information vs a small neural net

Status: LOCKED before any method was scored (UTC time + sha256 in results/lock.txt). Lane RES-1.

## Question
Classic single-sequence predictors, Chou-Fasman propensities (1974/78) and GOR (Garnier-Osguthorpe-Robson 1978), treat window residues independently. With homologs kept out of the test folds, does a small nonlinear model on the same window beat GOR on 3-state accuracy (Q3)?

## Data
RCSB DSSP-derived secondary structure (https://cdn.rcsb.org/etl/kabschSander/ss.txt.gz; time and sha256 in data/). Unique chain sequences, length 50-400, standard amino acids only; 1500 sampled with seed 21 (311,665 residues). DSSP 8 states mapped to 3: H,G,I -> H; E,B -> E; everything else, including unassigned -> C.

## Split
Groups = connected components of chains sharing 3-mer Jaccard >= 0.3; 5-fold GroupKFold, group order shuffled with seed 21.

## Methods (all parameters fit on training folds only)
- CF: Chou-Fasman-style: single-residue propensities P(s|a)/P(s), averaged over a +-3 window; predict the state with the highest mean.
- GOR: GOR-I-style information over a +-8 window: score(s) = log P(s) + sum over offsets j of log P(a_j | s, j), with +1 pseudocounts; predict argmax.
- MLP: sklearn MLPClassifier, one hidden layer of 64 ReLU units, on the one-hot +-8 window (sparse, 340 features); adam, early_stopping on a 10% split of the training fold, max_iter 30, seed 21.

## Metrics
Per-residue Q3; per-state Matthews correlation (H, E). 95% CIs by 2000 bootstrap resamples of groups, paired.

## Success gates (declared before scoring)
- G1: Q3(MLP) - Q3(GOR) >= 0.03, CI lower bound > 0.
- G2: MLP has higher MCC than GOR for both H and E.
- G3: Q3(MLP) >= 0.65.
All reported pass or fail; one post-hoc pivot allowed, locked first.
