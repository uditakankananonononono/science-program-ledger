# algo50/82 - Outbreak transmission inference: SNP-distance threshold calibration

Lane RES-2. Algorithm study. Protocol + Amendment 1 hashed before the results they gate (`results/lock.txt`). Topic lane-chosen (no list past 55).

## Bottom line
Both gate sets failed, and the failure is the finding: at 25 SNPs/genome/year with ~5-day generations (~0.34 SNPs/transmission), a 60-day outbreak is genetically almost star-shaped - most pairs within 2 SNPs - so NO distance threshold recovers direct transmission (best F1 0.26 at T=0, precision 0.16) or even within-2-steps epidemiological linkage (best F1 0.49, precision 0.37). Sibling/2-step pairs are genetically indistinguishable from direct pairs. This matches the field: threshold heuristics work for fast-evolving pathogens and fail for slow ones; phylodynamic models exist precisely because of this ceiling.

## Gates
- Original: G1-G4 all FAIL (best F1 0.258 at T=0; time-consistency filter added only +0.016).
- Amendment 1 (re-aimed at within-2-steps linkage): P1-P3 all FAIL (best F1 0.487 at T=0, precision 0.37).
No third amendment: the mutation-rate ceiling is the result.

## Data
Simulated (seed 83): 42-case chain outbreak, 30 kb genome, 0.068 subs/day, single-virion transmission bottleneck, sampling 0-15 days post-infection.

## Caveats
- One outbreak realization; topology varies, but the mutation-rate arithmetic (0.34 SNPs/transmission) is topology-independent.
- Within-host diversity excluded (single bottleneck genome); real deep sequencing adds minor-variant directionality signal.

## Reproduce
`python3 code/run.py && python3 code/pivot.py` (numpy only, <10 s).
