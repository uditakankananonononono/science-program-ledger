# SP-005: PET Hydrolases R3 - Structure-Aware Validation + Register-Aware Catalytic-Motif Model

Locked-gate OVERALL PASS 5/5. 19/20 shortlist candidates validated (A^B^C); MGYP001374132912 preserved as a fold-intact/register-destroyed negative.

- protocol/protocol.json + lock.json (sha256 d8491fa9a411fefbb4a688d385ae713d0c68cd9c141c51c5d3011da7548a5fcd) - gates locked before candidate execution
- protocol/environment_ledger.json - pinned tools/versions/endpoints, compute ceilings
- report/report.md - full findings; report/literature_ledger.md - live PubMed grounding
- paper/paper.md - manuscript-style writeup
- results/ - gate_evaluation_r3.json, model_scoring.json, leg_a_register.json, panel_triad_geometry_calibration.json, plddt_summary.json, foldseek TSVs, artifact_sha256_manifest.json (49 entries)
- data/ - shortlist20.fasta; raw/esm/ 20 ESMFold PDBs + prediction ledger; raw/structures/panel/ 11 panel PDBs + SHA256SUMS; raw/grounding/ RCSB/UniProt/PubMed caches
- figures/ - sp005_triad_geometry.png, sp005_model_legs.png
- code/ - esmfold_predict.py, leg_a.py (leg B/C + gate eval embedded in run logs/results)
