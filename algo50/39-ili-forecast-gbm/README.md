# 39 - Short-term ILI forecasting: gradient boosting vs persistence and climatology (PASS)

CDC ILINet wILI (Delphi Epidata), national + 10 HHS regions. Train seasons 2003/04-2016/17; test 2017/18, 2018/19, 2022/23, 2023/24 (COVID seasons excluded up front). 1-4 week-ahead point forecasts from Oct-May origins; 5,984 test forecasts. Gates locked before any fit (commit a07ec529).

| Gate | Result | Value (95% CI, 2000 bootstraps over 44 season x region blocks) |
|---|---|---|
| G1 mean relMAE vs persistence (h=1-4) <= 0.90 | PASS | 0.793 (0.734, 0.857) |
| G2 relMAE vs persistence at h=1 < 1 | PASS | 0.869 (0.808, 0.929) |
| G3 mean relMAE vs climatology < 1 | PASS | 0.487 (0.462, 0.515) |

MAE (wILI points) h=1..4: persistence 0.36/0.64/0.89/1.11, GBM 0.31/0.51/0.67/0.82, climatology about 1.2 at every horizon. Per-season relMAE vs persistence: 0.73, 0.73, 0.81, 0.92 (the gain shrinks in the post-COVID seasons, whose timing differs from training).

Takeaway: a pooled gradient-boosting model on recent lags plus historical seasonal shape cuts 1-4 week error by about 20% against the flat baseline FluSight uses, and beats climatology by half. Persistence and climatology are weak baselines; this is not a comparison with top FluSight ensemble models.

Caveats: fully revised data, not real-time (real forecasts face backfill, so these errors are optimistic for every model); point forecasts only, no WIS or interval scoring; one fixed model with no refitting, so the 2022-24 seasons use a model trained through 2017.
