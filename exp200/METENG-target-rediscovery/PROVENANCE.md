# PROVENANCE — METENG-insert

## Gates
- GATES.md locked 2026-09-24 ~03:38 IST BEFORE any scoring (design main-approved 03:32).
  SHA-256 in results/SHA256SUMS.txt. Frozen: panel, target sets, decoy null (seed 20260924),
  statistic, >=3/5 gate + fumarate sensitivity, failure tree R9.

## Model + the ONE locked edit
- Yeast8: data/yeast-GEM.xml SHA-256 30842b15eefb0ef7e36cbdea86a9efddfacf69a871c8b054165faa9af9f6c8eb
  (source: https://raw.githubusercontent.com/SysBioChalmers/yeast-GEM/main/model/yeast-GEM.xml)
- Locked edit (GATES.md): JEN1 transporters r_1254/r_1136/r_1207 (YKL217W) made reversible
  (shipped irreversible uptake-only; mirrors published pdc-negative/LDH-strain secretion).
  WT unchanged 0.0811; essentiality on edited model identical to unedited (194/1143, 0 unsolvable).

## Benchmark citations (target sets frozen pre-scoring; gene IDs verified vs SGD phenotype_data.tab)
- pyruvate PDC1/PDC5/PDC6: van Maris et al. 2004, AEM 70:159-166 (PMC321313)
- L-lactate PDC1: doi:10.1271/bbb.70.1148; PDC1+ADH1: PubMed 19122995
- fumarate FUM1: PLoS ONE 2012 7:e52086 (PMC3530589); fumarase-deficient mutants doi:10.1016/0378-1097(92)90667-d
- ethanol GPD2/GPD1/FPS1/ADH2/DLD3: PMC9375381 (Microb Cell Fact 2022 s12934-022-01885-3);
  J Biol Eng 12:29 (glycerol-reduction ethanol-yield); Biotechnol Biofuels 2017 s13068-017-0791-3
- 2,3-butanediol PDC1/PDC5: OSTI 1401461; Biotechnol Biofuels 2018 s13068-018-1176-y
- succinate (calibration): Otero 2012 PLoS ONE 7:e54144; Arikawa 1999 via FEMS Yeast Res 2017 fox057

## Code & artifacts (SHA-256 in results/SHA256SUMS.txt)
code/meteng_scan.py (essentiality + gc90 scans), code/meteng_score.py (frozen statistic),
meteng_cli.py (smoke-tested CLI), results/meteng_scores.json (scored artifact),
results/ess_parts.json (1143 genes), results/gc90_parts.json (949 non-essential x 6 products).

## Environment
python 3.10, cobra 0.32.1, scipy HiGHS (time_limit 20s/solve). All in-environment; no cost.
