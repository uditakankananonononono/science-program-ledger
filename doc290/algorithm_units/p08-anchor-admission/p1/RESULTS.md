# P1 measured stationary profile diagnostic results

Executed frozen a15f4cf4be02a3fab567d096579fa4c54d59621d after review/publication.
No code/protocol change. Five pinned source profiles,96 rows,93 finite speeds,all three
missing rows retained. Arithmetic comparator agreement only,not physical acceptance.

| Profile label (subsequent experiment) | Amplitude um/s | In-sample RMSE | In-sample MAE | Max abs | Leave-one-location RMSE |
|---|---:|---:|---:|---:|---:|
| 1V | 13.39345787 | 0.38397382 | 0.29217026 | 0.95137649 | 0.39818642 |
| 2V | 13.25003329 | 0.82278774 | 0.69093512 | 1.47712292 | 0.84817679 |
| 3V | 11.83054364 | 0.27135947 | 0.23776554 | 0.49644889 | 0.28580602 |
| 4V | 13.09038611 | 0.85255897 | 0.66952693 | 1.71223851 | 0.87201373 |
| 5V | 11.28033220 | 1.10070755 | 0.69123566 | 4.19167932 | 1.11546775 |

All speed errors in um/s; full precision,raw rows,all fold refit amplitudes/predictions
and all summary statistics retained in raw.json and five CSVs. All original profile
positions retained,including5V coordinates outside assumed mathematical walls±50um:
negative extrapolated parabola values are NOT clipped or hidden. This is one visible
geometry/grid/model mismatch,not evidence for wall-slip/physiology or a better method.

Both actual PNGs personally pixel-inspected: readable five panels,labels/legends and
units; profile finite counts18/19,18/19,18/19,19/19,20/20; red missing markers at
their reported y on a labeled bottom axes-coordinate strip (NOT speeds); residual
panels share common axis and retain the5V large positive leftmost residual. No error
bars,uncertainty calibration,acceptance tolerance or physics pass. File hashes verified
from saved manifest; all CSV row/missing counts read back. No partial run directory
failure occurred. Source figures are not pixel reproductions.

Differences across profiles remain descriptive. These were all pre-field measurements;
1V..5V labels name subsequent experiments,not field-on profiles. Leave-one-location
checks are not held-out validation or independent trials. Residual causes unseparated.
No new algorithm or novelty claim; no dynamic fitting,dt inference,S3column use or
magnetic-blood transfer. All P08 science gates OPEN.

Attribution Buness,Rana,Maass,Dey,CC-BY4.0: https://zenodo.org/records/13220167
