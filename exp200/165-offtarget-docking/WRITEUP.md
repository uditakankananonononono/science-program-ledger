# DOC-2-065 Can docking separate true kinase binders from non-binders? (exp200/165)

**Outcome: documented boundary, not counted.**

## Experiment
- AutoDock Vina docking of imatinib and erlotinib into 60 real PDB kinase structures: 10 measured binders (Kd < 1 uM) and 20 non-binders (Kd >= 10 uM) per drug, all from the Davis 2011 kinome panel.
- Structures and boxes were picked by a fixed rule before docking.

## Result
- Vina AUROC: 0.66 for imatinib, 0.53 for erlotinib. Mean 0.59, gate 0.70: FAIL.
- The homology baseline (sequence identity to ABL1 / EGFR) was near chance at 0.52.
- For imatinib, 4 of the top 7 scores were true binders (DDR1, ABL1, KIT, PDGFRA).
- Several non-binders crystallized with ATP/ADP (JNK2, DAPK1, CDC2L5) also scored near the top. Some pockets score well for any ligand, and a raw Vina score cannot separate that from real binding.

## Takeaway
Raw docking scores are not usable for kinome-wide off-target calls at this scale. Correcting for receptor bias (MASC, Vigers & Rizzi 2004) is the obvious next step but was too compute-heavy for this sandbox.

## Limits
- 30 kinases per drug.
- One structure per kinase.
- The ligand 3D conformer is unseeded, so scores vary by about 1 kcal/mol between runs.
- One non-binder (MTOR) was docked into its rapamycin site.

## Reproduce
code/structs.py, code/dock.py, code/analyze.py. PDB files are downloaded by the scripts.
