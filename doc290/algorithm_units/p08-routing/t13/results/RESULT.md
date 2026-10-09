# T13 audited multi-candidate incumbent: bounded improvement with added work

Prereg979aa457; exact published freezeab0b6fdb175a641d188d52e7fa6d49074bfe4080.
One disclosed400freshsubject run after freeze push/readback, seed244949.
400workerPASS/200paired independent originalstateDFS oracle+indexedwitnessPASS.
Allattempts/rawBOTHworkers retained; no retries/drop/resampling/corpus edits/rescore.

| Actual T13 vs unchanged T12 counter | Wins | Ties | LOSSES | Paired PASS denominator | Failure excluded |
| --- | --- | --- | --- | --- | --- |
| candidate_edges | 3 | 197 | 0 | 200 | 0 |
| charged_reverse_inspections | 3 | 197 | 0 | 200 | 0 |
| labels_inserted | 3 | 197 | 0 | 200 | 0 |

Complete preregistered candidate and baseline analysis, rederived from all rows:

```json
{
  "activation_classes": {
    "charged_bound": 1,
    "exposure_exit": 141,
    "old_bound_equality": 58
  },
  "baseline_classes": {
    "budget_infeasible": 11,
    "equality_exit": 55,
    "no_allowed_turn_path": 130,
    "strict_gap_search": 4
  },
  "baseline_counter_totals": {
    "candidate_edges": 15,
    "charged_bound_stronger": 0,
    "charged_reverse_inspections": 129,
    "charged_strict_exclusions": 0,
    "dominance_pruned": 0,
    "feasibility_pruned": 2,
    "forbidden_skipped": 0,
    "incumbent_inspections": 308,
    "labels_inserted": 15,
    "max_live_queue": 7,
    "objective_bound_pruned": 2,
    "pops": 12,
    "reverse_relaxations": 588,
    "scenario_reverse_inspections": 1152,
    "stale_pops": 0
  },
  "candidate_analysis": {
    "W_improved": 3,
    "W_tied": 56,
    "W_worsened": 0,
    "duplicate_cases": 59,
    "duplicate_rows_after_first": 172,
    "early_excluded": 141,
    "eligible": 235,
    "failure_excluded": 0,
    "feasible_paired_PASS_denominator": 59,
    "new_equality_cases": 3,
    "ordered_candidates": 236,
    "over_budget_valid_ineligible": 1,
    "scenario_candidates": 177,
    "scenario_eligible": 176,
    "scenario_over_budget": 1,
    "selected_index_counts": {
      "0": 56,
      "1": 3
    },
    "selected_objective_counts": {
      "exposure": 56,
      "scenario": 3
    }
  },
  "variant_classes": {
    "budget_infeasible": 11,
    "equality_exit": 58,
    "no_allowed_turn_path": 130,
    "strict_gap_search": 1
  },
  "variant_counter_totals": {
    "candidate_edges": 3,
    "charged_bound_stronger": 0,
    "charged_reverse_inspections": 45,
    "charged_strict_exclusions": 0,
    "dominance_pruned": 0,
    "feasibility_pruned": 2,
    "forbidden_skipped": 0,
    "incumbent_inspections": 308,
    "labels_inserted": 2,
    "max_live_queue": 1,
    "objective_bound_pruned": 0,
    "pops": 2,
    "reverse_relaxations": 588,
    "scalar_candidate_inspections": 923,
    "scenario_reverse_inspections": 1152,
    "stale_pops": 0
  }
}
```

The feasible incumbent comparison denominator is59, with141early cases and0
failures excluded explicitly. Three actual upper-bound improvements/56ties/
0worsenings, not3/200 incumbent comparisons. Three newold-bound equality exits
save exactsearch labels/candidates andchargedreverse inspections on thiscorpus.
Allzero/nochange/loss categories retained. Newscenario shortestpaths add923actual
inspections, plus audit/replay overhead UNMEASURED. No totalwork/runtime/memory
superiority, no fewercounters=>speedclaim, no invention credit. Existing T11
negative/T12counter result immutable, no rescore or generalclaim from sparsecorpus.

Candidate0 exactly original deterministic exposureincumbent. All n+1 candidates
ordered, duplicatesretained; original whole-scenario routeaudit under explicitly
labelled validation-only MAXbudgetcopy, originalstatement unchanged; original
budgeteligibility separatelychecked andselectedwitness originalbudgetrechecked.
Betterbutoverbudget routes validineligible, not no-feasible proof. Partial
Dijkstrafirstsink ledgers label settled/queued/unreached/tentative/pops/stales/
predecessors/remainingheap, NOTcomplete ALLstate distanceproof. Parent exact
rawstop/order/count/candidate/eligibility/firsttie/selectedW reconstruction BEFORE
classification; fullselectedW bound-event/phase/firstgoal replay. W>originalW
FAIL, not a worsening accepted under contract. SeparateunchangedT12baseline
checker, no variantmutableglobals; sharedoriginalmodel/proofhelper limits scoped.
No scenario-pathcompleteness/DGcertificate/physicalunitlambda claim.

