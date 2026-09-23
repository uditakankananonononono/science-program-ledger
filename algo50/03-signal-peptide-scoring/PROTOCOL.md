# algo50/03 - Explicit n/h/c segmentation scoring for signal-peptide detection vs hydrophobicity and composition baselines

Status: LOCKED before any model was fit or scored (timestamp + sha256 in results/lock.txt). Lane RES-1. Algorithm study (not counted toward the flagship 100).

## Question
Signal peptides (SPs) have a tripartite structure: positive n-region, hydrophobic h-region, polar c-region ending in the A-x-A cleavage motif. The classic confusion is an N-terminal transmembrane (TM) anchor, which is also hydrophobic. Does a small, interpretable dynamic-programming segmenter that scores an explicit n-h-c parse (plus cleavage motif) separate SPs from N-terminal TM anchors better than hydrophobicity or composition features, and does it transfer from human to distant organisms?

## Data
UniProtKB/Swiss-Prot reviewed, protein existence level 1, length 60-2000, organisms human (9606), yeast S. cerevisiae (559292), E. coli K-12 (83333); mouse downloaded but excluded (human-mouse ortholog leakage). Retrieval time and sha256 in data/.
- Positive: SIGNAL feature starting at 1 with experimental evidence (ECO:0000269 or ECO:0007744). Predicted-only SIGNAL (ECO:0000255 etc.) proteins are EXCLUDED entirely to avoid training on SignalP-style predictions.
- Negative: no SIGNAL feature.
- Hard negative subset: negative with a TRANSMEM feature starting at residue <= 40.
Input to every model: first 70 residues only.

## Split
Train and tune only on human (5-fold CV within human for hyperparameters). External test: yeast and E. coli, reported separately and pooled. No test-set tuning.

## Methods
- B1 hydrophobicity rule: max mean Kyte-Doolittle over 11-residue windows in residues 1-35; threshold chosen to maximise MCC on human train.
- B2 composition logistic regression: amino-acid composition of residues 1-10, 11-25, 26-40 (60 features) + B1 score; L2, C by human CV.
- P (proposed) NHC segmenter: DP over residues 1-70 choosing boundaries n (1-10 aa), h (6-20 aa), c (3-12 aa), cleavage after c; per-residue log-odds emission tables for n, h, c learned from human positives vs human background, plus a -3/-1 cleavage position log-odds term. Features = best parse total score, its n/h/c component scores, h-length, c-length; logistic regression on these (plus B1 score) fit on human.

## Metrics
MCC at the human-train-chosen operating point; AUROC; false-positive rate on the hard-negative subset. Uncertainty by 2,000 protein-level bootstrap resamples of the test set.

## Gates
- G1: pooled external (yeast+E. coli) MCC of P >= MCC of B2 + 0.05, and bootstrap 95% CI of the difference excludes 0.
- G2: pooled external hard-negative FPR of P <= 0.5 x FPR of B1.
- G3 (transfer): P's MCC on yeast and on E. coli each >= 0.6.
PASS = G1 and G2.

## Failure policy
Record failures as-is. Per standing instruction, a failed direction triggers a documented pivot with new gates locked in an amendment before new results are inspected; original gates are never re-scored.
