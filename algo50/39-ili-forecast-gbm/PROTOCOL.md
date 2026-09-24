# 39 - Short-term influenza-like-illness forecasting: gradient boosting vs persistence and climatology

Locked before any model is fit or scored.

Data: CDC ILINet weighted ILI (wILI) via the Delphi Epidata API (fluview), national + 10 HHS regions, epiweeks 2003w01-2024w39, latest issue (fully revised values).
Season S = epiweek 40 of year S through week 39 of S+1; wos = weeks since week 40.
Train: target and origin both in seasons 2003-2016. Test seasons: 2017/18, 2018/19, 2022/23, 2023/24 (COVID-disrupted 2019/20-2021/22 excluded, declared here before scoring). One fixed model, no refitting.
Forecast origins: every week with wos 0-33 (week 40 to about week 21); horizons h = 1-4 weeks; target must exist.

Models:
- Persistence (flat baseline; the FluSight "baseline" model family): y(t+h) = y(t).
- Climatology: mean over training seasons of wILI at the same region and wos (wos 52 falls back to 51).
- Method: HistGradientBoostingRegressor per horizon (max_iter 300, learning_rate 0.05, max_leaf_nodes 15, seed 39), pooled across the 11 series, target log y(t+h) - log y(t); features log y(t..t-3), log clim(wos_t), log clim(wos_t+h), log y(t) - log clim(wos_t), sin/cos(2 pi wos/52). Forecast = y(t) * exp(prediction).

Metric: MAE in wILI units over all test (series, origin, horizon). Relative MAE = MAE(method)/MAE(reference). 95% CI from 2000 bootstraps resampling (season, series) blocks (44 blocks), seed 39.
Gates:
- G1 (headline): mean over h=1-4 of relMAE vs persistence <= 0.90, CI upper bound < 1.
- G2: relMAE vs persistence at h=1 < 1, CI upper bound < 1.
- G3: mean over h of relMAE vs climatology < 1, CI upper bound < 1.
If G1 fails: one post-hoc pivot, locked and pushed before scoring.
Caveats declared: revised (not real-time) data - real-time forecasts face backfill; point forecasts only (no probabilistic scoring such as WIS); test seasons include post-COVID seasons with shifted timing.
