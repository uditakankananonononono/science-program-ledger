---
id: P06-08
title: "Ranked Hits with Guaranteed Error Rates: Conformal Prediction for DTA Screening Lists"
parent: "CBIO013 - Fighting Future Pandemics with Novel DeepGraphDTI (source abstract, 2024)"
---

# Ranked Hits with Guaranteed Error Rates

**Parent project:** CBIO013(2024) - picked 7 hits from score rankings with no calibrated false-hit control.

## Premise
In prospective screening, what matters is: how many of my top-k are real? Conformal prediction gives distribution-free error control on hit lists - directly computable on the parent's exact use case.

## Hypothesis
Conformal-calibrated DeepGraphDTI outputs achieve >= 90% of nominal precision control on held-out screens, and the calibrated top-20 list differs materially from the raw-score top-20.

## Data sources (free/public)
- Benchmarks from P06-01; the parent's screen setup reproduced.
- Split-conformal implementation (open libraries).

## Method outline
1. Implement split-conformal calibration per split regime (cold regimes included - the hard case).
2. Measure empirical precision at nominal levels across regimes; coverage/efficiency curves.
3. Apply to the NiV screen reproduction: calibrated hit list vs raw-score list; report set sizes at 80%/90% precision control.

## Success gates (locked before results)
- G1: empirical vs nominal calibration curves published for every regime - including where calibration breaks.
- G2: cold-regime calibration within 5 points of nominal, else conformal is declared unreliable exactly where it is needed (reported, not hidden).
- G3: the NiV calibrated list frozen with its guaranteed-error statement.

## Expected deliverable
`dtacalibrate`: a drop-in conformal wrapper for DTA screening pipelines + the calibrated NiV hit list with honest error guarantees.

## Failure/pivot rule
If calibration breaks in cold regimes, publish the breakdown analysis and the adaptive fixes tested - the limits of error control are themselves the result.
