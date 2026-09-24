# algo50/12 - Two-state dinucleotide HMM vs the Gardiner-Garden window rule for CpG islands

Status: LOCKED before any method-vs-method results were computed (lock time in results/lock.txt, sha256 of this file).
Lane: RES-2. Class: algorithm study (not counted toward the flagship 100).

## Question
The classic CpG island criterion (Gardiner-Garden & Frommer 1987: window >=200 bp, GC >= 50%, CpG observed/expected >= 0.6) is a hard window rule. Does a two-state (island/non-island) HMM with dinucleotide emissions (Durbin et al. style) recover annotated islands better, and does the window dinucleotide log-likelihood ratio alone (no segmentation) already beat the rule?

## Data
- Sequence: human chr22 (hg38, NC_000022.11), 2 Mb region seq_start=20000001 seq_stop=22000000 via NCBI efetch FASTA (timestamp + sha256 in data/).
- Labels: UCSC hg38 cpgIslandExt track (hgdownload.soe.ucsc.edu), islands intersecting the region.
- Train/test split: first half of the region (10 Mb) trains HMM emissions + transitions from labels; second half is the test bed (all reported metrics on the second half only).
- Windows: 200 bp windows every 100 bp over the test half; window label = annotated island covers >= 50% of the window.

## Methods
- RULE: Gardiner-Garden per window (GC >= 0.5 AND o/e CpG >= 0.6).
- LLR: window mean dinucleotide log-likelihood ratio (island model vs non-island model, add-1 smoothing), thresholded at 0.
- HMM (proposed): two-state Viterbi over dinucleotide emissions with label-trained transition probabilities; window called island if >= 50% of its positions decode as island state.

## Success gates
- G1: HMM window-level F1 >= RULE F1 + 0.10.
- G2: island-level recall: >= 70% of test-half annotated islands have >= 50% of their length covered by HMM island calls.
- G3: LLR window-level F1 >= RULE F1 + 0.05.
- G4: median length of HMM island segments within [0.5x, 2x] the median length of annotated islands it overlaps (segmentation sanity).
Project PASSES if G1 and G2 pass; G3/G4 reported either way.

## Failure policy
Negative results recorded as-is; a failed direction triggers a documented pivot with gates locked in an amendment before new results are inspected.

## Notes locked in advance
- UCSC cpgIslandExt is itself rule-derived (Gardiner-Garden-like with tweaks): agreement with it partially measures the rule, not biology. Documented circularity; a truly independent label set (e.g., unmethylated regions) is out of scope.
- chr22 is gene-rich and acrocentric; absolute numbers will not transfer to gene deserts.
