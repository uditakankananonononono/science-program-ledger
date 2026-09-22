# DOC-1-013 R2 locked protocol: family/physics replication
Locked 2026-09-21 21:38 IST after source/compute preflight and before R2 outcome modeling.

## Cohort
Use the openly available AlloBench.csv snapshot plus fresh RCSB coordinates. Exclude every R0 PDB (1C50, 1FRZ, 1H78, 1H79, 1H7A, 1LLC, 1LTH, 1PZO, 1PZP, 1XJF, 1XJG, 1XJJ, 1XJK, 1XJM, 1XJN) and R0 UniProt accessions (P00489, P0A759, P07071, P00343, E8ME30, P62593, O33839). Sort target_id then PDB. Select the first PDB per target that has a parseable chain named in the allosteric annotation, 60-1200 resolved standard residues, >=3 mapped allosteric residues, >=3 mapped active-site residues, and >=30 non-site residues. Stop after 80 targets. Preserve all exclusions. Require >=30 proteins and >=8 sequence families containing >=2 proteins.

## Families
Cluster full benchmark sequences at >=30% global identity by deterministic single-linkage, with alignment coverage >=70% of the shorter sequence. Clusters are frozen before features/outcomes. Report sensitivity at 40% identity, but the primary split is 30%.

## Labels and features
Positive site labels are the curated AlloBench allosteric-site residues mapped to resolved residues. Negatives are other resolved standard residues, excluding active-site residues and residues within two contact-graph edges of an allosteric positive (buffer prevents trivial boundary classification).

Primary ESM feature: pinned `facebook/esm2_t6_8M_UR50D`, final-layer per-residue embeddings, frozen. Strong baseline: amino-acid one-hot; family-alignment conservation where valid plus missing indicator; C-alpha contact-graph degree, closeness, betweenness and clustering; distance from chain centroid; sequence-relative position; and backbone local-angle descriptors. No ligand identity or coordinates are features. Ablations are ESM alone, structure/conservation alone, one-hot alone, and ESM with residue order scrambled within protein.

## Evaluation
Primary generalization is leave-family-out. Secondary is leave-PDB-out. Within each training split, standardize features, reduce ESM to <=32 training-only PCs, and fit class-weighted logistic regression. Choose C from {0.01,0.1,1,10} by grouped 4-fold training-only CV. Primary endpoint is macro protein AUPRC. Secondary endpoints: AUROC, top-10%-residue recall, Brier score and calibration slope. Bootstrap 10,000 family resamples, seed 130132.

## Pathway localization
Build an 8 Å C-alpha contact graph. For every allosteric-site/active-site pair, take all residues on any shortest path; remove endpoint sites. A protein is evaluable with >=3 corridor and >=30 matched non-site residues. The externally defined pathway endpoint is macro protein AUPRC for distinguishing corridor residues from non-site residues using predictions from the site model, without refitting. Scrambled-score and degree-matched random controls use seed 130132.

## Gate
R2 succeeds only if all hold: (1) leave-family-out ESM+baseline macro AUPRC exceeds strong baseline by >=0.03 and the family-bootstrap 95% CI excludes zero; (2) the gain remains positive in leave-PDB-out; (3) pathway-corridor AUPRC exceeds both prevalence by >=0.03 and the 97.5th percentile of 1,000 degree-matched scrambled controls; (4) Brier score is no worse than the strong baseline by >0.01. Otherwise R0 remains preliminary and the report must attribute its gain using family overlap, ablations, and controls.

Random-label-within-protein AUPRC must be within 0.03 of prevalence or inference is invalid. No gate, cohort, threshold, or endpoint changes after lock. All failures and negatives remain. Claims are residue enrichment and graph-corridor localization only, not causal dynamics.
