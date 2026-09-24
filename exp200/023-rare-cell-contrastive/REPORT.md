# DOC-1-023: Detecting Rare Cell Types with Contrastive Learning
Status: DOCUMENTED BOUNDARY - reported to main for adjudication (never self-counted). 2026-09-24.

## Question
Does a SimCLR-style contrastive embedding detect a rare pancreatic cell type better than the standard
published pipeline (PCA + Leiden; Wolf 2018 Genome Biol, Traag 2019 Sci Rep) as the type gets rarer?

## Design (GATES.md + Addendum A locked pre-outcome)
Rare target: pancreatic PP cell (Ppy). Controlled rarity grid 0.5/1/2/5% (nested, seed 7).
DEV: Tabula Muris FACS mouse Pancreas (1,327 cells, 107 PP). FROZEN: human pancreas smartseq2
(Segerstolpe via scIB task h5ad; gamma=213, bg=2,181) - species+pipeline shift (Addendum A: the locked
10x droplet Pancreas does not exist; droplet half of Tabula Muris has no Pancreas).
Same Leiden pipeline on PCA-50 (named baseline) vs SimCLR-lite embedding (dropout+noise aug, NT-Xent).

## Results (PP-class F1, majority-vote cluster mapping)
| rarity | dev baseline | dev contrastive | dev contrastive P1 (128d, 60ep) | frozen baseline | frozen contrastive |
|---|---|---|---|---|---|
| 0.5% | 0 | 0 | 0 | 0 | 0 |
| 1% | 0 | 0 | 0 | 0 | 0 |
| 2% | 0 | 0 | 0 | 0.706 | 0.769 |
| 5% | 0.679 | 0 | 0 | 0.911 | 0.933 |
| mean | 0.170 | 0.000 | 0.000 | 0.404 | 0.426 |

- G1: baseline sanity PASS (dev F1 at 5% = 0.679 >= 0.5).
- G2: FAIL (0.000 < 0.170+0.03). P1 (locked: 128d/60ep): FAIL again (0.000).
- G3: frozen contrastive +0.022 over frozen baseline - BELOW the locked +0.03 margin, so the topic arm
  does not pass; winner (baseline) stability PASS (frozen 0.404 >= dev 0.170-0.10).
- G4: marker identity confirmed (Ppy PP 4.38 vs bg 0.84 log-norm). Neighbor purity of PP cells (r=5%):
  PCA 0.618 vs contrastive 0.369 - the contrastive objective partially scrambles rare-type neighborhoods
  at small n; at r=1% both collapse (0.183 / 0.061). Augmentation ablation (r=1%): dropout-only 0,
  noise-only 0 - no rescue. Augmentations designed for abundant-image invariances dilute the sharp
  marker signature that IS the rare-type signal.
- G5: detect_rare.py CLI (winning arm: PCA+Leiden, honest rarity-floor banner) smoke PASS - recovers
  the PP rare cluster (45 cells, 3.5%) on held-out dev data. Regev lab nomination.

## Boundary statement (for the program summary)
Contrastive pretraining does not reliably beat plain PCA+Leiden for rare cell type detection: at
single-tissue mouse scale (1.2k cells) it destroys the signal (F1 0 vs 0.170 dev; PP neighbor purity
-40%), while at larger human cohort scale (2.4k cells) it edges ahead (+0.022) but below the locked
margin - scale-dependent, inconclusive, and NOT a win under locked gates. The sharper shared finding:
r <= 1% is a hard detection floor for Leiden-based detection at ~1-2.4k cells in BOTH cohorts and BOTH
representations (F1=0 everywhere), with PCA purity at 1% only 0.183 - rare-type detection below 1%
needs sub-clustering or dedicated rare-type methods (FiRE/RaceID family), not better embeddings.
Extends the task-type map: small self-supervised objectives help when they align an existing signal
(022 win), hurt when the augmentation prior fights the signal (023), fail to generate signal a
reference carries (021) or to cross library designs (020).

## Reproduce
code/prep_data.py, code/prep_frozen.py, code/score.py (dev|frozen; P1=1 env for P1), code/g4_mechanism.py,
code/detect_rare.py. Data per PROVENANCE.md (hashes). GATES.md + GATES_ADDENDUM_A.md locked pre-outcome.
