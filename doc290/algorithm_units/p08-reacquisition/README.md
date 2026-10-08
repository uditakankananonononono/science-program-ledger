# P08-03 bounded deferred reacquisition baseline

Development-only application baseline, not an invention. A first returning
measurement yields accept/reject Kalman branches; provisional output is prediction
only. One later confirmation measurement selects the smaller predictive Gaussian
negative log density (including covariance log determinant), then updates that
branch. Exact tie rejects. Returned confirmation state is current, not a retrospective
rewrite of the first output. Exactly two branches and one-observation latency.

This score omits the first-measurement likelihood, hypothesis priors, clutter model
and detection probability. It is a heuristic comparison, NOT posterior association
probability and NOT full MHT. Missing confirmation, longer sequences, repeated
corruption, and a bounded wall-clock wait policy are not implemented. A corrupted
confirmation can choose the wrong branch; the implementation makes no robustness
claim. covariance within a branch is not mixture uncertainty/calibrated confidence.

Four development fixtures pass: obvious corrupt return rejected, consistent return
accepted, bad confirmation leaves caller inputs unchanged, and reject-branch NLL
matches separately calculated Gaussian density. These are constructed examples,
not frozen evaluation trajectories or proof of performance. No S1 code modified.

## Prior-art search and novelty boundary

Fetched Reid, "An Algorithm for Tracking Multiple Targets", IEEE Transactions on
Automatic Control, December 1979, from the Stanford-hosted paper:
http://graphics.stanford.edu/courses/cs428-03-spring/Papers/readings/CollaborativeProcessing/Reid_MHT_ieee_trans_ac_1979.pdf
The abstract and introduction explicitly describe Kalman estimates per hypothesis,
later measurements informing prior association decisions, and pruning hypotheses.
Thus branching + deferred confirmation cannot be claimed here as a new general
tracking algorithm. This restricted single-target heuristic is an application unit.

Also fetched the review "Forty Years of Multiple Hypothesis Tracking":
https://isif.org/files/isif/2024-01/02-022019-0012R1_LR.pdf
and current adjacent occlusion tracking work:
https://arxiv.org/html/2309.10360v2
These are research leads, not evidence that this particular restricted policy is
novel or superior. Search is not exhaustive. Novelty and empirical performance are
unestablished. No imaging calibration or scientific gate passed.

Run from this directory:

    OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v

Depends on sibling p08-tracking/kalman.py (established reviewed baseline).
