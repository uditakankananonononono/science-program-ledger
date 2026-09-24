# algo50/43 - CRISPR guide efficiency: boosted trees on compact features vs Rule Set 1-style linear model

Lane RES-1. Adopted from the killed lane (claimed 2026-09-24T00:31Z, nothing pushed).

## Question
On-target Cas9 guide activity is predictable from the 34-mer sequence context
(NNNN[20nt spacer]NGGNNNNNNN). Rule Set 1 (Doench 2014) used a linear model on
position-specific sequence features; Azimuth (Doench 2016) showed gradient
boosting helps. This study asks, with everything implemented from scratch on
the raw public files: does a boosted model on a compact feature set beat a
Rule Set 1-style ridge, gene-held-out, and does the gain survive transfer to
an independent screen without refitting?

## Data
- Train/dev: Doench 2014 supplementary data (`V1_suppl_data.txt` in
  github.com/MicrosoftResearch/Azimuth, `azimuth/data/`). 2,144 guides,
  9 genes (human CD13/CD15/CD33, mouse CD45/CD43/CD5/CD28/H2-K/THY1),
  continuous `Activity` (log fold-change-based) and within-gene `Percent Rank`.
- Transfer test: Doench 2016 (`V2_data.xlsx`, sheet `Results`, header row 8),
  `sgRNA Score` as the label, guides with `Low Flag` set dropped. Different
  genes, different selection assays (AZD / 6TG / PLX survival). No refitting,
  no renormalization on V2 statistics.
- Raw files are not committed; sha256 + retrieval time in `data/`.

## Features (all from the 34-mer + annotation columns)
- B0 set: GC count of the 20-mer spacer only.
- B1 set (Rule Set 1-style): position-specific mononucleotides (34x4) and
  dinucleotides (33x16) one-hot; position-independent dinucleotide counts;
  GC count overall and in PAM-distal 5; melting temperature of the 20-mer
  (Wallace) and of 5'/3' thirds; amino acid cut position; percent peptide.
- M1 set (extended): B1 set + position of any GG dinucleotide within the
  spacer (one-hot over spacer positions, plus absent indicator) + GC in
  PAM-proximal 5 + longest homopolymer run.

## Models
- B0: ridge on B0 set.
- B1: ridge on B1 set, alpha in {0.1, 1, 10, 100} chosen by inner
  leave-one-gene-out on the training genes only.
- M1: histogram gradient boosting (sklearn HistGradientBoostingRegressor,
  squared loss, max_iter 300, learning_rate 0.06, max_leaf_nodes 31,
  min_samples_leaf 20, l2_regularization 1.0, early stopping off), fixed
  before seeing any result, on the M1 set.
- Diagnostic (not gated): ridge on the M1 set, to separate "better features"
  from "better model class" if G1 fails.

## Evaluation
- Within-V1: leave-one-gene-out over the 9 genes. Primary metric: Spearman
  correlation between prediction and Activity within the held-out gene,
  averaged over folds.
- Transfer: train on all V1, score V2 `sgRNA Score`, Spearman overall and
  per V2 gene.

## Gates (declared before any model is run)
- G1: mean LOGO Spearman(M1) >= mean LOGO Spearman(B1) + 0.02.
- G2 (reproduction sanity): mean LOGO Spearman(B1) >= mean LOGO Spearman(B0) + 0.05.
- G3 (transfer): trained on V1, tested on V2 with no refit:
  Spearman(M1) >= 0.25 AND Spearman(M1) >= Spearman(B1) - 0.01. Both clauses required.
- G4 (practical selection): for M1 gene-held-out, of the predicted top 10% of
  guides per held-out gene, >= 50% truly sit in that gene's top quartile
  (`Percent Rank` >= 0.75). Chance is 25%.

## Pivot plan (only if gates fail, each pre-registered as an amendment before results)
- P1: if G1 fails but the diagnostic ridge on M1 features beats B1, the win is
  features, not model class: gate P1 = M1-set ridge >= B1 + 0.02.
- P2: if G3 fails on a species split, re-run transfer restricted to V1 human
  genes as training (3 genes): gate P2 = Spearman(M1) on V2 >= 0.20.

## Honest-negatives policy
Every gate outcome is reported PASS/FAIL as declared. Failed gates stay in the
README with their numbers.
