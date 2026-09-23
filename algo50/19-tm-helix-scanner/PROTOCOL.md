# algo50/19 - Finding transmembrane helices: Kyte-Doolittle hydropathy window vs a learned window scanner

Status: LOCKED before any method was scored (UTC time + sha256 in results/lock.txt). Lane RES-1.

## Question
Kyte & Doolittle (1982, J Mol Biol 157:105) proposed spotting transmembrane (TM) helices as 19-residue windows with mean hydropathy >= 1.6. On proteins with structure-supported TM annotations, does a small learned window scanner find TM helices better, get the TM count right more often, and avoid more false calls on soluble proteins?

## Data (UniProt reviewed, with 3D structure, KW-0002)
- Positives: 719 proteins where EVERY TRANSMEM segment has structure or experimental evidence (ECO:0007744 or ECO:0000269; entries with any sequence-model-only ECO:0000255 segment dropped to avoid labels made by hydropathy predictors). Beta-barrel strands excluded. 4303 helices, 395 families.
- Negatives: 1500 random human soluble proteins with 3D structure, no TRANSMEM, not Membrane (KW-0472), not Signal (KW-0732), seed 19.
- URLs, time, sha256 in data/.

## Methods
- KD (published rule, no training): mean KD hydropathy over a centered 19-aa window; residues with value >= 1.6 are TM.
- M1 learned scanner: logistic regression (C=1, balanced) on a centered 21-aa window: position one-hot (420) + window mean KD + counts of charged (DEKR), aromatic (FWY), P. Trained on positive and negative proteins of the training folds; threshold picked on training folds (max segment F1 on training positives).
- Both: predicted segments = maximal runs of TM residues of length >= 5.
- Split: 5-fold GroupKFold by UniProt family (no family = own group), positives and negatives together, seed 19.

## Metrics
- Segment F1 on positive proteins: a true helix is found if a predicted segment overlaps it by >= 5 residues; precision = predicted segments overlapping a true helix by >= 5.
- TM-count accuracy: fraction of positive proteins with exactly the right number of predicted segments.
- Soluble false-call rate: fraction of negative proteins with >= 1 predicted segment.
- Paired bootstrap over proteins (2000) for differences.

## Success gates (declared before scoring)
- G1: segment F1(M1) - F1(KD) >= 0.05, CI lower bound > 0.
- G2: soluble false-call rate M1 <= KD.
- G3: TM-count accuracy M1 - KD >= 0.10, CI lower bound > 0.
Secondary (not gated): KD with its threshold tuned on training folds, to separate "better threshold" from "better model". One post-hoc pivot allowed, locked first.
