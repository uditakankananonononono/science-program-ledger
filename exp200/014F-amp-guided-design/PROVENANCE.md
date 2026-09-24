# PROVENANCE — 014F
- Seeds/pools: exp200/014-amp-generative-design/data/ (baseline_shuffled.fasta,
  heldout_apd.fasta, apd_natural.fasta - 014's committed).
- Guide: Macrel v1.6.1 (pip), peptides --keep-negatives full-set probabilities.
- Judges: amPEPpy 1.1.0 + pretrained model (github.com/tlawrence3/amPEPpy
  pretrained_models/amPEP.model, 17,166,090 B, downloaded 13:22); AMPlify BCGSC balanced
  weights (github.com/bcgsc/AMPlify models/balanced, cloned 13:21; tf-keras import shim
  only - weights/architecture untouched).
- Generator: ESM-2 t6_8M_UR50D masked decoding (014's generate.py machinery).
- Novelty: MMseqs2 16-747c6 -s 7.5 vs apd_natural.fasta.
