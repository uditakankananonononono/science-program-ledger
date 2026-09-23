# PPD-v2 — methylation-first PPD biomarkers (user-steered new direction, main 00:20)
# GATES locked 2026-09-24 ~00:42 IST, before any probe-level outcome inspection. EXP-1.
# NOT re-fishing the failed RNA-seq panels (v4 clause stands for those datasets).

## Cohort reality (documented before locking)
Only ONE public PPD-specific blood methylation cohort with labels exists in GEO:
GSE44132 (450K, antenatal whole blood, postpartum-depression labels: 23 yes / 32 no,
5 array batches). Excluded after verification: GSE43460 (mouse), GSE114685 (neurons),
GSE153934 (mouse adipose), GSE179393 (cardiac), GSE201287 (MDD blood, idat-only),
GSE35141 (cancer), GSE98203 (heroin brain), GSE192918 (no depression labels),
GSE32528/GSE43462/GSE41826 (brain/methods). No independent PPD methylation cohort
exists publicly -> the external-verification design below is honestly weaker and says so.

## Data (public; URLs + SHA-256 in provenance)
- DISCOVERY: GSE44132 series matrix (beta values, 483,267 probes x 55 samples).
- Platform annotation: GPL13534 (Illumina 450K) for probe->gene/chr mapping.
- CROSS-PHENOTYPE (attempt only): GSE201287 MDD blood 450K (idat raw) - requires
  python idat parsing (methylcheck via pip); if install/parse fails, leg is documented
  as infeasible, not silently dropped.

## Frozen design
- M-values: M = log2(beta/(1-beta)), beta clipped to [1e-4, 1-1e-4].
- Probe QC: drop probes with any missing value; autosomal only (chr 1-22 from GPL13534).
- Selection: top 200 probes by |t| (Welch, PPD vs no) inside each training fold only.
- Model: ElasticNet logistic (l1_ratio 0.5, C=1.0, saga, tol 1e-2), frozen seeds.
- Named published baseline (ISEF): Osborne/Payne HP1BP3 + TTC9B candidate regions -
  all 450K probes annotated to HP1BP3 or TTC9B (GPL13534); baseline score = mean z(M)
  of those probes. Frozen construction.

## Gates
- G1 (discovery): CV with BATCH-GROUPED folds (GroupKFold by array batch - batch
  cannot leak into fold-mates) mean AUROC >= 0.70 AND 200 full-pipeline permutations
  with observed > ALL nulls.
- G2 (internal-external, honestly weaker - declared): train on array batches 1-4,
  apply ONCE to batch 5: AUROC >= 0.65 AND bootstrap 95% CI lower > 0.5. If batch 5
  has <3 of either class, use batches 4+5 as holdout, declared in an addendum before
  running.
- G2c (named baseline gate): panel must beat the HP1BP3+TTC9B candidate-region score
  by >= 0.03 AUROC on the SAME held-out batch(es).
- G3 (cross-phenotype transport, reported if computable): frozen panel on GSE201287
  MDD blood - AUROC reported with CI; no pass/fail (different phenotype), interpreted
  as "does the PPD epigenetic signature generalize to major depression?"
- Mechanism check: panel genes vs HP1BP3/TTC9B/OXTR/estrogen-responsive literature.
- Tool + nomination: ppd_methyl_score.py CLI + top CpG nominated for a targeted
  bisulfite-pyrosequencing assay (only if G2 passes).
- Failure: if G1 fails -> documented boundary for the methylation angle; next new
  direction per main = multi-cohort joint training across the RNA-seq cohorts with
  leave-one-cohort-out (fresh gates, PPD-v3).
