# SP-006 / DOC-1-013 locked protocol

Locked: 2026-09-21 20:47 IST, before outcome data retrieval or model fitting.

## Question
Can per-residue embeddings from a pretrained protein language model identify residues lining experimentally solved allosteric ligand pockets better than matched low-dimensional sequence baselines on held-out proteins?

This is a bounded retrospective benchmark, not a claim that embeddings recover causal communication paths. "Allosteric pocket" means residues within 5.0 Å heavy-atom distance of a ligand explicitly described as allosteric in the RCSB PDB entry title. The experiment tests transfer across proteins.

## Sources
Only live RCSB PDB structure/metadata APIs and UniProt REST metadata are used for biological records. Model weights are the published `facebook/esm2_t6_8M_UR50D` artifact. Every request, URL, timestamp, HTTP status, byte count and SHA-256 is recorded.

## Cohort selection, frozen before search
1. Query RCSB Search API for entries whose title contains the exact word `allosteric` and whose experimental method is X-ray diffraction or electron microscopy.
2. Sort PDB IDs lexicographically, then inspect in that fixed order.
3. Include the first 15 entries satisfying all gates; no cherry-picking by model outcome.
4. Gates: resolution <=3.5 Å; exactly one protein entity selected; protein chain length 60-1200; title identifies an allosteric inhibitor/modulator/activator/binder; at least one non-polymer ligand with >=6 heavy atoms is present; one ligand can be tied to the title/entry annotations; ligand has >=3 protein residues within 5.0 Å; structure file parses; UniProt mapping exists.
5. Exclude crystallization additives, ions, waters, nucleotides when they are native substrates/cofactors, and covalently attached orthosteric ligands unless the entry calls the site allosteric. Every rejection and reason remains in `results/screening_log.csv`.
6. If fewer than 8 pass among the first 100 search results, terminate as an honest feasibility failure. Do not loosen gates.

## Labels and leakage controls
For the selected protein chain, positive residues are residues with any heavy atom <=5.0 Å from any heavy atom of the selected allosteric ligand. All other resolved standard amino-acid residues are negatives. Residues absent from coordinates are excluded. Ligand identity and labels derive only from structure, never model scores. All chains from one PDB entry remain in one fold.

## Features
Primary: frozen ESM-2 t6 8M per-residue final-layer embedding (320 dimensions), no fine-tuning. Baseline A: one-hot amino acid (20 dimensions). Baseline B: one-hot plus seven predeclared physicochemical properties (hydrophobicity, volume, charge, polarity, aromatic, glycine, proline). Context ablation: ESM embedding with residue order independently shuffled within each held-out protein after embedding; this tests whether performance depends only on residue composition.

## Model and evaluation
A class-weighted logistic regression is fitted inside leave-one-PDB-out cross-validation. Within each training fold, features are standardized; ESM is reduced by PCA to min(32, n_train-1) components using training data only. Hyperparameter C is selected from {0.01,0.1,1,10} by grouped 4-fold CV on training PDBs, optimizing average precision. Primary metric: macro mean per-protein average precision (AUPRC). Secondary: AUROC and recall among the top 10% ranked residues. Report bootstrap 95% CIs over proteins (10,000 resamples, seed 13013). Primary success gate: ESM macro AUPRC exceeds one-hot macro AUPRC by >=0.05 and the paired protein-bootstrap 95% CI for the difference excludes zero. Otherwise the result is negative/inconclusive. No threshold or model changes after seeing outcomes.

## Sanity and failure gates
Random-label control (labels permuted within protein, seed 13013) should have macro AUPRC within 0.05 absolute of prevalence; otherwise flag leakage and invalidate inferential results. Each held-out protein must have >=3 positives and >=30 negatives. At least 8 proteins must remain after all parsing/QC. Results are preserved even if negative. Retrieval failures get one retry and are logged. No simulated, augmented, or fabricated observations.

## Scope of claim
A positive result supports residue-level enrichment for known ligand-defined allosteric pockets across this benchmark. It does not establish causal signaling pathways, prospective druggability, or experimental activity. Structural distance, conservation, and ligand identity are not model inputs.
