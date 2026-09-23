---
id: P15-05
title: "FrameShift Finder: Deep Detection of Programmed Ribosomal Frameshifting in Viral Genomes"
parent: "CBIO045 - Viral Genome Annotation with RNNs (source abstract, 2024)"
---

# FrameShift Finder

**Parent project:** CBIO045 ViGAR (CDS mapping; frameshifts are the annotation edge case RNNs handle badly).

## Premise
Programmed ribosomal frameshifting is how viruses pack multiple proteins into minimal genomes - essential in coronaviruses, retroviruses, and most RNA viruses - yet frameshift sites are systematically misannotated or missed by both ORF-finders and sequence models trained on single-frame assumptions. This project builds a dedicated frameshift detector (sequence + RNA-structure + comparative signals), applies it across RefSeq viral genomes, and produces the first comprehensive frameshift-site catalog with confidence scores. Correct frameshift calls change the protein inventory of thousands of viruses; wrong ones poison downstream annotation, so calibration is the core science.

## Data sources
- RefSeq viral genomes with curated frameshift annotations (public): label set.
- Published Ribo-seq viral-infection datasets (SRA): orthogonal evidence of translation.
- ViennaRNA/RNAstructure (open tools) for structure signals.
- Recode-2-style curated frameshift lists from the literature.

## Method outline
1. Curate positive (curated sites) and hard-negative (homopolymer/shifty-mimic) sets.
2. Engineer features: shifty heptamers, downstream pseudoknot/stem-loop stability, codon usage, comparative conservation.
3. Train a calibrated classifier; scan all RefSeq viral genomes.
4. Validate a subset against viral Ribo-seq data where it exists.
5. Quantify annotation impact: how many genomes gain/change protein calls.

## Success gates (locked before results)
- G1: held-out curated-site recall >= 85% at precision >= 0.8 (calibrated).
- G2: catalog covers all RefSeq viral genomes with confidence tiers.
- G3: >= 1 known major-virus frameshift recovered without using its label (leave-one-family-out test).
- G4: Ribo-seq concordance reported where data exists; discordances analyzed, not hidden.

## Expected deliverable
The viral frameshift catalog (versioned), the detector as an open tool, and the annotation-impact analysis showing how protein inventories change.

## Failure/pivot rule
If Ribo-seq validation shows systematic overcalling (G4 discordance), pivot to the calibration paper: where sequence-only frameshift detection hits its information limit - gates re-locked around calibrated reissue.