Provenance: frozen initial-receipts.json retained unchanged as PRE-finalmanifest
identity5563de72, notfinalevidence. External final-author-development-receipts.json
andfinal-author-tests.txt separately carried, final manifest identity4dcd2827;
fullsha provenance in summary. No rewriting initialhistory. CORPUS-ARCHIVE +
launch-order.log + originaltoolchronology support recordedordering only, not
private-prerunabsenceproof. WorkerSOURCE copied before archive; archivebefore
subject-worker PROCESSlaunch. Historicalunreadableblob4340b673: scopedgit-show
materialization only, no whole-repoarchive/integrityclaim.

Durable400receipts/200hash-boundmarkers/ledger400/inflightnull/DONE/noFAIL,
100orders each/100chunksmax4.308231035s/finalize3.574487792s. Operationalbuilder
observations, nottimingexperiment. Exactengine/caps/source/runtime/oldreceipt
revalidation/permanentuncertaintyFAIL/noretry/exactfinal retained.
DONE!=PASS; FAIL!=success; markersnotsolemetric; marginsnotlifetime; synthetic
crashnotmidsolverorphanproof. No speed/total-work/invention/generaloptimizer/
science/production/blindvalidation claim. Freshsynthetic/sharedhelpers not
externalheldout/physiology. Historicalnegatives/rejected/retractionunchanged.

