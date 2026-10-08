# U188 closure - Zenodo 8018238 autoimmune wearables (SLE/Sjogren screener groups vs Fitbit daily features): DROP at power gate
No model, split, prereg, run.py or AUC computed. Main chose DROP at 12:58 IST Oct 8 2026 (builder-stated record).
Caveats (verbatim): (1) labels are self-reported screener ("diagnosed by a healthcare professional"), not clinical adjudication; (2) derived daily aggregates, not raw signals; (3) published primary (fdgth.2023.1099456) is a fatigue association, not a classification comparator: no published comparator.

## Integrity
Zenodo API license cc-by-4.0, DOI 10.5281/zenodo.8018238, published 2023-06-19 (zenodo_8018238_api.json). 12/12 files re-fetched, MD5 equals API checksum (md5_local.txt).

## Join and counts (a)
Screener 296 unique IDs: none 105, sle 104, ss 65, sle_ss 22 (4 raw categories; the 22 "both" are folded into Sjogren 87 by the publisher; not relabeled here). Activity 6992 rows x 100 columns (id, date, 98 features), 207 IDs, no duplicate (id,date). All 207 in screener; 89 screener IDs have no Fitbit. 207 = activity∩screener = activity∩baseline survey; 204 = activity∩daily-survey file (not the label intersect). Label-usable persons / days: none 73 / 2511; sle 72 / 2459; ss 44 / 1448; sle_ss 18 / 574. Days per person min 18, median 32, max 52; 0 persons <14 days. Dates 2020-08-14 to 2020-10-08. No feature column >50% missing.

## Confound table (b), counts/means only
Sex (F/M): none 52/21; sle 71/1; ss 44/0; sle_ss 18/0. 21 of 22 men are controls; sex alone separates SLE vs none at AUC ~0.64 (from counts: TPR 71/72, TNR 21/73 -> .5*(.986+.288)). Male stratum has one SLE case.
Age mean(sd): none 44.0 (11.2); sle 44.9 (11.7); sle_ss 46.8 (9.0); ss 51.1 (9.0).
Wear: mean active minutes/day (share of days <1000 min): none 1278 (.13); sle 1275 (.15); sle_ss 1390 (.03); ss 1310 (.12).
Baseline item "I feel fatigued" (not at all/a little/somewhat/quite a bit/very much): none 15/25/16/16/1; sle 2/16/21/27/6; sle_ss 0/4/6/5/3; ss 3/8/15/13/5.
Lupus-medication question asked only of self-reported lupus: none 72 NA + 1 Yes (label-noise case); sle 30 No / 42 Yes; sle_ss 5 / 13; ss NA. Structurally missing for controls: unusable as covariate.

## Identity audit (c)
No duplicate screener rows or start times, no identical baseline rows, no identical person trajectories or person-mean fingerprints across IDs; one rounded feature row shared by >1 ID (unexamined). Cross-ID human identity not independently excluded.

## Power (e), label-free, Hanley-McNeil SE at AUC .70, TEST = odd positions, 80% power, paired AUC gain, r(candidate,baseline)=0/.3/.6
SLE 72 vs none 73 (TEST 36/36): SE .062, MDE .244/.204/.155. SLE 71F vs none 52F (TEST 36/26): SE .066, MDE .261/.218/.165. SLE-any 90 vs none 73 (45/36): MDE .228/.191/.144. Any-AI 134 vs none 73 (67/36): MDE .205/.171/.129. Planning approximations (normal-theory); WIN bar 0.03.

## Verdict
DROP at power gate: MDE .13-.26 exceeds any plausible gain of daily Fitbit aggregates over the mandatory sex/age/wear-days comparator; classification endpoint uninterpretable without female-only stratification (71 vs 52). No clinical claim.
