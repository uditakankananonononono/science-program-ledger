---
id: P17-04
title: "GuidePilot: Unified On-Target Efficacy + 3D Off-Target Risk Guide Selection"
parent: "CBIO054 - 3D-Aware CRISPR Off-Target Prediction (source abstract, 2026)"
---

# GuidePilot

**Parent project:** CBIO054 TAG-Cas (off-target risk model; efficacy and risk are currently chosen with separate tools that ignore each other).

## Premise
Therapeutic guide design today is a two-step patchwork: score efficacy with one model (Rule Set 2/CRISPick lineage), score off-targets with another, eyeball both. The tradeoff is real - the highest-efficacy guide often sits in open chromatin where off-targets also cut. This project builds the unified selector: joint training on public efficacy screens and crisprSQL off-target data with 3D features, a Pareto frontier of efficacy vs. off-target risk per target site, and cell-type-specific risk weighting (the off-target that matters in hematopoietic stem cells differs from hepatocytes). The deliverable is the tool clinicians would actually use: gene + cell type in; ranked guides with both numbers and an honest uncertainty flag out.

## Data sources
- Public guide-efficacy screens (Doench-lineage datasets, CRISPick training data).
- crisprSQL (public): off-target labels.
- ENCODE/4DN: cell-type Hi-C/ATAC panels for risk weighting.
- Published therapeutic-guide case studies (public) for validation.

## Method outline
1. Harmonize efficacy and off-target datasets to a common guide schema.
2. Train joint model with shared 3D/chromatin encoder and two heads (efficacy, off-target).
3. Construct per-site Pareto frontiers; define selection policies for clinical vs. research use.
4. Cell-type risk weighting from matched epigenome panels.
5. Validate on published therapeutic-guide choices (does the tool rank the clinically chosen guides highly - and where it doesn't, why?).

## Success gates (locked before results)
- G1: joint model matches specialist single-task models within 0.02 PR-AUC/R^2 each (no performance tax for unification).
- G2: Pareto-frontier analysis shows >= 20% of target sites have a strictly better guide than the efficacy-only pick - the value-of-joint-selection number.
- G3: therapeutic-case validation: clinically used guides rank in tool's top tier, or divergences are each explained.
- G4: uncertainty flags calibrated: flagged guides genuinely have wider outcome spread.

## Expected deliverable
GuidePilot (gene + cell type in; Pareto-ranked guides out), the value-of-joint-selection study, and the cell-type risk-weighting framework - usable by any CRISPR therapeutic program.

## Failure/pivot rule
If G2 shows the tradeoff is trivial (efficacy pick almost always optimal), that is the certified result: publish the negative and pivot the tool to pure risk-auditing of pre-chosen guides - gates re-locked.
