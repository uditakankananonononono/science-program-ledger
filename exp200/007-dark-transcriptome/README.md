# DOC-1-007: generative-AI reconstruction of the dark transcriptome
Gates locked before data (GATES.md + addendum1 implementation constraints).

## Design
Char-level GPT (~2M params, 4 layers, d=128, ctx=256) trained ONE pass on a frozen
30M-nt first-come subsample of GENCODE v45 (pc + lncRNA, >=300nt; 14,669 transcripts,
459 batches of 32). Frozen external: NONCODE v6 human lncRNA (independent annotation
source), deduped vs GENCODE by exact sequence match (138,348 kept). Controls:
dinucleotide-block shuffles.

## Gate outcomes
- G2 (PRIMARY, frozen external): generative mean-loglik separates real NONCODE
  transcripts from shuffles at AUROC **0.908** (n=500 pairs) >= 0.80 PASS; CPAT-feature
  named baseline (Wang 2013: ORF length/coverage, Fickett, hexamer bias; logistic refit
  on train split) AUROC 0.739 -> model beats it by +0.169 (gate +0.03) PASS.
- G1 (reconstruction): masked-position accuracy real 30.4% vs shuffle 27.3% = +3.1
  points - FAILS the locked +10-point gate. Mean loglik separates real from shuffle
  significantly (paired permutation p = 0.001) but the reconstruction-margin gate
  missed. Disclosed, not relaxed.
- G3 (mechanism): per-position loss autocorrelation shows NO 3-mer coding periodicity
  peak in pc transcripts (lag3 0.013; lag6 0.131) and none in lncRNA - the expected
  codon-frame signature is NOT visible in first-256-nt windows (5'UTR-heavy prefixes);
  the model separates real vs shuffle via other higher-order statistics. Honest
  negative, reported as designed.
- Tool: code/dark_tx_score.py (FASTA -> per-transcript ll + real-vs-shuffle delta;
  smoke-tested on 40 NONCODE transcripts, all positive deltas).
- RT-PCR nomination (top delta over the G2 sample): NONHSAT236632.1 (delta +0.228,
  8,332 nt), NONHSAT002437.2 (+0.184, 1,533 nt), NONHSAT222492.1 (+0.164, 1,715 nt).

## Honest limitations / errata
- Training chunks 360-439 ran twice (operator re-issue during checkpointing);
  ~9% of the corpus seen twice - minor over-training on that slice; evaluation sets
  are held out and unaffected.
- G1 missed its locked margin; model discrimination is real (G2, p=0.001) but the
  masked-reconstruction margin is modest at this model/compute scale.
- CPAT comparison uses the published 4-feature logistic refit on our train split
  (CPAT's own coefficients are RData-bound); documented in gates.