| Case | Oracle | T13 | T12 | Selected/original W | Selected candidate |
| --- | --- | --- | --- | --- | --- |
| turn000 | None | PASS | PASS | None/None | None |
| turn001 | None | PASS | PASS | None/None | None |
| turn002 | None | PASS | PASS | None/None | None |
| turn003 | 14 | PASS | PASS | 14/14 | 0 |
| turn004 | None | PASS | PASS | None/None | None |
| turn005 | 11 | PASS | PASS | 11/11 | 0 |
| turn006 | 11 | PASS | PASS | 11/11 | 0 |
| turn007 | None | PASS | PASS | None/None | None |
| turn008 | 10 | PASS | PASS | 10/10 | 0 |
| turn009 | None | PASS | PASS | None/None | None |
| turn010 | None | PASS | PASS | None/None | None |
| turn011 | None | PASS | PASS | None/None | None |
| turn012 | None | PASS | PASS | None/None | None |
| turn013 | None | PASS | PASS | None/None | None |
| turn014 | None | PASS | PASS | None/None | None |
| turn015 | None | PASS | PASS | None/None | None |
| turn016 | None | PASS | PASS | None/None | None |
| turn017 | None | PASS | PASS | None/None | None |
| turn018 | 6 | PASS | PASS | 6/6 | 0 |
| turn019 | None | PASS | PASS | None/None | None |
| turn020 | None | PASS | PASS | None/None | None |
| turn021 | None | PASS | PASS | None/None | None |
| turn022 | 6 | PASS | PASS | 6/10 | 1 |
| turn023 | None | PASS | PASS | None/None | None |
| turn024 | None | PASS | PASS | None/None | None |
| turn025 | None | PASS | PASS | None/None | None |
| turn026 | None | PASS | PASS | None/None | None |
| turn027 | None | PASS | PASS | None/None | None |
| turn028 | None | PASS | PASS | None/None | None |
| turn029 | 8 | PASS | PASS | 8/8 | 0 |
| turn030 | None | PASS | PASS | None/None | None |
| turn031 | 11 | PASS | PASS | 11/11 | 0 |
| turn032 | None | PASS | PASS | None/None | None |
| turn033 | None | PASS | PASS | None/None | None |
| turn034 | None | PASS | PASS | None/None | None |
| turn035 | 1 | PASS | PASS | 1/1 | 0 |
| turn036 | None | PASS | PASS | None/None | None |
| turn037 | 6 | PASS | PASS | 6/8 | 1 |
| turn038 | 6 | PASS | PASS | 6/6 | 0 |
| turn039 | None | PASS | PASS | None/None | None |
| turn040 | None | PASS | PASS | None/None | None |
| turn041 | None | PASS | PASS | None/None | None |
| turn042 | None | PASS | PASS | None/None | None |
| turn043 | None | PASS | PASS | None/None | None |
| turn044 | 5 | PASS | PASS | 5/5 | 0 |
| turn045 | 3 | PASS | PASS | 3/3 | 0 |
| turn046 | None | PASS | PASS | None/None | None |
| turn047 | None | PASS | PASS | None/None | None |
| turn048 | 5 | PASS | PASS | 5/5 | 0 |
| turn049 | 0 | PASS | PASS | 0/0 | 0 |
| turn050 | 5 | PASS | PASS | 5/5 | 0 |
| turn051 | None | PASS | PASS | None/None | None |
| turn052 | 5 | PASS | PASS | 5/5 | 0 |
| turn053 | 3 | PASS | PASS | 3/3 | 0 |
| turn054 | None | PASS | PASS | None/None | None |
| turn055 | 5 | PASS | PASS | 5/5 | 0 |
| turn056 | 2 | PASS | PASS | 2/2 | 0 |
| turn057 | 5 | PASS | PASS | 5/5 | 0 |
| turn058 | None | PASS | PASS | None/None | None |
| turn059 | None | PASS | PASS | None/None | None |
| turn060 | 5 | PASS | PASS | 5/5 | 0 |
| turn061 | None | PASS | PASS | None/None | None |
| turn062 | None | PASS | PASS | None/None | None |
| turn063 | None | PASS | PASS | None/None | None |
| turn064 | None | PASS | PASS | None/None | None |
| turn065 | None | PASS | PASS | None/None | None |
| turn066 | None | PASS | PASS | None/None | None |
| turn067 | None | PASS | PASS | None/None | None |
| turn068 | None | PASS | PASS | None/None | None |
| turn069 | None | PASS | PASS | None/None | None |
| turn070 | 5 | PASS | PASS | 5/5 | 0 |
| turn071 | 5 | PASS | PASS | 5/5 | 0 |
| turn072 | None | PASS | PASS | None/None | None |
| turn073 | None | PASS | PASS | None/None | None |
| turn074 | None | PASS | PASS | None/None | None |
| turn075 | None | PASS | PASS | None/None | None |
| turn076 | 2 | PASS | PASS | 2/2 | 0 |
| turn077 | 12 | PASS | PASS | 12/13 | 1 |
| turn078 | None | PASS | PASS | None/None | None |
| turn079 | None | PASS | PASS | None/None | None |
| turn080 | None | PASS | PASS | None/None | None |
| turn081 | 3 | PASS | PASS | 3/3 | 0 |
| turn082 | 6 | PASS | PASS | 6/6 | 0 |
| turn083 | None | PASS | PASS | None/None | None |
| turn084 | None | PASS | PASS | None/None | None |
| turn085 | None | PASS | PASS | None/None | None |
| turn086 | 4 | PASS | PASS | 4/4 | 0 |
| turn087 | None | PASS | PASS | None/None | None |
| turn088 | None | PASS | PASS | None/None | None |
| turn089 | 5 | PASS | PASS | 5/5 | 0 |
| turn090 | None | PASS | PASS | None/None | None |
| turn091 | None | PASS | PASS | None/None | None |
| turn092 | None | PASS | PASS | None/None | None |
| turn093 | None | PASS | PASS | None/None | None |
| turn094 | None | PASS | PASS | None/None | None |
| turn095 | None | PASS | PASS | None/None | None |
| turn096 | None | PASS | PASS | None/None | None |
| turn097 | 6 | PASS | PASS | 6/6 | 0 |
| turn098 | None | PASS | PASS | None/None | None |
| turn099 | None | PASS | PASS | None/None | None |
| turn100 | None | PASS | PASS | None/None | None |
| turn101 | None | PASS | PASS | None/None | None |
| turn102 | None | PASS | PASS | None/None | None |
| turn103 | None | PASS | PASS | None/None | None |
| turn104 | None | PASS | PASS | None/None | None |
| turn105 | None | PASS | PASS | None/None | None |
| turn106 | None | PASS | PASS | None/None | None |
| turn107 | None | PASS | PASS | None/None | None |
| turn108 | None | PASS | PASS | None/None | None |
| turn109 | None | PASS | PASS | None/None | None |
| turn110 | None | PASS | PASS | None/None | None |
| turn111 | None | PASS | PASS | None/None | None |
| turn112 | None | PASS | PASS | None/None | None |
| turn113 | None | PASS | PASS | None/None | None |
| turn114 | 1 | PASS | PASS | 1/1 | 0 |
| turn115 | None | PASS | PASS | None/None | None |
| turn116 | None | PASS | PASS | None/None | None |
| turn117 | None | PASS | PASS | None/None | None |
| turn118 | None | PASS | PASS | None/None | None |
| turn119 | None | PASS | PASS | None/None | None |
| turn120 | None | PASS | PASS | None/None | None |
| turn121 | None | PASS | PASS | None/None | None |
| turn122 | 6 | PASS | PASS | 6/6 | 0 |
| turn123 | 4 | PASS | PASS | 4/4 | 0 |
| turn124 | None | PASS | PASS | None/None | None |
| turn125 | None | PASS | PASS | None/None | None |
| turn126 | 4 | PASS | PASS | 4/4 | 0 |
| turn127 | None | PASS | PASS | None/None | None |
| turn128 | 4 | PASS | PASS | 4/4 | 0 |
| turn129 | None | PASS | PASS | None/None | None |
| turn130 | None | PASS | PASS | None/None | None |
| turn131 | 5 | PASS | PASS | 5/5 | 0 |
| turn132 | None | PASS | PASS | None/None | None |
| turn133 | None | PASS | PASS | None/None | None |
| turn134 | None | PASS | PASS | None/None | None |
| turn135 | None | PASS | PASS | None/None | None |
| turn136 | None | PASS | PASS | None/None | None |
| turn137 | 9 | PASS | PASS | 9/9 | 0 |
| turn138 | 6 | PASS | PASS | 6/6 | 0 |
| turn139 | 1 | PASS | PASS | 1/1 | 0 |
| turn140 | 5 | PASS | PASS | 5/5 | 0 |
| turn141 | 5 | PASS | PASS | 5/5 | 0 |
| turn142 | None | PASS | PASS | None/None | None |
| turn143 | 5 | PASS | PASS | 5/5 | 0 |
| turn144 | 1 | PASS | PASS | 1/1 | 0 |
| turn145 | None | PASS | PASS | None/None | None |
| turn146 | 9 | PASS | PASS | 9/9 | 0 |
| turn147 | 6 | PASS | PASS | 6/6 | 0 |
| turn148 | None | PASS | PASS | None/None | None |
| turn149 | None | PASS | PASS | None/None | None |
| turn150 | None | PASS | PASS | None/None | None |
| turn151 | None | PASS | PASS | None/None | None |
| turn152 | None | PASS | PASS | None/None | None |
| turn153 | None | PASS | PASS | None/None | None |
| turn154 | None | PASS | PASS | None/None | None |
| turn155 | 8 | PASS | PASS | 8/8 | 0 |
| turn156 | None | PASS | PASS | None/None | None |
| turn157 | None | PASS | PASS | None/None | None |
| turn158 | 7 | PASS | PASS | 7/7 | 0 |
| turn159 | 5 | PASS | PASS | 5/5 | 0 |
| turn160 | None | PASS | PASS | None/None | None |
| turn161 | 6 | PASS | PASS | 6/6 | 0 |
| turn162 | None | PASS | PASS | None/None | None |
| turn163 | None | PASS | PASS | None/None | None |
| turn164 | 7 | PASS | PASS | 7/7 | 0 |
| turn165 | None | PASS | PASS | None/None | None |
| turn166 | None | PASS | PASS | None/None | None |
| turn167 | 6 | PASS | PASS | 6/6 | 0 |
| turn168 | None | PASS | PASS | None/None | None |
| turn169 | None | PASS | PASS | None/None | None |
| turn170 | None | PASS | PASS | None/None | None |
| turn171 | None | PASS | PASS | None/None | None |
| turn172 | None | PASS | PASS | None/None | None |
| turn173 | None | PASS | PASS | None/None | None |
| turn174 | 6 | PASS | PASS | 6/6 | 0 |
| turn175 | 4 | PASS | PASS | 4/4 | 0 |
| turn176 | None | PASS | PASS | None/None | None |
| turn177 | None | PASS | PASS | None/None | None |
| turn178 | None | PASS | PASS | None/None | None |
| turn179 | 6 | PASS | PASS | 6/6 | 0 |
| turn180 | 6 | PASS | PASS | 6/6 | 0 |
| turn181 | None | PASS | PASS | None/None | None |
| turn182 | None | PASS | PASS | None/None | None |
| turn183 | None | PASS | PASS | None/None | None |
| turn184 | None | PASS | PASS | None/None | None |
| turn185 | None | PASS | PASS | None/None | None |
| turn186 | None | PASS | PASS | None/None | None |
| turn187 | 6 | PASS | PASS | 6/6 | 0 |
| turn188 | None | PASS | PASS | None/None | None |
| turn189 | None | PASS | PASS | None/None | None |
| turn190 | 5 | PASS | PASS | 5/5 | 0 |
| turn191 | None | PASS | PASS | None/None | None |
| turn192 | None | PASS | PASS | None/None | None |
| turn193 | None | PASS | PASS | None/None | None |
| turn194 | 5 | PASS | PASS | 5/5 | 0 |
| turn195 | None | PASS | PASS | None/None | None |
| turn196 | None | PASS | PASS | None/None | None |
| turn197 | None | PASS | PASS | None/None | None |
| turn198 | None | PASS | PASS | None/None | None |
| turn199 | None | PASS | PASS | None/None | None |
