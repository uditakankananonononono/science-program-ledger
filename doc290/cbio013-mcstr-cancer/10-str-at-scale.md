---
id: P05-10
title: "STR Genotyping at Population Scale: A Cost-Optimized Open Pipeline Benchmark"
parent: "CBIO013 - Micro-Changing Tandem Repeats in 10 Human Cancers (source abstract, 2023)"
---

# STR Genotyping at Population Scale

**Parent project:** CBIO013 - genotyped 2,622 genomes; scaling STR analysis to 100k+ genomes needs measured cost/accuracy engineering nobody publishes.

## Premise
Every future mcSTR study hits the same wall: per-genome genotyping cost. A benchmarked, spot-instance-ready pipeline with published cost-per-genome makes the science reproducible at scale.

## Hypothesis
A sharded open pipeline (ExpansionHunter/GangSTR + targeted-loci mode) genotypes the 182-locus panel at <= $0.15/genome on spot compute while matching full-genome-mode accuracy at >= 99% concordance.

## Data sources (free/public)
- 1000G/TCGA open WGS CRAMs (public buckets).
- Open genotypers; public cloud spot pricing (documented, no spend - benchmark on free credits/local).

## Method outline
1. Implement targeted-loci vs whole-genome genotyping modes; measure accuracy concordance on a locked truth subset.
2. Profile runtime/memory per shard; build the cost model from published spot prices (no money spent - model + small free-tier runs only).
3. Publish scaling curves (genomes/hour, $/genome) and failure modes (low-coverage samples, CRAM access patterns).

## Success gates (locked before results)
- G1: targeted-mode concordance >= 99% vs full mode at panel loci, else the cheap mode is rejected for science use.
- G2: modeled cost <= $0.15/genome with all assumptions published; clearly labeled as a cost model, not spend.
- G3: pipeline reproduces from the repo on a fresh machine (one-command).

## Expected deliverable
`strscale`: the containerized pipeline + published cost/accuracy scaling curves - the tool every subsequent STR study reuses.

## Failure/pivot rule
If cheap mode loses accuracy, publish the accuracy-cost frontier so users can pick their operating point with open eyes.
