# P01-03 data-condition check (2026-09-24, lane A)
- Strain resolution (StrainPhlAn/inStrain): needs raw reads + reference DBs for ~800 samples; not feasible in the
  build environment (1GB RAM, 2 cores). No public per-sample strain table for these cohorts was found in cMD.
- G2 (pks vs SBS88): paired tumor WGS signatures are controlled-access (PCAWG/TCGA). Blocked.
- Partial option available: Wirbel 2019 publishes per-sample clb (pks), bft, fadA and bai gene abundances for all
  767 frozen samples (MOESM8 Panel_c + MOESM9 Panel_c), so a locus-resolution vs genus comparison (G1 locus arm,
  G3) is cheap to build. Not started pending parent decision.
