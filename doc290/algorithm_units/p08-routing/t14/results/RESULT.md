# T14 lazy incumbent-candidate activation: scalar work saved, other counters tied

Prereg53bc362b; exact published freeze106386f295314a36e8b01337dd5838d91025fa19.
One fixed400 run after freeze SSH publication, independent HTTPS exact-tip and
exact-commit raw byte readback. Seed264575; unchanged engine and literal inputs.
400workerPASS/200paired original-state DFS oracle and indexed witness agreement,
0failures. No retries, dropping, resampling, corpus edits, rescue, or rescoring.

| Actual T14 vs unchanged T13 counter | Wins | Ties | LOSSES | Paired PASS | Failure excluded |
| --- | --- | --- | --- | --- | --- |
| candidate_edges | 0 | 200 | 0 | 200 | 0 |
| charged_reverse_inspections | 0 | 200 | 0 | 200 | 0 |
| labels_inserted | 0 | 200 | 0 | 200 | 0 |
| scalar_candidate_inspections | 59 | 141 | 0 | 200 | 0 |

Full BOTH-method totals and candidate denominators:

```json
{
  "activated_details": [
    {
      "name": "turn040",
      "originalW": 6,
      "selectedW": 6,
      "selected_index": 0
    },
    {
      "name": "turn090",
      "originalW": 9,
      "selectedW": 6,
      "selected_index": 1
    }
  ],
  "activation_classes": {
    "charged_bound": 1,
    "exposure_exit": 139,
    "old_bound_equality": 60
  },
  "baseline_classes": {
    "budget_infeasible": 12,
    "equality_exit": 60,
    "no_allowed_turn_path": 127,
    "strict_gap_search": 1
  },
  "both_candidate_analysis": {
    "t13": {
      "W_improved": 1,
      "W_tied": 60,
      "W_worsened": 0,
      "candidate_ledger_PASS_denominator": 61,
      "duplicate_cases": 61,
      "duplicate_rows_after_first": 180,
      "early_excluded": 139,
      "eligible": 244,
      "failure_excluded": 0,
      "ordered_candidates": 244,
      "over_budget_valid_ineligible": 0,
      "scenario_candidates": 183,
      "scenario_eligible": 183,
      "scenario_over_budget": 0,
      "selected_index_counts": {
        "0": 60,
        "1": 1
      },
      "selected_objective_counts": {
        "exposure": 60,
        "scenario": 1
      },
      "skip_excluded": 0
    },
    "variant": {
      "W_improved": 1,
      "W_tied": 1,
      "W_worsened": 0,
      "candidate_ledger_PASS_denominator": 2,
      "duplicate_cases": 2,
      "duplicate_rows_after_first": 4,
      "early_excluded": 139,
      "eligible": 8,
      "failure_excluded": 0,
      "ordered_candidates": 8,
      "over_budget_valid_ineligible": 0,
      "scenario_candidates": 6,
      "scenario_eligible": 6,
      "scenario_over_budget": 0,
      "selected_index_counts": {
        "0": 1,
        "1": 1
      },
      "selected_objective_counts": {
        "exposure": 1,
        "scenario": 1
      },
      "skip_excluded": 59
    }
  },
  "both_counter_totals": {
    "t13": {
      "candidate_edges": 2,
      "charged_bound_stronger": 0,
      "charged_reverse_inspections": 21,
      "charged_strict_exclusions": 0,
      "dominance_pruned": 0,
      "feasibility_pruned": 0,
      "forbidden_skipped": 0,
      "incumbent_inspections": 285,
      "labels_inserted": 2,
      "max_live_queue": 1,
      "objective_bound_pruned": 1,
      "pops": 2,
      "reverse_relaxations": 620,
      "scalar_candidate_inspections": 828,
      "scenario_reverse_inspections": 1134,
      "stale_pops": 0
    },
    "variant": {
      "candidate_edges": 2,
      "charged_bound_stronger": 0,
      "charged_reverse_inspections": 21,
      "charged_strict_exclusions": 0,
      "dominance_pruned": 0,
      "feasibility_pruned": 0,
      "forbidden_skipped": 0,
      "incumbent_inspections": 285,
      "labels_inserted": 2,
      "max_live_queue": 1,
      "objective_bound_pruned": 1,
      "pops": 2,
      "reverse_relaxations": 620,
      "scalar_candidate_inspections": 29,
      "scenario_reverse_inspections": 1134,
      "stale_pops": 0
    }
  },
  "candidate_activation_classes": {
    "candidates_activated": 2,
    "exposure_exit": 139,
    "original_bound_equality": 59
  },
  "scalar_saved": 799,
  "variant_classes": {
    "budget_infeasible": 12,
    "equality_exit": 60,
    "no_allowed_turn_path": 127,
    "strict_gap_search": 1
  }
}
```

