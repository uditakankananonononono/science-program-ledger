# SP-004 Round 2 locked protocol

**Title:** Resolving the Small-Protein Annotation Contradiction Across Bacteria, Human, Mouse, and Yeast
**Topic:** DOC-2-077, round 2
**Locked:** 2026-09-21 21:38 IST, before round-2 cohort retrieval and outcome computation

## Prior evidence that motivates, but cannot be redefined by, this round
Round 0A found lower bacterial GO and function-comment coverage for 30-100 aa reviewed proteins, but slightly higher entry-level PDB coverage (3.79% vs 3.51%); exact-organism PDB effects were negative but uncertain. Round 0B found a raw human function-comment deficit that did not survive its locked adjusted gate, a strong opposite mouse association, and an uncertain yeast result. These are named prior results, not round-2 outcomes.

## Question and causal restraint
Does the apparent small-protein evidence deficit or reversal persist after balancing annotation age, taxon, family evidence, membrane/signal status, sequence composition, intrinsic-disorder proxy, proteomics detectability, and publication count? This is an observational decomposition of database evidence. It cannot identify causal effects of length or infer undiscovered proteins.

## Sources and population
Live UniProtKB reviewed records, sequence length 20-200 aa. Domains are (1) Bacteria, taxonomy 2, (2) human 9606, (3) mouse 10090, and (4) budding yeast 559292. Exposure is 20-100 aa; control is 101-200 aa. UniProt fields: creation/modification dates, function comments, GO IDs, PDB, AlphaFoldDB, InterPro, Pfam, PubMed IDs, protein existence, annotation score, transmembrane/signal features, sequence, and lineage. GO evidence codes will be taken from live EMBL-EBI QuickGO/GOA taxon files where retrievable and mapped by UniProt accession. Empty fields remain missing evidence, never negative biology.

## Frozen outcomes
Primary: explicit function comment. Co-primary evidence outcomes: any GO annotation, any experimental GO evidence (EXP, IDA, IPI, IMP, IGI, IEP and descendants used in GOA), any PDB link. Secondary: AlphaFoldDB, InterPro, Pfam, publication count, GO count. A structure reversal means short-minus-control PDB risk difference >0 before matching and <=0 after matching, or >=75% attenuation toward zero.

## Frozen covariates and mechanistic groups
- Baseline: domain and bacterial organism ID.
- Intrinsic: exact length, hydrophobic fraction, charged fraction, low-complexity fraction, Shannon entropy, disorder-promoting residue fraction, predicted tryptic peptide count (7-35 aa, zero missed cleavage), transmembrane and signal indicators.
- History/evidence opportunity: creation year/era, protein-existence tier, publication count bin.
- Family: InterPro and Pfam membership indicators and deterministic first family identifier; leave-family-out and family-exact analyses.
Annotation score is audited but excluded from primary weighting because it directly summarizes evidence outcomes; it appears only in a sensitivity analysis.

## Analysis
Within each domain, estimate unadjusted risk differences and odds ratios. Fit overlap weights from a regularized logistic propensity model using prespecified intrinsic + history + family-presence covariates; bacterial weights also include organism-frequency strata and phylum. Exact/coarsened matching uses taxon (species for eukaryotes, organism for bacteria where both groups exist), creation era (<=2010, 2011-2015, 2016-2020, >=2021), protein-existence tier, TM, signal, family-presence, and publication bins (0,1,2-4,>=5). Report effective sample size, maximum weight, overlap, and standardized mean differences before/after. No estimate is confirmatory if ESS is <200 per exposure arm or any absolute post-weight SMD exceeds 0.10.

Sequential decompositions are M0 baseline, M1 + intrinsic, M2 + age/evidence opportunity, M3 + family. Matching estimands are overlap-population associations, not causal effects. Uncertainty uses 1,000 taxon-cluster bootstrap replicates for bacteria and 1,000 ordinary bootstrap replicates for single-species domains, seed 20260921. BH correction is within outcome family.

## Sensitivity and negative controls
Cutoffs 80, 100, 120 aa; controls ending 180 and 200 aa. Exclude ribosomal names, uncertain names, TM proteins, signal-peptide proteins, proteins created after 2020, and proteins without family IDs. Leave-one-major-bacterial-phylum-out and leave-one-top-family-out analyses. Negative controls: accession-initial association (expected not biologically meaningful but historically structured) and AlphaFold coverage, expected near saturation in eukaryotic reviewed proteins. Negative controls cannot rescue a primary gate.

## Locked success gate
Round 2 succeeds only if data-integrity and overlap checks pass and one of these explanatory patterns replicates in at least two of the four domains:

**Gap pattern:** after M3 overlap weighting, function-comment or experimental-GO coverage is lower in short proteins by >=5 percentage points, 95% CI excludes zero, and direction persists in cutoff and leave-family-out sensitivity.

**Resolved-reversal pattern:** a raw short-protein PDB advantage becomes <=0 or attenuates >=75% after M3; the same sequential covariate block accounts for >=50% of the raw contrast in at least two domains; and the dominant block has at least one preweight absolute SMD >=0.20 reduced below 0.10 after weighting. The direction must survive leave-top-family-out checks.

Averaging opposite domains is forbidden. Domain results and contradictions are reported separately. If neither pattern replicates twice, status is unresolved/mixed. Post-hoc findings remain exploratory.

## Change and failure policy
The protocol hash is frozen before retrieval. Schema repairs are allowed only as dated amendments and cannot change cohorts, endpoints, cutoffs, model sequence, or gate. API or GOA unavailability is recorded; unavailable evidence-code analyses remain missing rather than substituted. Negative and nontransporting results are retained.
