# DOC-1-012 REPORT - A Foundation Model for Enzyme Commission Number Prediction
EXP-1, 2026-09-24. Gates locked BEFORE outcomes (commit 96434db1). VERDICT: DOCUMENTED BOUNDARY - both headline gates FAILED; failure tree followed (single passes, no new arms, no threshold changes, no model tuning).

## Task + data (GATES.md; PROVENANCE.md)
EC top-level class (1-7) prediction. ESM-2 t6_8M mean-pooled embeddings + logistic regression (C=1.0 fixed upfront). Train 3,000 / dev 800 (pre-2022 reviewed enzymes, disjoint, natural class mix) / frozen 1,200 (post-2022 reviewed, single pass). Multi-EC: first EC. 5,000 sequences, 5,000 embeddings (at cap).

## Results (results/gate_scores.json)
- Dev all-comers macro-F1: PLM 0.573 vs MMseqs2 EC-transfer 0.789.
- Dev LOW-IDENTITY stratum (<50% max pident to train, n=516): PLM 0.470 vs MMseqs2 0.655. G1 (PLM strictly beats baseline on this stratum): FAIL by -0.186.
- Frozen all-comers: PLM 0.459 (locked bar >= 0.60: FAIL); drop vs dev 0.115 (bound <= 0.15 met, but the macro-F1 bar decides): G2 FAIL. MMseqs2 frozen 0.574.
- Identity structure: dev median pident 38.7 (155/800 no-hit); frozen median 23.8 (554/1200 no-hit) - the post-2022 deposits are substantially more remote, which is exactly where both methods degrade but the PLM degrades more.
- G3: top confusions 3->2 (54), 2->3 (32), 1->3 (21), 1->2 (18), 4->2 (16): hydrolase/transferase and oxidoreductase boundaries - chemically adjacent classes sharing substrates/cofactors (consistent with CLEAN/DeepEC error analyses). Confusions chemically coherent: documented PASS.
- G4: code/ec_predict.py CLI (FASTA -> EC class + probabilities), smoke-tested; nomination: Enzyme Function Initiative (Gerlt).

## Boundary analysis
This experiment directly tested the hypothesis from the DOC-1-011 boundary - that PLM headroom exists where sequence signal is weak - and REFUTED it at the 8M-parameter scale with a linear head: even below 50% identity, MMseqs2 best-hit EC transfer beats the PLM classifier by 18.6 macro-F1 points. Best-hit transfer works because EC class is conserved far down the identity curve (functional signal in local motifs at 25-40% identity), so "weak sequence signal" is rarer than hypothesized for enzyme function. Combined with 011: small-PLM embeddings + simple heads are dominated by alignment-based transfer for both retrieval and function transfer on natural protein pools. Any future PLM project in this program must change the SCALE (larger model - outside current compute), the HEAD (fine-tuning - outside current compute), or the TASK SHAPE (generation/design where no retrieval target exists, e.g. DOC-1-014's antimicrobial peptide design) - not just the dataset.

## Honest limits
Logistic head with C=1.0 fixed (locked pre-registration) may underfit; a tuned head could narrow but per the failure tree was not tried. Linear-probe gaps of this size (18-21 points) are not typically closed by head tuning alone. 4 fasta records had header-embedded '>' characters that broke an initial parser; fixed and re-embedded all 8 affected sequences before any scoring (documented; parsing bug touched no outcomes).
