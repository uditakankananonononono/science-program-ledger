# PPD-v2: methylation-first postpartum depression biomarkers
USER-STEERED new direction (main 00:20, user verbatim "Try new directions, more biomarkers").

**Result: all primary gates PASS - candidate useful result, submitted for adjudication.**

## Design (GATES.md locked BEFORE outcomes; addendum1 = annotation source)
- Discovery: GSE44132, the ONLY public PPD blood 450K cohort with labels (23 PPD / 32 no,
  antenatal whole blood, 5 array batches). Cohort-reality documented in gates.
- M-values, autosomal complete probes (467,018), in-fold top-200 |t| + ElasticNet (l1 0.5).
- Batch-grouped CV (GroupKFold by array batch; batch cannot leak into fold-mates).

## Gate outcomes
- G1 discovery: batch-grouped CV AUROC 0.728 >= 0.70 AND observed exceeds ALL 200
  full-pipeline permutation nulls (null max 0.700). PASS.
- G2 internal-external (honestly weaker than a true independent cohort - none exists,
  declared in gates): train batches 1-4 (n=46), apply ONCE to batch 5 (n=9: 5 PPD/4 no):
  AUROC 0.90, bootstrap 95% CI [0.571, 1.00], lower > 0.5. PASS.
- G2c named published baseline: Osborne/Payne HP1BP3+TTC9B candidate-region score
  (29 probes, frozen) AUROC 0.70 on the same held-out batch; panel 0.90 -> +0.20 >= 0.03. PASS.
- G3 cross-phenotype transport: RUN as follow-up. Frozen panel (111/113 probes
  recoverable) applied to GSE201287 MDD-vs-healthy blood 450K (n=80, 40/40;
  GenomeStudio control-normalized AVG_Beta): AUROC 0.763, bootstrap 95% CI
  [0.646, 0.863]. The PPD epigenetic signature transports to major depression
  well above chance - the first FROZEN external-cohort evidence for the panel
  (cross-phenotype, not an independent PPD cohort; that test remains open
  because none exists publicly).

## Mechanism check
113 non-zero panel probes -> 110 genes. Panel CONTAINS TTC9B (one of the two published
PPD methylation loci; HP1BP3 not selected - reported honestly). Top genes: ZNF680,
COQ3, UBAP2L, ZNF92, KPNA5, AKT1S1 (mTOR-pathway regulator - plausible stress/hormone
biology), PNKP/TBC1D17. Consistent with an epigenetic signature that partly rediscovers
the published locus and adds novel candidates.

## Tool + prospective lab nomination
- code/ppd_methyl_score.py: scores a new 450K blood sample (smoke-tested: 0.992 on
  PPD-class mean profile, 0.036 on control mean).
- Nominated assay: cg15824611 (ZNF680 locus, largest |coef|) - targeted bisulfite
  pyrosequencing in a prospective antenatal cohort.

## Honest limitations
Batch-5 holdout is small (n=9, CI wide). Batch-grouped CV is internal, not a true
independent cohort; the field lacks one publicly. CV optimism controlled by permutation
discipline. G3 gives frozen cross-phenotype transport (MDD, AUROC 0.763, CI 0.646-0.863);
transport to independent PPD data remains the decisive open test.
