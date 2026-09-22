# DOC-1-013 R3 outcome protocol lock
Locked 2026-09-21 21:53 IST only after the mapping preflight passed.

## Mapping gate result entering lock
SIFTS release header 2026-09-13, PDB 37.26, UniProt 2026.04. Of 429 AlloBench targets, 416 (96.97%) have at least one candidate whose canonical accession and curated site chain match a SIFTS segment, exceeding the 80% gate. Thirty stratified control records cross-checked against the independent PDBe mapping API matched accession and chain 30/30 (100%, exceeding 95%). The mandatory 4UC5 contradiction is resolved by treating the curated site chain B as authoritative for site mapping; chain A is only the modulator chain. Chain roles are never merged. There are 252 records where modulator chain is not a curated site chain; these are flagged, not silently rewritten.

## Frozen residue mapping
For each candidate, parse curated allosteric chain + author residue number + residue name. Map only within that author chain using SIFTS per-entry residue XML/API, requiring exact author residue number and insertion code. Confirm mapped canonical accession equals AlloBench accession and mapped amino acid matches curated residue name. Never infer offsets. Missing/unobserved residues are excluded and logged. Chimeric/multi-accession chains are excluded unless each site maps uniquely to the declared canonical accession. Active-site canonical positions map in the reverse direction through the same SIFTS record. Round-trip PDB→UniProt→PDB must return the original chain, author residue number and insertion code. Any one-to-many mapping is ambiguous and excluded.

## Outcome cohort and modeling
Apply the R2 independent cohort exclusions and feature/evaluation protocol unchanged after mapping. Require >=30 proteins, >=8 families with >=2 proteins, and >=95% site round-trip success in every included protein. Use fresh RCSB coordinates. Families are 30% identity clusters. Primary endpoint is macro protein AUPRC in leave-family-out testing. Gate remains: ESM+strong structure/conservation baseline beats strong baseline by >=0.03 with family-bootstrap CI excluding zero; positive leave-PDB-out gain; pathway corridor AUPRC exceeds prevalence by >=0.03 and the 97.5th percentile of degree-matched controls; Brier not worse by >0.01. Random-label control must be within 0.03 AUPRC of prevalence.

## Cross-check and leakage rules
A second mapping surface (RCSB GraphQL/Data API mapping or PDBrenum-equivalent) is checked for a stratified 30-protein sample. Discrepancies are preserved and the affected protein is excluded from the primary cohort. Author and label asym IDs are kept as separate columns. Chain identity is checked at every join. Zero cross-chain site mapping is permitted. Features never include ligand or site labels.
