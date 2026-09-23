# METENG STATE at 04:36 IST - SCORING DONE: GATE FAIL -> boundary per R9. Writeup/push/report left.
- Scan complete (949/949). Scoring (results/meteng_scores.json, code/meteng_score.py):
  succinate CALIBRATION PASS (0.998 vs null max 0.894 - method validated on calibration);
  fumarate PASS (FUM1 rank 1/949, pct 0.9995); pyruvate FAIL 0.51; L-lactate FAIL 0.46;
  ethanol FAIL 0.61 (GPD2 0.88 but GPD1/FPS1/DLD3 0.45); 23BDO FAIL 0.36.
  EVALUATED 1/5 (<3) => GATE FAIL. R9: documented boundary, no relaxation, no new arms.
- Scoring-script erratum: percentile formula initially inverted (caught because succinate
  calibration failed against known 008 result); fixed before any use; corrected run is of record.
- Finding: gc90 coupling recovers DIRECT-CONSUMPTION KOs adjacent to the product (FUM1,
  SDH2/3 for TCA acids) but NOT redox/regulatory targets (PDC/GPD/ADH families) whose in-vivo
  effect works via cofactor balancing, not growth coupling.
- TODO next run: (1) R5 baseline arm: OptGene/Otero succinate (sdh3/ser3/ser33 vs our top-3
  FUM1/SDH3/SDH2 - partial overlap) + fetch PMC3530589 fumarate in-silico predicted targets;
  (2) R6 ablation note (008 G2-style non-growth-coupled scan is degenerate all-tie);
  (3) meteng_scan.py CLI + WT smoke test; (4) R8 nomination: fumarate top non-literature gene
  (fumarate top10 in meteng_scores.json: YPL262W top; #2/#3 at 0.1617 need ID check vs SGD tab);
  (5) RESULTS.md honest boundary writeup + PROVENANCE.md; (6) push ledger exp200/METENG-target-rediscovery
  (GIT_SSH_COMMAND="ssh -i ~/.ssh_exp1/exp1_deploy_key -o IdentitiesOnly=yes"; verify ancestor);
  (7) CLAIMS.md METENG boundary NOT counted, tracker stays 47/100; (8) report parent
  (boundary outcome + calibration-pass nuance); (9) next wake; (10) resume lane at DOC-1-010
  (009 deferred) after parent direction.
