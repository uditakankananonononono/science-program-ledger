# ADDENDUM A (locked 2026-09-24 07:37, BEFORE any G1/G2 outcome under the new cohort)

## Erratum: cohort eligibility flaw in the locked tissue/split choice
The locked GATES chose tissues Pancreas/Liver/Spleen/Lung (dev Liver/Spleen/Pancreas, frozen Lung) and a
shared-label rule ">=30 cells in >=2 of 4 tissues". The first baseline run exposed a label-PRESENCE artifact:
under leave-one-tissue-out, a held-out tissue's shared-label cells can have zero training examples (e.g.,
Pancreas's only shared labels - endothelial cell, leukocyte - appear in NEITHER Liver nor Spleen, making
94/94 test cells auto-wrong for every model; held-out Liver's NK cells likewise). Evidence: Harmony vs PCA
predictions differ (12 Spleen / 22 Pancreas) yet accuracies are bit-identical (0.3946 both), because the
metric is dominated by unsatisfiable cells, not embedding quality. The G1 sanity halt (Harmony < 0.30) did
not fire (0.3946) even though the metric was uninformative - a pre-locking eligibility-check miss.

## Repair (governs all outcomes below; thresholds unchanged)
1. Tissues become: DEV = Marrow, Lung, Heart; FROZEN = Spleen (all Tabula Muris FACS, same source/hashes).
   Eligibility verified on the annotation counts BEFORE any model is scored under the new cohort: every
   held-out tissue retains scorable shared-label cells with >=30 training cells in the training pool
   (Marrow/Lung/Heart pairwise and -> Spleen). Only fibroblast (Heart-only support) drops out.
2. Scoring rule tightened: for each leave-one-tissue-out split, score only test cells whose class has
   >=30 cells IN THE TRAINING POOL of that split (was: >=30 in >=2 of 4 tissues globally).
3. Shared label set recomputed under rule 2 on the new tissues and frozen in results/class_list.json.
4. All gate thresholds, margins, and the failure tree from GATES.md are UNCHANGED. The discarded baseline
   numbers (0.3946/0.3946) are recorded in results/baseline_scores_flawed_cohort.json and never reused.
