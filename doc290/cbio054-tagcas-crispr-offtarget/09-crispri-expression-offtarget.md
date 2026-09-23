---
id: P17-09
title: "SilenceOff: Off-Target Prediction for Epigenome Editors (dCas9 Effectors)"
parent: "CBIO054 - 3D-Aware CRISPR Off-Target Prediction (ISEF 2026 Grand Award)"
---

# SilenceOff

**Parent project:** CBIO054 (cutting off-targets; epigenome editors don't cut - their off-targets are expression changes).

## Premise
dCas9-based epigenome editors (CRISPRi/a, base-methylating effectors) are the next therapeutic wave - no breaks, no mutations, so they're assumed safe. But their off-targets are subtler: mis-silenced or mis-activated genes, potentially far from the guide site because these effectors act across 3D contact domains. Public CRISPRi screens (genome-wide, with expression readouts) and DepMap make off-target expression effects measurable at scale. This project builds the first off-target framework for epigenome editors: guide in; predicted expression-perturbation map out - with 3D contact domains as the physical mechanism, extending the parent's topology thesis to a modality where it should matter even more.

## Data sources
- Public genome-wide CRISPRi screens with RNA-seq readouts (Gilbert/Horlbeck-lineage datasets).
- DepMap (public): CRISPRi/CRISPR screen data across lines.
- ENCODE/4DN: Hi-C contact domains + histone tracks.
- Published dCas9-effector specificity studies (public) for validation.

## Method outline
1. Harmonize CRISPRi screens with guide and expression-change labels.
2. Model per-guide expression off-targets: sequence similarity + contact-domain membership + enhancer/promoter context.
3. Test the 3D hypothesis: are off-target expression effects enriched within the target's contact domain?
4. Build the predictor; validate leave-one-screen-out.
5. Safety-rank published dCas9-effector therapeutic proposals.

## Success gates (locked before results)
- G1: expression-off-target prediction AUC >= 0.72 held-out, or the certified finding that guide-specific expression off-targets are unpredictable from context.
- G2: contact-domain enrichment quantified (effect size + CI) - the mechanistic headline, either direction.
- G3: >= 2 published therapeutic dCas9 proposals safety-ranked with transparent evidence.
- G4: validation against published specificity studies: model flags match reported off-targets in >= 70% of cases.

## Expected deliverable
SilenceOff (guide + effector in; expression-risk map out), the contact-domain enrichment study, and the harmonized CRISPRi off-target dataset - the safety framework for the no-cutting era.

## Failure/pivot rule
If expression readouts are too noisy across screens (G1), pivot to the screen-quality audit: which CRISPRi screens have sufficient replication/sensitivity for off-target learning - plus the cleaned subset, gates re-locked.
