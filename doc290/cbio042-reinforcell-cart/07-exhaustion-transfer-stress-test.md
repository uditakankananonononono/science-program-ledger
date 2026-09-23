---
id: P13-07
title: "Exhaustion Transfer Stress Test: Cross-Cohort Transport of T-Cell Exhaustion Signatures"
parent: "CBIO042 - ReinforCell: CAR-T Cell Optimization Solution (source abstract, 2026)"
---

# Exhaustion Transfer Stress Test

**Parent project:** CBIO042 ReinforCell (in vivo prediction engine trained on longitudinal single-cell data).

## Premise
ReinforCell predicts exhaustion within its training context; nobody has stress-tested whether exhaustion signatures transport across cancers, products, and platforms. Field experience (including our own PAIR-GUARD work) says biomarker models routinely fail external validation. This project systematically trains exhaustion predictors on each major public T-cell single-cell cohort and tests them on every other cohort - a full leave-one-cohort-out transport matrix across tumor-infiltrating lymphocyte, CAR-T infusion-product, and chronic-infection datasets. The output is either a validated portable signature or a precise map of where transport breaks and why (batch, tissue, disease, or definition instability) - both outcomes are useful; the second is arguably more valuable.

## Data sources
- Public TIL scRNA-seq atlases via CELLxGENE Census and the Single Cell Portal (melanoma, NSCLC, colorectal, breast cohorts).
- Published CAR-T infusion-product single-cell datasets (e.g., the CD19 CAR-T axi-cel product datasets on GEO).
- Chronic-viral-infection T-cell exhaustion scRNA datasets (LCMV-model human-analog cohorts and HIV/HCV human datasets on GEO).
- Curated exhaustion gene sets from the literature as fixed baselines.

## Method outline
1. Harmonize 8+ cohorts to a common gene space with careful batch metadata.
2. Define multiple exhaustion labels (literature gene-set score, cluster-derived, trajectory-inferred) and report label instability first.
3. Train compact classifiers (logistic + gradient boosting) per cohort; evaluate on all others - full N x N transport matrix.
4. Decompose transport failure: how much is explained by platform, tissue, disease, and label definition (variance decomposition).
5. Search for a minimal portable core signature; if none exists, certify that with the matrix evidence.

## Success gates (locked before results)
- G1: transport matrix complete over >= 8 cohorts with CIs reported.
- G2: a signature is declared portable only if median cross-cohort AUC >= 0.75 with worst-case >= 0.65; otherwise the result is certified non-transport.
- G3: variance decomposition attributes >= 60% of transport failure to named factors (platform/tissue/disease/label).
- G4: honest-negative clause: certified non-transport with a named dominant factor counts as full success, per program standing rules.

## Expected deliverable
The exhaustion transport matrix (paper + interactive figure), either a validated portable core signature or a certified non-transport map with the dominant failure factor, and a "transport check" auditor tool that scores any proposed exhaustion signature against the matrix.

## Failure/pivot rule
Failure is pre-pivot-proofed: both G2 outcomes ship. If cohort harmonization itself fails (insufficient overlap), pivot to a metadata-standards report defining what future exhaustion studies must deposit to make transport testable - gates re-locked.
