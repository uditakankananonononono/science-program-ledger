# DOC-1-019 REPORT - A Metagenomic Protein Atlas of Extreme Environments
EXP-1, 2026-09-24. GATES.md locked 06:59 BEFORE any protein content inspection. VERDICT: DOCUMENTED BOUNDARY (submitted for adjudication) - G1 PASS, G2 batch-guard FAIL, G3 partial with a literature-refuting finding.

## Gate results
- G1 (dev, 5-fold CV seed 7): Arm T (thermal vs non-thermal) composite dipeptide-LR 0.686 vs IVYWREL baseline 0.579 (+0.107, PASS). Arm S (hypersaline vs rest) composite 0.785 vs D+E baseline 0.458 (+0.327, PASS). Notable even here: the D+E baseline is BELOW CHANCE (0.458) on dev.
- G2 (frozen, fit on dev only, single pass): Arm T frozen 0.649 - beats IVYWREL frozen (0.597, +0.051) but misses the locked 0.70 absolute bar: FAIL. Arm S frozen 0.553, BELOW the frozen D+E baseline (0.568): FAIL. The locked batch guard triggers: dev-learnable hypersaline "fingerprint" does not transport even to held-out samples of the same study - it was sample-batch, not environment.
- G3 (mechanism): PARTIAL. (c) IVYWREL atlas ordering HOLDS exactly as the thermophile literature predicts: hotspring 0.4095 > vent 0.3940 > hypersaline 0.3874 > control 0.3841. (c) D+E ordering FAILS and inverts: hypersaline is LOWEST (0.109) - the canonical halophile acidic-proteome signature is ABSENT in this metagenome. (a) Arm-T learned weights IVYWREL-consistent (top dipeptides IL, IA, ID, IE, IK, LL, IR, AL, IP, IS - Ile/Leu dominated; Spearman +0.087). (b) Arm-S weights not D/E-driven (-0.043). G3 FAIL as locked (needs all four).
- G4: atlas_signatures.tsv + atlas_lookup.py CLI (smoke-tested; honestly labeled descriptive-not-classifier). Lab nomination: Banfield lab (UC Berkeley).

## The three findings
1. Thermal fingerprints are real but weak in metagenomes. The IVYWREL ordering is visible at the biome level (matching Zeldovich 2007 direction) and a dipeptide model finds signal beyond it (+0.10 dev), but frozen transport decays (0.686 -> 0.649) and misses the absolute bar - mixed mesophile/thermophile communities dilute the organismal signature.
2. The halophile D+E signature does NOT survive metagenomic measurement: absent (inverted) in the only v5.0 hypersaline set available (MGYS00005861). Either that community is not dominated by salt-in strategists, or metagenomic mixing erases it. A direct caution against transferring organismal adaptation signatures to metagenomic atlases.
3. The batch guard did its job: Arm S dev 0.785 -> frozen 0.553, below its own baseline. Dev-learnable is not environment-general; the atlas's per-biome signature table should be read as descriptive, not predictive.

## Honest limits
Only ONE v5.0 assembly study exists for vent/hypersaline/control in the scanned MGnify biomes - sample-level (not study-level) frozen split for those arms is the weakest link and is exactly where the boundary showed up. Reservoir sampling to 3000 proteins/biome discards community structure. Predicted CDS include fragments (30-300 aa filter applied). No taxonomy normalization - composition differences partly track taxonomic composition.
