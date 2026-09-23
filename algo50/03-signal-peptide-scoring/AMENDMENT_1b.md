# Amendment 1b - correction of an ill-posed decision rule in Amendment 1 (locked before any Amendment 1 result was computed)

Amendment 1 said to threshold the adjusted posterior at the human threshold "rescaled by the same odds ratio". That is a monotone no-op: it reproduces the uncorrected decisions exactly. Caught on review before running anything. Amendment 1's gates A1-A3 are kept unchanged; only the decision rule is fixed:

1. P is trained with balanced class weights, so its raw output is treated as a posterior under a 0.5 training prior.
2. Human: map human CV posteriors to the human prevalence (744/15,547), and pick the MCC-optimal threshold tau_h on that posterior scale.
3. Target organism: estimate prevalence pi_t by EM prior-shift on the unlabeled target outputs (start 0.5, 200 iterations or tol 1e-6), map outputs to pi_t, predict SP when the mapped posterior >= tau_h.
No target labels are used for any choice.
