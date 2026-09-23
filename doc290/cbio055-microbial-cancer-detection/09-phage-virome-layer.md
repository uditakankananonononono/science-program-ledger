---
id: P18-09
title: "Phage Layer: Adding the Gut Virome as a Third View for Cancer Detection"
parent: "CBIO055 - Early Cancer Detection Using Microbial Information (source abstract, 2023)"
---

# Phage Layer

**Parent project:** CBIO055 Microbial Cancer Detection (taxonomy + microbial function features from >2000 tumor and blood samples; 18% synergy gain in tissue, weaker in cfDNA).

## Premise
The parent combined two views of bacterial and fungal DNA. Every stool metagenome also carries phage DNA, usually discarded. Phages track bacterial hosts at strain level and respond to inflammation, and CRC virome shifts have been reported (Nakatsu et al. 2018 Gastroenterology). This project adds the virome as a third view and tests for three-way synergy.

## Hypothesis
Adding phage features to taxonomy + function improves CRC LOCO AUROC by >= 0.03.

## Data sources (free/public)
- CRC stool shotgun cohorts with raw reads on ENA/SRA (subset of curatedMetagenomicData cohorts).
- Gut Phage Database (Camarillo-Guerrero et al. 2021) and Metagenomic Gut Virus catalogue (Nayfach et al. 2021), both public.
- geNomad and CheckV (free tools) for viral contig detection.

## Method outline
1. Map reads to a public gut phage catalogue to build phage abundance profiles (viral OTU level).
2. Predict phage hosts (catalogue annotations) to build host-linked phage features.
3. Train taxonomy, function, phage and all combinations; LOCO evaluation.
4. Check whether phage signal is independent of host abundance (partial correlations).

## Success gates (locked before results)
- G1: three-view model beats two-view by >= 0.03 LOCO AUROC (paired bootstrap p < 0.05).
- G2: >= 5 phage features remain significant after conditioning on host abundance.
- G3: per-cohort 95% CIs; null gain reported as the result.

## Expected deliverable
Phage abundance tables for public CRC cohorts, a three-view benchmark, and a list of host-independent phage markers.

## Failure/pivot rule
If phages only mirror their hosts (G2 fails), report that result and pivot to phage-host ratio features (lysogeny/induction proxies) as the candidate independent signal.
