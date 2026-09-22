# DOC-1-013 R2 family/physics replication: locked feasibility failure

## Status
Stopped before outcome modeling. No R2 performance result exists.

## What was attempted
The fresh protocol required a multi-family cohort independent of R0, with AlloBench-curated allosteric residues and active-site residues both mapped to resolved residues in the same fresh RCSB chain. It also required at least 30 proteins and eight multi-protein families before modeling. AlloBench supplied 2,257 PDB records, 429 targets, curated allosteric-site strings, active-site lists, sequences and citations. All 15 R0 PDB entries and seven R0 UniProt proteins were excluded.

The pipeline fetched 192 live RCSB mmCIF coordinate files before the execution ceiling. A cache-only deterministic screening pass then evaluated all 2,257 AlloBench rows under the locked gates. No protein passed. Among row-level decisions, 1,906 had not yet been fetched, 256 fetched records failed the locked mapping/gating requirement, and 95 were excluded as R0 overlap.

## Why the gate failed
Inspection showed that AlloBench fields use incompatible coordinate frames in many records. Allosteric sites are chain-qualified PDB residue identifiers, while `active_site_residue` is generally a list of sequence positions associated with the canonical target sequence. Direct intersection with PDB author residue numbers is invalid and produced fewer than three mapped active-site residues even when the structure and allosteric residues were present. Some records also disagree between the `modulator_chain` field and the chain embedded in the allosteric-site strings (for example 4UC5 records modulator chain A but allosteric residues on chain B).

A correct repair needs explicit SIFTS UniProt-to-PDB residue mapping, chain disambiguation, and a new preflight. The locked protocol did not authorize substituting inferred offsets or dropping the active-site gate. I therefore did not loosen gates after observing the failure.

## Consequence for R0
R0 remains preliminary. This round did not test whether its ESM gain survives family holdout or beats strong physics baselines. It also did not generate pathway-localization results. No inference about the source of the R0 gain can be made from this aborted round beyond the previously reported family duplication risk.

## Preserved evidence
The artifact contains the locked protocol and hash, preflight, source AlloBench table and license, 192 fetched RCSB coordinate files, request/hash ledger, screening log, environment record, and exact scripts. The interrupted runs and final cache-only screening produced no modeled outcomes. A follow-up round should first validate SIFTS mapping on a small, family-diverse sample before locking.
