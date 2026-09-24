# algo50/08 - Neighbor-joining vs UPGMA: how much does violating the molecular clock cost UPGMA?

Status: LOCKED before any method-vs-method results were computed (lock time in results/lock.txt, sha256 of this file).
Lane: RES-2. Class: algorithm study (not counted toward the flagship 100).

## Question
UPGMA assumes an ultrametric (clocklike) tree; neighbor-joining does not. On simulated evolution with known trees, how much topology accuracy does UPGMA lose as rate variation grows, and does NJ pay anything when the clock actually holds?

## Data (simulated, ground truth known)
32-taxon trees, 100 replicates per regime, seeds 1..100.
- CLOCK: coalescent-style ultrametric tree (join random pair at increasing heights, heights from sorted exponentials), branch lengths scaled to mean pairwise distance ~0.5 subs/site.
- RATEVAR: same topologies, each branch length independently multiplied by exp(N(0, 0.5)).
Sequences: length 1000 nt evolved along each tree under JC69 (per-branch change prob 3/4(1-exp(-4/3 d))).
Distance: JC69-corrected p-distance (p<0.74 enforced; pairs at/above saturation excluded from neither method - clamped to 0.749).
Everything regenerable from seeds; no downloads.

## Task
Topology recovery. Unit = one replicate tree. Metric: normalized Robinson-Foulds distance (unrooted splits) between inferred and true tree.

## Methods
- UPGMA on JC69 distances (average linkage, deterministic tie-break by taxon index).
- NJ: canonical neighbor-joining (Saitou-Nei), deterministic tie-break.
Both implemented from scratch, no phylo libraries.

## Success gates
- G1: RATEVAR mean nRF: NJ <= UPGMA - 0.05 (NJ wins without clock).
- G2: CLOCK mean nRF: NJ <= UPGMA + 0.05 (NJ does not lose meaningfully with clock).
- G3: UPGMA mean nRF under RATEVAR >= UPGMA under CLOCK + 0.05 (rate variation is what hurts UPGMA).
- G4: NJ mean nRF under RATEVAR <= 0.25 (NJ still usable under this much rate variation).
Project PASSES if G1 and G2 pass; G3/G4 are mechanism gates, reported either way.

## Failure policy
Negative results recorded as-is; a failed direction triggers a documented pivot with gates locked in an amendment before new results are inspected; original gates never re-scored.

## Notes locked in advance
- n=32 taxa and L=1000 chosen so 200 replicates run in minutes in pure Python; absolute RF values depend on these.
- Clamping saturated distances is a documented bias that can only help UPGMA (it reduces long-branch contrasts).
