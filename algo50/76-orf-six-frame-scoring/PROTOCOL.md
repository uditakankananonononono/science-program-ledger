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
