# algo50/07 - Minimum-length HMM segmentation of a learned composition score for intrinsic-disorder regions

Status: LOCKED before any model was fit or scored (timestamp + sha256 in results/lock.txt). Lane RES-1. Algorithm study (not counted toward the flagship 100).

## Question
Sequence-only disorder predictors output per-residue scores that are then thresholded, producing fragmented, flickering regions. Disordered regions are, in reality, contiguous stretches. Does a two-state HMM segmentation (Viterbi decoding with a minimum region length) on top of a light learned composition score improve region-level agreement with curated disorder, without losing residue-level accuracy, and how does it compare with the classic charge-hydropathy rule (FoldIndex)?

## Data
DisProt current release via the public API (URL, retrieval time, sha256 in data/). Positive residues: DisProt consensus 'Structural state' regions of type D. All other residues of the same proteins are treated as negative (the CAID "DisProt" convention; unannotated is not proof of order, stated as a limitation). Proteins with non-standard residues are dropped; proteins > 3,000 aa dropped.
Split: by UniRef50 cluster, 70% train / 30% test, seed 7. Test also reported for the non-human subset.

## Methods
- B1 FoldIndex (Prilusky 2005): 51-residue window, 2.785*<H> - |<R>| - 1.151 with normalised Kyte-Doolittle H; disorder score = -FoldIndex.
- B2 TOP-IDP (Campen 2008) propensity, 21-residue window mean.
- P score: logistic regression on per-residue window features at windows 11/31/61: TOP-IDP mean, normalised hydropathy mean, |net charge| per residue, fraction P, fraction G/S, Wootton-Federhen sequence entropy (window 12), fraction of charged residues; plus distance to terminus (log). Fit on train residues (subsample 400k residues, class_weight balanced).
- P-thr: P thresholded at the train-set MCC-optimal threshold.
- P-HMM (proposed): 2-state HMM with emissions from P's posterior (log-odds as emission score), states with a minimum duration of Lmin residues (implemented by state chains), transition penalty; Lmin and penalty chosen on a train-set held-out 20% of clusters for region F1 from grid Lmin in {5,10,20,30}, penalty in {1,2,4,8}.

## Metrics
Residue: AUROC (scores), MCC (binary). Region: F1 where a predicted region counts as a true positive if it overlaps a true region by >= 50% of the shorter one (one-to-one greedy match). Also the number of predicted regions per 1,000 residues. Uncertainty: 2,000 protein-level bootstrap resamples of the test set.

## Gates
- G1: P-HMM region F1 >= P-thr region F1 + 0.05, paired bootstrap CI excluding 0.
- G2: P-HMM residue MCC >= P-thr residue MCC - 0.01 (no residue-level cost).
- G3: P residue AUROC >= B1 FoldIndex AUROC + 0.05 on test, CI excluding 0.
- G4 (transfer): P AUROC on the non-human test subset >= 0.75.
PASS = G1 and G2.

## Failure policy
Failures are recorded as-is. A failed direction triggers a documented pivot with new gates locked in an amendment before new results are inspected. Original gates are never re-scored.
