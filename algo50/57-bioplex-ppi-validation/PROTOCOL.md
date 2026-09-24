# 57 - BioPlex validation: do GO semantic-similarity PPI predictions hold on an experimental AP-MS gold standard?

Lane RES-1. User-directed follow-up to algo50/31. Locked before any pair is scored.

## Question
algo50/31 scored GO semantic similarity against STRING physical interactions (aggregated evidence, partly curated). 57 re-runs the identical 13-measure suite against the BioPlex 3.0 AP-MS interactome - a single-technology experimental gold standard - and tests (a) whether the 31 findings replicate, and (b) whether a model trained on STRING transfers to BioPlex.

## Data
- BioPlex 3.0 293T network (BioPlex_293T_Network_10K_Dec_2019.tsv, bioplex.hms.harvard.edu/data/; 118,162 published interactions, symbol pairs + pW/pNI/pInt). HCT116 network (BioPlex_HCT116_Network_5.5K_Dec_2019.tsv) used ONLY to exclude cross-cell-line true pairs from the negative pool.
- GO: go-basic.obo + GOA human GAF (same releases as 31 where still current; record versions in data/provenance.txt). Same leakage controls as 31: drop NOT qualifiers, ALL IPI-evidence annotations (critical here: BioPlex-derived IPI annotations would be direct leakage), and GO:0005515 "protein binding".
- Gene identity: BioPlex SymbolA/SymbolB matched to GOA gene symbols. Unmapped symbols dropped and counted.

## Pairs
- Positives: 10,000 sampled (seed 57) from 293T edges where both partners have >= 1 BP annotation.
- Negatives: 10,000 degree-matched pairs drawn from the positives' protein multiset, excluding any edge in EITHER BioPlex network (293T or HCT116). No STRING exclusion (STRING is the transfer source, not the ground truth here; using it to filter negatives would bias toward the transfer model's errors).
- Proteins without annotations in an ontology score 0 there. Annotation sets reduced to most-specific terms before pairwise measures. IC = -log(fraction of annotated genes carrying the propagated term), per ontology.

## Measures (identical to 31)
Per ontology (BP/MF/CC): Resnik-BMA, Resnik-max, Lin-BMA, simGIC. Plus simGIC-ALL over the union of ontologies. 13 scores per pair.
Model Q: L2 logistic regression (C=1, standardized features) over all 13 scores; out-of-fold predictions from 5-fold stratified CV by pair (seed 57). Pre-registered primary model here (in 31 it was a post-hoc pivot; pre-registration is the point of this study).
Transfer arm: Q31 = the same logistic form trained on ALL of 31's STRING pairs (results/pair_scores.tsv.gz, 20k pairs), frozen, applied to this study's BioPlex pairs. No refit, no recalibration.

## Metric
AUROC on the 1:1 set; 95% CI from 1000 stratified bootstraps (seed 57).

## Gates
- G1 (headline): AUROC(Q) - max over the 13 single measures of AUROC >= 0.01, CI lower bound > 0.
- G2 (replication of 31's G2): AUROC(simGIC-ALL) - max over ontologies of AUROC(Resnik-BMA) >= 0.005, CI lower bound > 0.
- G3 (transfer): AUROC(Q31 frozen, STRING->BioPlex) >= 0.65, CI lower bound > 0.5 obviously; the gate is the 0.65 bar.
- G4 (sign replication of 31's G1 negative): AUROC(simGIC-BP) - AUROC(Resnik-BMA-BP) <= 0 (31 found simGIC-BP worse by 0.014; we predict the same sign on BioPlex).

## Pivot plan (only if gates fail, locked as amendments before their results)
- P1: if G1 fails, test whether the failure is concentration: AUROC(Q) vs the SINGLE measure chosen best on the STRING data (simGIC-ALL), not the best-on-BioPlex measure: gate P1 = AUROC(Q) - AUROC(simGIC-ALL) >= 0.005.
- P2: if G3 fails, retest transfer with Q31 restricted to the 4 BP scores only (less ontology-mixture shift): gate P2 = AUROC >= 0.60.

## Caveats declared up front
- AP-MS detects co-complex membership, not only direct physical contact; GO BP co-annotation may align with complex membership more than with binary contact. That inflates all measures roughly equally.
- Annotation-rich (well-studied) proteins carry both more GO terms and more detected interactions; degree-matched negatives reduce but do not remove this.
- 293T-specific negatives may include pairs that interact in other cell lines/states; HCT116 exclusion covers the only other large BioPlex map.
- Bootstraps treat pairs as independent; shared proteins induce mild dependence.

## Honest-negatives policy
Every gate outcome is reported PASS/FAIL as declared. Failed gates stay in the README with their numbers.