59 actual scalar-inspection wins are the59 original-bound-equality eligible
skips, with139early cases and2activated cases all scalar ties. Intentional absent
candidate ledgers and None selected indices on skips, not fake candidate0
selection. Activated denominator2 excludes139early/59skips/0failures, W1improved/
1tied/0worsened. BOTH baseline denominator61 excludes139early/0failures.
All labels, candidate-edge, charged-reverse comparisons0wins/200ties/0losses.
The counters do not establish total-work, runtime, memory, or science benefit.
Original exposure/scenario/incumbent counts preserved; validation and independent
raw replay overhead UNMEASURED. One original preprocessing pass, no rerun hidden.
No invention credit for Dijkstra, incumbents, lazy activation or bound equality.
No sparse synthetic result promoted to a general optimizer or production claim.

Skipped branch uses SAME original indexed exposure route with finite originalW
and selectedW, originalL equality, zero scalar/charged/phase work. Independent
parent skip proof uses original raw exposure incumbent and T12 equality audit,
without candidate scalar/expected/audit or charged expected helpers. Patched-RAISE
controls retained. Activated branch preserves original T13 candidate0 ordering,
scenario ledgers, valid overbudget ineligible candidates, duplicates, first ties,
MAXbudget-copy audit, original-budget selected witness recheck, raw stop/count
reconstruction, exact bound-event/phase/firstgoal replay. Partial first-sink
Dijkstra ledgers remain tentative settled/queued/unreached, not ALLstate proofs.
Separate unchanged T13 baseline checker; shared-model/helper scope disclosed.
No physical-parameter or scenario-path-completeness claim.

Initial18 receipts are preserved PRE-final7ff9e92b identity, NOT final evidence.
External FINAL-author18 receipts and final11PASS test log are separately carried
under final90e2bcb2 identity, identical to frozen manifest and fixed400 identities.
Full SHA provenance in summary. Initial development10PASS/1ERROR missing unused
BASE_COUNTERS compatibility alias repaired before freeze; rejected log retained.
No post-freeze executable or scoring rule edits. No hidden fixed-run failure.
CORPUS-ARCHIVE timestamp05:59:02.411Z, launch-order source log, freeze push/readback
and recorded tool chronology support recorded ordering only, NOT proof that no
private prerun happened. WorkerSOURCE copied earlier; archive preceded subject
worker PROCESS launch. Historical unreadableblob4340b673 limits materialization
to scoped git-show, no whole-repo integrity/archive claim.

Durable400 raw receipts/200paired markers/ledger400/inflightnull/DONE/noFAIL,
100alternating orders each/100chunks maximum4.911880323s/finalize4.267982372s.
These are operational observations, not timing experiment or superiority.
Exact identities/caps/source/old receipt revalidation/crash/concurrency/uncertainty
lock/no retry/idempotent final semantics retained. DONE!=PASS; marker existence
not sole metric; synthetic crash controls not mid-solver orphan proof. Existing
T11 negative/T12/T13 results and rejected development history unchanged.
Separate result gate required before publication, regardless of zeros or losses.

