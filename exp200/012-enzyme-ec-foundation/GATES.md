# DOC-1-012 GATES - A Foundation Model for Enzyme Commission Number Prediction
Locked 2026-09-24 05:28 IST by EXP-1 BEFORE any embeddings, training, or scoring.
Motivation follows the DOC-1-011 boundary: PLM headroom should exist specifically where sequence signal is weak. This experiment tests that hypothesis with locked identity-stratified strata.

## Task
Predict EC top-level class (1-7) from protein sequence. Method under test: ESM-2 t6_8M mean-pooled embeddings (512-aa truncation) + multinomial logistic regression (sklearn, C=1.0 default, FIXED upfront - no hyperparameter tuning). Primary metric: macro-F1.

## Data (UniProtKB reviewed, REST API; URLs + checksums in PROVENANCE.md)
- Train: reviewed entries with ec:* created < 2022-01-01 (279,671 - 4,649 available), seeded (RNG 42) stratified sample n=3,000 across the 7 classes (min-count classes capped, documented).
- Dev: same pool, disjoint seeded sample n=800.
- Frozen: reviewed entries with ec:* created >= 2022-01-01 (4,649 available), seeded sample n=1,200, touched ONCE.
- Multi-EC entries: first listed EC used (documented). All sequences 40-2000 aa (length filter at sampling).

## G1 - Named published baseline, locked stratum (beat or document loss)
Baseline: MMseqs2 easy-search (-s 7.5) best-hit EC transfer against the train set; no hit = wrong. Locked primary stratum: LOW-IDENTITY dev (max pident to train < 50%). G1 PASS iff PLM macro-F1 STRICTLY EXCEEDS baseline macro-F1 on this stratum. All-comers dev comparison also computed and reported beat-or-document.

## G2 - Frozen temporal validation
Single pass on the frozen set. G2 PASS iff frozen all-comers macro-F1 >= 0.60 AND drop vs dev all-comers macro-F1 <= 0.15.

## G3 - Mechanistic interpretation
Confusion matrix interpreted against EC chemistry (e.g., oxidoreductase/transferase/hydrolase boundaries); top-3 confusions checked for chemically adjacent mechanisms vs enzyme-annotation literature (CLEAN, Yu et al. Science 2023; DeepEC, Ryu et al. PNAS 2019). PASS iff confusions are chemically coherent or incoherence explained.

## G4 - Tool + nomination
ec_predict.py CLI: FASTA -> EC class + class probabilities, smoke-tested. Nomination: Enzyme Function Initiative (Gerlt) as prospective user for de-orphanization screening.

## Failure tree (locked)
Single scoring passes on dev and frozen. If G1 or G2 FAILS: NO new arms, NO threshold/model changes, NO re-sampling; documented boundary with failure analysis. Embedding cap: 5,000 sequences total. If the low-identity dev stratum has < 100 sequences, G1 is scored on all-comers dev instead and the stratum shortfall is documented (pre-registered contingency, thresholds unchanged).
