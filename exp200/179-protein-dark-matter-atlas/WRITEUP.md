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

---
## Addendum: forward nominations for genes still dark today (2026-09-23)
File: results/forward_nominations_2026.csv. Code: code/forward.py. The method is the one validated in Pivot 1, applied unchanged to the current STRING v12.0 network and current HGNC names.

- **746** human protein-coding genes still carry a placeholder symbol today (not ~950).
- **110** are eligible, meaning >= 3 high-confidence neighbours with a gene group. 441 have no high-confidence STRING neighbours at all, 161 have too few, and 34 are not in STRING v12. For about 85% of dark genes, the network method has nothing to say. That is the main limit of the tool.
- Of the 110: **97 new nominations**, and 13 are already in their top nominated HGNC group (placeholder name, but already classified).
- Expected accuracy for eligible genes: top-3 hit rate 44% (18/41, 95% Wilson CI 30-59%), measured on the 2019->2026 retrospective test. Expect roughly 4-6 of every 10 nominations to be right, and the CI is wide.
- Examples of new nominations: FAM89A/FAM89B -> anaphase-promoting complex (6/6 neighbours); TMEM179B -> SAGA complex (6/6); TMEM250 -> septins (5/5); C6orf15 -> RNA polymerase (11/16); FAM185A -> peroxins; CCDC63 -> outer dynein arm docking; CCDC9 -> exon junction complex; TMEM114 -> beta-gamma crystallins.

How to read the list:
1. Many "new" rows are dark by name only. HGNC groups lag the literature: CCDC47 (PAT complex), TMEM147 (BOS complex), CCDC22 (CCC complex), TMEM17/TMEM107/TMEM237 (MKS complex) and C9orf78 (spliceosome) are published. For those rows, the method re-derives known biology. That is a sanity check, not a discovery.
2. Hub attractors: nominations to ribosome, proteasome or RNA polymerase with many neighbours (e.g. KIAA2012/CCDC74B/CCDC92 -> proteasome, CCDC124 -> ribosome) can come from co-expression with abundant machinery. Treat them as low-specificity even when the vote share is high.
3. The best candidates for real follow-up are rows with a small, unanimous, specific neighbourhood (vote share 1.0, 3-6 neighbours, a non-hub complex) and no literature assignment yet. Checking each against PubMed is the next step. It is not done here.

Display rules (the two host-gene groups dropped, the already-classified flag) were set before reading the ranked list and are recorded in GATES.md.