| Case | Oracle | T14 | T13 | Candidate activation | Selected/original W | Selected index |
| --- | --- | --- | --- | --- | --- | --- |
| turn000 | 5 | PASS | PASS | original_bound_equality | 5/5 | None |
| turn001 | None | PASS | PASS | exposure_exit | None/None | None |
| turn002 | None | PASS | PASS | exposure_exit | None/None | None |
| turn003 | None | PASS | PASS | exposure_exit | None/None | None |
| turn004 | None | PASS | PASS | exposure_exit | None/None | None |
| turn005 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn006 | None | PASS | PASS | exposure_exit | None/None | None |
| turn007 | 5 | PASS | PASS | original_bound_equality | 5/5 | None |
| turn008 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn009 | 4 | PASS | PASS | original_bound_equality | 4/4 | None |
| turn010 | None | PASS | PASS | exposure_exit | None/None | None |
| turn011 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn012 | 12 | PASS | PASS | original_bound_equality | 12/12 | None |
| turn013 | None | PASS | PASS | exposure_exit | None/None | None |
| turn014 | None | PASS | PASS | exposure_exit | None/None | None |
| turn015 | None | PASS | PASS | exposure_exit | None/None | None |
| turn016 | 5 | PASS | PASS | original_bound_equality | 5/5 | None |
| turn017 | None | PASS | PASS | exposure_exit | None/None | None |
| turn018 | None | PASS | PASS | exposure_exit | None/None | None |
| turn019 | None | PASS | PASS | exposure_exit | None/None | None |
| turn020 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn021 | None | PASS | PASS | exposure_exit | None/None | None |
| turn022 | None | PASS | PASS | exposure_exit | None/None | None |
| turn023 | None | PASS | PASS | exposure_exit | None/None | None |
| turn024 | 4 | PASS | PASS | original_bound_equality | 4/4 | None |
| turn025 | None | PASS | PASS | exposure_exit | None/None | None |
| turn026 | 5 | PASS | PASS | original_bound_equality | 5/5 | None |
| turn027 | None | PASS | PASS | exposure_exit | None/None | None |
| turn028 | None | PASS | PASS | exposure_exit | None/None | None |
| turn029 | None | PASS | PASS | exposure_exit | None/None | None |
| turn030 | None | PASS | PASS | exposure_exit | None/None | None |
| turn031 | None | PASS | PASS | exposure_exit | None/None | None |
| turn032 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn033 | None | PASS | PASS | exposure_exit | None/None | None |
| turn034 | None | PASS | PASS | exposure_exit | None/None | None |
| turn035 | None | PASS | PASS | exposure_exit | None/None | None |
| turn036 | None | PASS | PASS | exposure_exit | None/None | None |
| turn037 | None | PASS | PASS | exposure_exit | None/None | None |
| turn038 | None | PASS | PASS | exposure_exit | None/None | None |
| turn039 | None | PASS | PASS | exposure_exit | None/None | None |
| turn040 | 6 | PASS | PASS | candidates_activated | 6/6 | 0 |
| turn041 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn042 | None | PASS | PASS | exposure_exit | None/None | None |
| turn043 | None | PASS | PASS | exposure_exit | None/None | None |
| turn044 | None | PASS | PASS | exposure_exit | None/None | None |
| turn045 | None | PASS | PASS | exposure_exit | None/None | None |
| turn046 | None | PASS | PASS | exposure_exit | None/None | None |
| turn047 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn048 | None | PASS | PASS | exposure_exit | None/None | None |
| turn049 | None | PASS | PASS | exposure_exit | None/None | None |
| turn050 | None | PASS | PASS | exposure_exit | None/None | None |
| turn051 | 5 | PASS | PASS | original_bound_equality | 5/5 | None |
| turn052 | None | PASS | PASS | exposure_exit | None/None | None |
| turn053 | None | PASS | PASS | exposure_exit | None/None | None |
| turn054 | None | PASS | PASS | exposure_exit | None/None | None |
| turn055 | None | PASS | PASS | exposure_exit | None/None | None |
| turn056 | None | PASS | PASS | exposure_exit | None/None | None |
| turn057 | None | PASS | PASS | exposure_exit | None/None | None |
| turn058 | None | PASS | PASS | exposure_exit | None/None | None |
| turn059 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn060 | 4 | PASS | PASS | original_bound_equality | 4/4 | None |
| turn061 | 7 | PASS | PASS | original_bound_equality | 7/7 | None |
| turn062 | None | PASS | PASS | exposure_exit | None/None | None |
| turn063 | None | PASS | PASS | exposure_exit | None/None | None |
| turn064 | 5 | PASS | PASS | original_bound_equality | 5/5 | None |
| turn065 | None | PASS | PASS | exposure_exit | None/None | None |
| turn066 | None | PASS | PASS | exposure_exit | None/None | None |
| turn067 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn068 | 10 | PASS | PASS | original_bound_equality | 10/10 | None |
| turn069 | 15 | PASS | PASS | original_bound_equality | 15/15 | None |
| turn070 | None | PASS | PASS | exposure_exit | None/None | None |
| turn071 | None | PASS | PASS | exposure_exit | None/None | None |
| turn072 | None | PASS | PASS | exposure_exit | None/None | None |
| turn073 | None | PASS | PASS | exposure_exit | None/None | None |
| turn074 | None | PASS | PASS | exposure_exit | None/None | None |
| turn075 | None | PASS | PASS | exposure_exit | None/None | None |
| turn076 | None | PASS | PASS | exposure_exit | None/None | None |
| turn077 | 5 | PASS | PASS | original_bound_equality | 5/5 | None |
| turn078 | 5 | PASS | PASS | original_bound_equality | 5/5 | None |
| turn079 | None | PASS | PASS | exposure_exit | None/None | None |
| turn080 | 12 | PASS | PASS | original_bound_equality | 12/12 | None |
| turn081 | None | PASS | PASS | exposure_exit | None/None | None |
| turn082 | None | PASS | PASS | exposure_exit | None/None | None |
| turn083 | 5 | PASS | PASS | original_bound_equality | 5/5 | None |
| turn084 | None | PASS | PASS | exposure_exit | None/None | None |
| turn085 | None | PASS | PASS | exposure_exit | None/None | None |
| turn086 | 4 | PASS | PASS | original_bound_equality | 4/4 | None |
| turn087 | 11 | PASS | PASS | original_bound_equality | 11/11 | None |
| turn088 | None | PASS | PASS | exposure_exit | None/None | None |
| turn089 | 5 | PASS | PASS | original_bound_equality | 5/5 | None |
| turn090 | 6 | PASS | PASS | candidates_activated | 6/9 | 1 |
| turn091 | None | PASS | PASS | exposure_exit | None/None | None |
| turn092 | None | PASS | PASS | exposure_exit | None/None | None |
| turn093 | None | PASS | PASS | exposure_exit | None/None | None |
| turn094 | None | PASS | PASS | exposure_exit | None/None | None |
| turn095 | None | PASS | PASS | exposure_exit | None/None | None |
| turn096 | None | PASS | PASS | exposure_exit | None/None | None |
| turn097 | None | PASS | PASS | exposure_exit | None/None | None |
| turn098 | None | PASS | PASS | exposure_exit | None/None | None |
| turn099 | 4 | PASS | PASS | original_bound_equality | 4/4 | None |
| turn100 | 10 | PASS | PASS | original_bound_equality | 10/10 | None |
| turn101 | None | PASS | PASS | exposure_exit | None/None | None |
| turn102 | None | PASS | PASS | exposure_exit | None/None | None |
| turn103 | 5 | PASS | PASS | original_bound_equality | 5/5 | None |
| turn104 | None | PASS | PASS | exposure_exit | None/None | None |
| turn105 | None | PASS | PASS | exposure_exit | None/None | None |
| turn106 | None | PASS | PASS | exposure_exit | None/None | None |
| turn107 | 9 | PASS | PASS | original_bound_equality | 9/9 | None |
| turn108 | 11 | PASS | PASS | original_bound_equality | 11/11 | None |
| turn109 | None | PASS | PASS | exposure_exit | None/None | None |
| turn110 | None | PASS | PASS | exposure_exit | None/None | None |
| turn111 | None | PASS | PASS | exposure_exit | None/None | None |
| turn112 | None | PASS | PASS | exposure_exit | None/None | None |
| turn113 | None | PASS | PASS | exposure_exit | None/None | None |
| turn114 | 14 | PASS | PASS | original_bound_equality | 14/14 | None |
| turn115 | 7 | PASS | PASS | original_bound_equality | 7/7 | None |
| turn116 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn117 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn118 | None | PASS | PASS | exposure_exit | None/None | None |
| turn119 | None | PASS | PASS | exposure_exit | None/None | None |
| turn120 | None | PASS | PASS | exposure_exit | None/None | None |
| turn121 | None | PASS | PASS | exposure_exit | None/None | None |
| turn122 | None | PASS | PASS | exposure_exit | None/None | None |
| turn123 | None | PASS | PASS | exposure_exit | None/None | None |
| turn124 | None | PASS | PASS | exposure_exit | None/None | None |
| turn125 | None | PASS | PASS | exposure_exit | None/None | None |
| turn126 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn127 | None | PASS | PASS | exposure_exit | None/None | None |
| turn128 | None | PASS | PASS | exposure_exit | None/None | None |
| turn129 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn130 | None | PASS | PASS | exposure_exit | None/None | None |
| turn131 | None | PASS | PASS | exposure_exit | None/None | None |
| turn132 | 5 | PASS | PASS | original_bound_equality | 5/5 | None |
| turn133 | None | PASS | PASS | exposure_exit | None/None | None |
| turn134 | None | PASS | PASS | exposure_exit | None/None | None |
| turn135 | None | PASS | PASS | exposure_exit | None/None | None |
| turn136 | None | PASS | PASS | exposure_exit | None/None | None |
| turn137 | None | PASS | PASS | exposure_exit | None/None | None |
| turn138 | None | PASS | PASS | exposure_exit | None/None | None |
| turn139 | None | PASS | PASS | exposure_exit | None/None | None |
| turn140 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn141 | None | PASS | PASS | exposure_exit | None/None | None |
| turn142 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn143 | None | PASS | PASS | exposure_exit | None/None | None |
| turn144 | None | PASS | PASS | exposure_exit | None/None | None |
| turn145 | None | PASS | PASS | exposure_exit | None/None | None |
| turn146 | None | PASS | PASS | exposure_exit | None/None | None |
| turn147 | 4 | PASS | PASS | original_bound_equality | 4/4 | None |
| turn148 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn149 | None | PASS | PASS | exposure_exit | None/None | None |
| turn150 | None | PASS | PASS | exposure_exit | None/None | None |
| turn151 | None | PASS | PASS | exposure_exit | None/None | None |
| turn152 | None | PASS | PASS | exposure_exit | None/None | None |
| turn153 | None | PASS | PASS | exposure_exit | None/None | None |
| turn154 | None | PASS | PASS | exposure_exit | None/None | None |
| turn155 | 5 | PASS | PASS | original_bound_equality | 5/5 | None |
| turn156 | 7 | PASS | PASS | original_bound_equality | 7/7 | None |
| turn157 | 5 | PASS | PASS | original_bound_equality | 5/5 | None |
| turn158 | 9 | PASS | PASS | original_bound_equality | 9/9 | None |
| turn159 | None | PASS | PASS | exposure_exit | None/None | None |
| turn160 | None | PASS | PASS | exposure_exit | None/None | None |
| turn161 | None | PASS | PASS | exposure_exit | None/None | None |
| turn162 | None | PASS | PASS | exposure_exit | None/None | None |
| turn163 | None | PASS | PASS | exposure_exit | None/None | None |
| turn164 | None | PASS | PASS | exposure_exit | None/None | None |
| turn165 | 5 | PASS | PASS | original_bound_equality | 5/5 | None |
| turn166 | None | PASS | PASS | exposure_exit | None/None | None |
| turn167 | None | PASS | PASS | exposure_exit | None/None | None |
| turn168 | None | PASS | PASS | exposure_exit | None/None | None |
| turn169 | None | PASS | PASS | exposure_exit | None/None | None |
| turn170 | None | PASS | PASS | exposure_exit | None/None | None |
| turn171 | None | PASS | PASS | exposure_exit | None/None | None |
| turn172 | None | PASS | PASS | exposure_exit | None/None | None |
| turn173 | None | PASS | PASS | exposure_exit | None/None | None |
| turn174 | None | PASS | PASS | exposure_exit | None/None | None |
| turn175 | None | PASS | PASS | exposure_exit | None/None | None |
| turn176 | None | PASS | PASS | exposure_exit | None/None | None |
| turn177 | None | PASS | PASS | exposure_exit | None/None | None |
| turn178 | None | PASS | PASS | exposure_exit | None/None | None |
| turn179 | None | PASS | PASS | exposure_exit | None/None | None |
| turn180 | 9 | PASS | PASS | original_bound_equality | 9/9 | None |
| turn181 | 10 | PASS | PASS | original_bound_equality | 10/10 | None |
| turn182 | 3 | PASS | PASS | original_bound_equality | 3/3 | None |
| turn183 | 4 | PASS | PASS | original_bound_equality | 4/4 | None |
| turn184 | None | PASS | PASS | exposure_exit | None/None | None |
| turn185 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn186 | None | PASS | PASS | exposure_exit | None/None | None |
| turn187 | 6 | PASS | PASS | original_bound_equality | 6/6 | None |
| turn188 | None | PASS | PASS | exposure_exit | None/None | None |
| turn189 | 5 | PASS | PASS | original_bound_equality | 5/5 | None |
| turn190 | 9 | PASS | PASS | original_bound_equality | 9/9 | None |
| turn191 | 3 | PASS | PASS | original_bound_equality | 3/3 | None |
| turn192 | None | PASS | PASS | exposure_exit | None/None | None |
| turn193 | None | PASS | PASS | exposure_exit | None/None | None |
| turn194 | None | PASS | PASS | exposure_exit | None/None | None |
| turn195 | None | PASS | PASS | exposure_exit | None/None | None |
| turn196 | None | PASS | PASS | exposure_exit | None/None | None |
| turn197 | None | PASS | PASS | exposure_exit | None/None | None |
| turn198 | None | PASS | PASS | exposure_exit | None/None | None |
| turn199 | None | PASS | PASS | exposure_exit | None/None | None |
