---
id: P22-02
title: "Linking Benchmark: Measuring Cross-Height and Cross-Time Cell Linking Against Standard Trackers"
parent: "CBIO064T - Automated 3D Cell Visualization (source abstract, 2025)"
---

# Linking Benchmark

**Parent project:** CBIO064T Automated 3D Cell Visualization (Cellpose 2.0 auto-outlining of z-stack slices, cross-height/time cell linking, mesh rendering and side-by-side comparison).

## Premise
The parent wrote its own algorithm to match outlines of the same cell across heights and time. That step decides whether a 3D cell is one object or three, and whether a dividing cell is tracked correctly. The Cell Tracking Challenge provides ground truth and standard metrics (SEG, TRA, DET) to score exactly this, and strong open trackers exist (Ultrack, Trackastra, TrackMate).

## Hypothesis
Overlap-based greedy linking (the parent's class of method) scores within 0.05 TRA of state-of-the-art trackers on sparse datasets but falls >= 0.1 behind on datasets with frequent divisions or fast motion.

## Data sources (free/public)
- Cell Tracking Challenge 3D+time datasets with ground truth (public).
- Open trackers: Ultrack, Trackastra, TrackMate (free).
- Official CTC evaluation software (free).

## Method outline
1. Re-implement the parent-style linking (overlap/centroid matching across z and t) as an open module.
2. Feed identical segmentations to all trackers so only linking differs.
3. Score with official CTC metrics (TRA, DET, division detection F1).
4. Add a Hungarian-assignment version with a division rule as a simple upgrade and test it.

## Success gates (locked before results)
- G1: all trackers scored with official metrics on >= 4 CTC 3D datasets.
- G2: gap vs best tracker reported per dataset; the dataset features that predict the gap identified.
- G3: the simple upgrade closes >= 50% of the gap on at least half the datasets, or that is reported as not achieved.

## Expected deliverable
An open linking module with benchmark scores and an upgraded default for the parent software.

## Failure/pivot rule
If the parent-style method is already competitive everywhere, pivot to lineage tree reconstruction quality (division timing accuracy) as the harder test.
