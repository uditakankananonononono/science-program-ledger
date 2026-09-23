---
id: P06-06
title: "Which Shape Do You Dock Against? Pre- vs Post-Fusion State Dependence of NiV Hit Rankings"
parent: "CBIO013 - Fighting Future Pandemics with Novel DeepGraphDTI (source abstract, 2024)"
---

# Which Shape Do You Dock Against?

**Parent project:** CBIO013(2024) - docking verification used whatever structures were available; fusion glycoproteins radically change shape, and hit rankings can flip by state.

## Premise
F proteins exist in pre-fusion and post-fusion states; G proteins have head-up/head-down conformations. A "hit" against the wrong state may be pharmacologically irrelevant.

## Hypothesis
>= 40% of top docked compounds change rank decile between conformational states; state-aware consensus rescoring produces a materially different, more defensible hit list.

## Data sources (free/public)
- All public NiV/HeV F and G structures across conformational states (PDB) + AlphaFold ensembles.
- The parent's drug boxes and hit identities.

## Method outline
1. Classify every available structure by conformational state (locked criteria).
2. Dock the top-100 parent-screen compounds + decoys into every state; rank-flip analysis per compound.
3. State-weighted consensus: weight pre-fusion/head-up (functional states) per published mechanism; issue the re-ranked list.

## Success gates (locked before results)
- G1: state-dependent rank-flip rate published; if < 10%, state-awareness is declared a non-issue (real negative, simpler future screens).
- G2: re-ranked hit list frozen and compared against the parent's 7; agreement rate reported.
- G3: decoy separation verified per state before any ranking.

## Expected deliverable
`statecheck`: a conformation-aware docking protocol + the state-annotated henipavirus structure catalog.

## Failure/pivot rule
If rankings are state-stable, publish that simplification - single-structure docking is adequate for this target class, saving everyone compute.
