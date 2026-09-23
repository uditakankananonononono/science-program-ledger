---
id: P16-03
title: "GlueBreak: Predicting Resistance Mutations to Molecular Glues and Degraders"
parent: "CBIO046T - Expanding the Druggable Human Proteome Five-Fold (ISEF 2026 Grand Award)"
---

# GlueBreak

**Parent project:** CBIO046T (CRBN/VHL-recruiting glue candidates Ceruclein and Vylodax).

## Premise
Every targeted therapy eventually meets resistance; for glues and degraders, resistance mutations in the E3 ligase machinery (CRBN, VHL, DDB1) and in target degrons are already documented clinically. Nobody has built the prospective map: which mutations break which glue mechanisms before they arise in patients. Deep mutational scanning data for E3 components is appearing in MaveDB, and variant-effect predictors can score every possible substitution. This project builds a resistance-risk atlas for the major glue-recruitment pathways, flags the parental candidates' (CRBN- and VHL-recruiting) most fragile interfaces, and proposes second-site backup recruiters for high-risk nodes.

## Data sources
- MaveDB (public): deep mutational scans of CRBN-pathway components where deposited.
- ClinVar/gnomAD (public): existing clinical and population variants.
- PDB/AlphaFold DB: ligase-substrate interface structures.
- Published degrader-resistance case reports (open literature) for validation.

## Method outline
1. Assemble DMS and variant data for CRBN, VHL, DDB1, and degron motifs of major targets.
2. Score all single substitutions with ensemble variant-effect predictors + interface-energy estimates.
3. Build per-mechanism resistance-risk maps; validate against published resistance cases.
4. Rank interface positions by fragility x clinical-plausibility (present in gnomAD = pre-existing).
5. For the highest-risk nodes, identify alternative ligases/recruitment routes as backups.

## Success gates (locked before results)
- G1: known resistance mutations rank in the top decile of scored variants >= 70% of the time.
- G2: atlas covers >= 4 recruitment mechanisms with per-position fragility scores and CIs.
- G3: >= 5 high-risk variants identified that exist in population databases (pre-existing-risk flags) - or the certified finding that pre-existing resistance is rare.
- G4: backup-recruiter proposals made for all top-risk nodes, with predicted feasibility scores.

## Expected deliverable
The glue-resistance atlas (interactive), the GlueBreak scoring tool (input: glue mechanism; output: fragility map + backup routes), and the pre-existing-risk variant report.

## Failure/pivot rule
If validation data is too sparse for G1, pivot to the prospective-study design: which DMS experiments would close the validation gap cheapest - a prioritized experiment list, gates re-locked around pilot feasibility.
