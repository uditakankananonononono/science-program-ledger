# SP-004 Round 3 locked protocol

**Title:** Common-Family Target Estimands for the Small-Protein Evidence Problem
**Locked:** 2026-09-21 22:00 IST, before R3 shared-family outcome computation

## Why the estimand changes
R2 outcomes are known: conventional overlap weights failed because length and tryptic-peptide count are structurally separated by the 100-aa exposure definition. R3 does not rerun those weights. It targets the subset where biological comparison is meaningful: reviewed proteins assigned to the same Pfam family, with both <=100 aa and 101-200 aa members in the same domain. This is a family-common-support estimand, not an all-protein length effect.

## Data
Frozen R2 live UniProt/GOA cohort and hashes. Domains: bacteria, human, mouse, yeast. Required: one deterministic first Pfam identifier; family must contain >=5 short and >=5 control entries. Primary bandwidth is all 20-200 aa; confirmatory common-length-edge bandwidth is 80-120 aa with >=3 per arm/family. Outcomes: function comment, experimental GO (eukaryotes only), PDB. AlphaFold is a negative control.

## Estimands
1. Family-equal: mean of family-specific short-minus-control risk differences, each eligible family weighted equally.
2. Protein-targeted within-family: family differences weighted by harmonic arm size, preventing one-sided large families from dominating.
3. Narrow-band family-equal at 80-120 aa.

Bacterial uncertainty resamples families, then organism clusters within family where feasible. Eukaryotic uncertainty resamples families and proteins within family. Main reported bootstrap is a family-cluster bootstrap (2,000 replicates; seed 20260921). No propensity scores.

## Diagnostics
Report eligible families/proteins, family size distribution, arm ratios, endpoint prevalence, and family heterogeneity. Leave-one-top-family-out and minimum-family-size sensitivity (3, 5, 10 per arm). A domain is non-estimable when <10 shared families or <200 proteins per arm; this is a result, not an invitation to pool domains.

## Locked gate
A contradiction is explained only if one of these replicates in >=2 estimable domains:
- Stable gap: family-equal function or experimental-GO RD <= -5 pp, 95% family-bootstrap CI excludes zero, narrow-band direction agrees, and >=70% of leave-top-family-out estimates agree.
- Structural selection: raw all-cohort PDB contrast differs from shared-family family-equal contrast by >=75% attenuation or sign reversal, 95% CI for the shared-family estimate includes zero or lies opposite raw, and narrow-band direction agrees.

Opposite domains cannot be averaged. AlphaFold cannot satisfy the gate. Multiple Pfam assignments are reduced to the first identifier exactly as frozen in R2; an all-Pfam graph is deferred. Negative results and non-estimable domains remain explicit.
