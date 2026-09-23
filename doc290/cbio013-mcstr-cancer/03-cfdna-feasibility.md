---
id: P05-03
title: "Can STR Signals Survive cfDNA? A Coverage-Realistic Liquid Biopsy Feasibility Audit"
parent: "CBIO013 - Micro-Changing Tandem Repeats in 10 Human Cancers (source abstract, 2023)"
---

# Can STR Signals Survive cfDNA?

**Parent project:** CBIO013 - detected case-study mcSTR1 in 4 HCC plasma samples, proposing liquid-biopsy diagnosis.

## Premise
cfDNA is fragmented (~167 bp), low tumor-fraction, and shallow - hostile to STR genotyping. A coverage-realistic feasibility audit must precede any liquid-biopsy claim.

## Hypothesis
STR length estimation from cfDNA WGS degrades sharply below 5% tumor fraction and 10x coverage; a targeted-capture or long-read design recovers signal - quantified as a detection limit curve.

## Data sources (free/public)
- Public cfDNA WGS datasets (healthy + cancer: e.g., Cristiano 2019 DELFI cohort raw data where open, SRA cfDNA studies).
- Simulated cfDNA: in silico fragmentation of public tumor WGS (locked fragment model).

## Method outline
1. Characterize STR-locus coverage in real public cfDNA: fraction of the 182 loci with usable spanning reads per sample.
2. Simulation: spike known STR lengths into fragmented backgrounds at locked tumor fractions (0.1-10%); measure genotype recovery vs coverage.
3. Design comparison: WGS vs targeted capture vs long-read (cost per sample at locked detection limits).

## Success gates (locked before results)
- G1: detection-limit curve published: minimum tumor fraction for >= 80% locus recovery at locked coverage.
- G2: if standard cfDNA WGS fails the recovery bar at clinically relevant fractions (<= 1%), say so plainly and report the design that works.
- G3: simulation model validated against real cfDNA locus-coverage distributions before use.

## Expected deliverable
`cfdna-str-limits`: the feasibility toolkit - input sequencing design, get predicted mcSTR recovery and cost, pre-run for the HCC panel.

## Failure/pivot rule
If no affordable design recovers signal at <= 1% tumor fraction, publish the negative: STR-based liquid biopsy is currently coverage-infeasible for early detection.
