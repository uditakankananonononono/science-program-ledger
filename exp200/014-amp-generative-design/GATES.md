# DOC-1-014 GATES - Design of Novel Antimicrobial Peptides with a Generative Protein Language Model
Locked 2026-09-24 06:14 IST by EXP-1 BEFORE any candidate generation. Instrument calibration (Macrel on known APD AMPs vs shuffled compositions) was performed pre-lock to set thresholds; NO generated sequence has been scored.

## Concept + task-shape rationale
Follows the DOC-1-012 boundary: PLM value should be tested where NO retrieval target exists - generative design. Question: is naive ProtGPT2 sampling (no fine-tuning, no prompting) a useful AMP idea generator under an INDEPENDENT published predictor?

## Method under test
ProtGPT2 (nferruz/ProtGPT2, Hugging Face; Rolnick et al./NVIDIA-Ferreira 2022), unconditional sampling, temperature 1.0, top-p 0.95, max length 50; keep sequences of 12-50 canonical aa. N=500 candidates, single batch, seeded.
Independent scorer: Macrel v1.6.1 (Santos-Junior et al., PeerJ 2020, 8:e10555) AMP_probability; AMP+ = prob >= 0.80 (locked from calibration: known APD AMPs 68.4% AMP+, composition-matched shuffled 9.3%; at 0.5 the tool saturates at 100%/100% and is useless - calibration documented in results/calibration.json).

## Baseline (G1 comparator)
500 seeded shuffles of APD natural AMPs (each known AMP's residues permuted; disjoint from the 200 calibration peptides; RNG seed 43), scored identically. This is the HARD baseline - it preserves length and composition exactly.

## G1 - enrichment vs baseline (beat or document loss)
G1 PASS iff generated AMP+ rate >= 3x the baseline AMP+ rate AND >= 15% absolute. Single scoring pass on both sets.

## G2 - novelty + plausibility vs held-out AMPs
Held-out set: APD natural AMPs not used in calibration or baseline (seeded sample 500). G2 PASS iff BOTH: (a) NOVELTY - >= 90% of generated AMP+ candidates have max MMseqs2 identity < 70% to the full APD natural set; (b) ENVELOPE - median net charge (pH 7, Lehninger scale) AND median hydrophobic ratio of generated AMP+ candidates fall inside the held-out APD interquartile ranges. Macrel hemolytic probabilities reported as context (no threshold).

## G3 - Mechanistic interpretation
Generated AMP+ candidates analyzed for cationic amphipathic character (net charge, hydrophobic ratio, amphipathic-moment proxy) vs AMP mechanism literature (Hancock & Sahl, Nat Biotechnol 2006). PASS iff the winners are mechanistically coherent or incoherence specifically explained.

## G4 - Tool + nomination
amp_design.py CLI: generate N candidates -> Macrel score -> novelty filter -> ranked shortlist. Smoke-tested. Nomination: Cesar de la Fuente lab (UPenn, machine-learning antibiotic discovery) as prospective evaluator.

## Failure tree (locked)
ONE generation batch of 500, ONE scoring pass. If G1 or G2 FAILS: no re-generation, no parameter moves, no threshold changes - documented boundary. Compute cap: 500 generated + 500 baseline + 500 held-out + 200 calibration (already run).
