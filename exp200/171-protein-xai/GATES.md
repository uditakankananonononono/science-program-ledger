# DOC-2-071 Explainable Protein Design Without Designing Anything - GATES (locked 2026-09-24 00:05 IST, before any data download or training)

## Question
When a CNN is trained to predict enzyme class from sequence alone, do its attributions land on the known catalytic residues? And does that hold beyond simply picking out catalytic-type amino acids (H/S/D/C/E/K)?

## Sandbox-fit slice
- Data: UniProt Swiss-Prot (reviewed) enzymes with one top-level EC class, length 100-600 aa, at most 1,200 per class, for 7 classes (EC 1-7).
- Split: train/val/test by UniProt "protein family" group, so whole families are held out (split seeded 0, 70/10/20 of families).
- Model: small 1D CNN (one-hot input, dilated conv, global max pool), CPU, at most about 15 min training. Attributions: integrated gradients (32 steps, zero baseline) for the true class, summed over channels; score per residue = |IG|.
- Evaluated set: test-set proteins with >= 1 UniProt ACT_SITE annotation.

## Gates (all must pass)
- G1 (the model learned something): test macro-F1 >= 0.50 (chance about 0.14).
- G2 (attribution localization): median over evaluated proteins of AUROC(|IG| ranks ACT_SITE residues above all other residues) >= 0.70.
- G3 (beyond residue identity): for each evaluated protein, AUROC of ACT_SITE residues vs non-site residues of the SAME amino-acid types in that protein. Pass requires mean AUROC >= 0.60 AND a one-sided Wilcoxon signed-rank test vs 0.5 with p < 0.01.
- Control reported (not gated): the same G2/G3 computed from a label-shuffled model trained identically.

## Pivot rule
If a gate fails, I keep the negative result, amend the gates and lock them here before new results, and do not re-fish.
