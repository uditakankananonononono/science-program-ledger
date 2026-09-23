---
id: P13-08
title: "Deviation Detector: Anomaly Detection for Cell-Therapy Manufacturing Runs"
parent: "CBIO042 - ReinforCell: CAR-T Cell Optimization Solution (ISEF 2026 Grand Award)"
---

# Deviation Detector

**Parent project:** CBIO042 ReinforCell (ex vivo manufacturing module; maximizing yield while minimizing exhaustion in bioreactors).

## Premise
Cell-therapy manufacturing fails quietly: a drifting pH probe or a contaminated feed shows up as a failed batch weeks and hundreds of thousands of dollars later. Pharma solves this with process-analytical-technology monitoring, but cell-therapy-specific open tools do not exist. This project builds an anomaly-detection stack for bioreactor sensor time series, pretrained on the public IndPenSim industrial-penicillin simulation benchmark (100 batches with labeled faults) and adapted to the cell-therapy regime, then validated on every public cell-culture sensor dataset available. The contribution is both a working early-warning detector and a honest answer to: does fault detection transfer from microbial fermentation physics to mammalian cell culture?

## Data sources
- IndPenSim (public, UCL): 100 simulated industrial penicillin batches with controlled faults - the training backbone.
- Public CHO/mammalian cell-culture process datasets deposited with open-access PAT papers.
- NIST and open bioprocess reference datasets where available.
- Published cell-therapy manufacturing failure-mode reports for fault taxonomy.

## Method outline
1. Build a fault taxonomy from published cell-therapy deviation reports (sensor drift, contamination, feed error, temperature excursion).
2. Train multivariate time-series anomaly detectors (LSTM autoencoder + isolation-forest ensemble) on IndPenSim nominal batches; calibrate alert thresholds at fixed false-alarm rates.
3. Measure detection lead time (time between fault onset and alert) per fault class.
4. Transfer-test on mammalian culture datasets; quantify the domain gap and adapt with minimal fine-tuning.
5. Package with a simulator mode so facilities can test the detector against their own historical runs.

## Success gates (locked before results)
- G1: on IndPenSim held-out faults, detection rate >= 90% at <= 1 false alarm per batch.
- G2: median detection lead time >= 20% of batch duration before fault manifestation.
- G3: transfer to mammalian data retains >= 70% detection rate with <= 2x false-alarm inflation, or the domain gap is quantified and published as the boundary.
- G4: honest-negative clause: a certified domain-gap measurement (G3 failure) is a full publishable result guiding what sensor data cell-therapy facilities must collect.

## Expected deliverable
An open "BatchSentinel" detector (Python package + simulator harness), the fault taxonomy, lead-time benchmarks per fault class, and the microbial-to-mammalian transfer study.

## Failure/pivot rule
If public mammalian sensor data is too scarce for G3 (likely risk), pivot to releasing the first open synthetic cell-therapy manufacturing benchmark (IndPenSim-style generator parameterized from published cell-culture physics) - gates re-locked around benchmark realism tests against published summary statistics.
