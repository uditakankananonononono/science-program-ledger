# Sculpted Project Summary - Allosteric Communication From Protein Embeddings

## Status
R0 locked-gate success followed by R2 coordinate-feasibility failure and R3 SIFTS mapping repair/preflight. The outcome round after repaired mapping remains open.

## Cumulative useful results
- R0 showed that embedding-derived residue relationships can recover bounded allosteric communication signal under its original locked benchmark.
- R2 caught an invalid residue-coordinate intersection before modeling. No outcome was fabricated from misaligned coordinates.
- R3 repaired the mapping path with SIFTS and passed a manual/automated mapping gate, producing a locked outcome protocol but not yet an outcome.

## What is new
The project treats residue coordinate mapping as a first-class scientific validity gate, not a preprocessing detail. It shows that allosteric-pathway claims can fail before modeling when PDB, UniProt and observed-chain coordinates are silently mixed.

## Why it matters
Residue-level explainability is only meaningful when every residue refers to the same biological coordinate system. A high-performing model on misregistered labels would be scientifically invalid.

## Working tool/application
A residue-mapping validator can reconcile PDB chains, UniProt canonical coordinates and observed segments; test manual controls; report unmappable positions; and block pathway modeling unless mapping gates pass. The later embedding/pathway model remains separate.

## Top-lab reviewer questions
1. After SIFTS repair, does the original allosteric signal replicate on independent proteins?
2. How sensitive are pathway claims to missing residues, alternate chains and isoforms?
3. Does an embedding model beat graph-distance, conservation and structural-contact baselines?
4. Are recovered paths mechanistically enriched in mutational or dynamical evidence?

## Next direction
Run the already locked R3 outcome protocol without changing the repaired cohort or thresholds. Until then, R3 is mapping feasibility, not a replicated allostery result.
