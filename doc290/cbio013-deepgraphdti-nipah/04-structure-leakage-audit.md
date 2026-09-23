---
id: P06-04
title: "Is the Graph Seeing Biology or Shortcuts? Structure and Degree Leakage Audit of DeepGraphDTI"
parent: "CBIO013 - Fighting Future Pandemics with Novel DeepGraphDTI (source abstract, 2024)"
---

# Is the Graph Seeing Biology or Shortcuts?

**Parent project:** CBIO013(2024) - atomic-graph protein encodings claimed as the model's edge.

## Premise
GNN DTA models can learn dataset shortcuts: node-degree patterns, atom-count correlations, benchmark family artifacts. Probing what the graph encoding actually uses determines whether the claimed structural advantage is real.

## Hypothesis
>= 30% of the model's benchmark edge over sequence baselines survives feature-nullification probes - or the edge is largely shortcut-driven.

## Data sources (free/public)
- Same benchmarks as P06-01; the reproduced model.
- Null encodings: degree-shuffled graphs, binned-coordinate graphs, sequence-only ablations.

## Method outline
1. Probe battery: (a) shuffle graph node identities within proteins, (b) destroy geometry (random coordinates, keep connectivity), (c) degree-matched random graphs; measure performance delta per null.
2. Attribution analysis: which substructures drive predictions for known binding vs decoy pairs.
3. Shortcut score = fraction of the sequence-baseline edge lost under each null.

## Success gates (locked before results)
- G1: per-null performance deltas published with CIs - the probe battery ships as the tool.
- G2: >= 30% of the edge must survive the strongest null to certify structural learning; below that, the structural claim is downgraded.
- G3: attribution examples published for >= 20 known binding pairs, not cherry-picked.

## Expected deliverable
`graphprobe`: a shortcut-audit suite for graph-based DTA models with the pre-run DeepGraphDTI certificate.

## Failure/pivot rule
If shortcuts dominate, publish the finding with the corrected benchmark ranking - the field learns what these models actually exploit.
