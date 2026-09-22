# SP-005: PET Hydrolases (DOC-1-016), Round 3 - Structure-Aware Validation of the 20-Candidate Shortlist and a Register-Aware Catalytic-Motif Model

## Outcome
**Locked-gate OVERALL PASS 5/5.** Protocol locked before any candidate execution (protocol sha256 d8491fa9a411fefbb4a688d385ae713d0c68cd9c141c51c5d3011da7548a5fcd). All gate text unmodified after lock.

| Gate | Requirement | Result |
|---|---|---|
| G1 grounding | >=8 positive + >=3 negative live-verified structures; >=4 ACT_SITE triads | PASS (8 pos, 3 neg, 4 ACT_SITE) |
| G2 structures | ESMFold structures >=18/20 | PASS (20/20) |
| G3 foldseek | >=15/20 pass leg C + positive-panel calibration | PASS (20/20; calibration holds) |
| G4 register-aware model | calibration + >=12/20 pass A^B^C | PASS (19/20) |
| G5 provenance | sha256 ledger, pinned versions, negatives preserved | PASS |

## The register-aware catalytic-motif model
Three legs, all thresholds reference-derived and frozen by the protocol lock:
- **Leg A (sequence register):** candidate-local triad positions mapped by global alignment vs IsPETase mature (A0A0K8P6T7 27-290; BLOSUM62 -11/-1). PASS requires order S<D<H, S->D spacing in [40,61] aa, D->H in [10,36] aa (reference spacings 45-55 and 13-32 with ~10% margin), and an exact G-x-S-x-G nucleophile elbow.
- **Leg B (3D geometry):** on the candidate's ESMFold structure, C-beta distances S-D in [6.7,11.8] A, S-H in [5.0,8.7] A, D-H in [3.4,6.0] A (panel crystal ranges +25% for prediction noise) and mean triad pLDDT >= 50 (0-100 scale).
- **Leg C (structural family):** foldseek 10-941cd33 best hit is a positive-panel member with E <= 1e-3 and alntmscore >= 0.5.

Calibration (locked in G4): all 4 ACT_SITE-grounded positives (IsPETase, LCC, F. vanettenii cutinase 1, T. fusca cutinase cut2) pass legs A+B; both adversarial negatives fail at least one leg of A (tannase B3Y018 has no catalytic triad; feruloyl esterase A O42807 has D->H = 53, outside [10,36] - the register rejects the PF07519-family geometry that defeated R2's sequence-only G3).

## Results
- **19/20 candidates pass A^B^C.** Passing triads sit tightly inside the crystal-derived envelope (S-D 9.17-9.48 A, S-H 6.59-6.98 A, D-H 4.46-4.70 A) with mean triad pLDDT 86.7-97.0. Foldseek best hits: 4EB0/LCC (7 candidates), 8ETX/8ETY ancestral PETases (6), 6EQE/9LMU IsPETase-family (4), 5ZOA/TfCut2 (2), 5XJH (1; the failing candidate).
- **Preserved negative: MGYP001374132912.** Fails leg A (the His register is disrupted: aligned residue A instead of H, D-H spacing 71 aa vs [10,36]) and leg B (S-H 18.78 A, D-H 13.75 A, triad pLDDT 58.7) - while its fold remains PETase-like (leg C passes, TM 0.928 to 5XJH, E=2.4e-22). This is exactly the failure mode the register-aware model exists to catch: fold intact, catalytic register destroyed. R2's alignment-based triad check had scored this candidate triad_intact=True; R3's structure-grade scoring overrides it. The shortlist's effective validated set is therefore 19.
- **Preserved limitation:** at fold level, all three negative controls cross-hit positive panel members (tannase 3WA6 -> 5XJH E=2.8e-5 TM=0.576; lipase 1TCA -> 9LMU E=7.0e-8 TM=0.537; FaeA 1USW -> 9LMU E=5.1e-4 TM=0.434). Foldseek alone cannot separate alpha/beta-hydrolase families; leg C is family-level evidence only, and the register legs carry the discrimination. This is reported as a model limitation, not hidden.

## Methods
- Reference panel: 8 positives (5XJH, 6EQE, 9LMU IsPETase-family; 4EB0 LCC; 1CUS cutinase 1; 5ZOA cutinase cut2; 8ETX, 8ETY ancestral PETases) + 3 negatives (3WA6 tannase, 1USW feruloyl esterase A, 1TCA lipase B), all live-verified at RCSB (search + entry titles + PDB sha256s in results/artifact_sha256_manifest.json).
- Catalytic annotation: live UniProt ACT_SITE features for A0A0K8P6T7, G9BY57, P00590, Q6A0I4 (positives) and O42807, B3Y018 (negatives). Signal-peptide offsets (1CUS: UniProt 136->PDB 120; 5ZOA: 170->PDB 130) resolved by alignment mapping and verified SER/ASP/HIS.
- Structure prediction: ESMFold API (api.esmatlas.com/foldSequence/v1/pdb/), 20/20 successful, per-structure sha256 ledger (data/raw/esm/prediction_ledger.json). Unit documentation: the API returns pLDDT on a 0-1 B-factor scale; values were multiplied by 100 to match the locked threshold's conventional 0-100 scale (unit normalization, not a gate edit).
- Compute ceilings (preserved): local structure prediction was not attempted (model weights not installable in the sandbox); the ESM Atlas fetchPredictedStructure endpoint returned HTTP 403, so all 20 predictions used the foldSequence endpoint.

## Provenance
49 artifacts sha256-ledgered (results/artifact_sha256_manifest.json): input FASTA, 20 ESMFold PDBs, 11 panel PDBs, grounding JSONs, foldseek TSVs, scoring tables, protocol, code. Environment ledger: protocol/environment_ledger.json (foldseek 10-941cd33 pinned by commit, Biopython 1.88, Python 3.10, API endpoints with access dates).
