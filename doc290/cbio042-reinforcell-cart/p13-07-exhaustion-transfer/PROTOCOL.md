# P13-07 Exhaustion Transfer Stress Test - locked protocol

Locked 2026-09-24 10:55 IST, before any label, classifier or transport result was computed.
Data: CELLxGENE Census 2025-11-08 (stable), human, cell_type == 'CD8-positive, alpha-beta T cell',
is_primary_data == True. The only thing seen before locking: per-dataset cell counts.

## Cohorts (dataset x disease x tissue x assay, >=500 CD8 cells), capped at 2000 cells, seed 0 (cap lowered from 4000 at 11:01 IST, before any expression data was read, because the 2 GB build sandbox cannot hold more)
C01 RCC kidney 10x5' (5af90777) | C02 LUAD lung 10x3'v2 (1e6a6ef9) | C03 LUAD lung BD Rhapsody (1e6a6ef9)
C04 LUAD lung Smart-seq2 (1e6a6ef9) | C05 LUSC lung 10x3'v2 (1e6a6ef9) | C06 colon adenocarcinoma 10x3'v2 (16023185)
C07 LUAD lung 10x3'v2 (9f222629, independent study) | C08 breast IDC 10x5'v1 (9fddb063)
C09 oropharynx SCC 10x3'v3 (b6b5ea88) | C10 B-NHL lymph node 10x multiome (67b6b9ac)
C11 COVID-19 blood 10x5'v2 (9dbab10c) - acute viral infection, the out-of-cancer arm.
Limit declared up front: no chronic HIV/HCV CD8 cohort with >=500 primary cells exists in Census; C11 is acute, not chronic.

## Labels (report instability first)
Exhaustion gene set EXH = PDCD1 HAVCR2 LAG3 TIGIT CTLA4 TOX ENTPD1 CXCL13 LAYN (fixed literature baseline).
- L1 score label: per cohort, mean z-scored log1p-CP10k EXH; top tertile = 1, bottom tertile = 0, middle dropped.
- L2 cluster label: per cohort Leiden (res 1.0) on PCA of HVGs; clusters whose mean EXH score is in the top
  third of clusters = 1, bottom third = 0.
Instability = Cohen's kappa between L1 and L2 on cells labeled by both.
Classifier features EXCLUDE all EXH genes (no leakage).

## Models
Logistic regression (L2, C=0.1, standardized) and HistGradientBoosting, trained per cohort per label,
tested on every other cohort. Feature panel = genes that are top-2000 HVG in >= 3 cohorts and present in all.
AUC with 200-resample bootstrap 95% CI.

## Gates
- G1: transport matrix complete over >= 8 cohorts with CIs reported.
- G2: portable only if median cross-cohort AUC >= 0.75 AND worst-case >= 0.65 (primary: logistic, L1);
  otherwise certified non-transport.
- G3: linear variance decomposition of the transport deficit (in-cohort AUC minus cross-cohort AUC) on
  named factors {platform family differs, tissue differs, disease class differs, label definition differs}
  attributes >= 60% of variance (R^2 >= 0.60).
- G4: certified non-transport with a named dominant factor counts as full success.
Evaluated once. Any instrument repair is disclosed.
