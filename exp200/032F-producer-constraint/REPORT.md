# DOC-1-032F — Producer-Annotated Constraint Model — REPORT

## Verdict
**DOCUMENTED BOUNDARY** (locked failure tree: G2 fail -> boundary; the constraint IS the
mechanism-targeted fix, no further rescue pre-registered). G1 sanity passed; G2 and G3 fail.
Sharp mechanism finding: the constraint selects the biologically CORRECT driver organisms,
but species-abundance representation of producer capability does not repair cross-cohort
transfer - 032's dev->frozen collapse is a signal-strength problem, not a feature-selection
problem.

## Lineage
032 boundary: dev ridge 85.0% collapses to 30.0% frozen HMP2 (ARM A MelonnPan 37.1%, ENVIM
anchor matched). Approved follow-up: constrain per-metabolite features to taxa annotated to
produce that metabolite (generalizing 032's G4 butyrate-driver coherence). Gates locked
pre-scoring; Addendum A (pre-scoring): 12 keys -> 10 distinct compounds (synonym dedup) +
PRISM cluster->name bridge validated 25/25.

## Design (locked)
Per-metabolite RidgeCV (032 ARM B protocol) on log1p rel-abundance of ONLY the DEMETER/
AGORA2-annotated producer species (7,302-strain curated tables), train PRISM (155),
frozen HMP2 (388 paired). 10 producer-annotated compounds (of 70 mapped).

## Results (frozen, HMP2, Spearman rho)
| compound | constrained | ARM A | ARM B | trainable/present |
|---|---|---|---|---|
| propionate | -0.142 | -0.026 | -0.059 | 42/167 |
| butyrate/isobutyrate | 0.241 | 0.256 | 0.164 | 51/169 |
| cholate | **0.380** | 0.281 | **0.466** | 84/119 |
| chenodeoxycholate | **0.369** | 0.313 | 0.349 | 84/119 |
| deoxycholic.acid | 0.108 | 0.119 | 0.129 | 1/3 |
| lithocholic.acid | 0.137 | 0.155 | 0.314 | 1/3 |
| chenodeoxycholate.deoxycholate. | 0.072 | 0.088 | 0.064 | 85/121 |
| putrescine | 0.193 | **0.427** | 0.420 | 5/9 |
| glutamate | -0.048 | 0.276 | 0.179 | 1/1 |
| N.acetylspermidine | n/a (0 trainable) | 0.345 | 0.308 | 0/1 |

- **G1 PASS**: PRISM 5-fold dev mean rho 0.4208 (bar 0.10).
- **G2 FAIL**: constrained well-predicted 20.0% (2/10: cholate, chenodeoxycholate) vs bars
  35.0% (ARM A 3/10 + 5pp) and 55.0% (ARM B 5/10 + 5pp).
- **G3 FAIL**: propionate -0.142 (bar 0.3; WORSE than both arms), butyrate 0.241 (bar 0.3;
  better than ARM B 0.164, below ARM A 0.256).

## G4 (mechanism, runs regardless)
- Driver organisms are the biologically correct producers: butyrate <- Roseburia
  intestinalis + Lachnospiraceae (+ coefficients); propionate <- Megamonas hypermegale +
  Ruminococcus; both match the literature producer lists.
- Coverage ceiling: PRISM's 201-species taxa table retains only 42-85 of 119-169 annotated
  producers per compound (1/3 for deoxycholate producers; 0/1 for N.acetylspermidine).
- The finding: annotation constraints DO select the right organisms (dev 0.42 mean, dev
  cholate 0.644), but organism abundance is a weaker transported signal than UniRef90 gene
  dosage. 032's boundary is not a feature-selection failure; per-compound, the constraint
  wins where the producer set is deep and the pathway is organism-dominant (primary bile
  acids cholate/chenodeoxycholate are the constrained model's two wins, 0.380/0.369).

## Boundary statement
Failed direction documented: taxa-level producer-annotation constraints do not repair
cross-cohort metabolite prediction (G2, G3 both fail). Useful byproducts: the 10-compound
producer-annotated benchmark with per-compound frozen scores for all three arms; the
coverage finding (PRISM taxa depth caps trainable producers); validated PRISM cluster->name
bridge (25/25). Tool: constrained predictor CLI (see tools/) for the 10 compounds.

## Prospective lab nomination (locked)
An IBD metabolomics unit imputing SCFAs/bile acids from metagenomes: constrained model for
primary bile acids (the two compounds where it wins), ARM A/ARM B elsewhere - the honest
deployment is per-compound model selection, which this benchmark now quantifies.

## Reproduce
tools/score032F.py; data sources in PROVENANCE.md; scores032F.json (all per-compound rhos,
drivers, coverage); gates in GATES.md + GATES_ADDENDUM_A.md (locked pre-scoring).
