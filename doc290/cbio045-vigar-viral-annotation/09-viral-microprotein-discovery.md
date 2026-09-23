---
id: P15-09
title: "MicroViral: Small-ORF Discovery in Viral Genomes With Ribo-seq Evidence"
parent: "CBIO045 - Viral Genome Annotation with RNNs (source abstract, 2024)"
---

# MicroViral

**Parent project:** CBIO045 ViGAR (CDS annotation; small ORFs below the length threshold are systematically invisible).

## Premise
Annotation pipelines enforce minimum ORF lengths, so viral microproteins (<100 aa) are under-called everywhere - yet the few characterized ones (viroporins, immune antagonists) punch far above their size in pathogenicity. Ribo-seq of infected cells now gives direct translation evidence. This project combines translation evidence (public viral-infection Ribo-seq), sequence signals, and structure prediction to build the first cross-virus small-ORF catalog, then asks the biology question: are microproteins enriched for host-interaction and immune-evasion functions, as the case studies suggest?

## Data sources
- Public Ribo-seq datasets from viral-infection studies (SRA; Trips-Viz/GWIPS-viz browsers).
- RefSeq viral genomes (public).
- SmProt/OpenProt-style small-ORF resources (public) as method references.
- AlphaFold DB / ESMFold for microprotein structure plausibility.

## Method outline
1. Aggregate public viral-infection Ribo-seq; map translated small ORFs per virus.
2. Train a small-ORF caller on Ribo-seq-supported positives with calibrated confidence.
3. Scan RefSeq viral genomes; catalog candidates with evidence tiers.
4. Structure/function prediction for high-confidence set; host-interaction enrichment analysis.
5. Comparative analysis: microprotein density vs. genome size and family.

## Success gates (locked before results)
- G1: caller recovers >= 80% of Ribo-seq-supported sORFs held out per virus.
- G2: catalog spans >= 200 viruses with confidence tiers.
- G3: host-interaction/immune-evasion enrichment test completed; result reported either direction with effect size.
- G4: >= 30 high-confidence novel microproteins with structure support, or the honest lower number with the sensitivity analysis.

## Expected deliverable
The cross-virus microprotein catalog, the sORF caller (open tool), and the enrichment study on microprotein function - plus per-virus annotation addenda.

## Failure/pivot rule
If Ribo-seq coverage is too sparse across families (G2 fails), pivot to the coverage-map deliverable: which viruses need infection-model Ribo-seq to close the microprotein gap - a targeted experimental agenda with pilot validation, gates re-locked.
