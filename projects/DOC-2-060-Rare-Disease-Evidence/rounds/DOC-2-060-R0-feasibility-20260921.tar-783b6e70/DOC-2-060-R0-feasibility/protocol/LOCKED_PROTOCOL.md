# DOC-2-060 R0 locked feasibility/experiment protocol
**Locked:** 2026-09-21 22:53 IST before source-version outcome audit.

Operational output: priority for manual evidence review, never diagnosis/treatment.

Historical cutoff: 2020-12-31. Development outcome: new gene-disease association appearing by 2023-12. Locked replication: appearing by current release among 2023 negatives. A candidate must be absent from all positive outcome sources at cutoff.

Cutoff channels, each from a versioned <=2020 release: (1) HPO phenotype similarity from disease-phenotype and gene-phenotype annotations; (2) gnomAD v2.1.1/v3.1 gene constraint; (3) Europe PMC literature co-mention dated <=cutoff; optional model-organism/pathway from versioned Monarch. Current snapshots may never backfill cutoff IDs/annotations.

Unit: normalized gene-disease pair, grouped by disease and gene for uncertainty. Candidate universe and negatives must be frozen at cutoff. Triangulation is transparent monotonic rank fusion; baselines each channel alone. Abstain on <2 available channels, unmapped disease, or unsupported gene. Gates: >=50,000 candidates, >=1,000 later positives in both transitions, top-1/5/10 enrichment CI>1, >=20% over best channel, calibration slope 0.8-1.2, ablation loss >=10%, controls collapse >=50%, source/license/version manifests complete.

If three historically versioned channels and later labels cannot be reconstructed without current backfill, stop at feasibility. No random split.
