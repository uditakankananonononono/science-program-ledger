# S2 frozen synthetic results

100 trajectories retained, 20 per scenario; no scoring exceptions, no failed-seed removal. Frozen code/protocol unchanged. Independent result review pending.

| Scenario | Immediate | Fixed NIS gate | Deferred | Deferred vs immediate lower/equal/higher | Deferred vs gate lower/equal/higher |
| --- | ---: | ---: | ---: | --- | --- |
| clean | 0.247930 | 0.246689 | 0.397020 | 3/0/17 | 3/0/17 |
| corrupt_first | 2.367834 | 0.413837 | 0.408909 | 20/0/0 | 2/15/3 |
| corrupt_confirmation | 1.592099 | 0.276163 | 2.449312 | 0/0/20 | 0/0/20 |
| both_corrupt | 3.502377 | 0.537385 | 2.931495 | 20/0/0 | 0/0/20 |
| maneuver_in_gap | 0.434202 | 3.345215 | 0.915468 | 0/0/20 | 14/0/6 |

RMSE covers causal outputs at indices 30-39. Lower/equal/higher uses exact paired differences, not rounded table values. Full raw secondary errors, gate indices, decisions and actual confirmation delay retained.

Negative outcome: no general benefit established. Corrupted confirmation worsens every deferred trajectory against both baselines. Clean return and maneuver are worse than immediate in 17/20 and 20/20 trajectories. Both-corrupt is worse than gate in 20/20. Corrupt-first mean is slightly lower than gate, but 15 ties and 3 individual losses remain; do not present the mean as universal advantage. Maneuver mean is lower than gate but loses in 6/20.

Known q/R, largely matched synthetic truth and prescribed gap/corruption policy; no realistic imaging, calibration, novelty or stable superiority claim. Gate acts at all observations while deferred acts only at prescribed return. One-observation confirmation latency is charged via prediction-only first-return output. No retrospective rewrite.

Publication reference and full manifest/run hashes are in raw.json and run-receipt.json. Earlier launch was interrupted without observable output; two recovery checks found no raw file/process, so the unchanged harness was executed after recovery. No claim that interrupted evaluation definitely never began. Completed run: 2.684 seconds, peak RSS 35724 KiB; one BLAS thread.
