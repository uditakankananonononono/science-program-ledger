# DOC-2-072 Protein grammar across families - GATES (locked 2026-09-24 09:16 IST, before any embedding or alignment)

## Question
Do protein language model embeddings recognize the same fold (shared structural grammar) across superfamilies whose sequences are unrelated, where sequence alignment fails?

## Data
- SCOPe 2.08 ASTRAL 40% identity domain set: https://scop.berkeley.edu/downloads/scopeseq-2.08/
- Classes a-d only; domains 50-300 aa.
- Folds kept only if they have >= 2 superfamilies with >= 3 domains each.

## Design (remote homology, superfamily held out)
- Per fold, one superfamily (seed 0) is the query set. Other superfamilies of the same fold, plus all other folds, form the reference database.
- Queries: seed-0 sample of 300 query domains.
- References: all domains of the other superfamilies of the query folds, plus a seed-0 sample of other-fold domains; at most 1,500 references.
- Task: 1-nearest-neighbour fold assignment; a query is correct if its top reference hit has the same fold.
- Model: frozen ESM-2 8M, mean-pooled last layer, cosine similarity. No training, so the whole set is external.

## Named baseline
B1: Smith-Waterman local alignment score (BLOSUM62, gap open 11, extend 1; the SSEARCH/BLAST default scoring; Smith & Waterman 1981). Best hit = highest raw score.

## Gates
- G1: ESM 1-NN fold accuracy >= 0.40.
- G2: ESM accuracy minus SW accuracy >= 0.10; McNemar exact p < 0.01.

## Reported (not gated)
- Mechanism: accuracy by SCOP class (all-alpha, all-beta, a/b, a+b). Hypothesis: gains over alignment are largest for all-beta folds, where sequence repeats are weak but topology is conserved.
- Tool: code/fold_nn.py (sequence -> nearest SCOPe folds).
- Nomination: one Pfam DUF (domain of unknown function) with no structure annotation, assigned its top ESM fold, to be checked by a lab structure (or an AlphaFold model + DALI).

## Pivot rule
Negatives are kept; amend and lock before new results.
