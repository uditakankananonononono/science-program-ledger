---
id: P13-05
title: "AlloCAR Risk Engine: HLA-Mismatch GvHD and Rejection Prediction for Off-the-Shelf Cell Therapy"
parent: "CBIO042 - ReinforCell: CAR-T Cell Optimization Solution (source abstract, 2026)"
---

# AlloCAR Risk Engine

**Parent project:** CBIO042 ReinforCell (making autologous and allogeneic CAR-T more affordable and accessible).

## Premise
ReinforCell's affordability argument depends on allogeneic (donor-derived) products working at scale, and the binding constraint there is immunological: graft-versus-host disease and host-versus-graft rejection. Transplant medicine has decades of HLA-matching data, but cell-therapy-specific risk models barely exist. This project builds an open risk engine that predicts allogeneic cell-therapy compatibility from HLA genotype features, killer-cell immunoglobulin-like receptor (KIR) haplotypes, and published outcome cohorts - and quantifies how many donors a "universal bank" would need to cover a population, translating immunogenetics into a manufacturing-planning tool.

## Data sources
- IPD-IMGT/HLA database (public): HLA allele sequences and nomenclature.
- IPD-KIR database (public): KIR gene content and haplotypes.
- Published CIBMTR transplant-outcome cohort statistics (open summaries) for GvHD-risk calibration.
- 1000 Genomes Project HLA-region calls for population coverage modeling.

## Method outline
1. Build an HLA-divergence feature set: allele-level mismatch counts, evolutionary divergence scores (HED), and predicted peptide-binding repertoire overlap.
2. Integrate KIR-HLA ligand pairing rules from IPD-KIR into a compatibility score.
3. Calibrate the score against published transplant outcome gradients (survival/GvHD rates by mismatch class).
4. Simulate donor-bank design over 1000 Genomes population HLA frequencies: coverage vs. bank size for multiple ancestry groups, with equity analysis of which populations are hardest to cover.
5. Package as a planning tool: given target population and acceptable risk threshold, output minimum bank size and optimal donor recruitment mix.

## Success gates (locked before results)
- G1: compatibility score reproduces published outcome gradients (monotonic risk ordering across >= 3 mismatch classes) on held-out cohort summaries.
- G2: bank-size simulation converges (coverage estimates stable within +/-2% under resampling).
- G3: equity analysis identifies ancestry groups with >= 2x donor-requirement disparity, or documents that disparity is absent at current resolution (either outcome is a finding).
- G4: if calibration data proves too aggregated to validate G1, document the evidence gap and ship the simulator with clearly labeled unvalidated risk curves.

## Expected deliverable
An open "AlloBank" planning tool (bank-size vs. coverage calculator with equity breakdown), the compatibility-scoring code, and a report on donor-bank feasibility for off-the-shelf cell therapy across ancestries.

## Failure/pivot rule
If outcome calibration fails (G4), pivot fully to the population-genetics simulator - coverage curves are valid without clinical calibration - and frame the clinical-validation gap as the study's central warning.
