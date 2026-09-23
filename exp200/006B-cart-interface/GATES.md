# DOC-1-006 (re-angle B) — CAR scFv-antigen interface prediction, validated on real structure
# GATES locked 2026-09-24 ~00:30 IST, before any structure is parsed. Lane EXP-1.
# Approved by main 00:28 ("Approved: (b) the CAR scFv-antigen interface re-angle against
# PDB 6AL5 with a named epitope-predictor baseline"). Replaces nothing - the boundary
# folder exp200/006-virtual-immune-cart stands.

## The experiment (docking-adjacent structural prediction, real PDB data)
Predict which residues of a CAR-T target antigen sit in the scFv-binding interface
(epitope), trained on OTHER antibody-protein complexes, validated FROZEN on the real
FMC63-CD19 complex structure (PDB 6AL5 - the clinical anti-CD19 CAR's parent antibody).

## Data (public; URLs + checksums in provenance)
- Training: antibody-protein-antigen complexes from PDB/PDBe (free REST), target ~30-60
  complexes meeting: protein antigen (not peptide/hapten), resolution <= 3.5A,
  non-CD19. Complex list FROZEN after curation (recorded with the gate hash).
- Frozen validation: PDB 6AL5 (FMC63 scFv - CD19 extracellular domain).
- Truth: interface residue = any antigen residue with a heavy atom within 5.0A of any
  antibody heavy atom (computed from coordinates).

## Frozen features (per residue, published encodings only)
- Named propensity scales: Parker hydrophilicity (1986), Kyte-Doolittle (1982),
  Karplus-Schulz flexibility (1985), Emini surface probability (1985), Chou-Fasman
  (1978) - windowed (w=5) means.
- Atchley factors (2005, 5 published factor scores per AA).
- Burial: CA-coordinate neighbor count within 10A (computed, no DSSP dependency).

## Model + gates
- Model: gradient-boosted trees (sklearn HistGradientBoostingClassifier) OR logistic -
  pick logistic for interpretability; frozen: LogisticRegression(C=1.0) on scaled
  features, per-complex grouped splits.
- G1 (training): GroupKFold-by-complex (5-fold, 20 seeds) mean per-residue AUROC
  >= 0.70 AND 200 full-pipeline residue-label permutations with observed > ALL nulls.
- G2 (PRIMARY, frozen external): trained model applied ONCE to CD19/6AL5: AUROC
  >= 0.70 AND beats the NAMED PUBLISHED BASELINE - Parker hydrophilicity scale alone
  (the classical epitope predictor, cited) - by >= 0.03 AUROC on the same residues.
- G3 (paratope): on FMC63, fraction of TRUE contact residues among the top-10
  predicted CDR residues >= 0.5 (sanity gate, reported).
- Mechanism check: predicted CD19 epitope must be discussed vs the known FMC63
  discontinuous epitope literature.
- Tool: epitope_predict.py CLI (PDB file + antigen chain -> per-residue scores) + ONE
  nomination: the top predicted NON-FMC63 epitope patch on CD19 as a candidate
  second-epitope target for bispecific CAR designs.
- Failure: if G2 fails, ONE pivot (v2): add neighbor-count-normalized surface weighting;
  if that fails, documented boundary.
