# F1 frozen software comparison results

360 paired repeats from 120 generated instances, 20 seeds x 3 horizons x 2 classes x 3 repeats. Raw rows all retained. No exceptions or expected-status mismatches. Independent result review pending.

| Horizon | Class | Median full/reduced | Mean full seconds | Mean reduced seconds | Reduced lower/equal/higher |
| ---: | --- | ---: | ---: | ---: | --- |
| 8 | constructed_feasible | 1.580530 | 0.002199 | 0.001392 | 60/0/0 |
| 8 | rank_deficient_impossible | 1.231339 | 0.001288 | 0.001025 | 60/0/0 |
| 32 | constructed_feasible | 3.712682 | 0.005279 | 0.001390 | 60/0/0 |
| 32 | rank_deficient_impossible | 2.406954 | 0.002215 | 0.000922 | 60/0/0 |
| 128 | constructed_feasible | 17.656795 | 0.027974 | 0.001541 | 60/0/0 |
| 128 | rank_deficient_impossible | 12.733351 | 0.012697 | 0.000987 | 60/0/0 |

Timing covers whole solver function, not generation. Reduced time lower in all observed pairs in this run; no ties/individual timing losses. Do not convert this into stable/statistical superiority or invention. Three repeats are not independent instances, no author-blind holdout, one process/warm cache, no OS noise control. Easy zero-row impossible class gives no general infeasibility runtime finding.

All expected feasible statuses have retained primal residuals. Solver-infeasible statuses lack general dual certificate; constructed class expectation follows impossible zero-row equation. No general floating equivalence guarantee from this matrix. Constant map and independent actuator limits/slew only; no corridor/coupling/hardware/calibration/anatomy/scientific claim.

Unchanged frozen harness executed once. Python 3.10.12, numpy 2.2.6, scipy 1.15.3, OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1. Total wall 3.774s, process peak RSS 106768 KiB. Budget documented, not enforced, measured usage under stated budget. Raw/manifest/provenance hashes and exact times retained in raw.json and run-receipt.json.
