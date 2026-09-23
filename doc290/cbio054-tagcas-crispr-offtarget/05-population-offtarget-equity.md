---
id: P17-05
title: "OffTarget-1000G: Population-Variant Personalization of CRISPR Off-Target Risk"
parent: "CBIO054 - 3D-Aware CRISPR Off-Target Prediction (ISEF 2026 Grand Award)"
---

# OffTarget-1000G

**Parent project:** CBIO054 (safer CRISPR screening; risk profiles assume one reference genome).

## Premise
Every off-target predictor scores guides against the reference genome - but patients carry variants, and a SNP can create a new off-target site or destroy the intended one. CRISPR therapies are heading to trials where the treated populations' variation is systematically underrepresented in reference-based screening (sickle-cell therapies being the urgent case). This project overlays 1000 Genomes and gnomAD variation onto off-target models to build population-aware risk profiles: for each therapeutic guide in development, how does the off-target landscape shift across ancestry groups, and which guides are equitable (low risk everywhere) vs. risky in specific populations?

## Data sources
- 1000 Genomes Project (public): population variation across 26 populations.
- gnomAD (public): larger-scale variant frequencies.
- crisprSQL + the parent's models: baseline off-target predictions.
- Published variant-aware off-target analyses (public) for methodology validation.

## Method outline
1. Build variant-aware genome panel: reference + common haplotypes per ancestry group.
2. Re-score published therapeutic-guide off-targets across the panel (variant-created and variant-destroyed sites).
3. Integrate with 3D-gating: do variant-created sites fall in accessible chromatin?
4. Equity metric: per-guide max-across-populations risk vs. reference risk.
5. Rank current clinical guides by equity; propose alternative guides where inequity is found.

## Success gates (locked before results)
- G1: pipeline reproduces published variant-created off-target cases blind (positive controls).
- G2: >= 20 therapeutic guides profiled across >= 5 ancestry groups with complete evidence.
- G3: equity analysis yields actionable divergences (guides whose population-max risk materially exceeds reference risk) or the certified finding that current guides are equitable - both publishable.
- G4: variant-site chromatin-accessibility analysis completed; inaccessible variant sites explicitly down-weighted, not ignored.

## Expected deliverable
The population-aware risk profiles for current therapeutic guides, an equity-ranking report, and OffTarget-1000G as an open tool (guide in; per-population risk panel out) - directly usable in trial design.

## Failure/pivot rule
If variant sites rarely overlap accessible chromatin (risk inflation mostly theoretical), that is itself the certified boundary result: publish the measured interaction rate and pivot to a screening-priority tool (which variants deserve empirical GUIDE-seq testing) - gates re-locked.
