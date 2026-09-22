# DOC-2-019 - RNA Model Hallucination Detector

## R0 verdict
Locked useful negative. A short-range sequence-complexity detector was not strong or precise enough under held-out Rfam-family generalization, even against a controlled first-order Markov surrogate.

## Useful discovery
The study was large and leakage-resistant: 2,110 eligible families, 15,658 authentic sequences and 427 fully held-out test families. Nuisance discrimination from length+GC was at chance (AUROC 0.506), and short/long strata each exceeded 0.70. But primary family-macro AUROC was 0.7043 versus the 0.75 gate, with family-bootstrap lower bound 0.6835 versus 0.70. The negative isolates the limitation to short-range sequence features, not trivial nuisance imbalance.

## What is new and why it matters
The experiment turns the playful "RNA hallucination" idea into a family-level audit estimand with an explicit generative null. It shows that plausible local statistics are not enough for a strong family-general detector and blocks premature claims about named RNA models.

## Application
R0 supplies a reusable surrogate benchmark and family-macro evaluation tool. It can screen future structurally informed detectors for family leakage, nuisance exploitation and length instability. It does not evaluate any named RNA generator and cannot establish structural or functional validity.

## Top-lab/grant next question
A separate locked study should use outputs from multiple named RNA generators, model-held-out plus family-held-out axes, experimental structure/error labels, calibrated abstention and external RNA classes. Grant readiness requires showing that the audit changes experimental-priority decisions and transports beyond the surrogate generator.

## Claim boundary
This is a useful negative result, not a complete sculpted project or deployable detector. It adds one result to the program ledger but does not graduate the topic.
