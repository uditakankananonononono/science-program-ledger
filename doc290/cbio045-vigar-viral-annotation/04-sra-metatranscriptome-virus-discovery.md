---
id: P15-04
title: "SRA Virus Hunt: Discovery and Annotation of Novel Viruses in Public Metatranscriptomes"
parent: "CBIO045 - Viral Genome Annotation with RNNs (ISEF 2024 Grand Award)"
---

# SRA Virus Hunt

**Parent project:** CBIO045 ViGAR (annotation speed enabling new virus characterization).

## Premise
The Sequence Read Archive holds petabytes of host RNA-seq runs that were never screened for viruses; previous large screens (e.g., the Serratus project) proved novel viruses hide there at scale but annotated only RdRP. This project runs a targeted re-screen: assemble viral contigs from under-screened host taxa (neglected tropical-disease vectors, livestock, sentinel wildlife), annotate them with the parent's stack, and release a discovery+annotation compendium. The twist: focus on public-health relevance ranking - every novel virus gets scored for human-host proximity (host taxonomy, tissue, abundance) rather than novelty alone.

## Data sources
- NCBI SRA (public): RNA-seq runs from priority host taxa.
- Serratus project outputs (public): known RdRP catalog for overlap exclusion.
- RefSeq viral + the parent's annotation models for characterization.
- NCBI Taxonomy (public) for host-proximity scoring.

## Method outline
1. Select under-screened SRA run sets by host-taxon prioritization.
2. Assemble (rnaSPAdes-class), viral-call (RdRP + capsid HMMs), and dereplicate contigs.
3. Annotate all novel genomes; classify against known families.
4. Score each discovery for public-health proximity (host, tissue, abundance, family history).
5. Release the compendium with per-virus evidence pages.

## Success gates (locked before results)
- G1: pipeline recovers >= 85% of planted known viruses in positive-control SRA runs.
- G2: >= 200 novel viral contigs (family-level distance from RefSeq) with complete annotation.
- G3: every discovery carries a reproducible evidence page (assembly stats, coverage, annotation confidence).
- G4: proximity ranking completed for 100% of discoveries; top-50 list published with explicit uncertainty.

## Expected deliverable
The novel-virus compendium with annotations and proximity scores, the screening pipeline (open tool), and the host-taxon prioritization map showing where unscreened SRA data still hides.

## Failure/pivot rule
If compute caps the screen scope, pivot to the prioritization deliverable first: the ranked map of highest-yield unscreened SRA sets is itself immediately useful to every group with bigger compute - gates re-locked around map validation on pilot subsets.
