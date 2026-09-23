---
id: P06-10
title: "The Open Pandemic Screen Atlas: All Three Drug Boxes Against Every WHO Priority Pathogen with Available Structures"
parent: "CBIO013 - Fighting Future Pandemics with Novel DeepGraphDTI (source abstract, 2024)"
---

# The Open Pandemic Screen Atlas

**Parent project:** CBIO013(2024) - screened 3 open drug boxes against one pathogen; the same boxes cover a curated anti-infective space waiting to be systematically screened.

## Premise
The highest-leverage extension: run the validated pipeline (with P06-01's honest operating envelope) across all WHO priority pathogens with usable structures, and publish the full ranked matrix as an open resource.

## Hypothesis
>= 10 pathogens yield >= 5 high-confidence candidates each (consensus of DTA + docking with decoy-verified assays), and cross-pathogen analysis identifies >= 3 drugs with multi-pathogen potential.

## Data sources (free/public)
- WHO R&D Blueprint priority pathogen list; PDB/AlphaFold structures per pathogen target.
- MMv Global Health Priority Box / Pandemic Response Box / Pathogen Box (open compound lists with structures).

## Method outline
1. Target selection per pathogen with locked criteria (essential, structured, druggable).
2. Run DTA screen + ortho-docking (P06-02 protocol) per target with per-assay decoy verification; only verified assays contribute hits.
3. Publish the full pathogen x drug score matrix, the per-pathogen shortlists, and cross-pathogen breadth analysis - all open.

## Success gates (locked before results)
- G1: every reported hit comes from a decoy-verified assay (EF10% above locked bar) - unverified assays produce no hits.
- G2: the full matrix (including negatives) is published - not just highlights.
- G3: >= 10 pathogens completed with shortlists, or the completed subset is published with the bottleneck analysis.

## Expected deliverable
`pandemicatlas`: the open screen matrix + per-pathogen shortlists + the end-to-end reusable pipeline - a standing resource for outbreak response.

## Failure/pivot rule
Where assays fail verification, those cells are published as unmeasurable - the atlas maps our ignorance as carefully as our candidates.
