# DOC-2-068 Mechanism-First Drug Fingerprint - sandbox slice (exp200/168)

**Outcome: documented boundary. Primary and Pivot 1 failed the absolute-precision gate. Not counted.**

## Setup
I represented 1,446 approved drugs (ChEMBL phase-4 mechanisms, human targets) by the Reactome pathways their targets sit in, with no drug names, targets or class labels in the representation. The test: does a drug's nearest neighbour *among drugs that share none of its targets* belong to the same ATC level-3 class? LINCS perturbation signatures did not fit the sandbox, so pathways stand in for "perturbed mechanism".

## Results
| | precision | vs null | gate |
|---|---|---|---|
| Primary, Jaccard | 0.129 | 6.6x (null 0.020), p = 0.001 | fail (>= 0.25) |
| Pivot 1, IDF-weighted cosine, hub pathways dropped | 0.138 | 7.0x, p = 0.001 | fail (>= 0.20 and >= 1.3x primary) |
| Reference: nearest neighbour by shared target identity | 0.625 | | not gated |

Higher pathway similarity did not make same-class neighbours more likely (tertile precision 0.10 / 0.20 / 0.11).

## What is useful from the failure
1. **A measured ceiling.** Once shared targets are removed, target-pathway context finds a same-class drug about 13-14% of the time. That is 7x chance, but about 5x worse than simply sharing a target (62%). Most of the "mechanism similarity" in target-annotation space is target identity in disguise. Repurposing claims built on pathway overlap of targets should report their no-shared-target performance.
2. **Where it works.** The cross-target hits are real mechanistic convergence:
   - thrombolytics: alteplase/tenecteplase/reteplase vs urokinase and streptokinase
   - migraine: triptans vs methysergide and lasmiditan
   - topoisomerase poisons: irinotecan/topotecan vs etoposide/teniposide
   - GABA-ergic antiepileptics: valproate vs vigabatrin
   - gonadotropins
   - IL-17 axis: secukinumab vs brodalumab
   - IL-5 axis: mepolizumab vs benralizumab

   These are ligand vs receptor, or enzyme vs substrate, pairs within one pathway. So the method's real use is finding "same pathway, different node" drugs, not general class recovery.
3. **Why similarity does not help.** Very high overlap usually comes from small fingerprints of one or two pathways shared across classes (e.g. GPCR signalling). ATC level 3 also groups some drugs by indication rather than mechanism, which caps achievable precision for any mechanism-only representation.

## Limits
- Target-pathway membership is a proxy for perturbation response, not measured transcriptional effect.
- ATC is an imperfect mechanism label.
- ChEMBL covers only annotated mechanisms, so polypharmacology is under-represented.

## Reproduce
python3 code/fetch.py (ChEMBL REST); UniProt2Reactome.txt from reactome.org/download/current; python3 code/run.py; python3 code/pivot1.py
