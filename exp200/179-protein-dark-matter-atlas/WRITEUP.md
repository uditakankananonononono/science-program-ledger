# DOC-2-079 Protein "Dark Matter" Atlas - sandbox slice (exp200/079)

**Outcome: primary hypothesis FAILED (preserved); Pivot 1 PASSED its locked gates.**

## Setup
Human protein-coding genes that had a placeholder symbol (C#orf#, FAM#, KIAA#, TMEM#, CCDC#) on 2019-01-01. Outcome, dated by HGNC: renamed to a functional symbol after that date (274/985) or still a placeholder. Features came only from the STRING v11.0 human network (released January 2019), so the predictors come before the outcome. Data: HGNC complete set, STRING v11.0 links and info (checksums in data/SHA256SUMS).

## Primary (fail)
Q: Does 2019 network evidence predict WHICH dark genes get characterized? Logistic CV AUROC was 0.581 (95% CI 0.541-0.624), below the 0.65 gate. It did not beat the presence-only baseline (0.581). Length baseline 0.507, permutation 0.497. Mechanism of the failure: the presence signal is a mapping artifact. 91% of still-dark genes map to STRING by their 2019 symbol, vs 72% of genes renamed later, which often carried more than one placeholder symbol. Network connectivity was not positively linked to being characterized later. Boundary: how "hot" a gene looks in the 2019 network does not tell you it will get a name.

## Pivot 1 (gates locked before computation - pass)
Q: For dark genes that did get characterized, did the 2019 network already say WHAT they would turn out to be? Prediction: the top-3 HGNC gene groups among STRING >= 700 neighbours. Placeholder-family groups were excluded up front.
- Hit rate 18/41 = 43.9%. Null (neighbour sets shuffled) 3.6%. That is 12.3x, empirical p = 0.001. All three gates pass (>= 20%, >= 3x with p < 0.01, n >= 40).
- Examples: C7orf26 -> INTS15 (Integrator), C12orf66 -> KICS2 (KICSTOR), CXorf56 -> STEEP1 (spliceosome C/P), FAM98A/B and C2orf49 -> TSLIG3A/B and TSLIG2 (tRNA splicing ligase), CCDC151 -> ODAD3, CCDC103 -> DNAAF19 (axonemal dynein), C14orf2 -> ATP5MJ (complex V), KIAA1147/FAM45A -> DENND11/DENND10.
- Sensitivity (post hoc, reported as such): dropping the non-functional "MicroRNA protein coding host genes" group removes one hit (CLMB). That gives 17/41 = 41.5%, still passing.

## Useful result
The 2019 network could not say which dark genes would be studied next. For the ones that were, though, it already pointed at their eventual complex or family 42-44% of the time, about 12x chance. Practical use: rank the ~700 still-dark genes in this cohort by the confidence of their neighbourhood-group call. That gives a list of "annotation-ready" hypotheses, e.g. candidate complex subunits to test.

## Limits
- n = 41 is small and just clears the gate.
- HGNC gene groups are current. A group created at rename time that already contains the 2019 neighbours is the signal being claimed, but it also means complex-subunit discoveries dominate the hits.
- Paralog pairs (FAM98A/B) are not independent.
- There is no textmining-channel ablation, because the detailed links file was not used for memory reasons.
- Scope is human only and a single snapshot.

## Reproduce
python3 code/run.py; python3 code/pivot1.py (downloads listed in GATES.md). Outputs are in results/.
