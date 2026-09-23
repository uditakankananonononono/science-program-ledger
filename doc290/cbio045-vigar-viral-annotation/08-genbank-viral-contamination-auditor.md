---
id: P15-08
title: "VirAudit: Contamination and Mislabel Detection in Public Viral Genome Records"
parent: "CBIO045 - Viral Genome Annotation with RNNs (ISEF 2024 Grand Award)"
---

# VirAudit

**Parent project:** CBIO045 ViGAR (GenBank as the substrate; its data quality is assumed, not verified).

## Premise
Every annotation pipeline trusts its inputs, but public viral genomes carry host contamination, mislabeled taxonomy, chimeric assemblies, and vector sequence - and errors propagate: one contaminated genome trains a hundred models. This project builds an auditor that flags suspect viral records using internal evidence alone: annotation inconsistency (the parent's models disagreeing with deposited labels), k-mer composition outliers within families, host-ribosomal signatures, and assembly-coverage pathologies. The deliverable is both a cleanup (flagged list to NCBI-style curation workflows) and a measurement: the error rate of the substrate the whole field builds on.

## Data sources
- GenBank viral division (public): the audit target.
- RefSeq viral (public): the trusted reference backbone.
- UniVec/host-genome references (public): contamination detection.
- NCBI Taxonomy (public): label-consistency checks.

## Method outline
1. Compute per-record evidence channels: composition outliers, annotation-model disagreement, host-signature hits, taxonomy-tree outliers.
2. Build a calibrated suspicion score from channels; hand-audit a stratified sample to estimate precision.
3. Estimate the overall contamination/mislabel rate with CIs.
4. Rank flags by downstream-impact (how many tools/citations consume each record).
5. Release the auditor + flagged list with a dispute-friendly evidence format.

## Success gates (locked before results)
- G1: hand-audited precision >= 0.85 at a fixed recall operating point (locked).
- G2: substrate error-rate estimate produced with CIs, stratified by family and deposit year.
- G3: >= 1 known-retracted or corrected record recovered blind (positive control).
- G4: zero-flag list also published: records passing all channels - the clean-core set the field can train on safely.

## Expected deliverable
The VirAudit tool, the flagged/clean lists with evidence, and the substrate-error-rate study - a data-quality baseline for viral genomics.

## Failure/pivot rule
If hand-audit precision fails G1, the channels are individually weak: pivot to shipping the per-channel diagnostics as standalone QC metrics (each still useful) with combined-score development marked as future work - gates re-locked.
