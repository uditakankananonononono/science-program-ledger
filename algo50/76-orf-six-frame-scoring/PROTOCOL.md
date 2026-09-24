# algo50/76 - ORF finding: longest-ORF vs codon-scored six-frame search

Status: LOCKED before any results (results/lock.txt). Lane RES-2. Algorithm study. Topic lane-chosen (no list past 55).

## Question
Naive gene finding picks the longest ORF; codon-usage scoring should beat it when a long non-coding ORF outlives the true CDS. Quantify: P(longest ORF != true gene) as non-coding ORF length grows, and the rescue from a simple in-frame hexamer/CDS-score (reusing 04's hexamer machinery on E. coli).

## Data
Real E. coli genome (NC_000913.3, already in repo from 04, hashed). Known protein-coding genes from its GenBank features (CDS with gene names, length >= 300bp, first isoform per gene, up to 1500 genes). Context: for each gene, take its genomic span +/- 3kb flanks.
Hexamer score table: from 04's CDS-vs-intron... from this genome: in-frame hexamer frequencies in all other CDS vs shuffled non-coding background (built once, hashed).

## Methods
For each gene locus: (a) LONGEST: longest ORF (ATG..stop, same strand) in the locus region - predicted gene = that ORF; (b) SCORED: among ALL ORFs in region, pick max mean log-odds hexamer score per codon. Correct if predicted ORF's stop codon == true CDS stop AND same frame (start may differ - start prediction is a separate problem, documented).
Background: true gene wins ties... no ties possible; score.

## Gates
- G1: SCORED correct-stop rate >= LONGEST correct-stop rate + 0.10 overall.
- G2: LONGEST fails >= 15% of loci (long wrong ORFs exist and mislead).
- G3: SCORED correct-stop rate >= 0.85.
- G4: when LONGEST != SCORED choice, SCORED right in >= 60% of disagreements.
PASS if all.

## Failure policy
Negatives preserved; pivots via locked amendments.

---

# AMENDMENT 1 (locked before pivot scoring)
Original scored variant has a known modeling flaw plus a hard design regime: (a) MEAN log-odds per codon favors short ORFs (variance ~ 1/length) - the standard fix is TOTAL log-odds; (b) +/-3kb flanks include real neighboring genes, so longest-ORF-in-region often legitimately picks a neighbor (both methods ~2-16% correct-stop). Both documented as the original's findings.
Pivot P (same lock, same genome): score = TOTAL log-odds (sum over codons); report flank +/-1kb AND +/-3kb.
- P1: total-scored correct-stop >= longest + 0.10 at both flank sizes.
- P2: total-scored correct-stop >= 0.60 at +/-1kb.
- P3: at +/-3kb, longest-ORF picks a DIFFERENT REAL gene (neighbor) in >= 30% of its errors - the "longest is real, just elsewhere" effect, measured by checking whether the longest ORF's stop matches any other true CDS stop in the test set.
PASS if P1+P3.
