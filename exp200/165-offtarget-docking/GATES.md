# DOC-2-065 Off-target vs state change - GATES (locked 2026-09-24 01:22 IST, before any docking or structure selection)

## Question (docking slice)
Can AutoDock Vina 1.2 docking tell measured DIRECT kinase binders of a drug from non-binders? And does it do better than the sequence-homology heuristic?

## Data and ground truth
- Davis et al., Nat Biotechnol 2011 (29:1046) kinome Kd panel, DeepDTA copy: https://github.com/hkmztrk/DeepDTA/tree/master/data/davis
- Nothing is trained, so the whole set is external.
- Drugs: imatinib (primary target ABL1) and erlotinib (primary target EGFR).
- Kinases: wild-type, non-phosphorylated entries only.
- Labels: binder Kd < 1,000 nM; non-binder Kd >= 10,000 nM.
- Per drug: all binders with a usable structure, plus seed-0 random non-binders at twice the binder count; at most 30 kinases per drug.

## Structures and docking (fixed before docking)
- For each kinase, use its human UniProt accession and take the best-resolution X-ray PDB entry (<= 3.0 A) that has a small-molecule ligand of >= 15 heavy atoms (RCSB search).
- Box: 22 A cube centered on that ligand.
- Receptor: that chain with ligand and waters removed; hydrogens added with Open Babel.
- Ligand: Davis SMILES converted to 3D with Open Babel.
- Vina: exhaustiveness 4, seed 0; score = best-pose affinity.

## Named baseline
B1: global sequence identity of each kinase to the primary target (BLOSUM62 global alignment). This is the homology heuristic behind reading selectivity off the kinome tree (Manning et al., Science 2002).

## Gates (all must pass)
- G1: mean over the 2 drugs of AUROC(-Vina score, binder vs non-binder) >= 0.70.
- G2: mean Vina AUROC minus mean B1 AUROC >= 0.05.

## Reported (not gated)
- Mechanism: imatinib binds DFG-out kinases.
  Per-binder scores are listed with the PDB used.
- Tool: code/dock.py (UniProt + SMILES -> score).
- Nomination: top-scoring unmeasured kinase.

## Pivot rule
Negatives are kept; amend and lock before new results.
