---
id: P05-02
title: "ExpansionHunter vs GangSTR vs HipSTR: A Truth-Set Benchmark for Cancer STR Genotyping"
parent: "CBIO013 - Micro-Changing Tandem Repeats in 10 Human Cancers (source abstract, 2023)"
---

# STR Genotyper Truth-Set Benchmark

**Parent project:** CBIO013 - entire result depends on ExpansionHunter genotypes; genotyper choice can change which loci look "micro-changing."

## Premise
STR genotypers disagree systematically by motif, length, and coverage. Public truth sets (assembled haplotypes, GIAB-adjacent STR references) let us measure per-tool accuracy and re-derive the parent's conclusions per tool.

## Hypothesis
Tool disagreement concentrates at long/motif-complex loci; >= 10% of the parent's significant mcSTR associations are tool-specific and disappear under at least one alternative genotyper.

## Data sources (free/public)
- Public long-read assemblies (HPRC/HGSVC) as STR truth.
- ExpansionHunter, GangSTR, HipSTR (all open); TCGA/1000G WGS.

## Method outline
1. Benchmark the three tools against assembly-derived truth at the 182 mcSTR loci: concordance, length bias, dropout by motif/coverage.
2. Re-run the cancer-association tests with each tool's genotypes; per-locus robustness classification (all-tools / two-tools / single-tool).
3. Publish a per-locus recommended tool + confidence.

## Success gates (locked before results)
- G1: per-tool genotype concordance vs truth reported per motif class - no pooled averages hiding motif-specific failure.
- G2: robustness classification for all 182 loci published; single-tool loci explicitly flagged in any downstream use.
- G3: association re-tests use identical statistical pipelines across tools.

## Expected deliverable
`strbench`: benchmark harness + the per-locus tool-confidence table for the mcSTR panel, reusable for any STR study.

## Failure/pivot rule
If most associations are single-tool, publish the tool-dependence audit and restrict the biomarker panel to all-tool-robust loci only.
