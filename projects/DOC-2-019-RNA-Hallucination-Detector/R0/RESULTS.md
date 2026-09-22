# DOC-2-019 R0 results

## Verdict
**Feasible to run, successfully locked, but negative on the locked R0 success criterion.** The study had ample data and passed the nuisance and length-robustness checks. The frozen detector did not reach the required primary AUROC or bootstrap lower bound. Per protocol, this is a stop, not a tuning invitation.

## Results
| Quantity | Result | Gate | Pass |
|---|---:|---:|:---:|
| Eligible families | 2,110 | >=100 | Yes |
| Authentic sequences | 15,658 | >=1,000 | Yes |
| Test families | 427 | - | - |
| Test rows | 6,314 | - | - |
| Primary family-macro AUROC | 0.7043 | >=0.75 | **No** |
| Family-bootstrap 95% CI | 0.6835-0.7258 | lower >=0.70 | **No** |
| Length+GC control AUROC | 0.5061 | <=0.60 | Yes |
| Short-sequence AUROC | 0.7237 | >=0.70 | Yes |
| Long-sequence AUROC | 0.7031 | >=0.70 | Yes |

Test median authentic length was 90 nt. Family counts were 1,244 train, 439 reserved validation, and 427 test. Input SHA-256: `41f014f4ab5628620935f089b1bb77987ebc162fda7c72bff368a32c9cccabac`.

## Readout
The result is informative. Trivial length and GC imbalance did not drive performance, and discrimination remained above 0.70 on each side of the length split. But the prespecified effect-size and precision requirements were missed. The honest inference is that short-range sequence-complexity features are not strong enough for the proposed audit role, even against this relatively simple null, under family-disjoint generalization.

A future study, if separately approved and locked, should change the scientific object rather than fish this result: evaluate a structurally informed detector against outputs from named RNA generators, with model-held-out and family-held-out axes and experimental/structure proxies selected before outcome access. Those results must not be pooled with R0.
