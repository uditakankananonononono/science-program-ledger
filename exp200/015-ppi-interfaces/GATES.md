# DOC-1-015 GATES - Predicting Protein-Protein Interaction Interfaces with Multimodal Embeddings
Locked 2026-09-24 06:21 IST by EXP-1 BEFORE any embeddings, training, or scoring.

## Task + data
Per-residue PPI interface prediction (binary). Data: Dset_186 (train) / Dset_72 + Dset_164 (TWO independent frozen test sets) from the published DeepPPISP benchmark (Zeng et al., Brief Bioinform 2020; github.com/CSUBioGroup/DeepPPISP, data_cache/*.pkl; integer-encoded sequences, per-residue interface labels, precomputed PSSMs; checksums in PROVENANCE.md). The benchmark's train/test construction is identity-filtered by the original authors. Compute rule (locked): proteins truncated to 512 residues N-terminal for the PLM pass; a protein is DROPPED if truncation removes > 20% of its labeled interface residues (dropped counts documented; PSSM truncated identically).

## Method under test (multimodal)
Per-residue ESM-2 t6_8M final-layer residue embeddings (320-d) + PSSM (20-d) -> logistic regression (C=1.0 fixed upfront). Metric: per-residue AUROC (primary) and AUPRC.

## G1 - Named baseline + ablations (beat or document loss)
Named baseline: PSSM-only logistic regression - the classical evolutionary-feature approach (SPPIDER lineage, Porollo & Meller, Proteins 2007). Ablation: ESM-only logistic. G1 PASS iff multimodal AUROC on Dset_72 STRICTLY EXCEEDS both PSSM-only and ESM-only on Dset_72. Published DeepPPISP numbers (AUROC ~0.79 on Dset_72 with a full deep model + DSSP structure features) cited as context only.

## G2 - Frozen external validation (two independent sets)
Single scoring pass on Dset_72 and Dset_164. G2 PASS iff multimodal AUROC >= 0.72 on Dset_72 AND >= 0.70 on Dset_164 (locked against published benchmark difficulty, below full-model context numbers given our 8M encoder + linear head).

## G3 - Interface biochemistry interpretation
Top-scoring residues must be enriched for known interface biochemistry: hydrophobic (L/I/V/F/M) + aromatic (W/Y) enrichment in the top score decile vs bottom decile, interpreted vs Janin & Chothia interface principles (Janin et al., Prog Biophys Mol Biol 2008). PASS iff enrichment direction is coherent or incoherence explained.

## G4 - Tool + nomination
ppi_interface.py CLI: protein sequence -> per-residue interface probability, smoke-tested. Nomination: Dror lab (Stanford; DIPS docking-interface benchmark) as prospective evaluator.

## Failure tree (locked)
Single scoring passes. If G1 or G2 FAILS: no new arms, no hyperparameter moves, no re-sampling - documented boundary. Embedding cap: 422 protein forward passes.
