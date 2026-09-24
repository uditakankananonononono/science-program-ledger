# 86 - EM transcript quantification (kallisto-lite)

Topic lane-chosen (no list past 55). Question: does EM over k-mer equivalence classes recover true transcript abundances from simulated RNA-seq reads, and where does isoform sharing break attribution?

## Setup (all seeds fixed)
- 200 transcripts: 180 singleton genes + 10 genes x 2 isoforms (isoforms share a 400bp constitutive region; total length 800-1500bp), random sequences seed 86.
- True abundances: geometric (p=0.15), normalized to TPM.
- Reads: 75bp, uniform along transcript, sampled proportional to abundance x length, 1% substitution error. Depths 50k / 200k / 800k, seeds 861/862/863.
- Index: k=31 k-mers -> transcript sets; read equivalence class = intersection of 3 evenly-spaced k-mer sets. EM: 100 iterations on class counts.

## Gates (locked before scoring)
- G1: at 200k depth, Spearman rho >= 0.95 (estimated vs true abundance, all transcripts).
- G2: at 200k, median |log2(est/true)| <= 0.5 for transcripts with true expected count >= 50 reads.
- G3: isoform transcripts with unique-k-mer fraction >= 0.3: |log2(est/true)| <= 1.0 at 200k.
- G4: G2 error non-increasing from 50k to 200k to 800k.

## Failure policy
Failed direction -> documented pivot with new gates locked in an AMENDMENT before new results inspected. Original gates never re-scored. Two amendments max, then ship documented negative.
