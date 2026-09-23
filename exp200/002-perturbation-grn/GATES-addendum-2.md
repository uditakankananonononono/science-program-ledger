# ADDENDUM 2 (locked 2026-09-23 ~22:50 IST, before any network-prediction outcome metrics)
Null-calibration repair: the 100x control-split null used ~307-cell halves, but target
groups have n=27-156; smaller pseudobulks carry larger sampling noise, so the v2 filter
passed 27/27 (miscalibrated null, documented). Repair: PER-TARGET size-matched null -
for a target with n cells, subsample n controls vs n disjoint controls 100x, same ss_DE
statistic; target passes if ss_DE > q95 of ITS size-matched null. Panel cap (if >20
pass) = 20 largest ss_DE. All other gates unchanged. No outcome metrics inspected yet.
