# 165F - follow-up to 165 (DOC-2-065): MASC receptor-bias correction for docking off-target calls
Approved by the parent (11:17) as a fresh attack on 165's failure. Locked 2026-09-24 ~12:50 IST, before any decoy docking.
Failure being attacked: some pockets (e.g., JNK2, DAPK1 crystallized with ATP/ADP) score well for any ligand, so raw Vina cannot separate binders.
Fix: multiple active site correction (MASC; Vigers & Rizzi 2004, J Med Chem).

## Design
- Receptors, boxes and the raw imatinib and erlotinib scores are frozen from 165 (data/raw_dock_165.json; no re-docking of the drugs).
- Decoys: 3 non-kinase drugs of similar size, from PubChem (data/decoys.csv): atorvastatin (558 Da), telmisartan (515), glyburide (494).
- Each decoy is docked into every receptor with 165's exact protocol (dock.py, exhaustiveness 4, box 22 A, seed 0).
- PRIMARY corrected score = raw - mean(decoy scores on the same receptor).
- Secondary (reported): MASC z-score, (raw - mean) / sd.

## Gates
- G1 (primary, imatinib; the 30 receptors of 165): corrected AUROC >= 0.75 AND >= raw 0.66 + 0.08.
- G2 (frozen external, erlotinib; its 30 receptors, same decoys and rule): corrected AUROC >= 0.65 AND >= raw 0.53 + 0.08.
- G3 (mechanism): the pockets 165 flagged as promiscuous (JNK2, DAPK1, and CDC2L5 if present) drop in rank after correction (the mean rank of these non-binders worsens by >= 5 positions). This is the receptor-bias mechanism MASC targets.
- G4: tool (a corrected-docking CLI), plus one prospective nomination: the top-ranked Davis non-binder or untested kinase after correction, named as a possible imatinib off-target to check.
- Baselines: raw Vina (165) and sequence identity to ABL1/EGFR (0.52, from 165).
- PASS = G1-G4. Otherwise a boundary. No decoy swaps or protocol changes after the first decoy score is seen.
