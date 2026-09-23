# algo50/09 - Docking screen of adenosine deaminase (DUD-E) with interaction-fingerprint rescoring

Status: LOCKED before any active or decoy was docked (UTC time + sha256 in results/lock.txt). Lane RES-1. Restart of the 09 attempt whose sandbox died with nothing pushed; same design.

## Question
AutoDock Vina ranks compounds by a noisy physics-like score. Does rescoring docked poses by how well their protein-ligand interaction fingerprint (IFP) matches the crystal ligand's interactions enrich true actives better than the Vina score? Is any gain more than what 2D similarity to the crystal ligand already gives?

## Data
DUD-E target ADA (adenosine deaminase): receptor.pdb, crystal_ligand.mol2, actives_final.ism (93 actives), decoys_final.ism (5450 decoys), from https://dude.docking.org/targets/ada/ada.tar.gz (time, sha256 in data/). All 93 actives plus 465 decoys (5 per active) sampled uniformly at random with seed 9. Library = 558 compounds; crystal ligand redocked separately as a check.

## Methods
- Ligand prep: RDKit from SMILES, add H, ETKDG seed 9, MMFF, meeko PDBQT. Receptor: PDB heavy atoms + polar H via meeko/openbabel-free route (gemmi/meeko); box = crystal ligand centroid, 22 A cube.
- Docking: Vina 1.2 python API, exhaustiveness 4, 5 poses, seed 9.
- Scores (higher = more active-like): S_vina = -best Vina energy; S_ifp = max over 5 poses of Tanimoto(IFP_pose, IFP_crystal); S_cons = mean of the percentile ranks of S_vina and S_ifp.
- IFP: per binding-site residue (any atom within 6 A of crystal ligand), bits for hydrophobic contact (C-C <= 4.0 A), H-bond (N/O ligand to N/O protein <= 3.5 A), and metal/ionic proximity (ligand N/O <= 2.8 A of Zn). Implemented from scratch.
- Baselines: S_2d = ECFP4 Tanimoto to crystal ligand; S_size = heavy atom count; random.

## Metrics
AUROC, EF5% (top 5% of 558 = 28 cmpds), BEDROC(alpha=20). 95% CIs by 2000 stratified bootstrap resamples of compounds, paired between methods.

## Success gates (declared before docking)
- G0 validity: redocked crystal ligand top pose heavy-atom RMSD < 2.0 A. If G0 fails, all IFP results are reported but labelled as unreliable.
- G1: S_cons AUROC - S_vina AUROC >= 0.05 with paired bootstrap 95% CI lower bound > 0.
- G2: S_cons EF5% >= 1.5 x S_vina EF5%.
- G3 (the honest control): S_cons AUROC > S_2d AUROC with paired CI lower bound > 0 (gain is not just 2D similarity to the crystal ligand).
- Also reported, not gated: S_ifp alone, S_size (DUD-E decoys are property-matched so size should be near 0.5).

## Honest-negative policy
All gate results are reported whether pass or fail. Any pivot after results is a written, timestamped amendment below the lock and is labelled post hoc.

## Disclosure note (2026-09-23T21:24Z, added while docking was running, before any analysis)
The earlier, lost attempt at 09 (previous sandbox) ran a single-ligand timing test on an ADA active and docked about 3 library compounds before it died. Those outputs were never pushed and were not available to or seen by this restart. The "LOCKED before any active or decoy was docked" statement applies to this restart's run.
