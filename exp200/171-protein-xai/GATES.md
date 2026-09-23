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

## Amendment A (00:10, after download, before any training or results)
- The UniProt query was restricted at download to proteins with ACT_SITE annotation, for all classes, so every test protein is evaluable.
- EC 7 returned only 16 entries and is dropped. That leaves 6 classes, chance about 0.17. The G1 threshold is unchanged at 0.50.
- Entries whose EC numbers span more than one top-level class are excluded.

## Primary result (00:10) - FAIL, preserved
Test macro-F1 0.272 (G1 FAIL, needed >= 0.50; val best 0.388). G2 median AUROC 0.699 (FAIL by 0.001, needed >= 0.70; n=1612). G3 mean 0.608 / median 0.647, Wilcoxon p=1e-37 (PASS). Label-shuffled control running (reported, not gated).
Reading: enzyme class cannot be learned from sequence well enough under a family-held-out split with a small one-hot CNN. Its attributions do prefer catalytic residues over same-type residues, but the model is too weak to count.

## Pivot 1 (locked 00:16, before any Pivot 1 code was run). Follows the parent's ISEF checklist (00:10).
Re-angle: drop enzyme class as a proxy. Train a DL model directly to find catalytic residues: a frozen ESM-2 (8M) protein language model plus a trained per-residue MLP head. Validate frozen on an independent, literature-curated catalytic-site atlas.
- Training labels: UniProt ACT_SITE from the Amendment A download, family-grouped split seed 0 (train/val families only). Remove every protein whose accession is in M-CSA and every protein whose UniProt family contains an M-CSA protein.
- External set: M-CSA (Ribeiro et al., Nucleic Acids Res 2018, https://www.ebi.ac.uk/thornton-srv/m-csa/) reference UniProt residues. Keep proteins of 50-1000 aa whose residue codes match the UniProt sequence at the given positions.
- Named published baselines, computed on the same external set:
  - B1: zero-shot ESM-2 wild-type marginal log-probability (the "wt-marginal" scoring of Meier et al., NeurIPS 2021, "Language models enable zero-shot prediction of the effects of mutations"). The score is -log p(wt), so less expected residues score higher. The sign that gives the better AUROC on the TRAIN set is fixed before external scoring.
  - B2: catalytic residue-type propensity (Bartlett et al., J Mol Biol 2002, 324:105), estimated from the training labels.
- P1-G1 (beats named baselines): on M-CSA external, pooled AUPRC of the model > the max of B1 and B2 by >= 0.05 absolute, with the 1,000x protein-bootstrap 95% CI lower bound of the difference > 0. Also median per-protein AUROC >= 0.85.
- P1-G2 (beyond residue identity): per-protein AUROC among residues of the catalytic types in that protein, mean >= 0.70, one-sided Wilcoxon vs 0.5 p < 0.01.
- Reported, not gated:
  - Mechanism check: recall at top-5 per protein, split by M-CSA role class (reactant, e.g. nucleophile or proton acceptor, vs spectator only). Hypothesis locked: reactant residues are recovered more often than spectator-only residues.
- Deliverables:
  - Tool: predict.py (sequence in, ranked residues out).
  - Prospective nomination: the top-scoring residue in a reviewed human enzyme with an EC number and no ACT_SITE annotation, proposed for an alanine-substitution activity assay.

## Pivot 1 result (00:19) - PASS
- External M-CSA set: 932 proteins, 4,564 catalytic residues.
- P1-G1 PASS: model AUPRC 0.205 vs best named baseline B2 (Bartlett propensity) 0.045 and B1 (ESM-2 wt-marginal) 0.036. Diff +0.160, bootstrap CI 0.146-0.176. Median per-protein AUROC 0.904.
- P1-G2 PASS: type-matched AUROC mean 0.776 (n=930), Wilcoxon p=2e-144.
- Mechanism (locked hypothesis supported): top-5 recall is 0.41 for reactant residues (n=1,464) vs 0.20 for spectator-only residues (n=3,100).
- Nomination: ABHD4 (Q8TB40) S146, within the GHSLG (GXSXG) motif. Its predicted triad partners are H320 and D170.

## Label-shuffled control (primary, reported, not gated; finished 01:05)
Test macro-F1 0.126 (chance). G2 median AUROC 0.589. G3 mean 0.522 (p=1e-4). Architecture and positional priors alone give attributions a little above chance. The trained primary model (0.699 / 0.608) sits well above this control. The Pivot 1 result is not affected.
