---
id: P15-06
title: "Overlap Resolver: Systematic Detection of Overlapping Viral Genes"
parent: "CBIO045 - Viral Genome Annotation with RNNs (ISEF 2024 Grand Award)"
---

# Overlap Resolver

**Parent project:** CBIO045 ViGAR (CDS annotation; overlapping genes violate the one-ORF-one-gene assumption).

## Premise
Viruses routinely encode genes inside genes - overlapping ORFs in alternate frames - and standard annotation pipelines, ViGAR included, are trained to pick one frame. Overprinted proteins (like SARS-CoV-2 ORF3d or influenza PB1-F2) keep being discovered years after the genome was "finished." This project builds a dedicated overlapping-ORF detector using dual-coding-sequence statistical signatures (SAMEER-style codon-usage asymmetry, synonymous-constraint analysis across virus families) plus pLM evidence, scans the viral RefSeq, and quantifies how much hidden coding capacity the standard annotation model leaves on the table.

## Data sources
- RefSeq viral genomes (public).
- Known overprinted-gene sets from the literature (curated).
- Virus-family genome alignments (public) for synonymous-constraint analysis.
- AlphaFold DB for structural plausibility of predicted novel overlaps.

## Method outline
1. Curate known overlapping-gene positives and length-matched negatives.
2. Implement dual-coding detection: codon-asymmetry statistics + phylogenetic synonymous-constraint.
3. Add pLM/structure plausibility scoring for candidates.
4. Scan RefSeq viral; produce a candidate catalog with evidence tiers.
5. Estimate the hidden-proteome fraction per virus family.

## Success gates (locked before results)
- G1: recovers >= 80% of curated known overlaps at controlled FDR <= 0.2.
- G2: catalog released with per-candidate evidence and confidence; family-level hidden-coding estimates with CIs.
- G3: >= 20 high-confidence novel overlap candidates with structure support (pLDDT threshold locked).
- G4: negative result honored: families where no overlap signal exists are reported as clean, not forced.

## Expected deliverable
The overlapping-gene candidate catalog, the detector (open tool), and the per-family hidden-coding-capacity estimates - a direct measurement of annotation completeness.

## Failure/pivot rule
If statistical signals prove too weak beyond curated cases (G1 fails), pivot to the boundary paper: which virus families/genome sizes permit reliable overlap detection from sequence alone - a methods map, gates re-locked.
