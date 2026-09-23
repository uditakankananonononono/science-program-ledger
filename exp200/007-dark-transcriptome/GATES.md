# DOC-1-007 — generative-AI reconstruction of the dark transcriptome
# GATES locked 2026-09-24 ~01:25 IST, BEFORE any data download or outcome.

## Question
Can a small generative model trained only on the ANNOTATED transcriptome (GENCODE v45)
assign faithfully higher likelihood to real unannotated ("dark") transcripts than to
matched controls, transfer to an INDEPENDENT annotation source (NONCODE v6, frozen),
reconstruct masked sequence, and beat a named published baseline (CPAT feature model)?

## Data (public; URLs + SHA-256 in provenance; all direct FASTA, no genome extraction)
- TRAIN/DEV: GENCODE v45 protein-coding + lncRNA transcript FASTAs (GRCh38).
  Split: 90/10 by transcript ID hash (frozen).
- FROZEN EXTERNAL: NONCODE v6 human lncRNA FASTA (independent source), deduplicated
  vs GENCODE v45 by exact sequence match (locked rule).
- CONTROLS: dinucleotide-preserving shuffles of every evaluation transcript (locked
  implementation in code).

## Model (DL actually trained; recipe frozen)
Char-level GPT: vocab 5 (ACGTN->4 + mask), d_model 128, 4 layers, 4 heads, ctx 256,
~2M params, Adam 3e-4, batch 64, dropout 0.1, ONE pass over a frozen 30M-nt subsample
of train transcripts (first-come order, seed 20260924), torch CPU. Any recipe change
requires a pre-outcome addendum.

## Named published baseline
CPAT feature model (Wang et al. 2013, NAR): ORF length, ORF coverage, Fickett TESTCODE,
hexamer usage bias - logistic regression on these four published features, fit ONLY on
the train split (hexamer table computed from train transcripts). Documented as a
CPAT-feature reproduction if CPAT's own human coefficients are not fetchable.

## Gates
- G1 (reconstruction): on held-out GENCODE transcripts, masked-position prediction
  accuracy on REAL sequences exceeds dinucleotide-shuffled versions of the SAME
  sequences by >= 10 points, paired permutation p < 0.001.
- G2 (frozen external, primary): on NONCODE-vs-shuffle discrimination, generative
  mean-loglik AUROC >= 0.80 AND beats CPAT-feature logistic by >= 0.03.
- G3 (mechanism): per-position likelihood profile recovers 3-mer coding periodicity
  in pc transcripts and its absence in lncRNA (documented either way); top k-mers
  driving discrimination inspected for known biology.
- Tool + nomination: dark_tx_score.py CLI (FASTA -> per-transcript scores) + top-3
  highest-scoring NONCODE transcripts nominated for RT-PCR validation (only if G2 passes).
- Failure: G2 fails -> documented boundary; no threshold relaxation post-hoc.

## Compute honesty
30M-nt training budget is small by design (single CPU); gates are calibrated to what
a 2M-param char model can plausibly learn; a negative G2 with a positive G1 is reported
as "learns annotation statistics but does not transport" - itself a finding.
