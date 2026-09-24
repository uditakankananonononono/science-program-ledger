# algo50/04 - In-frame hexamer scoring for CDS vs shadow-ORF discrimination, and its cross-genome boundary

Status: LOCKED before any method-vs-method results were computed (lock time recorded in results/lock.txt, sha256 of this file).
Lane: RES-2. Class: algorithm study (not counted toward the flagship 100).

## Question
Bacterial gene finders score coding regions with Markov chains over in-frame hexamers (Glimmer-style). On a gene-dense genome the real decision is not "CDS vs random sequence" but "annotated CDS vs the shadow ORFs that tile the genome in other frames/strands". How well does a plain in-frame hexamer log-likelihood-ratio separate real CDS from stop-to-stop shadow ORFs that contain no annotated gene, and does a model trained on one genome transfer to genomes of different GC content?

## Data
Three complete genomes with annotations via NCBI efetch (GenBank; retrieval timestamp + sha256 in data/):
- E. coli K-12 MG1655 NC_000913.3 (GC ~51%)
- Bacillus subtilis 168 NC_000964.3 (GC ~44%)
- Mycobacterium tuberculosis H37Rv NC_000962.3 (GC ~66%)
Positives: annotated CDS features (joined features collapsed; keep loci with length >= 150 nt and no internal stop in the annotated frame, standard code table 11).
Negatives ("shadow ORFs"): every maximal stop-to-stop ORF (all 6 frames, stops TAA/TAG/TGA) with length >= 150 nt that does NOT wholly contain any annotated CDS on either strand. Subsampled 1:1 against positives, length-matched within 10% where possible, seed 1.

## Task
Binary discrimination, unit = one ORF/CDS region. Score the region in its own frame.

## Methods
- GC: overall GC fraction of the region.
- GC3: GC fraction at third codon positions.
- LEN: region length.
- DI: amino-acid usage log-likelihood ratio (independent aa model, CDS vs shadow ORFs).
- HEX (proposed): in-frame hexamer (5th-order Markov) log-likelihood ratio, P_region under CDS model / under shadow-ORF model, add-1 smoothing.
Trained/evaluated with 5-fold CV, folds split by locus (locus-held-out) within each genome. Transfer: train on all E. coli, test on each other genome.

## Success gates
- G1: within E. coli, HEX AUROC >= best single-feature baseline + 0.05.
- G2: within E. coli, HEX AUROC >= 0.90.
- G3 (transfer gate): HEX trained on E. coli, tested on B. subtilis: AUROC >= 0.85.
- G4 (boundary gate): within M. tuberculosis (5-fold, retrained), HEX AUROC >= 0.90 - in-genome signal persists even if cross-GC transfer fails.
Project PASSES if G1 and G2 pass; G3/G4 are the transfer/boundary gates, reported either way.

## Failure policy
Negative results are recorded as-is. A failed direction triggers a documented pivot with new gates locked in an amendment before new results are inspected; original gates are never re-scored or re-tuned.

## Notes locked in advance
- Pseudogenes and mis-annotations contaminate positives slightly; accepted as label noise.
- Shadow ORFs on the opposite strand of real genes overlap coding sequence and may carry weak coding signal: this is the intended hard setting, not a bug.
- Length enters as an explicit baseline; the 1:1 length-matched subsample limits how far length alone can go.
